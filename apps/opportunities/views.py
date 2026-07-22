from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from apps.categories.models import Category
from apps.applications.models import Application
from .models import Opportunity


SORT_OPTIONS = {
    "recent": "-created_at",
    "deadline": "deadline",
    "popular": "-views",
}


def _filtered_queryset(request):
    qs = Opportunity.objects.filter(status="active").select_related("organization", "category")

    search = request.GET.get("search", "").strip()
    category_slug = request.GET.get("category", "")
    country = request.GET.get("country", "")
    opportunity_type = request.GET.get("type", "")
    experience = request.GET.get("experience", "")
    remote_only = request.GET.get("remote") == "1"
    sort = request.GET.get("sort", "recent")

    if search:
        qs = qs.filter(
            Q(title__icontains=search) |
            Q(short_description__icontains=search) |
            Q(organization__name__icontains=search)
        )
    if category_slug:
        qs = qs.filter(category__slug=category_slug)
    if country:
        qs = qs.filter(country__iexact=country)
    if opportunity_type:
        qs = qs.filter(opportunity_type=opportunity_type)
    if experience:
        qs = qs.filter(experience_level=experience)
    if remote_only:
        qs = qs.filter(remote=True)

    qs = qs.order_by(SORT_OPTIONS.get(sort, "-created_at"))
    return qs


def list_view(request):
    qs = _filtered_queryset(request)

    paginator = Paginator(qs, 12)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.filter(active=True).order_by("display_order")

    context = {
        "page_obj": page_obj,
        "categories": categories,
        "opportunity_types": Opportunity.Type.choices,
        "experience_levels": Opportunity.ExperienceLevel.choices,
        "total_count": paginator.count,
        "current_search": request.GET.get("search", ""),
        "current_category": request.GET.get("category", ""),
        "current_country": request.GET.get("country", ""),
        "current_type": request.GET.get("type", ""),
        "current_experience": request.GET.get("experience", ""),
        "current_remote": request.GET.get("remote") == "1",
        "current_sort": request.GET.get("sort", "recent"),
        "current_category_obj": Category.objects.filter(slug=request.GET.get("category", "")).first(),
    }

    if request.htmx:
        return render(request, "opportunities/partials/results.html", context)

    return render(request, "opportunities/list.html", context)


def detail_view(request, slug):
    opportunity = get_object_or_404(
        Opportunity.objects.select_related("organization", "category"), slug=slug
    )

    Opportunity.objects.filter(pk=opportunity.pk).update(views=opportunity.views + 1)

    already_applied = False
    if request.user.is_authenticated:
        already_applied = Application.objects.filter(
            opportunity=opportunity, user=request.user
        ).exists()

    related = Opportunity.objects.filter(
        category=opportunity.category, status="active"
    ).exclude(pk=opportunity.pk).select_related("organization", "category")[:3]

    context = {
        "opportunity": opportunity,
        "already_applied": already_applied,
        "related_opportunities": related,
        "is_expired": opportunity.deadline < timezone.now().date(),
    }
    return render(request, "opportunities/detail.html", context)