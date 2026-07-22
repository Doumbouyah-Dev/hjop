from django.http import HttpResponse


def list_view(request):
    return HttpResponse("Articles list - built in Phase 11.")


def detail_placeholder(request, slug):
    return HttpResponse(f"Article detail for '{slug}' - built in Phase 11.")