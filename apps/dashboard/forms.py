from django import forms

from apps.accounts.models import User


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name", "last_name", "avatar", "phone", "bio",
            "location", "county", "website", "linkedin",
            "education_level", "field_of_study", "years_of_experience",
            "resume",
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-input"}),
            "last_name": forms.TextInput(attrs={"class": "form-input"}),
            "avatar": forms.ClearableFileInput(attrs={
                "class": "block w-full text-sm text-gray-600 file:mr-4 file:py-2 file:px-4 "
                         "file:rounded-lg file:border-0 file:bg-amber/10 file:text-amber-dark "
                         "file:font-medium hover:file:bg-amber/20 file:cursor-pointer cursor-pointer",
            }),
            "phone": forms.TextInput(attrs={"class": "form-input", "placeholder": "+231 XXX XXX XXXX"}),
            "bio": forms.Textarea(attrs={"class": "form-input", "rows": 4, "placeholder": "Tell us about yourself"}),
            "location": forms.TextInput(attrs={"class": "form-input", "placeholder": "City, Country"}),
            "county": forms.TextInput(attrs={"class": "form-input", "placeholder": "e.g., Montserrado"}),
            "website": forms.URLInput(attrs={"class": "form-input", "placeholder": "https://yourwebsite.com"}),
            "linkedin": forms.URLInput(attrs={"class": "form-input", "placeholder": "https://linkedin.com/in/..."}),
            "education_level": forms.Select(attrs={"class": "form-input"}),
            "field_of_study": forms.TextInput(attrs={"class": "form-input", "placeholder": "e.g., Computer Science"}),
            "years_of_experience": forms.NumberInput(attrs={"class": "form-input", "min": 0}),
            "resume": forms.ClearableFileInput(attrs={
                "class": "block w-full text-sm text-gray-600 file:mr-4 file:py-2 file:px-4 "
                         "file:rounded-lg file:border-0 file:bg-amber/10 file:text-amber-dark "
                         "file:font-medium hover:file:bg-amber/20 file:cursor-pointer cursor-pointer",
            }),
        }

    def clean_resume(self):
        resume = self.cleaned_data.get("resume")
        if resume and hasattr(resume, "size"):
            if resume.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Resume file must be smaller than 5MB.")
        return resume

    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")
        if avatar and hasattr(avatar, "size"):
            if avatar.size > 2 * 1024 * 1024:
                raise forms.ValidationError("Avatar image must be smaller than 2MB.")
        return avatar