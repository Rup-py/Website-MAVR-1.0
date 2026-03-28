"""
Workout Engine Service
Rule-based workout plan generation with AI enhancement
"""
from datetime import datetime, timezone
from typing import Optional, List
from models.user import UserProfileData, AthleteLevel, Goal, WorkoutSetup
from models.workout import (
    WorkoutPlan, WorkoutSession, Exercise, MuscleGroup, ExerciseType
)

# Exercise database
EXERCISE_DATABASE = {
    "gym": {
        MuscleGroup.CHEST: [
            {"name": "Bench Press", "type": ExerciseType.COMPOUND, "equipment": ["barbell", "bench"]},
            {"name": "Incline Dumbbell Press", "type": ExerciseType.COMPOUND, "equipment": ["dumbbells", "incline bench"]},
            {"name": "Cable Flyes", "type": ExerciseType.ISOLATION, "equipment": ["cable machine"]},
            {"name": "Dips", "type": ExerciseType.COMPOUND, "equipment": ["dip bars"]},
            {"name": "Pec Deck Machine", "type": ExerciseType.ISOLATION, "equipment": ["pec deck"]},
        ],
        MuscleGroup.BACK: [
            {"name": "Deadlift", "type": ExerciseType.COMPOUND, "equipment": ["barbell"]},
            {"name": "Lat Pulldown", "type": ExerciseType.COMPOUND, "equipment": ["lat pulldown machine"]},
            {"name": "Barbell Rows", "type": ExerciseType.COMPOUND, "equipment": ["barbell"]},
            {"name": "Seated Cable Rows", "type": ExerciseType.COMPOUND, "equipment": ["cable machine"]},
            {"name": "Face Pulls", "type": ExerciseType.ISOLATION, "equipment": ["cable machine"]},
        ],
        MuscleGroup.SHOULDERS: [
            {"name": "Overhead Press", "type": ExerciseType.COMPOUND, "equipment": ["barbell"]},
            {"name": "Lateral Raises", "type": ExerciseType.ISOLATION, "equipment": ["dumbbells"]},
            {"name": "Front Raises", "type": ExerciseType.ISOLATION, "equipment": ["dumbbells"]},
            {"name": "Reverse Pec Deck", "type": ExerciseType.ISOLATION, "equipment": ["pec deck"]},
        ],
        MuscleGroup.BICEPS: [
            {"name": "Barbell Curls", "type": ExerciseType.ISOLATION, "equipment": ["barbell"]},
            {"name": "Dumbbell Hammer Curls", "type": ExerciseType.ISOLATION, "equipment": ["dumbbells"]},
            {"name": "Preacher Curls", "type": ExerciseType.ISOLATION, "equipment": ["preacher bench", "ez bar"]},
        ],
        MuscleGroup.TRICEPS: [
            {"name": "Tricep Pushdowns", "type": ExerciseType.ISOLATION, "equipment": ["cable machine"]},
            {"name": "Skull Crushers", "type": ExerciseType.ISOLATION, "equipment": ["ez bar", "bench"]},
            {"name": "Overhead Tricep Extension", "type": ExerciseType.ISOLATION, "equipment": ["dumbbell"]},
        ],
        MuscleGroup.LEGS: [
            {"name": "Squats", "type": ExerciseType.COMPOUND, "equipment": ["barbell", "squat rack"]},
            {"name": "Leg Press", "type": ExerciseType.COMPOUND, "equipment": ["leg press machine"]},
            {"name": "Romanian Deadlift", "type": ExerciseType.COMPOUND, "equipment": ["barbell"]},
            {"name": "Leg Curls", "type": ExerciseType.ISOLATION, "equipment": ["leg curl machine"]},
            {"name": "Leg Extensions", "type": ExerciseType.ISOLATION, "equipment": ["leg extension machine"]},
            {"name": "Calf Raises", "type": ExerciseType.ISOLATION, "equipment": ["smith machine"]},
        ],
        MuscleGroup.CORE: [
            {"name": "Cable Crunches", "type": ExerciseType.ISOLATION, "equipment": ["cable machine"]},
            {"name": "Hanging Leg Raises", "type": ExerciseType.COMPOUND, "equipment": ["pull up bar"]},
            {"name": "Planks", "type": ExerciseType.STRENGTH, "equipment": []},
        ],
    },
    "home": {
        MuscleGroup.CHEST: [
            {"name": "Push-ups", "type": ExerciseType.COMPOUND, "equipment": []},
            {"name": "Diamond Push-ups", "type": ExerciseType.COMPOUND, "equipment": []},
            {"name": "Incline Push-ups", "type": ExerciseType.COMPOUND, "equipment": []},
            {"name": "Decline Push-ups", "type": ExerciseType.COMPOUND, "equipment": []},
        ],
        MuscleGroup.BACK: [
            {"name": "Pull-ups", "type": ExerciseType.COMPOUND, "equipment": ["pull up bar"]},
            {"name": "Inverted Rows", "type": ExerciseType.COMPOUND, "equipment": ["table or bar"]},
            {"name": "Superman Hold", "type": ExerciseType.ISOLATION, "equipment": []},
        ],
        MuscleGroup.SHOULDERS: [
            {"name": "Pike Push-ups", "type": ExerciseType.COMPOUND, "equipment": []},
            {"name": "Lateral Raises", "type": ExerciseType.ISOLATION, "equipment": ["dumbbells", "water bottles"]},
            {"name": "Wall Handstand Hold", "type": ExerciseType.STRENGTH, "equipment": []},
        ],
        MuscleGroup.BICEPS: [
            {"name": "Chin-ups", "type": ExerciseType.COMPOUND, "equipment": ["pull up bar"]},
            {"name": "Resistance Band Curls", "type": ExerciseType.ISOLATION, "equipment": ["resistance band"]},
        ],
        MuscleGroup.TRICEPS: [
            {"name": "Diamond Push-ups", "type": ExerciseType.COMPOUND, "equipment": []},
            {"name": "Bench Dips", "type": ExerciseType.COMPOUND, "equipment": ["chair"]},
        ],
        MuscleGroup.LEGS: [
            {"name": "Bodyweight Squats", "type": ExerciseType.COMPOUND, "equipment": []},
            {"name": "Lunges", "type": ExerciseType.COMPOUND, "equipment": []},
            {"name": "Bulgarian Split Squats", "type": ExerciseType.COMPOUND, "equipment": ["chair"]},
            {"name": "Glute Bridges", "type": ExerciseType.ISOLATION, "equipment": []},
            {"name": "Calf Raises", "type": ExerciseType.ISOLATION, "equipment": []},
        ],
        MuscleGroup.CORE: [
            {"name": "Planks", "type": ExerciseType.STRENGTH, "equipment": []},
            {"name": "Mountain Climbers", "type": ExerciseType.CARDIO, "equipment": []},
            {"name": "Bicycle Crunches", "type": ExerciseType.ISOLATION, "equipment": []},
            {"name": "Leg Raises", "type": ExerciseType.ISOLATION, "equipment": []},
        ],
    }
}

