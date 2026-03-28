"""
Notification Service Abstraction
Ready for Resend (email) and WhatsApp integration
"""
from typing import Optional, List
from datetime import datetime, timezone
from models.notification import (
    NotificationType, NotificationChannel, NotificationJob, NotificationPreference
)

class EmailService:
    """
    Email service abstraction (Resend-ready)
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.enabled = bool(api_key)
    
    async def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        from_email: str = "noreply@mavr.fitness"
    ) -> dict:
        """
        Send email via Resend
        Currently returns mock response - integrate Resend when ready
        """
        if not self.enabled:
            return {
                "status": "mocked",
                "message": "Email service not configured. Add RESEND_API_KEY to enable.",
                "to": to_email,
                "subject": subject
            }
        
        # TODO: Integrate with Resend API
        # from resend import Resend
        # resend = Resend(self.api_key)
        # response = resend.emails.send({
        #     "from": from_email,
        #     "to": to_email,
        #     "subject": subject,
        #     "html": body
        # })
        
        return {
            "status": "mocked",
            "message": "Resend integration placeholder",
            "to": to_email
        }

class WhatsAppService:
    """
    WhatsApp service abstraction (Meta Cloud API-ready)
    """
    
    def __init__(self, access_token: Optional[str] = None, phone_number_id: Optional[str] = None):
        self.access_token = access_token
        self.phone_number_id = phone_number_id
        self.enabled = bool(access_token and phone_number_id)
    
    async def send_message(
        self,
        to_number: str,
        message: str,
        template_name: Optional[str] = None
    ) -> dict:
        """
        Send WhatsApp message via Meta Cloud API
        Currently returns mock response - integrate when ready
        """
        if not self.enabled:
            return {
                "status": "mocked",
                "message": "WhatsApp service not configured. Add META_WHATSAPP_TOKEN to enable.",
                "to": to_number
            }
        
        # TODO: Integrate with Meta WhatsApp Cloud API
        # import httpx
        # async with httpx.AsyncClient() as client:
        #     response = await client.post(
        #         f"https://graph.facebook.com/v17.0/{self.phone_number_id}/messages",
        #         headers={"Authorization": f"Bearer {self.access_token}"},
        #         json={
        #             "messaging_product": "whatsapp",
        #             "to": to_number,
        #             "type": "text",
        #             "text": {"body": message}
        #         }
        #     )
        
        return {
            "status": "mocked",
            "message": "WhatsApp integration placeholder",
            "to": to_number
        }

class NotificationService:
    """
    Unified notification service
    Handles email, WhatsApp, and in-app notifications
    """
    
    # Notification templates
    TEMPLATES = {
        NotificationType.WELCOME: {
            "subject": "Welcome to MAVR - Your Athlete OS is Ready",
            "body": """Your system is ready. Your personalized plans are waiting in your dashboard.
            
Stay locked in. Build with intent.

- Team MAVR"""
        },
        NotificationType.PLAN_READY: {
            "subject": "Your Daily Plan is Ready",
            "body": "Today's workout and diet plan are live in your dashboard. One day at a time."
        },
        NotificationType.DASHBOARD_REMINDER: {
            "subject": "Check In Pending",
            "body": "Your daily check-in is waiting. Don't break the chain."
        },
        NotificationType.STREAK_RISK: {
            "subject": "Streak at Risk",
            "body": "Your {streak} day streak is at risk. One check-in keeps it alive."
        },
        NotificationType.WEEKLY_REPORT: {
            "subject": "Your Weekly Report is Ready",
            "body": "Your weekly performance report is ready in your dashboard. See how you're progressing."
        },
        NotificationType.ACHIEVEMENT: {
            "subject": "Achievement Unlocked",
            "body": "You've hit a milestone: {achievement}. Progress is earned."
        },
        NotificationType.EVENT_REMINDER: {
            "subject": "Event Countdown: {days} Days Left",
            "body": "Your event is {days} days away. Stay focused. Stay locked in."
        },
        NotificationType.ORDER_UPDATE: {
            "subject": "Order Update: {status}",
            "body": "Your MAVR order #{order_id} has been {status}."
        }
    }
    
    def __init__(self, email_service: EmailService, whatsapp_service: WhatsAppService, db=None):
        self.email = email_service
        self.whatsapp = whatsapp_service
        self.db = db
    
    async def send_notification(
        self,
        user_id: str,
        notification_type: NotificationType,
        channel: NotificationChannel,
        context: Optional[dict] = None
    ) -> dict:
        """Send a notification through the specified channel"""
        
        template = self.TEMPLATES.get(notification_type, {})
        subject = template.get("subject", "MAVR Notification")
        body = template.get("body", "Check your MAVR dashboard.")
        
        # Apply context variables
        if context:
            subject = subject.format(**context)
            body = body.format(**context)
        
        result = {"status": "pending", "channel": channel.value}
        
        if channel == NotificationChannel.EMAIL:
            # Get user email from DB
            user_email = context.get("email", "")
            if user_email:
                result = await self.email.send_email(user_email, subject, body)
        
        elif channel == NotificationChannel.WHATSAPP:
            phone = context.get("phone", "")
            if phone:
                result = await self.whatsapp.send_message(phone, body)
        
        elif channel == NotificationChannel.IN_APP:
            # Store in-app notification in database
            if self.db:
                job = NotificationJob(
                    user_id=user_id,
                    notification_type=notification_type,
                    channel=channel,
                    subject=subject,
                    content=body,
                    scheduled_at=datetime.now(timezone.utc),
                    status="delivered"
                )
                await self.db.notification_jobs.insert_one(job.model_dump())
                result = {"status": "delivered", "channel": "in_app"}
        
        return result
    
    async def send_welcome(self, user_id: str, email: str) -> dict:
        """Send welcome notification"""
        return await self.send_notification(
            user_id,
            NotificationType.WELCOME,
            NotificationChannel.EMAIL,
            {"email": email}
        )
    
    async def send_streak_risk(self, user_id: str, email: str, streak: int) -> dict:
        """Send streak risk alert"""
        return await self.send_notification(
            user_id,
            NotificationType.STREAK_RISK,
            NotificationChannel.EMAIL,
            {"email": email, "streak": str(streak)}
        )
