from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, timezone, date
from enum import Enum

class MealType(str, Enum):
    BREAKFAST = "breakfast"
    MID_MORNING = "mid_morning"
    LUNCH = "lunch"
    EVENING_SNACK = "evening_snack"
    DINNER = "dinner"
    PRE_WORKOUT = "pre_workout"
    POST_WORKOUT = "post_workout"

class FoodItem(BaseModel):
    name: str
    quantity: str
    calories: int
    protein: float
    carbs: float
    fats: float
    notes: Optional[str] = None
    substitutes: Optional[List[str]] = None

class Meal(BaseModel):
    meal_type: MealType
    time_suggestion: str
    items: List[FoodItem]
    total_calories: int
    total_protein: float
    total_carbs: float
    total_fats: float

class DietPlan(BaseModel):
    user_id: str
    date: str  # YYYY-MM-DD
    target_calories: int
    target_protein: int
    target_carbs: int
    target_fats: int
    target_water_liters: float
    meals: List[Meal]
    ai_guidance: Optional[str] = None
    notes: Optional[str] = None
    budget_friendly: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class DietPlanResponse(BaseModel):
    id: str
    user_id: str
    date: str
    target_calories: int
    target_protein: int
    target_carbs: int
    target_fats: int
    target_water_liters: float
    meals: List[Meal]
    ai_guidance: Optional[str] = None
    notes: Optional[str] = None
