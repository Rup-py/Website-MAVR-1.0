from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, timezone
from enum import Enum

class NotificationType(str, Enum):
    WELCOME = "welcome"
    PLAN_READY = "plan_ready"
    DASHBOARD_REMINDER = "dashboard_reminder"
    STREAK_RISK = "streak_risk"
    WEEKLY_REPORT = "weekly_report"
    ACHIEVEMENT = "achievement"
    EVENT_REMINDER = "event_reminder"
    ORDER_UPDATE = "order_update"

class NotificationChannel(str, Enum):
    EMAIL = "email"
    WHATSAPP = "whatsapp"
    IN_APP = "in_app"

class NotificationPreference(BaseModel):
    user_id: str
    email_enabled: bool = True
    whatsapp_enabled: bool = False
    whatsapp_number: Optional[str] = None
    notification_types: List[NotificationType] = [
        NotificationType.WELCOME,
        NotificationType.PLAN_READY,
        NotificationType.WEEKLY_REPORT,
        NotificationType.STREAK_RISK
    ]
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class NotificationJob(BaseModel):
    user_id: str
    notification_type: NotificationType
    channel: NotificationChannel
    subject: Optional[str] = None
    content: str
    scheduled_at: datetime
    sent_at: Optional[datetime] = None
    status: str = "pending"  # pending, sent, failed
    error_message: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class NotificationTemplate(BaseModel):
    notification_type: NotificationType
    channel: NotificationChannel
    subject_template: Optional[str] = None
    body_template: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
