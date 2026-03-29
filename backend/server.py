"""
MAVR - Athlete Operating System
Main FastAPI Application
"""
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, APIRouter, HTTPException, Depends, Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from datetime import datetime, timezone, timedelta
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr
import os
import bcrypt
import jwt
import secrets
import logging
from pathlib import Path

# Models
from models.user import (
    UserCreate, UserLogin, UserResponse, UserProfileData, UserProfile, 
    AthleteLevel, Goal, DietPreference, BudgetLevel, WorkoutSetup
)
from models.diet import DietPlan, DietPlanResponse, Meal
from models.workout import WorkoutPlan, WorkoutPlanResponse, WorkoutLog
from models.tracking import (
    DailyCheckin, MorningCheckin, WorkoutCheckin, NightCheckin,
    DailyTarget, ReadinessScore, StreakRecord, ProgressionRecord, WeeklyReport
)
from models.event_commerce import EventMode, EventType, BodyStage, ClothingRecommendation, Product

# Services
from services.classification_service import ClassificationService
from services.calorie_service import CalorieService
from services.diet_engine import DietEngineService
from services.workout_engine import WorkoutEngineService
from services.readiness_engine import ReadinessEngineService
from services.streak_engine import StreakEngineService
from services.ai_service import ai_service
from services.clothing_engine import ClothingEngineService

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# JWT Configuration
JWT_SECRET = os.environ.get("JWT_SECRET", "mavr_default_secret_change_in_production")
JWT_ALGORITHM = "HS256"

# Create FastAPI app
app = FastAPI(title="MAVR - Athlete Operating System", version="1.0.0")

# Create API router
api_router = APIRouter(prefix="/api")

# ==================== AUTH UTILITIES ====================

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

def create_access_token(user_id: str, email: str) -> str:
    payload = {
        "sub": user_id,
        "email": email,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=60),
        "type": "access"
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def create_refresh_token(user_id: str) -> str:
    payload = {
        "sub": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(days=7),
        "type": "refresh"
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

async def get_current_user(request: Request) -> dict:
    token = request.cookies.get("access_token")
    if not token:
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]
    
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid token type")
        
        user = await db.users.find_one({"_id": ObjectId(payload["sub"])})
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        user["_id"] = str(user["_id"])
        user.pop("password_hash", None)
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def get_optional_user(request: Request) -> Optional[dict]:
    try:
        return await get_current_user(request)
    except:
        return None

async def require_admin(request: Request) -> dict:
    user = await get_current_user(request)
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

# ==================== AUTH ROUTES ====================

@api_router.post("/auth/register")
async def register(data: UserCreate, response: Response):
    email = data.email.lower()
    
    existing = await db.users.find_one({"email": email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_doc = {
        "email": email,
        "name": data.name,
        "password_hash": hash_password(data.password),
        "role": "user",
        "onboarding_completed": False,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    result = await db.users.insert_one(user_doc)
    user_id = str(result.inserted_id)
    
    access_token = create_access_token(user_id, email)
    refresh_token = create_refresh_token(user_id)
    
    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=False, samesite="lax", max_age=3600, path="/")
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, secure=False, samesite="lax", max_age=604800, path="/")
    
    return UserResponse(
        id=user_id,
        email=email,
        name=data.name,
        role="user",
        onboarding_completed=False,
        created_at=user_doc["created_at"]
    )

@api_router.post("/auth/login")
async def login(data: UserLogin, response: Response):
    email = data.email.lower()
    
    user = await db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not verify_password(data.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user_id = str(user["_id"])
    access_token = create_access_token(user_id, email)
    refresh_token = create_refresh_token(user_id)
    
    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=False, samesite="lax", max_age=3600, path="/")
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, secure=False, samesite="lax", max_age=604800, path="/")
    
    return UserResponse(
        id=user_id,
        email=user["email"],
        name=user["name"],
        role=user.get("role", "user"),
        onboarding_completed=user.get("onboarding_completed", False),
        created_at=user.get("created_at")
    )

@api_router.post("/auth/logout")
async def logout(response: Response):
    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/")
    return {"message": "Logged out successfully"}

@api_router.get("/auth/me")
async def get_me(request: Request):
    user = await get_current_user(request)
    return UserResponse(
        id=user["_id"],
        email=user["email"],
        name=user["name"],
        role=user.get("role", "user"),
        onboarding_completed=user.get("onboarding_completed", False),
        created_at=user.get("created_at")
    )

