"""
Calorie & Macro Calculator Service
Rule-based engine for TDEE, BMR, and macro calculations
"""
from models.user import UserProfileData, Goal, AthleteLevel

class CalorieService:
    """
    Rule-based calorie and macro calculator
    Uses Mifflin-St Jeor equation with activity multipliers
    """
    
    ACTIVITY_MULTIPLIERS = {
        "sedentary": 1.2,
        "lightly_active": 1.375,
        "moderately_active": 1.55,
        "very_active": 1.725,
        "extremely_active": 1.9
    }
    
    GOAL_ADJUSTMENTS = {
        Goal.FAT_LOSS: -0.20,  # 20% deficit
        Goal.MUSCLE_GAIN: 0.15,  # 15% surplus
        Goal.MAINTENANCE: 0,
        Goal.STRENGTH: 0.10,  # 10% surplus
        Goal.ENDURANCE: 0.05,  # 5% surplus
        Goal.SPORTS_PERFORMANCE: 0.10,
        Goal.GENERAL_FITNESS: 0
    }
    
    @staticmethod
    def calculate_bmr(weight_kg: float, height_cm: float, age: int, gender: str = "male") -> float:
        """
        Calculate BMR using Mifflin-St Jeor equation
        """
        if gender.lower() == "female":
            bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
        else:
            bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
        return round(bmr, 2)
    
    @staticmethod
    def calculate_tdee(bmr: float, activity_level: str) -> float:
        """Calculate TDEE based on activity level"""
        multiplier = CalorieService.ACTIVITY_MULTIPLIERS.get(activity_level, 1.55)
        return round(bmr * multiplier, 2)
    
    @staticmethod
    def calculate_target_calories(tdee: float, goal: Goal) -> int:
        """Calculate target calories based on goal"""
        adjustment = CalorieService.GOAL_ADJUSTMENTS.get(goal, 0)
        target = tdee * (1 + adjustment)
        return round(target)
    
    @staticmethod
    def calculate_macros(calories: int, weight_kg: float, goal: Goal, athlete_level: AthleteLevel) -> dict:
        """
        Calculate macro targets based on goal and athlete level
        Returns protein, carbs, fats in grams
        """
        # Protein: Based on goal and level
        protein_multipliers = {
            Goal.FAT_LOSS: 2.2,  # Higher protein during cut
            Goal.MUSCLE_GAIN: 2.0,
            Goal.STRENGTH: 2.0,
            Goal.MAINTENANCE: 1.6,
            Goal.ENDURANCE: 1.4,
            Goal.SPORTS_PERFORMANCE: 1.8,
            Goal.GENERAL_FITNESS: 1.6
        }
        
        level_bonus = {
            AthleteLevel.BEGINNER: 0,
            AthleteLevel.INTERMEDIATE: 0.1,
            AthleteLevel.ADVANCED: 0.2,
            AthleteLevel.PROFESSIONAL: 0.3
        }
        
        protein_per_kg = protein_multipliers.get(goal, 1.6) + level_bonus.get(athlete_level, 0)
        protein_g = round(weight_kg * protein_per_kg)
        protein_calories = protein_g * 4
        
        # Fats: 25-30% of calories based on goal
        fat_percentage = 0.25 if goal == Goal.FAT_LOSS else 0.28
        fat_calories = calories * fat_percentage
        fat_g = round(fat_calories / 9)
        
        # Carbs: Remaining calories
        remaining_calories = calories - protein_calories - fat_calories
        carbs_g = round(remaining_calories / 4)
        
        return {
            "protein_g": protein_g,
            "carbs_g": carbs_g,
            "fats_g": fat_g,
            "protein_calories": protein_calories,
            "carbs_calories": carbs_g * 4,
            "fat_calories": fat_g * 9
        }
    
    @staticmethod
    def calculate_water_target(weight_kg: float, activity_level: str) -> float:
        """Calculate daily water target in liters"""
        base = weight_kg * 0.033  # Base: 33ml per kg
        activity_bonus = {
            "sedentary": 0,
            "lightly_active": 0.3,
            "moderately_active": 0.5,
            "very_active": 0.8,
            "extremely_active": 1.0
        }
        return round(base + activity_bonus.get(activity_level, 0.3), 1)
    
    @staticmethod
    def get_full_calculation(profile: UserProfileData, athlete_level: AthleteLevel) -> dict:
        """Get complete calorie and macro calculation"""
        weight = profile.weight_kg or 70
        height = profile.height_cm or 170
        age = profile.age or 25
        gender = profile.gender or "male"
        activity = profile.activity_level or "moderately_active"
        goal = profile.goal or Goal.GENERAL_FITNESS
        
        bmr = CalorieService.calculate_bmr(weight, height, age, gender)
        tdee = CalorieService.calculate_tdee(bmr, activity)
        target_calories = CalorieService.calculate_target_calories(tdee, goal)
        macros = CalorieService.calculate_macros(target_calories, weight, goal, athlete_level)
        water = CalorieService.calculate_water_target(weight, activity)
        
        return {
            "bmr": bmr,
            "tdee": tdee,
            "target_calories": target_calories,
            "target_protein": macros["protein_g"],
            "target_carbs": macros["carbs_g"],
            "target_fats": macros["fats_g"],
            "water_target_liters": water,
            "macros_detail": macros
        }
