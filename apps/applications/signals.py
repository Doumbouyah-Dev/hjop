from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.accounts.services import notify
from .models import Application


STATUS_MESSAGES = {
    Application.Status.SHORTLISTED: "Your application has been shortlisted!",
    Application.Status.INTERVIEW: "You've been invited to an interview.",
    Application.Status.ACCEPTED: "Congratulations! Your application was accepted.",
    Application.Status.REJECTED: "Your application status has been updated.",
}


@receiver(pre_save, sender=Application)
def notify_on_status_change(sender, instance, **kwargs):
    if not instance.pk:
        return  # new application, not a status change — no notification needed yet

    try:
        previous = Application.objects.get(pk=instance.pk)
    except Application.DoesNotExist:
        return

    if previous.status == instance.status:
        return  # nothing changed

    message = STATUS_MESSAGES.get(instance.status)
    if not message:
        return  # e.g., transition to "applied"/"viewed"/"withdrawn" — no notification needed

    notify(
        user=instance.applicant,
        notification_type="application_update",
        title=f"Update on {instance.opportunity.title}",
        message=message,
        link=f"/opportunities/{instance.opportunity.slug}/",
    )