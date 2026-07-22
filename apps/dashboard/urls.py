from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.home, name="home"),
    path("saved/", views.saved, name="saved"),
    path("profile/", views.profile, name="profile"),
    path("applications/", views.applications, name="applications"),
]