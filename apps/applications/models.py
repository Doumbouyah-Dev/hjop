from django.conf import settings
from django.db import models

from apps.opportunities.models import Opportunity


class Application(models.Model):

    class Status(models.TextChoices):
        APPLIED = "applied", "Applied"
        VIEWED = "viewed", "Viewed"
        SHORTLISTED = "shortlisted", "Shortlisted"
        INTERVIEW = "interview", "Interview"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"
        WITHDRAWN = "withdrawn", "Withdrawn"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications"
    )
    opportunity = models.ForeignKey(
        Opportunity, on_delete=models.CASCADE, related_name="applications"
    )

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.APPLIED)
    cover_letter = models.TextField()
    resume = models.FileField(upload_to="application_resumes/", blank=True, null=True)
    portfolio_url = models.URLField(blank=True)
    answers = models.JSONField(blank=True, default=dict)
    notes = models.TextField(blank=True)

    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "applications"
        ordering = ["-applied_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "opportunity"], name="unique_application_per_user"
            )
        ]
        indexes = [
            models.Index(fields=["user", "status"]),
        ]

    def __str__(self):
        return f"{self.user} → {self.opportunity}"