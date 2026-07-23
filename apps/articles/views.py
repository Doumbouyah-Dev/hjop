from django.core.paginator import Paginator
from django.db.models import F
from django.shortcuts import render, get_object_or_404

from .models import Article


def list_view(request):
    articles_qs = Article.objects.filter(published=True).order_by("-published_at")

    category = request.GET.get("category", "")
    if category:
        articles_qs = articles_qs.filter(category__iexact=category)

    # Distinct categories in use, for the filter dropdown — computed from
    # actual published articles rather than a hardcoded list, so it never
    # goes stale as new categories get used
    categories = (
        Article.objects.filter(published=True)
        .exclude(category="")
        .values_list("category", flat=True)
        .distinct()
        .order_by("category")
    )

    featured_article = Article.objects.filter(published=True, featured=True).order_by("-published_at").first()

    paginator = Paginator(articles_qs, 9)
    page_obj = paginator.get_page(request.GET.get("page", 1))

    return render(request, "articles/list.html", {
        "page_obj": page_obj,
        "categories": categories,
        "current_category": category,
        "featured_article": featured_article,
    })


def detail_view(request, slug):
    article = get_object_or_404(Article, slug=slug, published=True)

    # Atomic increment avoids a read-then-write race condition under
    # concurrent requests (two visitors hitting "view" at once won't
    # clobber each other's increment)
    Article.objects.filter(pk=article.pk).update(view_count=F("view_count") + 1)
    article.refresh_from_db(fields=["view_count"])

    related_articles = Article.objects.filter(
        published=True, category=article.category
    ).exclude(pk=article.pk).order_by("-published_at")[:3] if article.category else []

    return render(request, "articles/detail.html", {
        "article": article,
        "related_articles": related_articles,
    })