from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from formtools.wizard.views import SessionWizardView

from apps.organizations.models import Organization
from .forms import StepBasicInfoForm, StepDetailsForm, StepApplicationInfoForm
from .models import Opportunity


FORMS = [
    ("basic_info", StepBasicInfoForm),
    ("details", StepDetailsForm),
    ("application_info", StepApplicationInfoForm),
]

STEP_TITLES = {
    "basic_info": "Basic Information",
    "details": "Description & Requirements",
    "application_info": "Compensation & Application",
}


class PostOpportunityWizard(SessionWizardView):
    form_list = FORMS
    template_name = "organizations/post_opportunity_wizard.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, "Please sign in to post an opportunity.")
            return redirect("account_login")

        if request.user.role != "employer":
            messages.error(request, "Only employer accounts can post opportunities.")
            return redirect("dashboard:home")

        self.organization = Organization.objects.filter(owner=request.user).first()
        if not self.organization:
            messages.info(request, "Please set up your organization profile first.")
            return redirect("organizations:create")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        context["step_titles"] = STEP_TITLES
        context["current_step_number"] = int(self.steps.step1)
        context["total_steps"] = len(self.form_list)
        context["organization"] = self.organization
        context["current_step_title"] = STEP_TITLES.get(self.steps.current, "")
        return context

    def done(self, form_list, **kwargs):
        data = {}
        for form in form_list:
            data.update(form.cleaned_data)

        tags_raw = data.pop("tags", "")
        tag_list = [t.strip() for t in tags_raw.split(",") if t.strip()]

        opportunity_type = data.pop("opportunity_type", "")

        opportunity = Opportunity.objects.create(
            title=data["title"],
            category=data["category"],
            opportunity_type=opportunity_type,
            location=data.get("location", ""),
            country=data["country"],
            county=data.get("county", ""),
            remote=data.get("remote", False),
            deadline=data["deadline"],
            short_description=data.get("short_description", ""),
            description=data["description"],
            requirements=data.get("requirements", ""),
            benefits=data.get("benefits", ""),
            experience_level=data.get("experience_level", "any"),
            education_level=data.get("education_level", "any"),
            salary_min=data.get("salary_min"),
            salary_max=data.get("salary_max"),
            salary_currency=data.get("salary_currency", "USD"),
            funding_amount=data.get("funding_amount", ""),
            duration=data.get("duration", ""),
            application_link=data.get("application_link", ""),
            application_email=data.get("application_email", ""),
            organization=self.organization,
            posted_by=self.request.user,
            status=Opportunity.Status.ACTIVE if self.organization.status == "active" else Opportunity.Status.DRAFT,
        )

        if tag_list:
            opportunity.tags.add(*tag_list)

        if opportunity.status == Opportunity.Status.DRAFT:
            messages.success(
                self.request,
                "Opportunity saved as a draft — it will go live once your organization is verified."
            )
        else:
            messages.success(self.request, "Opportunity posted successfully!")

        return redirect(reverse("opportunities:detail", kwargs={"slug": opportunity.slug}))


post_opportunity_wizard = PostOpportunityWizard.as_view()