from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


@login_required
def home(request):
    return HttpResponse(
        f"Welcome, {request.user.get_full_name() or request.user.email}! "
        f"Role: {request.user.get_role_display()}. "
        "Full dashboard UI built in Phase 9."
    )