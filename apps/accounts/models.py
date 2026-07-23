from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone

from config import settings


class UserManager(BaseUserManager):
    """
    Custom manager required because we're using email instead of
    username as the unique identifier for authentication.
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", User.Role.ADMIN)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Unified user model. Replaces the original project's split between
    `users` (OAuth) and `localUsers` (email/password) tables — here,
    OAuth accounts (added in Phase 4) simply attach to this same model
    via django-allauth's SocialAccount, so there is only ever ONE user
    record per person regardless of how they signed up.
    """

    class Role(models.TextChoices):
        JOB_SEEKER = "user", "Job Seeker"
        EMPLOYER = "employer", "Employer"
        ADMIN = "admin", "Administrator"

    class EducationLevel(models.TextChoices):
        HIGH_SCHOOL = "high_school", "High School"
        BACHELOR = "bachelor", "Bachelor's Degree"
        MASTER = "master", "Master's Degree"
        PHD = "phd", "PhD"
        OTHER = "other", "Other"

    # --- Identity ---
    username = models.CharField(max_length=150, unique=False, blank=True, null=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.JOB_SEEKER)

    # --- Profile (folds in the original `userProfiles` table) ---
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    county = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)

    education_level = models.CharField(
        max_length=20, choices=EducationLevel.choices, blank=True
    )
    field_of_study = models.CharField(max_length=255, blank=True)
    years_of_experience = models.PositiveIntegerField(default=0)

    skills = ArrayField(
        models.CharField(max_length=100), blank=True, default=list
    )
    languages = models.JSONField(blank=True, default=list)
    # Expected shape: [{"language": "English", "proficiency": "Fluent"}, ...]

    resume = models.FileField(upload_to="resumes/", blank=True, null=True)

    email_verified = models.BooleanField(default=False)
    last_sign_in_at = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = "users"
        ordering = ["-date_joined"]

    def __str__(self):
        return self.get_full_name() or self.email

    @property
    def profile_completion_percent(self) -> int:
        """
        Mirrors the original project's ad-hoc profile-completeness
        calculation, now as a clean computed property instead of a
        stored/stale field that has to be manually recalculated
        on every profile update.
        """
        fields_to_check = [
            self.bio,
            self.location,
            self.education_level,
            self.skills,
            self.languages,
            self.resume,
        ]
        filled = sum(1 for f in fields_to_check if f)
        return round((filled / len(fields_to_check)) * 100)

class Notification(models.Model):
    class NotificationType(models.TextChoices):
        APPLICATION_UPDATE = "application_update", "Application Update"
        OPPORTUNITY_MATCH = "opportunity_match", "New Opportunity Match"
        DEADLINE_REMINDER = "deadline_reminder", "Deadline Reminder"
        SYSTEM = "system", "System"
        MESSAGE = "message", "Message"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications"
    )
    notification_type = models.CharField(max_length=30, choices=NotificationType.choices)
    title = models.CharField(max_length=255)
    message = models.TextField(blank=True)
    link = models.CharField(max_length=500, blank=True)
    read = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "notifications"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "read"]),
        ]

    def __str__(self):
        return f"{self.get_notification_type_display()} → {self.user}"