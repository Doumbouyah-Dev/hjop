from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone

from apps.accounts.services import notify
from apps.bookmarks.models import Bookmark
from apps.opportunities.models import Opportunity


class Command(BaseCommand):
    help = (
        "Sends deadline-reminder notifications to users who bookmarked "
        "opportunities expiring within the next 3 days. Intended to be run "
        "once daily via Windows Task Scheduler or a cron equivalent."
    )

    def handle(self, *args, **options):
        today = timezone.now().date()
        soon = today + timedelta(days=3)

        expiring_soon = Opportunity.objects.filter(
            status="active", deadline__gte=today, deadline__lte=soon
        )

        sent_count = 0
        for opportunity in expiring_soon:
            bookmarking_users = Bookmark.objects.filter(
                opportunity=opportunity
            ).select_related("user")

            for bookmark in bookmarking_users:
                # Avoid spamming — only send one reminder per opportunity per user,
                # checked by looking for an existing unread reminder about this link
                already_notified = bookmark.user.notifications.filter(
                    notification_type="deadline_reminder",
                    link=f"/opportunities/{opportunity.slug}/",
                ).exists()
                if already_notified:
                    continue

                days_left = (opportunity.deadline - today).days
                notify(
                    user=bookmark.user,
                    notification_type="deadline_reminder",
                    title=f"Deadline approaching: {opportunity.title}",
                    message=f"This opportunity closes in {days_left} day{'s' if days_left != 1 else ''}.",
                    link=f"/opportunities/{opportunity.slug}/",
                )
                sent_count += 1

        self.stdout.write(self.style.SUCCESS(f"Sent {sent_count} deadline reminder(s)."))