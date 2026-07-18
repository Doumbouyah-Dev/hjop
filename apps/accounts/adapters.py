from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse


class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Central hook for auth-related behavior overrides.
    Replaces the ad-hoc redirect logic scattered across the
    original's Login.tsx / Register.tsx (window.location.href).
    """

    def get_login_redirect_url(self, request):
        return reverse("dashboard:home")

    def is_open_for_signup(self, request):
        # Flip to False if you ever want to close public registration
        return True

    def save_user(self, request, user, form, commit=True):
        """
        Ensure email is always lowercased/normalized —
        the original had no such normalization, a minor
        data-quality bug we're fixing here.
        """
        user.email = user.email.lower().strip()
        return super().save_user(request, user, form, commit)