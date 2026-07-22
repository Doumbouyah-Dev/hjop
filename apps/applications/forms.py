from django import forms

from .models import Application


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["cover_letter", "resume", "portfolio_url"]
        widgets = {
            "cover_letter": forms.Textarea(attrs={
                "rows": 6,
                "placeholder": "Tell the employer why you're a great fit for this opportunity...",
                "class": "form-input",
            }),
            "resume": forms.ClearableFileInput(attrs={
                "class": "block w-full text-sm text-gray-600 file:mr-4 file:py-2 file:px-4 "
                         "file:rounded-lg file:border-0 file:bg-amber/10 file:text-amber-dark "
                         "file:font-medium hover:file:bg-amber/20 file:cursor-pointer cursor-pointer",
            }),
            "portfolio_url": forms.URLInput(attrs={
                "placeholder": "https://your-portfolio.com (optional)",
                "class": "form-input",
            }),
        }
        labels = {
            "cover_letter": "Cover Letter",
            "resume": "Resume / CV",
            "portfolio_url": "Portfolio URL (optional)",
        }

    def clean_resume(self):
        resume = self.cleaned_data.get("resume")
        if resume:
            if resume.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError("Resume file must be smaller than 5MB.")
            allowed_extensions = [".pdf", ".doc", ".docx"]
            if not any(resume.name.lower().endswith(ext) for ext in allowed_extensions):
                raise forms.ValidationError("Resume must be a PDF, DOC, or DOCX file.")
        return resume