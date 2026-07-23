from django.urls import path
from . import views

app_name = "organizations"

urlpatterns = [
    path("", views.list_view, name="list"),
    path("create/", views.create, name="create"),
    path("my-organization/", views.my_organization, name="my_organization"),
    # path("post-opportunity/", wizard.post_opportunity_wizard, name="post_opportunity"),
    path("<slug:slug>/", views.detail, name="detail"),
]