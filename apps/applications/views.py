from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from apps.opportunities.models import Opportunity
from .forms import ApplicationForm
from .models import Application


@login_required
def apply(request, slug):
    opportunity = get_object_or_404(Opportunity, slug=slug, status="active")

    # Guard: already applied → redirect back with a message instead of
    # showing the form again (the UniqueConstraint would reject it anyway,
    # but catching it here gives a much better UX than a raw IntegrityError page)
    if Application.objects.filter(opportunity=opportunity, user=request.user).exists():
        messages.info(request, "You have already applied for this opportunity.")
        return redirect("opportunities:detail", slug=slug)

    if opportunity.deadline_has_passed if hasattr(opportunity, "deadline_has_passed") else opportunity.is_expired:
        messages.error(request, "This opportunity's application deadline has passed.")
        return redirect("opportunities:detail", slug=slug)

    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.opportunity = opportunity
            application.user = request.user
            try:
                application.save()
            except IntegrityError:
                # Race-condition safety net: two tabs submitting simultaneously
                messages.info(request, "You have already applied for this opportunity.")
                return redirect("opportunities:detail", slug=slug)

            opportunity.applications_count = opportunity.applications.count()
            opportunity.save(update_fields=["applications_count"])

            messages.success(request, "Your application was submitted successfully!")
            return redirect("applications:confirmation", pk=application.pk)
    
    if opportunity.posted_by_id == request.user.id:
        messages.error(request, "You cannot apply to your own posted opportunity.")
        return redirect("opportunities:detail", slug=slug)
    
    else:
        form = ApplicationForm()

    return render(request, "applications/apply.html", {
        "form": form,
        "opportunity": opportunity,
    })


@login_required
def confirmation(request, pk):
    application = get_object_or_404(
        Application.objects.select_related("opportunity", "opportunity__organization"),
        pk=pk, user=request.user,
    )
    return render(request, "applications/confirmation.html", {"application": application})


@login_required
@require_POST
def apply_external(request, slug):
    """
    Records an Application row in the background when the opportunity has
    an external application_link — the user is sent to the external site,
    but we still track that they applied, matching the original's
    behavior of firing applyMutation.mutate() alongside window.open().
    """
    opportunity = get_object_or_404(Opportunity, slug=slug, status="active")

    application, created = Application.objects.get_or_create(
        opportunity=opportunity,
        user=request.user,
        defaults={"status": Application.Status.APPLIED},
    )

    if created:
        opportunity.applications_count = opportunity.applications.count()
        opportunity.save(update_fields=["applications_count"])

    return redirect(opportunity.application_link)


@login_required
@require_POST
def withdraw(request, pk):
    application = get_object_or_404(Application, pk=pk, user=request.user)
    application.status = Application.Status.WITHDRAWN
    application.save(update_fields=["status"])
    messages.success(request, "Application withdrawn.")
    return redirect("dashboard:applications")


