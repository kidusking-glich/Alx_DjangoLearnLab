from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer

# Create your views here.

# notifications/views.py



class NotificationListView(generics.ListAPIView):
    """
    Lists notifications for the authenticated user, ordered by timestamp.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only fetch notifications addressed to the current user
        return Notification.objects.filter(recipient=self.request.user).order_by('-timestamp')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        # Automatically mark all fetched notifications as read
        queryset.filter(is_read=False).update(is_read=True)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)