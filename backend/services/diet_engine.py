"""
Diet Engine Service
Rule-based diet plan generation with AI enhancement
"""
import os
import json
from datetime import datetime, timezone
from typing import Optional
from models.user import UserProfileData, AthleteLevel, DietPreference, BudgetLevel, Goal
from models.diet import DietPlan, Meal, MealType, FoodItem
from services.calorie_service import CalorieService

# Indian food database by budget and preference
INDIAN_FOOD_DATABASE = {
    "vegetarian": {
        "low": {
            "breakfast": [
                {"name": "Poha", "qty": "1 plate", "cal": 250, "p": 6, "c": 45, "f": 8},
                {"name": "Upma", "qty": "1 plate", "cal": 230, "p": 5, "c": 40, "f": 7},
                {"name": "Besan Chilla", "qty": "2 pieces", "cal": 200, "p": 10, "c": 25, "f": 8},
                {"name": "Roti + Sabzi", "qty": "2 roti", "cal": 280, "p": 8, "c": 45, "f": 10},
            ],
            "lunch": [
                {"name": "Dal Rice", "qty": "1 plate", "cal": 400, "p": 14, "c": 65, "f": 10},
                {"name": "Rajma Chawal", "qty": "1 plate", "cal": 420, "p": 16, "c": 60, "f": 12},
                {"name": "Chole Roti", "qty": "2 roti + curry", "cal": 380, "p": 15, "c": 55, "f": 10},
                {"name": "Khichdi + Curd", "qty": "1 plate", "cal": 350, "p": 12, "c": 50, "f": 10},
            ],
            "dinner": [
                {"name": "Roti Sabzi", "qty": "3 roti + sabzi", "cal": 350, "p": 10, "c": 55, "f": 12},
                {"name": "Dal + Rice", "qty": "1 plate", "cal": 380, "p": 14, "c": 60, "f": 10},
                {"name": "Palak Paneer + Roti", "qty": "2 roti", "cal": 400, "p": 18, "c": 45, "f": 15},
            ],
            "snacks": [
                {"name": "Roasted Chana", "qty": "50g", "cal": 180, "p": 10, "c": 30, "f": 3},
                {"name": "Makhana", "qty": "1 cup", "cal": 100, "p": 4, "c": 20, "f": 1},
                {"name": "Sprouts Chaat", "qty": "1 bowl", "cal": 150, "p": 10, "c": 25, "f": 2},
            ],
            "protein_sources": [
                {"name": "Paneer", "qty": "100g", "cal": 265, "p": 20, "c": 3, "f": 20},
                {"name": "Curd", "qty": "200g", "cal": 120, "p": 8, "c": 10, "f": 6},
                {"name": "Soy Chunks", "qty": "50g dry", "cal": 170, "p": 26, "c": 15, "f": 0.5},
                {"name": "Moong Dal", "qty": "50g dry", "cal": 170, "p": 12, "c": 30, "f": 0.5},
            ]
        },
        "medium": {
            "breakfast": [
                {"name": "Paneer Paratha", "qty": "2 pieces", "cal": 380, "p": 16, "c": 40, "f": 18},
                {"name": "Idli Sambar", "qty": "4 idli", "cal": 280, "p": 10, "c": 50, "f": 5},
                {"name": "Oats Upma", "qty": "1 plate", "cal": 250, "p": 10, "c": 35, "f": 8},
            ],
            "lunch": [
                {"name": "Paneer Curry + Roti", "qty": "3 roti", "cal": 500, "p": 25, "c": 55, "f": 20},
                {"name": "Mixed Dal + Brown Rice", "qty": "1 plate", "cal": 420, "p": 18, "c": 60, "f": 10},
            ],
            "dinner": [
                {"name": "Paneer Tikka + Roti", "qty": "2 roti", "cal": 420, "p": 25, "c": 40, "f": 18},
                {"name": "Mixed Veg Curry + Rice", "qty": "1 plate", "cal": 380, "p": 12, "c": 60, "f": 12},
            ],
            "snacks": [
                {"name": "Greek Yogurt", "qty": "150g", "cal": 130, "p": 15, "c": 8, "f": 4},
                {"name": "Protein Shake", "qty": "1 scoop", "cal": 120, "p": 24, "c": 3, "f": 1},
            ],
            "protein_sources": [
                {"name": "Cottage Cheese", "qty": "100g", "cal": 98, "p": 12, "c": 3, "f": 4},
                {"name": "Tofu", "qty": "100g", "cal": 144, "p": 15, "c": 3, "f": 8},
            ]
        }
    },
    "non_vegetarian": {
        "low": {
            "breakfast": [
                {"name": "Egg Bhurji + Roti", "qty": "3 eggs + 2 roti", "cal": 350, "p": 22, "c": 35, "f": 15},
                {"name": "Boiled Eggs", "qty": "4 eggs", "cal": 280, "p": 24, "c": 2, "f": 20},
                {"name": "Poha + Egg", "qty": "1 plate + 2 eggs", "cal": 350, "p": 18, "c": 45, "f": 12},
            ],
            "lunch": [
                {"name": "Chicken Curry + Rice", "qty": "150g chicken", "cal": 480, "p": 35, "c": 50, "f": 15},
                {"name": "Egg Curry + Roti", "qty": "3 eggs + 2 roti", "cal": 400, "p": 22, "c": 40, "f": 18},
                {"name": "Fish Curry + Rice", "qty": "150g fish", "cal": 420, "p": 30, "c": 50, "f": 12},
            ],
            "dinner": [
                {"name": "Chicken + Roti", "qty": "150g + 2 roti", "cal": 420, "p": 35, "c": 40, "f": 14},
                {"name": "Egg Omelette + Roti", "qty": "3 eggs + 2 roti", "cal": 380, "p": 22, "c": 35, "f": 18},
            ],
            "snacks": [
                {"name": "Boiled Eggs", "qty": "2 eggs", "cal": 140, "p": 12, "c": 1, "f": 10},
                {"name": "Chicken Breast", "qty": "100g", "cal": 165, "p": 31, "c": 0, "f": 4},
            ],
            "protein_sources": [
                {"name": "Chicken Breast", "qty": "150g", "cal": 248, "p": 46, "c": 0, "f": 6},
                {"name": "Eggs", "qty": "4 whole", "cal": 280, "p": 24, "c": 2, "f": 20},
                {"name": "Fish (Rohu)", "qty": "150g", "cal": 180, "p": 30, "c": 0, "f": 6},
            ]
        },
        "medium": {
            "breakfast": [
                {"name": "Egg White Omelette + Toast", "qty": "5 whites", "cal": 250, "p": 25, "c": 25, "f": 5},
                {"name": "Chicken Sandwich", "qty": "1 sandwich", "cal": 350, "p": 28, "c": 30, "f": 12},
            ],
            "lunch": [
                {"name": "Grilled Chicken + Rice", "qty": "200g chicken", "cal": 520, "p": 45, "c": 50, "f": 12},
                {"name": "Fish Tikka + Roti", "qty": "200g", "cal": 400, "p": 40, "c": 35, "f": 12},
            ],
            "dinner": [
                {"name": "Chicken Tikka + Salad", "qty": "200g", "cal": 350, "p": 42, "c": 10, "f": 16},
                {"name": "Grilled Fish + Veggies", "qty": "200g", "cal": 320, "p": 38, "c": 15, "f": 12},
            ],
            "snacks": [
                {"name": "Protein Shake + Banana", "qty": "1 serving", "cal": 220, "p": 26, "c": 25, "f": 2},
            ],
            "protein_sources": [
                {"name": "Chicken Breast", "qty": "200g", "cal": 330, "p": 62, "c": 0, "f": 8},
                {"name": "Salmon", "qty": "150g", "cal": 280, "p": 34, "c": 0, "f": 16},
            ]
        }
    },
    "eggetarian": {
        "low": {
            "breakfast": [
                {"name": "Egg Bhurji", "qty": "3 eggs", "cal": 250, "p": 18, "c": 3, "f": 18},
                {"name": "Omelette + Bread", "qty": "2 eggs + 2 bread", "cal": 300, "p": 16, "c": 30, "f": 14},
            ],
            "lunch": [
                {"name": "Egg Curry + Rice", "qty": "3 eggs", "cal": 420, "p": 20, "c": 55, "f": 15},
                {"name": "Dal Rice + Egg", "qty": "1 plate + 2 eggs", "cal": 480, "p": 22, "c": 65, "f": 14},
            ],
            "dinner": [
                {"name": "Egg Bhurji + Roti", "qty": "3 eggs + 2 roti", "cal": 400, "p": 22, "c": 40, "f": 18},
            ],
            "snacks": [
                {"name": "Boiled Eggs", "qty": "2 eggs", "cal": 140, "p": 12, "c": 1, "f": 10},
            ],
            "protein_sources": [
                {"name": "Eggs", "qty": "4 whole", "cal": 280, "p": 24, "c": 2, "f": 20},
                {"name": "Egg Whites", "qty": "6 whites", "cal": 102, "p": 22, "c": 1, "f": 0},
                {"name": "Paneer", "qty": "100g", "cal": 265, "p": 20, "c": 3, "f": 20},
            ]
        }
    }
}

