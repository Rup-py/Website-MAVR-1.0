from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, timezone
from enum import Enum

class MuscleGroup(str, Enum):
    CHEST = "chest"
    BACK = "back"
    SHOULDERS = "shoulders"
    BICEPS = "biceps"
    TRICEPS = "triceps"
    LEGS = "legs"
    CORE = "core"
    CARDIO = "cardio"
    FULL_BODY = "full_body"

class ExerciseType(str, Enum):
    STRENGTH = "strength"
    CARDIO = "cardio"
    FLEXIBILITY = "flexibility"
    COMPOUND = "compound"
    ISOLATION = "isolation"

class Exercise(BaseModel):
    name: str
    muscle_group: MuscleGroup
    exercise_type: ExerciseType
    sets: int
    reps: str  # Can be "8-12" or "30 sec" etc
    rest_seconds: int
    notes: Optional[str] = None
    video_link: Optional[str] = None
    substitutes: Optional[List[str]] = None
    equipment_needed: Optional[List[str]] = None

class WorkoutSession(BaseModel):
    name: str  # e.g., "Push Day", "Leg Day"
    day_of_week: str
    focus_areas: List[MuscleGroup]
    warmup: List[Exercise]
    main_workout: List[Exercise]
    cooldown: List[Exercise]
    estimated_duration_mins: int
    intensity_level: str  # low, medium, high

class WorkoutPlan(BaseModel):
    user_id: str
    date: str  # YYYY-MM-DD
    session: WorkoutSession
    ai_guidance: Optional[str] = None
    progression_notes: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class WorkoutPlanResponse(BaseModel):
    id: str
    user_id: str
    date: str
    session: WorkoutSession
    ai_guidance: Optional[str] = None
    progression_notes: Optional[str] = None

class WorkoutLog(BaseModel):
    user_id: str
    workout_plan_id: str
    date: str
    exercises_completed: List[dict]  # {exercise_name, sets_completed, reps_done, weight_used}
    duration_mins: int
    intensity_rating: int  # 1-10
    notes: Optional[str] = None
    completed: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
