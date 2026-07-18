from django.http import HttpResponse


def article_list(request):
    return HttpResponse("Articles list — built in Phase 11.")