from django import forms

from .models import Opportunity


INPUT_CLASS = "form-input"
SELECT_CLASS = "form-input"
TEXTAREA_CLASS = "form-input"


class StepBasicInfoForm(forms.Form):
    title = forms.CharField(
        max_length=500,
        widget=forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "e.g., Senior Software Engineer"}),
    )
    category = forms.ChoiceField(
        choices=Opportunity.Category_.choices,
        widget=forms.Select(attrs={"class": SELECT_CLASS}),
    )
    opportunity_type = forms.ChoiceField(
        choices=Opportunity.Type.choices, required=False,
        widget=forms.Select(attrs={"class": SELECT_CLASS}),
    )
    location = forms.CharField(
        max_length=255, required=False,
        widget=forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "City, Region"}),
    )
    country = forms.CharField(
        max_length=100, initial="Liberia",
        widget=forms.TextInput(attrs={"class": INPUT_CLASS}),
    )
    county = forms.CharField(
        max_length=100, required=False,
        widget=forms.TextInput(attrs={"class": INPUT_CLASS}),
    )
    remote = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "rounded border-gray-300 text-amber focus:ring-amber"}),
    )
    deadline = forms.DateField(
        widget=forms.DateInput(attrs={"class": INPUT_CLASS, "type": "date"}),
    )


class StepDetailsForm(forms.Form):
    short_description = forms.CharField(
        max_length=500, required=False,
        widget=forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Brief summary (max 500 chars)"}),
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={"class": TEXTAREA_CLASS, "rows": 6, "placeholder": "Detailed description of the opportunity..."}),
    )
    requirements = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"class": TEXTAREA_CLASS, "rows": 5, "placeholder": "What are you looking for in candidates?"}),
    )
    benefits = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"class": TEXTAREA_CLASS, "rows": 4, "placeholder": "What benefits does this opportunity offer?"}),
    )
    experience_level = forms.ChoiceField(
        choices=Opportunity.ExperienceLevel.choices, initial="any",
        widget=forms.Select(attrs={"class": SELECT_CLASS}),
    )
    education_level = forms.ChoiceField(
        choices=Opportunity.EducationLevel.choices, initial="any",
        widget=forms.Select(attrs={"class": SELECT_CLASS}),
    )


class StepApplicationInfoForm(forms.Form):
    salary_min = forms.DecimalField(
        required=False, max_digits=12, decimal_places=2,
        widget=forms.NumberInput(attrs={"class": INPUT_CLASS, "placeholder": "0"}),
    )
    salary_max = forms.DecimalField(
        required=False, max_digits=12, decimal_places=2,
        widget=forms.NumberInput(attrs={"class": INPUT_CLASS, "placeholder": "0"}),
    )
    salary_currency = forms.CharField(
        max_length=3, initial="USD",
        widget=forms.TextInput(attrs={"class": INPUT_CLASS}),
    )
    funding_amount = forms.CharField(
        max_length=255, required=False,
        widget=forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "e.g., $5,000 or Full funding"}),
    )
    duration = forms.CharField(
        max_length=100, required=False,
        widget=forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "e.g., 6 months, 1 year"}),
    )
    application_link = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={"class": INPUT_CLASS, "placeholder": "https://..."}),
    )
    application_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={"class": INPUT_CLASS, "placeholder": "applications@example.com"}),
    )
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Remote, Full-time, NGO (comma separated)"}),
        help_text="Comma-separated tags",
    )

    def clean(self):
        cleaned_data = super().clean()
        salary_min = cleaned_data.get("salary_min")
        salary_max = cleaned_data.get("salary_max")
        if salary_min and salary_max and salary_min > salary_max:
            raise forms.ValidationError("Minimum salary cannot be greater than maximum salary.")
        return cleaned_data