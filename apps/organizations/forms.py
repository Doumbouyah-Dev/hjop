from django import forms

from .models import Organization


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = [
            "name", "description", "logo", "website", "email", "phone",
            "location", "country", "county", "org_type", "size",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-input", "placeholder": "Organization name"}),
            "description": forms.Textarea(attrs={"class": "form-input", "rows": 4, "placeholder": "Tell candidates about your organization"}),
            "logo": forms.ClearableFileInput(attrs={
                "class": "block w-full text-sm text-gray-600 file:mr-4 file:py-2 file:px-4 "
                         "file:rounded-lg file:border-0 file:bg-amber/10 file:text-amber-dark "
                         "file:font-medium hover:file:bg-amber/20 file:cursor-pointer cursor-pointer",
            }),
            "website": forms.URLInput(attrs={"class": "form-input", "placeholder": "https://yourcompany.com"}),
            "email": forms.EmailInput(attrs={"class": "form-input", "placeholder": "contact@yourcompany.com"}),
            "phone": forms.TextInput(attrs={"class": "form-input"}),
            "location": forms.TextInput(attrs={"class": "form-input", "placeholder": "City, Region"}),
            "country": forms.TextInput(attrs={"class": "form-input"}),
            "county": forms.TextInput(attrs={"class": "form-input"}),
            "org_type": forms.Select(attrs={"class": "form-input"}),
            "size": forms.Select(attrs={"class": "form-input"}),
        }

    def clean_logo(self):
        logo = self.cleaned_data.get("logo")
        if logo and hasattr(logo, "size") and logo.size > 2 * 1024 * 1024:
            raise forms.ValidationError("Logo image must be smaller than 2MB.")
        return logo