@api_router.post("/auth/refresh")
async def refresh_token(request: Request, response: Response):
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=401, detail="No refresh token")
    
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        
        user = await db.users.find_one({"_id": ObjectId(payload["sub"])})
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        user_id = str(user["_id"])
        new_access_token = create_access_token(user_id, user["email"])
        
        response.set_cookie(key="access_token", value=new_access_token, httponly=True, secure=False, samesite="lax", max_age=3600, path="/")
        
        return {"message": "Token refreshed"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

# ==================== ONBOARDING ROUTES ====================

class OnboardingData(BaseModel):
    profile_data: UserProfileData

@api_router.post("/onboarding/save")
async def save_onboarding(data: OnboardingData, request: Request):
    user = await get_current_user(request)
    user_id = user["_id"]
    
    # Calculate athlete classification
    profile_data = data.profile_data
    athlete_level = ClassificationService.classify_athlete(profile_data)
    
    # Calculate calories and macros
    calculations = CalorieService.get_full_calculation(profile_data, athlete_level)
    
    # Create/update profile
    profile_doc = {
        "user_id": user_id,
        "profile_data": profile_data.model_dump(),
        "athlete_level": athlete_level.value,
        "bmr": calculations["bmr"],
        "tdee": calculations["tdee"],
        "target_calories": calculations["target_calories"],
        "target_protein": calculations["target_protein"],
        "target_carbs": calculations["target_carbs"],
        "target_fats": calculations["target_fats"],
        "updated_at": datetime.now(timezone.utc).isoformat()
    }
    
    await db.user_profiles.update_one(
        {"user_id": user_id},
        {"$set": profile_doc},
        upsert=True
    )
    
    # Mark onboarding complete
    await db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"onboarding_completed": True}}
    )
    
    # Generate initial plans for today
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    day_of_week = datetime.now(timezone.utc).strftime("%A").lower()
    
    # Generate diet plan
    diet_plan = DietEngineService.generate_diet_plan(user_id, profile_data, athlete_level, today)
    await db.generated_diet_plans.update_one(
        {"user_id": user_id, "date": today},
        {"$set": diet_plan.model_dump()},
        upsert=True
    )
    
    # Generate workout plan
    workout_plan = WorkoutEngineService.generate_workout_plan(user_id, profile_data, athlete_level, today, day_of_week)
    if workout_plan:
        await db.generated_workout_plans.update_one(
            {"user_id": user_id, "date": today},
            {"$set": workout_plan.model_dump()},
            upsert=True
        )
    
    # Initialize streak
    await db.streak_records.update_one(
        {"user_id": user_id, "streak_type": "daily_checkin"},
        {"$set": {"user_id": user_id, "current_streak": 0, "longest_streak": 0, "streak_type": "daily_checkin"}},
        upsert=True
    )
    
    return {
        "message": "Onboarding completed successfully",
        "athlete_level": athlete_level.value,
        "target_calories": calculations["target_calories"],
        "target_protein": calculations["target_protein"]
    }

@api_router.get("/onboarding/profile")
async def get_profile(request: Request):
    user = await get_current_user(request)
    profile = await db.user_profiles.find_one({"user_id": user["_id"]}, {"_id": 0})
    return profile or {}

# ==================== DASHBOARD ROUTES ====================

