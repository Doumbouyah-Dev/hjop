from .models import Notification


def notify(user, notification_type, title, message="", link=""):
    """
    Central entry point for creating notifications — every app that
    needs to notify a user should call this rather than creating
    Notification rows directly, so delivery logic (email, push, etc.)
    can be added here later in one place.
    """
    return Notification.objects.create(
        user=user,
        notification_type=notification_type,
        title=title,
        message=message,
        link=link,
    )