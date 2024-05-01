from celery import Celery

from app.services import send_email, send_sms
from app.settings import CELERY_BROKER, CELERY_BACKEND

# Initialize Celery instance
celery = Celery(
    __name__,
    broker=CELERY_BROKER,
    backend=CELERY_BACKEND
)


@celery.task
def send_notification(user_id: str, message: str, notification_type: str, notification_time: str, **kwargs):
    """
    Celery task to send notifications based on user preferences.
    """
    try:
        print(f"Sending notification at {notification_time}")
        user_preferences = kwargs.get("user_preferences")
        print("user_preferences", user_preferences)

        if not user_preferences:
            print("User preferences not found")

        if notification_type == "email" and user_preferences.get("email_enabled"):
            # Replace this with actual email sending logic
            print(f"Sending email to {user_id}: {message}")
            send_email(user_preferences.get("email"), message)

        elif notification_type == "sms" and user_preferences.get("sms_enabled"):
            # Replace this with actual SMS sending logic
            print(f"Sending SMS to {user_id}: {message}")
            send_sms(user_preferences.get("phone"), message)
        else:
            print(f"No {notification_type} preference set for user {user_id}")
    except Exception as ex:
        print(f"Failed to send notification for user {user_id}: ", ex)
