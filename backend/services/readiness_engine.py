"""
Readiness Engine Service
Rule-based readiness scoring and recommendations
"""
from datetime import datetime, timezone
from typing import Optional
from models.tracking import ReadinessScore, ReadinessLevel, MorningCheckin, DailyCheckin

class ReadinessEngineService:
    """
    Rule-based readiness score calculation
    Uses sleep, soreness, mood, energy, and recent workout data
    """
    
    # Weight factors for readiness calculation
    WEIGHTS = {
        "sleep_hours": 0.20,
        "sleep_quality": 0.15,
        "soreness": 0.20,
        "mood": 0.15,
        "energy": 0.30
    }
    
    # Optimal ranges
    OPTIMAL_SLEEP_HOURS = 7.5
    
    @staticmethod
    def calculate_readiness(
        user_id: str,
        date_str: str,
        morning_checkin: MorningCheckin,
        last_workout_intensity: Optional[int] = None
    ) -> ReadinessScore:
        """Calculate readiness score from morning check-in data"""
        
        factors = {}
        
        # Sleep hours score (0-10 scale)
        sleep_hours = morning_checkin.sleep_hours or 7
        sleep_score = min(10, (sleep_hours / ReadinessEngineService.OPTIMAL_SLEEP_HOURS) * 10)
        factors["sleep_hours"] = round(sleep_score)
        
        # Sleep quality (already 1-10)
        factors["sleep_quality"] = morning_checkin.sleep_quality or 5
        
        # Soreness (inverse - lower is better)
        soreness = morning_checkin.soreness_level or 3
        factors["soreness"] = 10 - soreness  # Invert so low soreness = high score
        
        # Mood (already 1-10)
        factors["mood"] = morning_checkin.mood or 5
        
        # Energy (already 1-10)
        factors["energy"] = morning_checkin.energy or 5
        
        # Calculate weighted score
        weighted_score = sum(
            factors[key] * ReadinessEngineService.WEIGHTS[key]
            for key in factors
        )
        
        # Apply workout recovery modifier
        if last_workout_intensity:
            recovery_penalty = max(0, (last_workout_intensity - 5) * 0.5)
            weighted_score -= recovery_penalty
        
        # Convert to 0-100 scale
        final_score = int(min(100, max(0, weighted_score * 10)))
        
        # Determine level and recommendation
        level, recommendation = ReadinessEngineService._get_recommendation(final_score, factors)
        
        return ReadinessScore(
            user_id=user_id,
            date=date_str,
            score=final_score,
            level=level,
            factors=factors,
            recommendation=recommendation
        )
    
    @staticmethod
    def _get_recommendation(score: int, factors: dict) -> tuple:
        """Get readiness level and recommendation based on score"""
        
        if score >= 75:
            level = ReadinessLevel.PUSH
            recommendation = "Your body is primed. Push hard today - this is an optimal training day."
        elif score >= 50:
            level = ReadinessLevel.MAINTAIN
            recommendation = "Moderate readiness. Maintain your regular intensity. Focus on consistency."
        else:
            level = ReadinessLevel.RECOVER
            # Identify the weakest factor
            weakest = min(factors, key=factors.get)
            weak_recommendations = {
                "sleep_hours": "Prioritize sleep tonight. Consider a lighter workout or active recovery.",
                "sleep_quality": "Sleep quality is affecting your readiness. Consider a deload session.",
                "soreness": "High soreness detected. Focus on mobility work and proper recovery.",
                "mood": "Mental recovery matters. Keep the session short and enjoyable.",
                "energy": "Low energy levels. Consider rest or very light activity today."
            }
            recommendation = weak_recommendations.get(weakest, "Listen to your body. Recovery is part of progress.")
            level = ReadinessLevel.RECOVER
        
        return level, recommendation
    
    @staticmethod
    def get_weekly_average(readiness_scores: list) -> dict:
        """Calculate weekly readiness statistics"""
        if not readiness_scores:
            return {"average": 0, "trend": "neutral", "best_day": None, "worst_day": None}
        
        scores = [r.score for r in readiness_scores]
        avg = sum(scores) / len(scores)
        
        # Calculate trend
        if len(scores) >= 3:
            first_half = scores[:len(scores)//2]
            second_half = scores[len(scores)//2:]
            trend = "improving" if sum(second_half)/len(second_half) > sum(first_half)/len(first_half) else "declining"
        else:
            trend = "neutral"
        
        best_day = readiness_scores[scores.index(max(scores))].date if scores else None
        worst_day = readiness_scores[scores.index(min(scores))].date if scores else None
        
        return {
            "average": round(avg),
            "trend": trend,
            "best_day": best_day,
            "worst_day": worst_day,
            "days_tracked": len(scores)
        }
