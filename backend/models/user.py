from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime, timezone
from enum import Enum

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class AthleteLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    PROFESSIONAL = "professional"

class Goal(str, Enum):
    FAT_LOSS = "fat_loss"
    MUSCLE_GAIN = "muscle_gain"
    MAINTENANCE = "maintenance"
    STRENGTH = "strength"
    ENDURANCE = "endurance"
    SPORTS_PERFORMANCE = "sports_performance"
    GENERAL_FITNESS = "general_fitness"

class DietPreference(str, Enum):
    VEGETARIAN = "vegetarian"
    NON_VEGETARIAN = "non_vegetarian"
    EGGETARIAN = "eggetarian"
    VEGAN = "vegan"

class BudgetLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class WorkoutSetup(str, Enum):
    GYM = "gym"
    HOME = "home"
    BOTH = "both"

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    role: str = "user"
    onboarding_completed: bool = False
    created_at: Optional[str] = None

class UserProfileData(BaseModel):
    # Basic Info
    age: Optional[int] = None
    gender: Optional[str] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    target_weight_kg: Optional[float] = None
    
    # Goals
    goal: Optional[Goal] = None
    training_age_months: Optional[int] = None
    
    # Workout Preferences
    workout_frequency: Optional[int] = None  # days per week
    preferred_workout_days: Optional[List[str]] = None
    workout_setup: Optional[WorkoutSetup] = None
    available_equipment: Optional[List[str]] = None
    weak_muscle_groups: Optional[List[str]] = None
    injuries: Optional[List[str]] = None
    
    # Lifestyle
    sleep_hours: Optional[float] = None
    stress_level: Optional[int] = None  # 1-10
    activity_level: Optional[str] = None
    daily_steps: Optional[int] = None
    water_intake_liters: Optional[float] = None
    
    # Diet
    diet_preference: Optional[DietPreference] = None
    allergies: Optional[List[str]] = None
    food_dislikes: Optional[List[str]] = None
    meal_frequency: Optional[int] = None
    budget_level: Optional[BudgetLevel] = None
    supplements: Optional[List[str]] = None
    
    # Event
    event_goal: Optional[str] = None
    event_date: Optional[str] = None

class UserProfile(BaseModel):
    user_id: str
    profile_data: UserProfileData
    athlete_level: Optional[AthleteLevel] = None
    bmr: Optional[float] = None
    tdee: Optional[float] = None
    target_calories: Optional[int] = None
    target_protein: Optional[int] = None
    target_carbs: Optional[int] = None
    target_fats: Optional[int] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
