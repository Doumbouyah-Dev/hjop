from django.shortcuts import render

from apps.categories.models import Category
from apps.opportunities.models import Opportunity
from apps.organizations.models import Organization
from apps.articles.models import Article


def home(request):
    context = {
        "categories": Category.objects.filter(active=True).order_by("display_order")[:12],
        "featured_opportunities": Opportunity.objects.filter(
            status="active", featured=True
        ).select_related("organization")[:6],
        "latest_jobs": Opportunity.objects.filter(
            status="active", category="jobs"
        ).select_related("organization").order_by("-created_at")[:3],
        "latest_scholarships": Opportunity.objects.filter(
            status="active", category="scholarships"
        ).select_related("organization").order_by("-created_at")[:3],
        "articles": Article.objects.filter(published=True).order_by("-published_at")[:3],
        "stats": {
            "total_opportunities": Opportunity.objects.filter(status="active").count(),
            "active_jobs": Opportunity.objects.filter(status="active", category="jobs").count(),
            "scholarships": Opportunity.objects.filter(status="active", category="scholarships").count(),
            "organizations": Organization.objects.filter(status="active").count(),
        },
    }
    return render(request, "core/home.html", context)