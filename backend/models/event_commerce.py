from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, timezone
from enum import Enum

class EventType(str, Enum):
    TRANSFORMATION = "transformation"
    FOOTBALL_TRIAL = "football_trial"
    FIGHT_CAMP = "fight_camp"
    MARATHON = "marathon"
    POWERLIFTING = "powerlifting"
    PHYSIQUE = "physique"
    CUSTOM = "custom"

class EventMode(BaseModel):
    user_id: str
    event_name: str
    event_type: EventType
    event_date: str  # YYYY-MM-DD
    start_date: str
    target_weight: Optional[float] = None
    current_weight: Optional[float] = None
    daily_targets: Optional[dict] = None  # Enhanced targets during event
    is_active: bool = True
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class EventProgress(BaseModel):
    event_id: str
    user_id: str
    date: str
    days_remaining: int
    weight: Optional[float] = None
    adherence_score: int
    readiness_score: int
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Clothing/Bodywear Models
class BodyStage(str, Enum):
    START_FIT = "start_fit"
    BUILD_FIT = "build_fit"
    PEAK_FIT = "peak_fit"

class ClothingProfile(BaseModel):
    user_id: str
    body_stage: BodyStage
    training_consistency: int  # 0-100
    body_composition_progress: int  # 0-100
    current_fit_size: str
    recommended_fit_size: str
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ClothingRecommendation(BaseModel):
    user_id: str
    body_stage: BodyStage
    recommendation_text: str
    recommended_products: List[str]
    reason: str
    is_acknowledged: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Product & Commerce (Abstraction)
class ProductCategory(str, Enum):
    COMPRESSION = "compression"
    PERFORMANCE = "performance"
    RECOVERY = "recovery"
    ACCESSORIES = "accessories"

class Product(BaseModel):
    id: str
    name: str
    description: str
    category: ProductCategory
    body_stage: BodyStage
    price: float
    currency: str = "INR"
    images: List[str] = []
    sizes: List[str] = []
    in_stock: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class CartItem(BaseModel):
    product_id: str
    quantity: int
    size: str

class Order(BaseModel):
    user_id: str
    items: List[CartItem]
    total_amount: float
    currency: str = "INR"
    status: str = "pending"  # pending, paid, shipped, delivered
    payment_id: Optional[str] = None
    shipping_address: Optional[dict] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
