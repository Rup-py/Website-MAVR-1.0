from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime, timezone
from enum import Enum

class CheckinType(str, Enum):
    MORNING = "morning"
    WORKOUT = "workout"
    NIGHT = "night"

class ReadinessLevel(str, Enum):
    PUSH = "push"
    MAINTAIN = "maintain"
    RECOVER = "recover"

class MorningCheckin(BaseModel):
    weight_kg: Optional[float] = None
    sleep_hours: Optional[float] = None
    sleep_quality: Optional[int] = None  # 1-10
    soreness_level: Optional[int] = None  # 1-10
    mood: Optional[int] = None  # 1-10
    energy: Optional[int] = None  # 1-10
    notes: Optional[str] = None

class WorkoutCheckin(BaseModel):
    workout_completed: bool = False
    exercises_logged: Optional[List[dict]] = None
    cardio_completed: bool = False
    cardio_duration_mins: Optional[int] = None
    session_intensity: Optional[int] = None  # 1-10
    notes: Optional[str] = None

class NightCheckin(BaseModel):
    protein_target_hit: bool = False
    water_target_hit: bool = False
    steps_completed: bool = False
    steps_count: Optional[int] = None
    diet_adherence: Optional[int] = None  # 1-10
    calories_consumed: Optional[int] = None
    reflections: Optional[str] = None

class DailyCheckin(BaseModel):
    user_id: str
    date: str  # YYYY-MM-DD
    morning: Optional[MorningCheckin] = None
    workout: Optional[WorkoutCheckin] = None
    night: Optional[NightCheckin] = None
    checklist_items: Dict[str, bool] = {}  # Generic checklist
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class DailyTarget(BaseModel):
    user_id: str
    date: str
    workout_target: bool = True
    protein_target_g: int = 0
    water_target_l: float = 0
    steps_target: int = 0
    calories_target: int = 0
    sleep_target_hrs: float = 7
    custom_targets: Optional[List[dict]] = None  # [{name, completed}]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ReadinessScore(BaseModel):
    user_id: str
    date: str
    score: int  # 0-100
    level: ReadinessLevel
    factors: Dict[str, int]  # {sleep: 8, soreness: 3, mood: 7, energy: 8}
    recommendation: str
    ai_insight: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StreakRecord(BaseModel):
    user_id: str
    current_streak: int = 0
    longest_streak: int = 0
    last_checkin_date: Optional[str] = None
    streak_type: str = "daily_checkin"  # Can be workout, diet, etc
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ProgressionRecord(BaseModel):
    user_id: str
    date: str
    metric_type: str  # weight, strength, adherence, etc
    value: float
    previous_value: Optional[float] = None
    change: Optional[float] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class WeeklyReport(BaseModel):
    user_id: str
    week_start: str
    week_end: str
    workouts_completed: int
    workouts_target: int
    adherence_score: int  # 0-100
    strongest_habit: str
    weakest_habit: str
    weight_change: Optional[float] = None
    average_readiness: int
    progression_summary: str
    ai_insights: Optional[str] = None
    next_week_focus: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