class DietEngineService:
    """
    Rule-based diet plan generator with AI enhancement layer
    """
    
    @staticmethod
    def generate_diet_plan(
        user_id: str,
        profile: UserProfileData,
        athlete_level: AthleteLevel,
        date_str: str,
        ai_client=None
    ) -> DietPlan:
        """Generate a complete diet plan for the day"""
        
        # Get calorie and macro targets
        calculations = CalorieService.get_full_calculation(profile, athlete_level)
        target_calories = calculations["target_calories"]
        target_protein = calculations["target_protein"]
        target_carbs = calculations["target_carbs"]
        target_fats = calculations["target_fats"]
        water_target = calculations["water_target_liters"]
        
        # Get food database based on preference and budget
        diet_pref = profile.diet_preference or DietPreference.VEGETARIAN
        budget = profile.budget_level or BudgetLevel.LOW
        
        # Map diet preference to database key
        pref_key = diet_pref.value if diet_pref else "vegetarian"
        if pref_key == "vegan":
            pref_key = "vegetarian"  # Use veg database for vegan
        
        budget_key = budget.value if budget else "low"
        
        foods = INDIAN_FOOD_DATABASE.get(pref_key, INDIAN_FOOD_DATABASE["vegetarian"])
        foods = foods.get(budget_key, foods.get("low", {}))
        
        # Generate meals based on meal frequency
        meal_count = profile.meal_frequency or 4
        meals = DietEngineService._generate_meals(
            foods, target_calories, target_protein, meal_count, profile
        )
        
        # Generate AI guidance if client available
        ai_guidance = None
        if ai_client:
            ai_guidance = DietEngineService._get_ai_guidance(
                profile, meals, target_calories, target_protein
            )
        
        # Build notes based on goal
        notes = DietEngineService._generate_notes(profile, target_calories, target_protein)
        
        return DietPlan(
            user_id=user_id,
            date=date_str,
            target_calories=target_calories,
            target_protein=target_protein,
            target_carbs=target_carbs,
            target_fats=target_fats,
            target_water_liters=water_target,
            meals=meals,
            ai_guidance=ai_guidance,
            notes=notes,
            budget_friendly=budget in [BudgetLevel.LOW, BudgetLevel.MEDIUM]
        )
    
    @staticmethod
    def _generate_meals(foods: dict, target_calories: int, target_protein: int, 
                        meal_count: int, profile: UserProfileData) -> list:
        """Generate meal structure based on targets"""
        meals = []
        
        # Calorie distribution by meal count
        if meal_count <= 3:
            distribution = {"breakfast": 0.25, "lunch": 0.40, "dinner": 0.35}
        elif meal_count == 4:
            distribution = {"breakfast": 0.25, "mid_morning": 0.10, "lunch": 0.35, "dinner": 0.30}
        else:
            distribution = {"breakfast": 0.20, "mid_morning": 0.10, "lunch": 0.30, 
                          "evening_snack": 0.15, "dinner": 0.25}
        
        time_suggestions = {
            "breakfast": "7:00 - 8:30 AM",
            "mid_morning": "10:30 - 11:00 AM",
            "lunch": "12:30 - 1:30 PM",
            "evening_snack": "4:00 - 5:00 PM",
            "dinner": "7:30 - 8:30 PM",
            "pre_workout": "1 hour before workout",
            "post_workout": "Within 30 mins after workout"
        }
        
        allergies = set(a.lower() for a in (profile.allergies or []))
        dislikes = set(d.lower() for d in (profile.food_dislikes or []))
        
        for meal_type, calorie_share in distribution.items():
            meal_calories = int(target_calories * calorie_share)
            meal_protein = int(target_protein * calorie_share)
            
            # Get food items for this meal type
            food_key = meal_type if meal_type in foods else "snacks"
            available_foods = foods.get(food_key, foods.get("snacks", []))
            
            # Filter out allergies and dislikes
            filtered_foods = [
                f for f in available_foods 
                if not any(a in f["name"].lower() for a in allergies)
                and not any(d in f["name"].lower() for d in dislikes)
            ]
            
            if not filtered_foods:
                filtered_foods = available_foods[:2] if available_foods else []
            
            # Select items to meet calorie target
            selected_items = []
            current_calories = 0
            current_protein = 0
            
            for food in filtered_foods[:2]:  # Max 2 items per meal
                item = FoodItem(
                    name=food["name"],
                    quantity=food["qty"],
                    calories=food["cal"],
                    protein=food["p"],
                    carbs=food["c"],
                    fats=food["f"],
                    substitutes=DietEngineService._get_substitutes(food["name"], filtered_foods)
                )
                selected_items.append(item)
                current_calories += food["cal"]
                current_protein += food["p"]
            
            # Add protein source if needed
            if current_protein < meal_protein * 0.8 and "protein_sources" in foods:
                protein_sources = foods["protein_sources"]
                if protein_sources:
                    ps = protein_sources[0]
                    selected_items.append(FoodItem(
                        name=ps["name"],
                        quantity=ps["qty"],
                        calories=ps["cal"],
                        protein=ps["p"],
                        carbs=ps["c"],
                        fats=ps["f"],
                        notes="Additional protein source"
                    ))
                    current_calories += ps["cal"]
                    current_protein += ps["p"]
            
            meal_type_enum = getattr(MealType, meal_type.upper(), MealType.LUNCH)
            
            meals.append(Meal(
                meal_type=meal_type_enum,
                time_suggestion=time_suggestions.get(meal_type, "Flexible"),
                items=selected_items,
                total_calories=current_calories,
                total_protein=current_protein,
                total_carbs=sum(i.carbs for i in selected_items),
                total_fats=sum(i.fats for i in selected_items)
            ))
        
        return meals
    
    @staticmethod
    def _get_substitutes(food_name: str, available_foods: list) -> list:
        """Get substitute options for a food item"""
        return [f["name"] for f in available_foods if f["name"] != food_name][:3]
    
    @staticmethod
    def _generate_notes(profile: UserProfileData, calories: int, protein: int) -> str:
        """Generate personalized notes based on goal"""
        goal = profile.goal or Goal.GENERAL_FITNESS
        
        notes_map = {
            Goal.FAT_LOSS: f"Stay in a {calories} cal deficit. Focus on protein ({protein}g) to preserve muscle. Keep carbs moderate, especially later in the day.",
            Goal.MUSCLE_GAIN: f"Eat {calories} cals with emphasis on post-workout nutrition. Hit {protein}g protein spread across meals.",
            Goal.STRENGTH: f"Prioritize protein ({protein}g) and complex carbs pre-workout. Stay hydrated.",
            Goal.MAINTENANCE: f"Maintain {calories} cals consistently. Balance macros across meals.",
            Goal.ENDURANCE: f"Focus on carbs for energy. {protein}g protein for recovery. Stay well hydrated.",
            Goal.GENERAL_FITNESS: f"Balanced nutrition with {calories} cals. Focus on whole foods and hydration."
        }
        
        return notes_map.get(goal, notes_map[Goal.GENERAL_FITNESS])
    
    @staticmethod
    def _get_ai_guidance(profile, meals, calories, protein) -> Optional[str]:
        """Generate AI-powered personalized guidance (placeholder for now)"""
        # This will be enhanced with actual AI integration
        return None
