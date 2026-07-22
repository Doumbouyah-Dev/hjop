from django.urls import path
from . import views

app_name = "applications"

urlpatterns = [
    path("apply/<slug:slug>/", views.apply, name="apply"),
    path("apply-external/<slug:slug>/", views.apply_external, name="apply_external"),
    path("confirmation/<int:pk>/", views.confirmation, name="confirmation"),
    path("withdraw/<int:pk>/", views.withdraw, name="withdraw"),
]