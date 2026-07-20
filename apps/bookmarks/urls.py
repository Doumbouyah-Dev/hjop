from django.urls import path
from . import views

app_name = "bookmarks"

urlpatterns = [
    path("toggle/<int:opportunity_id>/", views.toggle, name="toggle"),
]