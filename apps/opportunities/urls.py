from django.urls import path
from . import views

app_name = "opportunities"

urlpatterns = [
    path("", views.list_view, name="list"),
    path("<slug:slug>/", views.detail_view, name="detail"),
]