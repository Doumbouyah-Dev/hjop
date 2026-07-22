from django.urls import path
from . import views

app_name = "organizations"

urlpatterns = [
    path("post-opportunity/", views.post_opportunity, name="post_opportunity"),
]
