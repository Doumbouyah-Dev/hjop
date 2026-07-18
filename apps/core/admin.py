from django.contrib import admin

admin.site.site_header = "HJ Opportunity Hub — Admin"
admin.site.site_title = "HJ Opportunity Hub Admin"
admin.site.index_title = "Management Dashboard"
from django.contrib.admin.apps import AdminConfig

from taggit.models import Tag

try:
    admin.site.register(Tag)
except admin.sites.AlreadyRegistered:
    pass

class CustomAdminSite(admin.AdminSite):
    site_header = "HJ Opportunity Hub — Admin"
    site_title = "HJ Opportunity Hub Admin"
    index_title = "Management Dashboard"

    def get_app_list(self, request, app_label=None):
        """
        Force a business-priority ordering instead of Django's default
        alphabetical app listing — Opportunities and Applications matter
        most day-to-day, Accounts/Admin housekeeping matters least.
        """
        app_dict = self._build_app_dict(request, app_label)
        priority_order = [
            "opportunities", "organizations", "applications",
            "bookmarks", "categories", "articles", "accounts",
            "taggit", "socialaccount", "account", "sites", "auth",
        ]
        app_list = sorted(
            app_dict.values(),
            key=lambda x: priority_order.index(x["app_label"])
            if x["app_label"] in priority_order else 999,
        )
        for app in app_list:
            app["models"].sort(key=lambda x: x["name"])
        return app_list