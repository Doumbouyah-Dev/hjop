from django.contrib import admin
from django.utils.html import format_html

from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = [
        "user", "opportunity", "status_badge", "applied_at", "updated_at",
    ]
    list_filter = ["status", "applied_at"]
    search_fields = ["user__email", "user__first_name", "opportunity__title"]
    autocomplete_fields = ["user", "opportunity"]
    readonly_fields = ["applied_at", "updated_at"]
    date_hierarchy = "applied_at"
    actions = ["mark_shortlisted", "mark_interview", "mark_accepted", "mark_rejected"]

    @admin.display(description="Status")
    def status_badge(self, obj):
        colors = {
            "applied": "#2563eb", "viewed": "#7c3aed", "shortlisted": "#d97706",
            "interview": "#4f46e5", "accepted": "#16a34a", "rejected": "#dc2626",
            "withdrawn": "#6b7280",
        }
        return format_html(
            '<span style="color:white;background:{};padding:2px 8px;'
            'border-radius:9999px;font-size:11px;font-weight:600;">{}</span>',
            colors.get(obj.status, "#6b7280"), obj.get_status_display()
        )

    @admin.action(description="Mark as Shortlisted")
    def mark_shortlisted(self, request, queryset):
        updated = queryset.update(status=Application.Status.SHORTLISTED)
        self.message_user(request, f"{updated} application(s) shortlisted.")

    @admin.action(description="Mark as Interview")
    def mark_interview(self, request, queryset):
        updated = queryset.update(status=Application.Status.INTERVIEW)
        self.message_user(request, f"{updated} application(s) moved to interview.")

    @admin.action(description="Mark as Accepted")
    def mark_accepted(self, request, queryset):
        updated = queryset.update(status=Application.Status.ACCEPTED)
        self.message_user(request, f"{updated} application(s) accepted.")

    @admin.action(description="Mark as Rejected")
    def mark_rejected(self, request, queryset):
        updated = queryset.update(status=Application.Status.REJECTED)
        self.message_user(request, f"{updated} application(s) rejected.", level="warning")