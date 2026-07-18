from django.contrib import admin
from django.utils.html import format_html

from .models import Organization
from apps.opportunities.models import Opportunity


class OpportunityInline(admin.TabularInline):
    """
    Shows an organization's opportunities directly on its admin page —
    replaces the need to jump between the Organizations and
    Opportunities admin lists separately.
    """
    model = Opportunity
    extra = 0
    fields = ["title", "category", "status", "deadline", "featured", "views"]
    readonly_fields = ["views"]
    show_change_link = True
    ordering = ["-created_at"]


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = [
        "name", "org_type", "country", "status_badge",
        "verified", "featured", "opportunity_count", "created_at",
    ]
    list_filter = ["org_type", "status", "verified", "featured", "country"]
    search_fields = ["name", "description", "email", "country"]
    prepopulated_fields = {"slug": ("name",)}
    list_editable = []  # kept empty; status changes go through actions below (auditable)
    readonly_fields = ["created_at", "updated_at"]
    autocomplete_fields = ["owner"]
    inlines = [OpportunityInline]
    actions = ["verify_organizations", "unverify_organizations", "feature_organizations", "suspend_organizations"]

    fieldsets = (
        (None, {"fields": ("name", "slug", "org_type", "size", "logo")}),
        ("Details", {"fields": ("description", "website", "email", "phone")}),
        ("Location", {"fields": ("location", "country", "county")}),
        ("Status", {"fields": ("status", "verified", "featured", "owner")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    @admin.display(description="Status")
    def status_badge(self, obj):
        colors = {"active": "#16a34a", "pending": "#d97706", "suspended": "#dc2626"}
        return format_html(
            '<span style="color:white;background:{};padding:2px 8px;'
            'border-radius:9999px;font-size:11px;font-weight:600;">{}</span>',
            colors.get(obj.status, "#6b7280"), obj.get_status_display()
        )

    @admin.display(description="Listings")
    def opportunity_count(self, obj):
        return obj.opportunities.count()

    @admin.action(description="Mark selected organizations as Verified")
    def verify_organizations(self, request, queryset):
        updated = queryset.update(verified=True)
        self.message_user(request, f"{updated} organization(s) marked as verified.")

    @admin.action(description="Remove verification from selected organizations")
    def unverify_organizations(self, request, queryset):
        updated = queryset.update(verified=False)
        self.message_user(request, f"{updated} organization(s) unverified.")

    @admin.action(description="Feature selected organizations")
    def feature_organizations(self, request, queryset):
        updated = queryset.update(featured=True)
        self.message_user(request, f"{updated} organization(s) featured.")

    @admin.action(description="Suspend selected organizations")
    def suspend_organizations(self, request, queryset):
        updated = queryset.update(status=Organization.Status.SUSPENDED)
        self.message_user(request, f"{updated} organization(s) suspended.", level="warning")