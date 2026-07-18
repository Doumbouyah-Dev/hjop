from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Organization(models.Model):

    class OrgType(models.TextChoices):
        COMPANY = "company", "Company"
        NGO = "ngo", "NGO"
        UNIVERSITY = "university", "University"
        GOVERNMENT = "government", "Government"
        INTERNATIONAL_ORG = "international_org", "International Organization"
        OTHER = "other", "Other"

    class OrgSize(models.TextChoices):
        MICRO = "1-10", "1–10 employees"
        SMALL = "11-50", "11–50 employees"
        MEDIUM = "51-200", "51–200 employees"
        LARGE = "201-500", "201–500 employees"
        XLARGE = "501-1000", "501–1000 employees"
        ENTERPRISE = "1000+", "1000+ employees"

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        PENDING = "pending", "Pending Review"
        SUSPENDED = "suspended", "Suspended"

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to="org_logos/", blank=True, null=True)
    website = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)

    location = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=100)
    county = models.CharField(max_length=100, blank=True)

    org_type = models.CharField(max_length=30, choices=OrgType.choices)
    size = models.CharField(max_length=20, choices=OrgSize.choices, blank=True)

    verified = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="owned_organizations",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "organizations"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["org_type"]),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Organization.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("organizations:detail", kwargs={"slug": self.slug})