# notifications/urls.py

from django.urls import path
from .views import NotificationListView

urlpatterns = [
    # Endpoint to list and automatically mark notifications as read
    path('', NotificationListView.as_view(), name='notification-list'),
]