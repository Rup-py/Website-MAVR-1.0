"""
Streak Engine Service
Tracks and manages user streaks
"""
from datetime import datetime, timezone, timedelta
from typing import Optional
from models.tracking import StreakRecord

class StreakEngineService:
    """
    Streak tracking and management
    """
    
    @staticmethod
    def update_streak(
        current_record: Optional[StreakRecord],
        user_id: str,
        checkin_date: str,
        streak_type: str = "daily_checkin"
    ) -> StreakRecord:
        """Update streak based on check-in"""
        
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        
        if not current_record:
            # First check-in ever
            return StreakRecord(
                user_id=user_id,
                current_streak=1,
                longest_streak=1,
                last_checkin_date=checkin_date,
                streak_type=streak_type
            )
        
        last_date = current_record.last_checkin_date
        
        if not last_date:
            # No previous check-in
            return StreakRecord(
                user_id=user_id,
                current_streak=1,
                longest_streak=max(1, current_record.longest_streak),
                last_checkin_date=checkin_date,
                streak_type=streak_type
            )
        
        # Parse dates
        try:
            last = datetime.strptime(last_date, "%Y-%m-%d")
            current = datetime.strptime(checkin_date, "%Y-%m-%d")
        except ValueError:
            return current_record
        
        days_diff = (current - last).days
        
        if days_diff == 0:
            # Same day check-in, no change
            return current_record
        elif days_diff == 1:
            # Consecutive day - extend streak
            new_streak = current_record.current_streak + 1
            return StreakRecord(
                user_id=user_id,
                current_streak=new_streak,
                longest_streak=max(new_streak, current_record.longest_streak),
                last_checkin_date=checkin_date,
                streak_type=streak_type
            )
        else:
            # Streak broken
            return StreakRecord(
                user_id=user_id,
                current_streak=1,
                longest_streak=current_record.longest_streak,
                last_checkin_date=checkin_date,
                streak_type=streak_type
            )
    
    @staticmethod
    def check_streak_at_risk(record: StreakRecord) -> bool:
        """Check if streak is at risk (no check-in today)"""
        if not record.last_checkin_date:
            return True
        
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        
        try:
            last = datetime.strptime(record.last_checkin_date, "%Y-%m-%d")
            current = datetime.strptime(today, "%Y-%m-%d")
            days_diff = (current - last).days
            return days_diff >= 1  # At risk if last check-in was yesterday or earlier
        except ValueError:
            return True
    
    @staticmethod
    def get_streak_milestone(streak: int) -> Optional[str]:
        """Get milestone message for streak achievements"""
        milestones = {
            7: "One week strong! Your discipline is showing.",
            14: "Two weeks locked in. Building real habits.",
            21: "21 days - habits are forming. Keep pushing.",
            30: "30 days! You're a different athlete now.",
            60: "60 days of consistency. Elite mindset.",
            90: "90 days. You've transformed. Respect.",
            100: "Century mark! Legendary consistency.",
            180: "6 months. You're built different.",
            365: "365 days. A full year of dedication. Champion."
        }
        return milestones.get(streak)
    
    @staticmethod
    def get_streak_message(record: StreakRecord) -> str:
        """Get motivational message based on streak status"""
        streak = record.current_streak
        
        if streak == 0:
            return "Start your streak today. One check-in at a time."
        elif streak < 3:
            return f"{streak} day streak. Keep it going - momentum is building."
        elif streak < 7:
            return f"{streak} days strong. One week is within reach."
        elif streak < 14:
            return f"{streak} days! You're proving something to yourself."
        elif streak < 30:
            return f"{streak} days. Habits are forming. Don't break the chain."
        elif streak < 60:
            return f"{streak} days. You're in the elite zone now."
        else:
            return f"{streak} days. Legendary. You're not the same person who started."
