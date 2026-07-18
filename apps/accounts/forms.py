from allauth.account.forms import SignupForm
from django import forms

from .models import User


class CustomSignupForm(SignupForm):
    """
    Extends allauth's base signup form to collect full name and role,
    matching the original Register.tsx UX (Job Seeker vs Employer toggle).
    """

    full_name = forms.CharField(
        max_length=255,
        label="Full Name",
        widget=forms.TextInput(attrs={
            "placeholder": "John Doe",
            "class": (
                "w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg "
                "focus:outline-none focus:ring-2 focus:ring-amber-400 focus:border-amber-400"
            ),
        }),
    )
    role = forms.ChoiceField(
        choices=User.Role.choices,
        initial=User.Role.JOB_SEEKER,
        widget=forms.RadioSelect,
        label="I am a...",
    )

    field_order = ["full_name", "email", "role", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_input = (
            "w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg "
            "focus:outline-none focus:ring-2 focus:ring-amber-400 focus:border-amber-400"
        )
        for field_name in ["email", "password1", "password2"]:
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update({
                    "class": base_input,
                    "placeholder": {
                        "email": "you@example.com",
                        "password1": "Minimum 8 characters",
                        "password2": "Confirm your password",
                    }.get(field_name, ""),
                })
    
    def signup(self, request, user):
        """Called by allauth after the User instance is built but before final save."""
        full_name = self.cleaned_data["full_name"].strip()
        name_parts = full_name.split(" ", 1)
        user.first_name = name_parts[0]
        user.last_name = name_parts[1] if len(name_parts) > 1 else ""
        user.role = self.cleaned_data["role"]
        user.save()
        return user