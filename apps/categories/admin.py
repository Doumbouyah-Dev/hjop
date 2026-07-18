from django.contrib import admin
from django.utils.html import format_html

from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "color_swatch", "display_order", "active", "opportunity_count"]
    list_filter = ["active"]
    list_editable = ["display_order", "active"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["display_order"]

    @admin.display(description="Color")
    def color_swatch(self, obj):
        return format_html(
            '<span style="display:inline-block;width:20px;height:20px;'
            'background:{};border-radius:4px;border:1px solid #ccc;"></span> {}',
            obj.color, obj.color
        )

    @admin.display(description="Active Opportunities")
    def opportunity_count(self, obj):
        return obj.opportunity_count