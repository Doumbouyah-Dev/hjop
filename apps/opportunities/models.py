from django.utils import timezone
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from taggit.managers import TaggableManager

from apps.organizations.models import Organization
from apps.categories.models import Category


class Opportunity(models.Model):

    class Type(models.TextChoices):
        FULL_TIME = "full_time", "Full-time"
        PART_TIME = "part_time", "Part-time"
        CONTRACT = "contract", "Contract"
        TEMPORARY = "temporary", "Temporary"
        REMOTE = "remote", "Remote"
        HYBRID = "hybrid", "Hybrid"
        ONSITE = "onsite", "Onsite"

    class ExperienceLevel(models.TextChoices):
        ENTRY = "entry", "Entry Level"
        MID = "mid", "Mid Level"
        SENIOR = "senior", "Senior Level"
        EXECUTIVE = "executive", "Executive"
        ANY = "any", "Any"

    class EducationLevel(models.TextChoices):
        HIGH_SCHOOL = "high_school", "High School"
        BACHELOR = "bachelor", "Bachelor's Degree"
        MASTER = "master", "Master's Degree"
        PHD = "phd", "PhD"
        ANY = "any", "Any"
        OTHER = "other", "Other"

    class SalaryPeriod(models.TextChoices):
        HOURLY = "hourly", "Hourly"
        DAILY = "daily", "Daily"
        WEEKLY = "weekly", "Weekly"
        MONTHLY = "monthly", "Monthly"
        YEARLY = "yearly", "Yearly"
        ONE_TIME = "one_time", "One-time"

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        ACTIVE = "active", "Active"
        PAUSED = "paused", "Paused"
        EXPIRED = "expired", "Expired"
        CLOSED = "closed", "Closed"

    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=550, unique=True, blank=True)
    description = models.TextField()
    short_description = models.CharField(max_length=500, blank=True)
    requirements = models.TextField(blank=True)
    benefits = models.TextField(blank=True)

    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="opportunities"
    )
    subcategory = models.CharField(max_length=100, blank=True)
    opportunity_type = models.CharField(max_length=20, choices=Type.choices, blank=True)
    experience_level = models.CharField(
        max_length=20, choices=ExperienceLevel.choices, default=ExperienceLevel.ANY
    )
    education_level = models.CharField(
        max_length=20, choices=EducationLevel.choices, default=EducationLevel.ANY
    )

    location = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=100, db_index=True)
    county = models.CharField(max_length=100, blank=True)
    remote = models.BooleanField(default=False)

    salary_min = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    salary_currency = models.CharField(max_length=3, default="USD")
    salary_period = models.CharField(max_length=20, choices=SalaryPeriod.choices, blank=True)
    funding_amount = models.CharField(max_length=255, blank=True)

    duration = models.CharField(max_length=100, blank=True)
    start_date = models.DateField(null=True, blank=True)
    deadline = models.DateField(db_index=True)

    application_link = models.URLField(blank=True)
    application_email = models.EmailField(blank=True)
    application_instructions = models.TextField(blank=True)
    max_users = models.PositiveIntegerField(null=True, blank=True)

    tags = TaggableManager(blank=True)

    seo_title = models.CharField(max_length=70, blank=True)
    seo_description = models.CharField(max_length=160, blank=True)

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, db_index=True)
    featured = models.BooleanField(default=False, db_index=True)
    urgent = models.BooleanField(default=False)
    sponsored = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)

    views = models.PositiveIntegerField(default=0)
    bookmarks_count = models.PositiveIntegerField(default=0)
    applications_count = models.PositiveIntegerField(default=0)

    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="opportunities",
        null=True, blank=True,
    )
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        related_name="posted_opportunities",
    )

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "opportunities"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "category"]),
            models.Index(fields=["status", "deadline"]),
            models.Index(fields=["status", "featured"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)[:500]
            slug = base_slug
            n = 1
            while Opportunity.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                n += 1
                slug = f"{base_slug}-{n}"
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    # Inside your Opportunity model (is_expired property)
    @property
    def is_expired(self):
        if not self.deadline:
            return False
        return self.deadline < timezone.now().date()

    @property
    def days_left(self):
        from django.utils import timezone
        delta = self.deadline - timezone.now().date()
        return delta.days

    # --- Application details ---
    application_link = models.URLField(blank=True)
    application_email = models.EmailField(blank=True)
    application_instructions = models.TextField(blank=True)
    max_users = models.PositiveIntegerField(null=True, blank=True)

    tags = TaggableManager(blank=True)

    # --- SEO ---
    seo_title = models.CharField(max_length=70, blank=True)
    seo_description = models.CharField(max_length=160, blank=True)

    # --- Status flags ---
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    featured = models.BooleanField(default=False)
    urgent = models.BooleanField(default=False)
    sponsored = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)

    # --- Denormalized counters (updated via signals/F() expressions, see Phase 8) ---
    views = models.PositiveIntegerField(default=0)
    bookmark_count = models.PositiveIntegerField(default=0)
    application_count = models.PositiveIntegerField(default=0)

    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE,
        related_name="opportunities", null=True, blank=True,
    )
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, related_name="posted_opportunities",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "opportunities"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["opportunity_type"]),
            models.Index(fields=["status"]),
            models.Index(fields=["featured"]),
            models.Index(fields=["deadline"]),
            models.Index(fields=["country"]),
            models.Index(fields=["organization"]),
            models.Index(fields=["status", "opportunity_type"]),  # composite, for filtered browse
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)[:500]
            slug = f"{base_slug}-{int(timezone.now().timestamp())}"
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("opportunities:detail", kwargs={"slug": self.slug})
    @property
    def is_expired(self):
        if not self.deadline:
            return False
        return self.deadline < timezone.now().date()

    @property
    def days_left(self):
        delta = self.deadline - timezone.now().date()
        return delta.days

    @property
    def is_urgent_deadline(self):
        return 0 <= self.days_left <= 7
    
    @property
    def days_left(self):
        from django.utils import timezone
        delta = self.deadline - timezone.now().date()
        return delta.days