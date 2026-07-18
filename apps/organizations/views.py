from django.http import HttpResponse


def organization_list(request):
    return HttpResponse("Organizations list — built in Phase 10.")