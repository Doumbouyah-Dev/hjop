from django.http import HttpResponse


def opportunity_list(request):
    return HttpResponse("Opportunities list — built in Phase 7.")