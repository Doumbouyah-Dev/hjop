from apps.categories.models import Category


def site_settings(request):
    """
    Injects data needed on every page (navbar categories, saved-count badge)
    without every view having to remember to fetch it manually.
    """
    context = {
        "nav_categories": Category.objects.filter(active=True).order_by("display_order")[:6],
        "more_categories": Category.objects.filter(active=True).order_by("display_order")[6:14],
    }

    if request.user.is_authenticated:
        context["saved_count"] = request.user.bookmarks.count()

    return context