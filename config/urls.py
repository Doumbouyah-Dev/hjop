from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),

    path("", include("apps.core.urls")),
    path("opportunities/", include("apps.opportunities.urls")),
    path("organizations/", include("apps.organizations.urls")),
    path("dashboard/", include("apps.dashboard.urls")),
    path("articles/", include("apps.articles.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])