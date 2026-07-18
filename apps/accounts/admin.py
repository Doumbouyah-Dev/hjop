from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom admin for our email-based User model.
    Django's default UserAdmin assumes `username` — we override
    fieldsets/list views to match our actual fields.
    """

    ordering = ["-date_joined"]
    list_display = [
        "email", "get_full_name", "role", "is_staff",
        "is_active", "profile_complete_percent", "date_joined",
    ]
    list_filter = ["role", "is_staff", "is_active", "is_superuser", "education_level"]
    search_fields = ["email", "first_name", "last_name", "phone"]
    readonly_fields = ["date_joined", "last_login", "last_sign_in_at"]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {
            "fields": (
                "first_name", "last_name", "avatar", "phone", "bio",
                "location", "county", "website", "linkedin",
            )
        }),
        ("Professional Info", {
            "fields": (
                "education_level", "field_of_study", "years_of_experience",
                "skills", "languages", "resume",
            )
        }),
        ("Role & Access", {
            "fields": ("role", "is_active", "is_staff", "is_superuser", "groups", "user_permissions")
        }),
        ("Important Dates", {
            "fields": ("last_login", "date_joined", "last_sign_in_at", "created_at", "updated_at")
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "role", "is_staff", "is_active"),
        }),
    )

    @admin.display(description="Full Name")
    def get_full_name(self, obj):
        return obj.get_full_name() or "—"

    @admin.display(description="Profile %")
    def profile_complete_percent(self, obj):
        return f"{obj.profile_complete_percent}%"