@api_router.get("/dashboard")
async def get_dashboard(request: Request):
    user = await get_current_user(request)
    user_id = user["_id"]
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    # Get profile
    profile = await db.user_profiles.find_one({"user_id": user_id}, {"_id": 0})
    
    # Get today's diet plan
    diet_plan = await db.generated_diet_plans.find_one({"user_id": user_id, "date": today}, {"_id": 0})
    
    # Get today's workout plan
    workout_plan = await db.generated_workout_plans.find_one({"user_id": user_id, "date": today}, {"_id": 0})
    
    # Get today's checkin
    checkin = await db.daily_checkins.find_one({"user_id": user_id, "date": today}, {"_id": 0})
    
    # Get readiness score
    readiness = await db.readiness_scores.find_one({"user_id": user_id, "date": today}, {"_id": 0})
    
    # Get streak
    streak = await db.streak_records.find_one({"user_id": user_id, "streak_type": "daily_checkin"}, {"_id": 0})
    
    # Get active event
    event = await db.event_modes.find_one({"user_id": user_id, "is_active": True}, {"_id": 0})
    
    # Calculate event countdown
    event_countdown = None
    if event and event.get("event_date"):
        try:
            event_date = datetime.strptime(event["event_date"], "%Y-%m-%d")
            today_date = datetime.strptime(today, "%Y-%m-%d")
            event_countdown = (event_date - today_date).days
        except:
            pass
    
    # Get clothing recommendation
    clothing_rec = await db.clothing_recommendations.find_one(
        {"user_id": user_id, "is_acknowledged": False},
        {"_id": 0},
        sort=[("created_at", -1)]
    )
    
    # Build checklist status
    checklist = {
        "morning_checkin": bool(checkin and checkin.get("morning")),
        "workout_checkin": bool(checkin and checkin.get("workout")),
        "night_checkin": bool(checkin and checkin.get("night")),
        "workout_completed": bool(checkin and checkin.get("workout", {}).get("workout_completed")),
        "protein_hit": bool(checkin and checkin.get("night", {}).get("protein_target_hit")),
        "water_hit": bool(checkin and checkin.get("night", {}).get("water_target_hit")),
        "steps_completed": bool(checkin and checkin.get("night", {}).get("steps_completed"))
    }
    
    # Calculate consistency score (last 7 days)
    seven_days_ago = (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%d")
    recent_checkins = await db.daily_checkins.count_documents({
        "user_id": user_id,
        "date": {"$gte": seven_days_ago}
    })
    consistency_score = int((recent_checkins / 7) * 100)
    
    return {
        "user": {
            "name": user["name"],
            "athlete_level": profile.get("athlete_level") if profile else None
        },
        "profile": profile,
        "diet_plan": diet_plan,
        "workout_plan": workout_plan,
        "checkin": checkin,
        "checklist": checklist,
        "readiness": readiness,
        "streak": streak,
        "consistency_score": consistency_score,
        "event": event,
        "event_countdown": event_countdown,
        "clothing_recommendation": clothing_rec,
        "date": today
    }

# ==================== DIET ROUTES ====================

@api_router.get("/diet/today")
async def get_today_diet(request: Request):
    user = await get_current_user(request)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    diet_plan = await db.generated_diet_plans.find_one(
        {"user_id": user["_id"], "date": today},
        {"_id": 0}
    )
    
    if not diet_plan:
        # Generate if not exists
        profile = await db.user_profiles.find_one({"user_id": user["_id"]})
        if profile:
            profile_data = UserProfileData(**profile.get("profile_data", {}))
            athlete_level = AthleteLevel(profile.get("athlete_level", "beginner"))
            diet_plan = DietEngineService.generate_diet_plan(user["_id"], profile_data, athlete_level, today)
            await db.generated_diet_plans.insert_one(diet_plan.model_dump())
            return diet_plan.model_dump()
    
    return diet_plan or {}

@api_router.get("/diet/history")
async def get_diet_history(request: Request, days: int = 7):
    user = await get_current_user(request)
    start_date = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")
    
    plans = await db.generated_diet_plans.find(
        {"user_id": user["_id"], "date": {"$gte": start_date}},
        {"_id": 0}
    ).sort("date", -1).to_list(days)
    
    return plans

# ==================== WORKOUT ROUTES ====================

@api_router.get("/workout/today")
async def get_today_workout(request: Request):
    user = await get_current_user(request)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    workout_plan = await db.generated_workout_plans.find_one(
        {"user_id": user["_id"], "date": today},
        {"_id": 0}
    )
    
    if not workout_plan:
        profile = await db.user_profiles.find_one({"user_id": user["_id"]})
        if profile:
            profile_data = UserProfileData(**profile.get("profile_data", {}))
            athlete_level = AthleteLevel(profile.get("athlete_level", "beginner"))
            day_of_week = datetime.now(timezone.utc).strftime("%A").lower()
            workout_plan = WorkoutEngineService.generate_workout_plan(
                user["_id"], profile_data, athlete_level, today, day_of_week
            )
            if workout_plan:
                await db.generated_workout_plans.insert_one(workout_plan.model_dump())
                return workout_plan.model_dump()
    
    return workout_plan or {"rest_day": True, "message": "Rest day - focus on recovery"}

class WorkoutLogInput(BaseModel):
    exercises_completed: List[dict]
    duration_mins: int
    intensity_rating: int
    notes: Optional[str] = None

@api_router.post("/workout/log")
async def log_workout(data: WorkoutLogInput, request: Request):
    user = await get_current_user(request)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    workout_plan = await db.generated_workout_plans.find_one({"user_id": user["_id"], "date": today})
    
    log_doc = {
        "user_id": user["_id"],
        "workout_plan_id": str(workout_plan["_id"]) if workout_plan else None,
        "date": today,
        "exercises_completed": data.exercises_completed,
        "duration_mins": data.duration_mins,
        "intensity_rating": data.intensity_rating,
        "notes": data.notes,
        "completed": True,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    await db.workout_logs.insert_one(log_doc)
    
    return {"message": "Workout logged successfully"}

# ==================== CHECK-IN ROUTES ====================

class MorningCheckinInput(BaseModel):
    weight_kg: Optional[float] = None
    sleep_hours: Optional[float] = None
    sleep_quality: Optional[int] = None
    soreness_level: Optional[int] = None
    mood: Optional[int] = None
    energy: Optional[int] = None
    notes: Optional[str] = None

@api_router.post("/checkin/morning")
async def morning_checkin(data: MorningCheckinInput, request: Request):
    user = await get_current_user(request)
    user_id = user["_id"]
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    morning_data = data.model_dump()
    
    # Update daily checkin
    await db.daily_checkins.update_one(
        {"user_id": user_id, "date": today},
        {
            "$set": {
                "morning": morning_data,
                "updated_at": datetime.now(timezone.utc).isoformat()
            },
            "$setOnInsert": {
                "user_id": user_id,
                "date": today,
                "created_at": datetime.now(timezone.utc).isoformat()
            }
        },
        upsert=True
    )
    
    # Log weight if provided
    if data.weight_kg:
        await db.body_metrics.insert_one({
            "user_id": user_id,
            "date": today,
            "metric_type": "weight",
            "value": data.weight_kg,
            "created_at": datetime.now(timezone.utc).isoformat()
        })
    
    # Calculate readiness score
    morning_checkin = MorningCheckin(**morning_data)
    readiness = ReadinessEngineService.calculate_readiness(user_id, today, morning_checkin)
    
    # Get AI insight if available
    ai_insight = await ai_service.get_readiness_insight(readiness.model_dump())
    if ai_insight:
        readiness.ai_insight = ai_insight
    
    await db.readiness_scores.update_one(
        {"user_id": user_id, "date": today},
        {"$set": readiness.model_dump()},
        upsert=True
    )
    
    # Update streak
    current_streak = await db.streak_records.find_one({"user_id": user_id, "streak_type": "daily_checkin"})
    if current_streak:
        streak_record = StreakRecord(**{k: v for k, v in current_streak.items() if k != "_id"})
    else:
        streak_record = None
    
    new_streak = StreakEngineService.update_streak(streak_record, user_id, today)
    await db.streak_records.update_one(
        {"user_id": user_id, "streak_type": "daily_checkin"},
        {"$set": new_streak.model_dump()},
        upsert=True
    )
    
    return {
        "message": "Morning check-in saved",
        "readiness": readiness.model_dump(),
        "streak": new_streak.model_dump()
    }

class WorkoutCheckinInput(BaseModel):
    workout_completed: bool = False
    exercises_logged: Optional[List[dict]] = None
    cardio_completed: bool = False
    cardio_duration_mins: Optional[int] = None
    session_intensity: Optional[int] = None
    notes: Optional[str] = None

@api_router.post("/checkin/workout")
async def workout_checkin(data: WorkoutCheckinInput, request: Request):
    user = await get_current_user(request)
    user_id = user["_id"]
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    await db.daily_checkins.update_one(
        {"user_id": user_id, "date": today},
        {
            "$set": {
                "workout": data.model_dump(),
                "updated_at": datetime.now(timezone.utc).isoformat()
            },
            "$setOnInsert": {
                "user_id": user_id,
                "date": today,
                "created_at": datetime.now(timezone.utc).isoformat()
            }
        },
        upsert=True
    )
    
    return {"message": "Workout check-in saved"}

class NightCheckinInput(BaseModel):
    protein_target_hit: bool = False
    water_target_hit: bool = False
    steps_completed: bool = False
    steps_count: Optional[int] = None
    diet_adherence: Optional[int] = None
    calories_consumed: Optional[int] = None
    reflections: Optional[str] = None

@api_router.post("/checkin/night")
async def night_checkin(data: NightCheckinInput, request: Request):
    user = await get_current_user(request)
    user_id = user["_id"]
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    await db.daily_checkins.update_one(
        {"user_id": user_id, "date": today},
        {
            "$set": {
                "night": data.model_dump(),
                "updated_at": datetime.now(timezone.utc).isoformat()
            },
            "$setOnInsert": {
                "user_id": user_id,
                "date": today,
                "created_at": datetime.now(timezone.utc).isoformat()
            }
        },
        upsert=True
    )
    
    return {"message": "Night check-in saved"}

# ==================== PROGRESSION ROUTES ====================

@api_router.get("/progression/summary")
async def get_progression_summary(request: Request, days: int = 30):
    user = await get_current_user(request)
    user_id = user["_id"]
    start_date = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")
    
    # Get weight history
    weight_history = await db.body_metrics.find(
        {"user_id": user_id, "metric_type": "weight", "date": {"$gte": start_date}},
        {"_id": 0}
    ).sort("date", 1).to_list(days)
    
    # Get checkin history
    checkins = await db.daily_checkins.find(
        {"user_id": user_id, "date": {"$gte": start_date}},
        {"_id": 0}
    ).to_list(days)
    
    # Get readiness history
    readiness_history = await db.readiness_scores.find(
        {"user_id": user_id, "date": {"$gte": start_date}},
        {"_id": 0}
    ).sort("date", 1).to_list(days)
    
    # Calculate metrics
    workout_count = sum(1 for c in checkins if c.get("workout", {}).get("workout_completed"))
    protein_hit_count = sum(1 for c in checkins if c.get("night", {}).get("protein_target_hit"))
    water_hit_count = sum(1 for c in checkins if c.get("night", {}).get("water_target_hit"))
    
    total_days = len(checkins) or 1
    
    # Weight change
    weight_change = None
    if len(weight_history) >= 2:
        weight_change = weight_history[-1]["value"] - weight_history[0]["value"]
    
    # Average readiness
    avg_readiness = 0
    if readiness_history:
        avg_readiness = sum(r["score"] for r in readiness_history) / len(readiness_history)
    
    return {
        "period_days": days,
        "checkins_completed": len(checkins),
        "workout_completion_rate": round((workout_count / total_days) * 100),
        "protein_adherence_rate": round((protein_hit_count / total_days) * 100),
        "water_adherence_rate": round((water_hit_count / total_days) * 100),
        "weight_change_kg": round(weight_change, 1) if weight_change else None,
        "average_readiness": round(avg_readiness),
        "weight_history": weight_history,
        "readiness_history": readiness_history
    }

# ==================== EVENT MODE ROUTES ====================

class EventModeInput(BaseModel):
    event_name: str
    event_type: str
    event_date: str
    target_weight: Optional[float] = None
    notes: Optional[str] = None

@api_router.post("/event/create")
async def create_event(data: EventModeInput, request: Request):
    user = await get_current_user(request)
    user_id = user["_id"]
    
    # Deactivate any existing events
    await db.event_modes.update_many(
        {"user_id": user_id, "is_active": True},
        {"$set": {"is_active": False}}
    )
    
    event_doc = {
        "user_id": user_id,
        "event_name": data.event_name,
        "event_type": data.event_type,
        "event_date": data.event_date,
        "start_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "target_weight": data.target_weight,
        "is_active": True,
        "notes": data.notes,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    result = await db.event_modes.insert_one(event_doc)
    
    return {"message": "Event created", "event_id": str(result.inserted_id)}

@api_router.get("/event/active")
async def get_active_event(request: Request):
    user = await get_current_user(request)
    event = await db.event_modes.find_one(
        {"user_id": user["_id"], "is_active": True},
        {"_id": 0}
    )
    return event or {}

@api_router.post("/event/{event_id}/deactivate")
async def deactivate_event(event_id: str, request: Request):
    user = await get_current_user(request)
    await db.event_modes.update_one(
        {"user_id": user["_id"], "_id": ObjectId(event_id)},
        {"$set": {"is_active": False}}
    )
    return {"message": "Event deactivated"}

# ==================== WEEKLY REPORT ROUTES ====================

@api_router.get("/reports/weekly")
async def get_weekly_report(request: Request):
    user = await get_current_user(request)
    user_id = user["_id"]
    
    # Calculate week range
    today = datetime.now(timezone.utc)
    week_start = (today - timedelta(days=today.weekday())).strftime("%Y-%m-%d")
    week_end = today.strftime("%Y-%m-%d")
    
    # Check for existing report
    existing = await db.weekly_reports.find_one(
        {"user_id": user_id, "week_start": week_start},
        {"_id": 0}
    )
    
    if existing:
        return existing
    
    # Generate new report
    checkins = await db.daily_checkins.find(
        {"user_id": user_id, "date": {"$gte": week_start, "$lte": week_end}},
        {"_id": 0}
    ).to_list(7)
    
    workouts_completed = sum(1 for c in checkins if c.get("workout", {}).get("workout_completed"))
    protein_hit = sum(1 for c in checkins if c.get("night", {}).get("protein_target_hit"))
    water_hit = sum(1 for c in checkins if c.get("night", {}).get("water_target_hit"))
    
    profile = await db.user_profiles.find_one({"user_id": user_id})
    workouts_target = profile.get("profile_data", {}).get("workout_frequency", 4) if profile else 4
    
    # Determine strongest/weakest
    habits = {
        "workout": workouts_completed / max(workouts_target, 1),
        "protein": protein_hit / max(len(checkins), 1),
        "water": water_hit / max(len(checkins), 1)
    }
    strongest = max(habits, key=habits.get)
    weakest = min(habits, key=habits.get)
    
    # Readiness average
    readiness_scores = await db.readiness_scores.find(
        {"user_id": user_id, "date": {"$gte": week_start}},
        {"_id": 0}
    ).to_list(7)
    avg_readiness = sum(r["score"] for r in readiness_scores) / len(readiness_scores) if readiness_scores else 50
    
    report = {
        "user_id": user_id,
        "week_start": week_start,
        "week_end": week_end,
        "workouts_completed": workouts_completed,
        "workouts_target": workouts_target,
        "adherence_score": int((len(checkins) / 7) * 100),
        "strongest_habit": strongest,
        "weakest_habit": weakest,
        "average_readiness": int(avg_readiness),
        "progression_summary": f"Completed {workouts_completed}/{workouts_target} workouts. {strongest.title()} was your strongest area.",
        "next_week_focus": f"Focus on improving {weakest} adherence next week.",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    # Get AI insights
    ai_insights = await ai_service.get_weekly_insights(
        {"user_id": user_id, "athlete_level": profile.get("athlete_level") if profile else "beginner"},
        report
    )
    if ai_insights:
        report["ai_insights"] = ai_insights
    
    # Insert a copy to avoid _id mutation
    await db.weekly_reports.insert_one(report.copy())
    
    # Return clean report (without _id)
    return report

# ==================== ADMIN ROUTES ====================

@api_router.get("/admin/users")
async def admin_get_users(request: Request, skip: int = 0, limit: int = 50):
    await require_admin(request)
    
    users = await db.users.find(
        {},
        {"password_hash": 0}
    ).skip(skip).limit(limit).to_list(limit)
    
    for user in users:
        user["_id"] = str(user["_id"])
    
    total = await db.users.count_documents({})
    
    return {"users": users, "total": total}

@api_router.get("/admin/analytics")
async def admin_get_analytics(request: Request):
    await require_admin(request)
    
    total_users = await db.users.count_documents({})
    onboarded_users = await db.users.count_documents({"onboarding_completed": True})
    
    # Athlete level distribution using aggregation pipeline (optimized)
    level_pipeline = [
        {"$group": {"_id": "$athlete_level", "count": {"$sum": 1}}}
    ]
    level_results = await db.user_profiles.aggregate(level_pipeline).to_list(None)
    level_dist = {r["_id"] or "unknown": r["count"] for r in level_results}
    
    # Active today
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    active_today = await db.daily_checkins.count_documents({"date": today})
    
    # Event mode usage
    active_events = await db.event_modes.count_documents({"is_active": True})
    
    return {
        "total_users": total_users,
        "onboarded_users": onboarded_users,
        "onboarding_rate": round((onboarded_users / total_users) * 100) if total_users else 0,
        "active_today": active_today,
        "athlete_level_distribution": level_dist,
        "active_events": active_events
    }

@api_router.get("/admin/user/{user_id}")
async def admin_get_user_detail(user_id: str, request: Request):
    await require_admin(request)
    
    user = await db.users.find_one({"_id": ObjectId(user_id)}, {"password_hash": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user["_id"] = str(user["_id"])
    
    profile = await db.user_profiles.find_one({"user_id": user_id}, {"_id": 0})
    streak = await db.streak_records.find_one({"user_id": user_id}, {"_id": 0})
    
    return {
        "user": user,
        "profile": profile,
        "streak": streak
    }

# ==================== PRODUCTS ROUTES (Commerce Abstraction) ====================

@api_router.get("/products")
async def get_products(category: Optional[str] = None, body_stage: Optional[str] = None):
    query = {"in_stock": True}
    if category:
        query["category"] = category
    if body_stage:
        query["body_stage"] = body_stage
    
    products = await db.products.find(query, {"_id": 0}).to_list(100)
    return products

@api_router.get("/products/{product_id}")
async def get_product(product_id: str):
    product = await db.products.find_one({"id": product_id}, {"_id": 0})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# ==================== HEALTH CHECK ====================

@api_router.get("/")
async def root():
    return {"message": "MAVR API - Athlete Operating System", "version": "1.0.0"}

@api_router.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()}

# Include router
app.include_router(api_router)

# CORS
cors_origins = os.environ.get("CORS_ORIGINS", "*")
frontend_url = os.environ.get("FRONTEND_URL", "http://localhost:3000")
if cors_origins == "*":
    allowed_origins = ["*"]
else:
    allowed_origins = [o.strip() for o in cors_origins.split(",") if o.strip()]
    if frontend_url not in allowed_origins:
        allowed_origins.append(frontend_url)
    if "http://localhost:3000" not in allowed_origins:
        allowed_origins.append("http://localhost:3000")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event
@app.on_event("startup")
async def startup_event():
    # Create indexes
    await db.users.create_index("email", unique=True)
    await db.user_profiles.create_index("user_id", unique=True)
    await db.generated_diet_plans.create_index([("user_id", 1), ("date", 1)])
    await db.generated_workout_plans.create_index([("user_id", 1), ("date", 1)])
    await db.daily_checkins.create_index([("user_id", 1), ("date", 1)])
    await db.readiness_scores.create_index([("user_id", 1), ("date", 1)])
    await db.streak_records.create_index([("user_id", 1), ("streak_type", 1)])
    await db.body_metrics.create_index([("user_id", 1), ("date", 1)])
    await db.weekly_reports.create_index([("user_id", 1), ("week_start", 1)])
    await db.event_modes.create_index([("user_id", 1), ("is_active", 1)])
    
    # Seed admin
    admin_email = os.environ.get("ADMIN_EMAIL", "admin@mavr.com")
    admin_password = os.environ.get("ADMIN_PASSWORD", "MavrAdmin123!")
    
    existing = await db.users.find_one({"email": admin_email})
    if not existing:
        await db.users.insert_one({
            "email": admin_email,
            "name": "MAVR Admin",
            "password_hash": hash_password(admin_password),
            "role": "admin",
            "onboarding_completed": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        })
        logger.info(f"Admin user created: {admin_email}")
    
    # Write test credentials
    Path("/app/memory").mkdir(exist_ok=True)
    with open("/app/memory/test_credentials.md", "w") as f:
        f.write(f"""# MAVR Test Credentials

## Admin Account
- Email: {admin_email}
- Password: {admin_password}
- Role: admin

## Test User
- Register a new user via /api/auth/register

## Auth Endpoints
- POST /api/auth/register
- POST /api/auth/login
- POST /api/auth/logout
- GET /api/auth/me
- POST /api/auth/refresh
""")
    
    logger.info("MAVR API started successfully")

@app.on_event("shutdown")
async def shutdown_event():
    client.close()
