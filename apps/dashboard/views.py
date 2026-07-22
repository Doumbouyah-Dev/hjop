from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from apps.applications.models import Application
from apps.bookmarks.models import Bookmark
from .forms import ProfileForm


@login_required
def home(request):
    recent_applications = (
        Application.objects.filter(applicant=request.user)
        .select_related("opportunity", "opportunity__organization")
        .order_by("-applied_at")[:4]
    )
    recent_bookmarks = (
        Bookmark.objects.filter(user=request.user)
        .select_related("opportunity", "opportunity__organization")
        .order_by("-created_at")[:4]
    )

    stats = {
        "saved": Bookmark.objects.filter(user=request.user).count(),
        "applied": Application.objects.filter(applicant=request.user).exclude(
            status=Application.Status.WITHDRAWN
        ).count(),
        "interviews": Application.objects.filter(
            applicant=request.user, status=Application.Status.INTERVIEW
        ).count(),
        "accepted": Application.objects.filter(
            applicant=request.user, status=Application.Status.ACCEPTED
        ).count(),
    }

    context = {
        "active_tab": "home",
        "stats": stats,
        "recent_applications": recent_applications,
        "recent_bookmarks": recent_bookmarks,
    }
    return render(request, "dashboard/home.html", context)


@login_required
def saved(request):
    bookmarks_qs = (
        Bookmark.objects.filter(user=request.user)
        .select_related("opportunity", "opportunity__organization")
        .order_by("-created_at")
    )
    paginator = Paginator(bookmarks_qs, 12)
    page_obj = paginator.get_page(request.GET.get("page", 1))

    return render(request, "dashboard/saved.html", {
        "active_tab": "saved",
        "page_obj": page_obj,
    })


@login_required
def applications(request):
    status_filter = request.GET.get("status", "")

    apps_qs = (
        Application.objects.filter(applicant=request.user)
        .select_related("opportunity", "opportunity__organization")
        .order_by("-applied_at")
    )
    if status_filter:
        apps_qs = apps_qs.filter(status=status_filter)

    paginator = Paginator(apps_qs, 10)
    page_obj = paginator.get_page(request.GET.get("page", 1))

    return render(request, "dashboard/applications.html", {
        "active_tab": "applications",
        "page_obj": page_obj,
        "status_choices": Application.Status.choices,
        "current_status": status_filter,
    })


@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("dashboard:profile")
    else:
        form = ProfileForm(instance=request.user)

    return render(request, "dashboard/profile.html", {
        "active_tab": "profile",
        "form": form,
    })