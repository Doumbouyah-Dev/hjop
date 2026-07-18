from django.http import HttpResponse


def dashboard_home(request):
    return HttpResponse("Dashboard home — built in Phase 9.")