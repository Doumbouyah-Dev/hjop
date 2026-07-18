from django.contrib import admin

from .models import Bookmark


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ["user", "opportunity", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["user__email", "opportunity__title"]
    autocomplete_fields = ["user", "opportunity"]
    readonly_fields = ["created_at"]