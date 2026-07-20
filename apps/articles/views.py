from django.http import HttpResponse

def detail_placeholder(request, slug):
    return HttpResponse(f"Article detail for '{slug}' — built in Phase 11.")