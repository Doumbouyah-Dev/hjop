from django.urls import path

from . import notification_views

app_name = "accounts"

urlpatterns = [
    path("notifications/", notification_views.list_view, name="notifications"),
    path("notifications/dropdown/", notification_views.dropdown, name="notifications_dropdown"),
    path("notifications/badge/", notification_views.bell_badge, name="notifications_badge"),
    path("notifications/<int:pk>/read/", notification_views.mark_read, name="notification_read"),
    path("notifications/mark-all-read/", notification_views.mark_all_read, name="notifications_mark_all_read"),
]