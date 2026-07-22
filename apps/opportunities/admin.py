from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone

from .models import Opportunity


class DeadlineStatusFilter(admin.SimpleListFilter):
    """Custom filter: quickly find expiring-soon or already-expired listings."""
    title = "deadline status"
    parameter_name = "deadline_status"

    def lookups(self, request, model_admin):
        return [
            ("expired", "Expired"),
            ("this_week", "Expiring this week"),
            ("active", "Still open"),
        ]

    def queryset(self, request, queryset):
        today = timezone.now().date()
        if self.value() == "expired":
            return queryset.filter(deadline__lt=today)
        if self.value() == "this_week":
            return queryset.filter(deadline__gte=today, deadline__lte=today + timezone.timedelta(days=7))
        if self.value() == "active":
            return queryset.filter(deadline__gte=today)
        return queryset


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = [
        "title", "organization", "category", "status_badge",
        "country", "deadline", "featured", "urgent", "views",
        "application_count", "bookmark_count",
    ]
    list_filter = [
        "status", "category", "opportunity_type", "experience_level",
        "featured", "urgent", "verified", "remote", DeadlineStatusFilter,
    ]
    search_fields = ["title", "description", "country", "organization__name"]
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ["organization", "posted_by"]
    readonly_fields = ["views", "bookmark_count", "application_count", "created_at", "updated_at"]
    date_hierarchy = "created_at"
    list_per_page = 25
    actions = [
        "feature_opportunities", "unfeature_opportunities",
        "mark_urgent", "activate_opportunities", "close_opportunities",
    ]

    fieldsets = (
        ("Basic Info", {
            "fields": ("title", "slug", "organization", "posted_by", "category", "subcategory", "opportunity_type")
        }),
        ("Description", {
            "fields": ("short_description", "description", "requirements", "benefits")
        }),
        ("Requirements", {
            "fields": ("experience_level", "education_level")
        }),
        ("Location", {
            "fields": ("location", "country", "county", "remote")
        }),
        ("Compensation", {
            "fields": (
                "salary_min", "salary_max", "salary_currency",
                "salary_period", "funding_amount",
            )
        }),
        ("Timing", {"fields": ("duration", "start_date", "deadline")}),
        ("Application", {
            "fields": (
                "application_link", "application_email",
                "application_instructions", "max_users",
            )
        }),
        ("Tags & SEO", {"fields": ("tags", "seo_title", "seo_description")}),
        ("Status & Visibility", {
            "fields": ("status", "featured", "urgent", "sponsored", "verified")
        }),
        ("Stats (read-only)", {
            "fields": ("views", "bookmark_count", "application_count")
        }),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    @admin.display(description="Status")
    def status_badge(self, obj):
        colors = {
            "draft": "#6b7280", "active": "#16a34a", "paused": "#d97706",
            "expired": "#dc2626", "closed": "#4b5563",
        }
        return format_html(
            '<span style="color:white;background:{};padding:2px 8px;'
            'border-radius:9999px;font-size:11px;font-weight:600;">{}</span>',
            colors.get(obj.status, "#6b7280"), obj.get_status_display()
        )

    @admin.action(description="Feature selected opportunities")
    def feature_opportunities(self, request, queryset):
        updated = queryset.update(featured=True)
        self.message_user(request, f"{updated} opportunity(ies) featured.")

    @admin.action(description="Unfeature selected opportunities")
    def unfeature_opportunities(self, request, queryset):
        updated = queryset.update(featured=False)
        self.message_user(request, f"{updated} opportunity(ies) unfeatured.")

    @admin.action(description="Mark as urgent")
    def mark_urgent(self, request, queryset):
        updated = queryset.update(urgent=True)
        self.message_user(request, f"{updated} opportunity(ies) marked urgent.")

    @admin.action(description="Activate selected (set status = Active)")
    def activate_opportunities(self, request, queryset):
        updated = queryset.update(status=Opportunity.Status.ACTIVE)
        self.message_user(request, f"{updated} opportunity(ies) activated.")

    @admin.action(description="Close selected (set status = Closed)")
    def close_opportunities(self, request, queryset):
        updated = queryset.update(status=Opportunity.Status.CLOSED)
        self.message_user(request, f"{updated} opportunity(ies) closed.", level="warning")