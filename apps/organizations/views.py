from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from apps.opportunities.models import Opportunity
from .forms import OrganizationForm
from .models import Organization


def detail(request, slug):
    organization = get_object_or_404(Organization, slug=slug, status="active")

    opportunities_qs = Opportunity.objects.filter(
        organization=organization, status="active"
    ).order_by("-created_at")

    paginator = Paginator(opportunities_qs, 9)
    page_obj = paginator.get_page(request.GET.get("page", 1))

    return render(request, "organizations/detail.html", {
        "organization": organization,
        "page_obj": page_obj,
        "total_opportunities": paginator.count,
    })


def list_view(request):
    organizations_qs = Organization.objects.filter(status="active").order_by("-featured", "-created_at")

    org_type = request.GET.get("type", "")
    if org_type:
        organizations_qs = organizations_qs.filter(org_type=org_type)

    paginator = Paginator(organizations_qs, 12)
    page_obj = paginator.get_page(request.GET.get("page", 1))

    return render(request, "organizations/list.html", {
        "page_obj": page_obj,
        "org_types": Organization.OrgType.choices,
        "current_type": org_type,
    })


@login_required
def create(request):
    # Employers only — job seekers have no reason to register an organization
    if request.user.role != "employer":
        messages.error(request, "Only employer accounts can register an organization.")
        return redirect("dashboard:home")

    # Prevent creating duplicate orgs if the user already owns one
    if Organization.objects.filter(owner=request.user).exists():
        messages.info(request, "You already have an organization profile.")
        return redirect("organizations:my_organization")

    if request.method == "POST":
        form = OrganizationForm(request.POST, request.FILES)
        if form.is_valid():
            organization = form.save(commit=False)
            organization.owner = request.user
            organization.status = Organization.Status.PENDING  # requires admin verification
            organization.save()
            messages.success(
                request,
                "Organization profile created! It's pending review — "
                "you can start drafting opportunities in the meantime."
            )
            return redirect("organizations:my_organization")
    else:
        form = OrganizationForm()

    return render(request, "organizations/create.html", {"form": form})


@login_required
def my_organization(request):
    organization = Organization.objects.filter(owner=request.user).first()
    if not organization:
        return redirect("organizations:create")

    opportunities = Opportunity.objects.filter(organization=organization).order_by("-created_at")

    return render(request, "organizations/my_organization.html", {
        "organization": organization,
        "opportunities": opportunities,
    })