# Training splits by level and frequency
TRAINING_SPLITS = {
    AthleteLevel.BEGINNER: {
        2: ["full_body", "full_body"],
        3: ["full_body", "full_body", "full_body"],
        4: ["upper", "lower", "upper", "lower"],
    },
    AthleteLevel.INTERMEDIATE: {
        3: ["push", "pull", "legs"],
        4: ["upper", "lower", "push", "pull"],
        5: ["push", "pull", "legs", "upper", "lower"],
    },
    AthleteLevel.ADVANCED: {
        4: ["chest_triceps", "back_biceps", "shoulders_arms", "legs"],
        5: ["chest", "back", "shoulders", "arms", "legs"],
        6: ["push", "pull", "legs", "push", "pull", "legs"],
    },
    AthleteLevel.PROFESSIONAL: {
        5: ["chest", "back", "shoulders", "arms", "legs"],
        6: ["push", "pull", "legs", "push", "pull", "legs"],
    }
}

SPLIT_MUSCLE_GROUPS = {
    "full_body": [MuscleGroup.CHEST, MuscleGroup.BACK, MuscleGroup.LEGS, MuscleGroup.CORE],
    "upper": [MuscleGroup.CHEST, MuscleGroup.BACK, MuscleGroup.SHOULDERS, MuscleGroup.BICEPS, MuscleGroup.TRICEPS],
    "lower": [MuscleGroup.LEGS, MuscleGroup.CORE],
    "push": [MuscleGroup.CHEST, MuscleGroup.SHOULDERS, MuscleGroup.TRICEPS],
    "pull": [MuscleGroup.BACK, MuscleGroup.BICEPS, MuscleGroup.CORE],
    "legs": [MuscleGroup.LEGS, MuscleGroup.CORE],
    "chest": [MuscleGroup.CHEST],
    "back": [MuscleGroup.BACK],
    "shoulders": [MuscleGroup.SHOULDERS],
    "arms": [MuscleGroup.BICEPS, MuscleGroup.TRICEPS],
    "chest_triceps": [MuscleGroup.CHEST, MuscleGroup.TRICEPS],
    "back_biceps": [MuscleGroup.BACK, MuscleGroup.BICEPS],
    "shoulders_arms": [MuscleGroup.SHOULDERS, MuscleGroup.BICEPS, MuscleGroup.TRICEPS],
}

