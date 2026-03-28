"""
Athlete Classification Service
Rule-based classification engine for determining athlete level
"""
from models.user import AthleteLevel, UserProfileData, Goal

class ClassificationService:
    """
    Rule-based athlete classification
    Uses training age, workout frequency, goal complexity, and fitness indicators
    """
    
    @staticmethod
    def classify_athlete(profile: UserProfileData) -> AthleteLevel:
        """
        Classify athlete based on multiple factors
        Returns: beginner, intermediate, advanced, or professional
        """
        score = 0
        
        # Training Age (max 30 points)
        training_age = profile.training_age_months or 0
        if training_age < 6:
            score += 5
        elif training_age < 12:
            score += 10
        elif training_age < 24:
            score += 20
        elif training_age < 48:
            score += 25
        else:
            score += 30
        
        # Workout Frequency (max 20 points)
        frequency = profile.workout_frequency or 0
        if frequency <= 2:
            score += 5
        elif frequency <= 3:
            score += 10
        elif frequency <= 5:
            score += 15
        else:
            score += 20
        
        # Activity Level (max 15 points)
        activity = profile.activity_level or "sedentary"
        activity_scores = {
            "sedentary": 3,
            "lightly_active": 6,
            "moderately_active": 10,
            "very_active": 13,
            "extremely_active": 15
        }
        score += activity_scores.get(activity, 5)
        
        # Goal Complexity (max 15 points)
        goal = profile.goal
        if goal in [Goal.GENERAL_FITNESS, Goal.FAT_LOSS]:
            score += 5
        elif goal in [Goal.MUSCLE_GAIN, Goal.MAINTENANCE]:
            score += 10
        elif goal in [Goal.STRENGTH, Goal.ENDURANCE]:
            score += 12
        elif goal == Goal.SPORTS_PERFORMANCE:
            score += 15
        
        # Equipment/Setup (max 10 points)
        equipment_count = len(profile.available_equipment or [])
        if equipment_count > 10:
            score += 10
        elif equipment_count > 5:
            score += 7
        else:
            score += 3
        
        # Has Event Goal (max 10 points)
        if profile.event_goal:
            score += 10
        
        # Classification Thresholds
        if score < 25:
            return AthleteLevel.BEGINNER
        elif score < 50:
            return AthleteLevel.INTERMEDIATE
        elif score < 75:
            return AthleteLevel.ADVANCED
        else:
            return AthleteLevel.PROFESSIONAL
    
    @staticmethod
    def get_classification_breakdown(profile: UserProfileData) -> dict:
        """Get detailed breakdown of classification factors"""
        training_age = profile.training_age_months or 0
        frequency = profile.workout_frequency or 0
        activity = profile.activity_level or "sedentary"
        
        return {
            "training_age_months": training_age,
            "workout_frequency": frequency,
            "activity_level": activity,
            "goal": profile.goal.value if profile.goal else "not_set",
            "has_event": bool(profile.event_goal),
            "equipment_count": len(profile.available_equipment or []),
            "classification": ClassificationService.classify_athlete(profile).value
        }
