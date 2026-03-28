"""
AI Service
Hybrid AI integration for personalized guidance
Uses rule-based outputs as source of truth, AI for personalization
"""
import os
import json
from typing import Optional
from emergentintegrations.llm.chat import LlmChat, UserMessage

class AIService:
    """
    AI-powered personalization layer
    Enhances rule-based outputs with personalized guidance
    """
    
    def __init__(self):
        self.api_key = os.environ.get("EMERGENT_LLM_KEY")
        self.enabled = bool(self.api_key)
    
    async def get_diet_guidance(
        self,
        user_profile: dict,
        diet_plan: dict,
        date: str
    ) -> Optional[str]:
        """Generate personalized diet guidance"""
        if not self.enabled:
            return None
        
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"diet-{user_profile.get('user_id', 'unknown')}-{date}",
                system_message="""You are MAVR's nutrition coach. Provide brief, sharp, actionable diet guidance.
                Keep responses under 100 words. Be direct, premium, performance-focused.
                Tone: Sharp, motivational without being childish. Example: "Today decides the week."
                Focus on practical Indian diet adherence tips."""
            ).with_model("openai", "gpt-5.2")
            
            prompt = f"""Based on this athlete's profile and today's plan, give one sharp insight.

Profile:
- Goal: {user_profile.get('goal', 'general fitness')}
- Budget: {user_profile.get('budget_level', 'medium')}
- Preference: {user_profile.get('diet_preference', 'vegetarian')}

Today's targets:
- Calories: {diet_plan.get('target_calories', 2000)}
- Protein: {diet_plan.get('target_protein', 120)}g

Give ONE actionable tip for today's nutrition success."""
            
            response = await chat.send_message(UserMessage(text=prompt))
            return response.strip() if response else None
            
        except Exception as e:
            print(f"AI diet guidance error: {e}")
            return None
    
    async def get_workout_guidance(
        self,
        user_profile: dict,
        workout_plan: dict,
        date: str
    ) -> Optional[str]:
        """Generate personalized workout guidance"""
        if not self.enabled:
            return None
        
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"workout-{user_profile.get('user_id', 'unknown')}-{date}",
                system_message="""You are MAVR's performance coach. Provide brief, sharp, actionable workout guidance.
                Keep responses under 80 words. Be direct, premium, elite mindset.
                Tone: Coach-like, no fluff. Example: "Build with intent."
                Focus on execution tips and intensity management."""
            ).with_model("openai", "gpt-5.2")
            
            session = workout_plan.get('session', {})
            exercises = session.get('main_workout', [])[:3]
            exercise_names = [e.get('name', '') for e in exercises]
            
            prompt = f"""Based on today's workout, give one execution tip.

Athlete Level: {user_profile.get('athlete_level', 'intermediate')}
Session: {session.get('name', 'Training Day')}
Key exercises: {', '.join(exercise_names)}
Duration: {session.get('estimated_duration_mins', 45)} mins
Intensity: {session.get('intensity_level', 'medium')}

ONE sharp tip for today's session."""
            
            response = await chat.send_message(UserMessage(text=prompt))
            return response.strip() if response else None
            
        except Exception as e:
            print(f"AI workout guidance error: {e}")
            return None
    
    async def get_weekly_insights(
        self,
        user_profile: dict,
        weekly_data: dict
    ) -> Optional[str]:
        """Generate weekly report insights"""
        if not self.enabled:
            return None
        
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"weekly-{user_profile.get('user_id', 'unknown')}",
                system_message="""You are MAVR's performance analyst. Analyze weekly data and provide sharp insights.
                Keep responses under 120 words. Be data-driven, direct, actionable.
                Highlight what's working and one key area to improve.
                Tone: Professional coach reviewing athlete performance."""
            ).with_model("openai", "gpt-5.2")
            
            prompt = f"""Analyze this week's performance:

Workouts completed: {weekly_data.get('workouts_completed', 0)}/{weekly_data.get('workouts_target', 4)}
Adherence score: {weekly_data.get('adherence_score', 0)}%
Average readiness: {weekly_data.get('average_readiness', 50)}
Strongest habit: {weekly_data.get('strongest_habit', 'tracking')}
Weakest habit: {weekly_data.get('weakest_habit', 'consistency')}

Give 2-3 sharp insights and ONE focus for next week."""
            
            response = await chat.send_message(UserMessage(text=prompt))
            return response.strip() if response else None
            
        except Exception as e:
            print(f"AI weekly insights error: {e}")
            return None
    
    async def get_readiness_insight(
        self,
        readiness_data: dict
    ) -> Optional[str]:
        """Generate readiness-based guidance"""
        if not self.enabled:
            return None
        
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"readiness-{readiness_data.get('user_id', 'unknown')}",
                system_message="""You are MAVR's recovery specialist. Analyze readiness and give guidance.
                Keep responses under 50 words. Be direct, supportive, action-oriented.
                Tone: Elite sports psychologist meets performance coach."""
            ).with_model("openai", "gpt-5.2")
            
            prompt = f"""Readiness check:
Score: {readiness_data.get('score', 50)}/100
Level: {readiness_data.get('level', 'maintain')}
Sleep: {readiness_data.get('factors', {}).get('sleep_hours', 7)} hrs
Energy: {readiness_data.get('factors', {}).get('energy', 5)}/10
Soreness: {readiness_data.get('factors', {}).get('soreness', 5)}/10

ONE sentence on how to approach today."""
            
            response = await chat.send_message(UserMessage(text=prompt))
            return response.strip() if response else None
            
        except Exception as e:
            print(f"AI readiness insight error: {e}")
            return None

# Singleton instance
ai_service = AIService()
