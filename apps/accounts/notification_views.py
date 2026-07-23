from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import Notification


@login_required
def dropdown(request):
    """
    Renders the notification bell's dropdown contents — called via HTMX
    whenever the bell icon is clicked, keeping the navbar itself lightweight.
    """
    notifications = request.user.notifications.all()[:8]
    unread_count = request.user.notifications.filter(read=False).count()
    return render(request, "accounts/partials/notification_dropdown.html", {
        "notifications": notifications,
        "unread_count": unread_count,
    })


@login_required
def bell_badge(request):
    """
    Renders just the unread-count badge — used for periodic HTMX polling
    so the bell shows a live-ish unread count without a full page reload.
    """
    unread_count = request.user.notifications.filter(read=False).count()
    return render(request, "accounts/partials/notification_badge.html", {
        "unread_count": unread_count,
    })


@login_required
@require_POST
def mark_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.read = True
    notification.save(update_fields=["read"])

    if notification.link:
        return redirect(notification.link)
    return redirect("dashboard:home")


@login_required
@require_POST
def mark_all_read(request):
    request.user.notifications.filter(read=False).update(read=True)
    return dropdown(request)


@login_required
def list_view(request):
    notifications = request.user.notifications.all()
    return render(request, "accounts/notifications.html", {"notifications": notifications})