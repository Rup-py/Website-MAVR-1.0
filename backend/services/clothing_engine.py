"""
Clothing Recommendation Engine
Rule-based bodywear recommendations based on progress
"""
from typing import Optional, List
from datetime import datetime, timezone
from models.event_commerce import BodyStage, ClothingProfile, ClothingRecommendation

class ClothingEngineService:
    """
    Rule-based clothing recommendation engine
    Uses body stage, training consistency, and progress metrics
    """
    
    # Body stage thresholds
    STAGE_THRESHOLDS = {
        BodyStage.START_FIT: {
            "min_consistency": 0,
            "min_progress": 0,
            "description": "Beginning your fitness journey"
        },
        BodyStage.BUILD_FIT: {
            "min_consistency": 50,
            "min_progress": 30,
            "description": "Building strength and conditioning"
        },
        BodyStage.PEAK_FIT: {
            "min_consistency": 80,
            "min_progress": 70,
            "description": "Peak performance ready"
        }
    }
    
    @staticmethod
    def calculate_body_stage(
        training_consistency: int,  # 0-100
        body_composition_progress: int  # 0-100
    ) -> BodyStage:
        """Determine body stage based on metrics"""
        
        if training_consistency >= 80 and body_composition_progress >= 70:
            return BodyStage.PEAK_FIT
        elif training_consistency >= 50 and body_composition_progress >= 30:
            return BodyStage.BUILD_FIT
        else:
            return BodyStage.START_FIT
    
    @staticmethod
    def get_size_recommendation(
        weight_kg: float,
        height_cm: float,
        body_stage: BodyStage
    ) -> str:
        """Get recommended fit size based on body metrics"""
        
        # BMI-based sizing (simplified)
        bmi = weight_kg / ((height_cm / 100) ** 2)
        
        if body_stage == BodyStage.PEAK_FIT:
            # Peak fit users typically want tighter fit
            if bmi < 22:
                return "S"
            elif bmi < 25:
                return "M"
            elif bmi < 28:
                return "L"
            else:
                return "XL"
        elif body_stage == BodyStage.BUILD_FIT:
            # Build fit - standard sizing
            if bmi < 21:
                return "S"
            elif bmi < 24:
                return "M"
            elif bmi < 27:
                return "L"
            else:
                return "XL"
        else:
            # Start fit - slightly looser for comfort
            if bmi < 20:
                return "S"
            elif bmi < 23:
                return "M"
            elif bmi < 26:
                return "L"
            else:
                return "XL"
    
    @staticmethod
    def generate_recommendation(
        user_id: str,
        current_stage: BodyStage,
        new_stage: BodyStage,
        training_consistency: int,
        weight_change: Optional[float] = None
    ) -> Optional[ClothingRecommendation]:
        """Generate clothing recommendation if stage transition detected"""
        
        if current_stage == new_stage:
            return None  # No transition
        
        # Stage upgrade messages
        messages = {
            (BodyStage.START_FIT, BodyStage.BUILD_FIT): {
                "text": "Your body has evolved. Based on your progress, Build Fit now matches you better.",
                "reason": "Consistency above 50% and visible body composition changes detected.",
                "products": ["Build Fit Compression Tee", "Performance Training Shorts"]
            },
            (BodyStage.BUILD_FIT, BodyStage.PEAK_FIT): {
                "text": "Your current phase is aligned with Peak Fit. Time to upgrade your gear.",
                "reason": "Elite consistency (80%+) and significant body transformation achieved.",
                "products": ["Peak Fit Compression Set", "Elite Performance Tank"]
            },
            (BodyStage.START_FIT, BodyStage.PEAK_FIT): {
                "text": "Remarkable transformation. Your body is ready for Peak Fit gear.",
                "reason": "Exceptional progress and consistency metrics detected.",
                "products": ["Peak Fit Full Kit", "Competition Compression Wear"]
            }
        }
        
        transition = (current_stage, new_stage)
        if transition not in messages:
            return None
        
        msg = messages[transition]
        
        return ClothingRecommendation(
            user_id=user_id,
            body_stage=new_stage,
            recommendation_text=msg["text"],
            recommended_products=msg["products"],
            reason=msg["reason"]
        )
    
    @staticmethod
    def get_products_for_stage(stage: BodyStage) -> List[dict]:
        """Get recommended products for a body stage"""
        
        products = {
            BodyStage.START_FIT: [
                {"name": "Start Fit Training Tee", "price": 999, "category": "performance"},
                {"name": "Essential Training Shorts", "price": 799, "category": "performance"},
                {"name": "Basic Compression Socks", "price": 299, "category": "accessories"}
            ],
            BodyStage.BUILD_FIT: [
                {"name": "Build Fit Compression Tee", "price": 1499, "category": "compression"},
                {"name": "Performance Training Shorts", "price": 1199, "category": "performance"},
                {"name": "Build Fit Tank Top", "price": 999, "category": "performance"},
                {"name": "Pro Compression Socks", "price": 499, "category": "accessories"}
            ],
            BodyStage.PEAK_FIT: [
                {"name": "Peak Fit Compression Set", "price": 2999, "category": "compression"},
                {"name": "Elite Performance Tank", "price": 1799, "category": "performance"},
                {"name": "Competition Shorts", "price": 1599, "category": "performance"},
                {"name": "Peak Recovery Compression", "price": 1999, "category": "recovery"}
            ]
        }
        
        return products.get(stage, products[BodyStage.START_FIT])
