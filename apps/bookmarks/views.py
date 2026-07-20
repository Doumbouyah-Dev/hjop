from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST

from apps.opportunities.models import Opportunity
from .models import Bookmark


@login_required
@require_POST
def toggle(request, opportunity_id):
    opportunity = get_object_or_404(Opportunity, id=opportunity_id)
    bookmark = Bookmark.objects.filter(user=request.user, opportunity=opportunity).first()

    if bookmark:
        bookmark.delete()
        opportunity.bookmarks_count = opportunity.bookmarked_by.count()
    else:
        Bookmark.objects.create(user=request.user, opportunity=opportunity)
        opportunity.bookmarks_count = opportunity.bookmarked_by.count()

    opportunity.save(update_fields=["bookmarks_count"])

    return render(request, "bookmarks/partials/bookmark_button.html", {
        "opportunity": opportunity,
        "user": request.user,
    })