from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [
    path("", views.list_view, name="list"),
    path("<slug:slug>/", views.detail_placeholder, name="detail"),
]