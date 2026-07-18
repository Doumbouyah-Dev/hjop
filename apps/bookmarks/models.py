from django.conf import settings
from django.db import models

from apps.opportunities.models import Opportunity


class Bookmark(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookmarks"
    )
    opportunity = models.ForeignKey(
        Opportunity, on_delete=models.CASCADE, related_name="bookmarked_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "bookmarks"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "opportunity"], name="unique_bookmark_per_user"
            )
        ]

    def __str__(self):
        return f"{self.user} saved {self.opportunity}"