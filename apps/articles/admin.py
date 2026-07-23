from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html

from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = [
        "title", "category", "author_display", "published_badge",
        "featured", "view_count", "published_at",
    ]
    list_filter = ["published", "featured", "category"]
    search_fields = ["title", "content", "excerpt"]
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ["author"]
    readonly_fields = ["view_count", "created_at", "updated_at"]
    date_hierarchy = "published_at"
    actions = ["publish_articles", "unpublish_articles", "feature_articles"]

    fieldsets = (
        (None, {"fields": ("title", "slug", "category", "cover_image")}),
        ("Content", {"fields": ("excerpt", "content"), "description": "Content supports Markdown formatting: **bold**, # Headers, - lists, [links](url)."}),
        ("Authorship", {"fields": ("author", "author_name")}),
        ("Publishing", {"fields": ("published", "featured", "published_at")}),
        ("Stats", {"fields": ("view_count",)}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    @admin.display(description="Author")
    def author_display(self, obj):
        return obj.author or obj.author_name or "—"

    @admin.display(description="Published")
    def published_badge(self, obj):
        color = "#16a34a" if obj.published else "#6b7280"
        label = "Published" if obj.published else "Draft"
        return format_html(
            '<span style="color:white;background:{};padding:2px 8px;'
            'border-radius:9999px;font-size:11px;font-weight:600;">{}</span>',
            color, label
        )

    @admin.action(description="Publish selected articles")
    def publish_articles(self, request, queryset):
        updated = queryset.update(published=True, published_at=timezone.now())
        self.message_user(request, f"{updated} article(s) published.")

    @admin.action(description="Unpublish selected articles")
    def unpublish_articles(self, request, queryset):
        updated = queryset.update(published=False)
        self.message_user(request, f"{updated} article(s) unpublished.", level="warning")

    @admin.action(description="Feature selected articles")
    def feature_articles(self, request, queryset):
        updated = queryset.update(featured=True)
        self.message_user(request, f"{updated} article(s) featured.")