class WorkoutEngineService:
    """
    Rule-based workout plan generator with AI enhancement layer
    """
    
    @staticmethod
    def generate_workout_plan(
        user_id: str,
        profile: UserProfileData,
        athlete_level: AthleteLevel,
        date_str: str,
        day_of_week: str,
        ai_client=None
    ) -> Optional[WorkoutPlan]:
        """Generate a workout plan for the day"""
        
        # Check if it's a workout day
        preferred_days = profile.preferred_workout_days or ["monday", "wednesday", "friday"]
        if day_of_week.lower() not in [d.lower() for d in preferred_days]:
            return None  # Rest day
        
        # Get training split
        frequency = profile.workout_frequency or 3
        level_splits = TRAINING_SPLITS.get(athlete_level, TRAINING_SPLITS[AthleteLevel.BEGINNER])
        split_list = level_splits.get(frequency, level_splits.get(3, ["full_body", "full_body", "full_body"]))
        
        # Determine which day of the split
        day_index = preferred_days.index(day_of_week.lower()) if day_of_week.lower() in preferred_days else 0
        split_day = split_list[day_index % len(split_list)]
        
        # Get muscle groups for this split
        muscle_groups = SPLIT_MUSCLE_GROUPS.get(split_day, [MuscleGroup.FULL_BODY])
        
        # Get setup type
        setup = profile.workout_setup or WorkoutSetup.GYM
        setup_key = "gym" if setup == WorkoutSetup.GYM else "home"
        
        # Generate session
        session = WorkoutEngineService._generate_session(
            split_day, muscle_groups, setup_key, athlete_level, profile
        )
        
        # Generate AI guidance if available
        ai_guidance = None
        progression_notes = WorkoutEngineService._generate_progression_notes(athlete_level, profile)
        
        return WorkoutPlan(
            user_id=user_id,
            date=date_str,
            session=session,
            ai_guidance=ai_guidance,
            progression_notes=progression_notes
        )
    
    @staticmethod
    def _generate_session(
        split_name: str,
        muscle_groups: List[MuscleGroup],
        setup: str,
        level: AthleteLevel,
        profile: UserProfileData
    ) -> WorkoutSession:
        """Generate a complete workout session"""
        
        exercises_db = EXERCISE_DATABASE.get(setup, EXERCISE_DATABASE["home"])
        available_equipment = set(e.lower() for e in (profile.available_equipment or []))
        injuries = set(i.lower() for i in (profile.injuries or []))
        weak_points = profile.weak_muscle_groups or []
        
        # Set parameters based on level
        level_params = {
            AthleteLevel.BEGINNER: {"sets": 3, "reps": "10-12", "exercises_per_group": 2, "rest": 90},
            AthleteLevel.INTERMEDIATE: {"sets": 4, "reps": "8-12", "exercises_per_group": 3, "rest": 75},
            AthleteLevel.ADVANCED: {"sets": 4, "reps": "6-10", "exercises_per_group": 4, "rest": 60},
            AthleteLevel.PROFESSIONAL: {"sets": 5, "reps": "5-8", "exercises_per_group": 4, "rest": 60},
        }
        params = level_params.get(level, level_params[AthleteLevel.INTERMEDIATE])
        
        # Warmup
        warmup = [
            Exercise(
                name="Light Cardio (Treadmill/Cycling)",
                muscle_group=MuscleGroup.CARDIO,
                exercise_type=ExerciseType.CARDIO,
                sets=1,
                reps="5 mins",
                rest_seconds=0,
                notes="Gradually increase intensity"
            ),
            Exercise(
                name="Dynamic Stretches",
                muscle_group=MuscleGroup.FULL_BODY,
                exercise_type=ExerciseType.FLEXIBILITY,
                sets=1,
                reps="5 mins",
                rest_seconds=0,
                notes="Arm circles, leg swings, hip rotations"
            )
        ]
        
        # Main workout
        main_workout = []
        for muscle_group in muscle_groups:
            group_exercises = exercises_db.get(muscle_group, [])
            
            # Filter by equipment and injuries
            filtered = []
            for ex in group_exercises:
                # Check equipment availability
                required_equipment = [e.lower() for e in ex.get("equipment", [])]
                has_equipment = not required_equipment or all(e in available_equipment or setup == "home" for e in required_equipment)
                
                # Check for injury-related exclusions
                is_safe = not any(inj in ex["name"].lower() for inj in injuries)
                
                if has_equipment and is_safe:
                    filtered.append(ex)
            
            if not filtered:
                filtered = group_exercises[:2]  # Fallback
            
            # Prioritize weak points
            is_weak_point = muscle_group.value in [w.lower() for w in weak_points]
            exercises_count = params["exercises_per_group"] + (1 if is_weak_point else 0)
            
            for ex in filtered[:exercises_count]:
                # Adjust reps for compound vs isolation
                reps = params["reps"]
                if ex["type"] == ExerciseType.ISOLATION:
                    reps = "12-15" if level in [AthleteLevel.BEGINNER, AthleteLevel.INTERMEDIATE] else "10-12"
                
                exercise = Exercise(
                    name=ex["name"],
                    muscle_group=muscle_group,
                    exercise_type=ex["type"],
                    sets=params["sets"],
                    reps=reps,
                    rest_seconds=params["rest"],
                    equipment_needed=ex.get("equipment", []),
                    substitutes=WorkoutEngineService._get_substitutes(ex["name"], filtered)
                )
                main_workout.append(exercise)
        
        # Cooldown
        cooldown = [
            Exercise(
                name="Static Stretching",
                muscle_group=MuscleGroup.FULL_BODY,
                exercise_type=ExerciseType.FLEXIBILITY,
                sets=1,
                reps="5-10 mins",
                rest_seconds=0,
                notes="Hold each stretch for 20-30 seconds"
            )
        ]
        
        # Calculate duration
        main_duration = len(main_workout) * (params["sets"] * 1.5 + params["rest"] / 60)
        total_duration = int(10 + main_duration + 10)  # warmup + main + cooldown
        
        # Determine intensity
        intensity = "medium"
        if level in [AthleteLevel.ADVANCED, AthleteLevel.PROFESSIONAL]:
            intensity = "high"
        elif level == AthleteLevel.BEGINNER:
            intensity = "low"
        
        return WorkoutSession(
            name=f"{split_name.replace('_', ' ').title()} Day",
            day_of_week=profile.preferred_workout_days[0] if profile.preferred_workout_days else "Monday",
            focus_areas=muscle_groups,
            warmup=warmup,
            main_workout=main_workout,
            cooldown=cooldown,
            estimated_duration_mins=total_duration,
            intensity_level=intensity
        )
    
    @staticmethod
    def _get_substitutes(exercise_name: str, exercises: list) -> List[str]:
        """Get substitute exercises"""
        return [e["name"] for e in exercises if e["name"] != exercise_name][:2]
    
    @staticmethod
    def _generate_progression_notes(level: AthleteLevel, profile: UserProfileData) -> str:
        """Generate progression notes based on level"""
        notes = {
            AthleteLevel.BEGINNER: "Focus on form and technique. Increase weight only when you can complete all reps with good form.",
            AthleteLevel.INTERMEDIATE: "Progressive overload is key. Aim to add weight or reps each week. Track your lifts.",
            AthleteLevel.ADVANCED: "Focus on intensity techniques. Consider adding drop sets or supersets for lagging body parts.",
            AthleteLevel.PROFESSIONAL: "Periodization is essential. Deload every 4-6 weeks. Listen to your body."
        }
        return notes.get(level, notes[AthleteLevel.INTERMEDIATE])
