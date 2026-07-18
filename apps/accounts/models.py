from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model — unifies what the original project split
    across `users` (OAuth) and `localUsers` (email/password) tables.
    Extended fully in Phase 3.
    """
    email = models.EmailField(unique=True)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.get_full_name() or self.username