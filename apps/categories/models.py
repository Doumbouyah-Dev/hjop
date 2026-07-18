from django.db import models
from django.urls import reverse


class Category(models.Model):
    """
    Opportunity taxonomy. Matches the original `categories` table 1:1 —
    this one was already clean in the source project.
    """

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(
        max_length=50, blank=True,
        help_text="Lucide icon name, e.g. 'Briefcase', 'GraduationCap'"
    )
    color = models.CharField(max_length=7, default="#0B1F33")
    display_order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "categories"
        ordering = ["display_order", "name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("opportunities:list") + f"?category={self.slug}"

    @property
    def opportunity_count(self):
        return self.opportunities.filter(status="active").count()