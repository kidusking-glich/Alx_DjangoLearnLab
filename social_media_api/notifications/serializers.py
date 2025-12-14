# notifications/serializers.py

from rest_framework import serializers
from .models import Notification
from django.contrib.contenttypes.models import ContentType

class NotificationSerializer(serializers.ModelSerializer):
    actor_username = serializers.CharField(source='actor.username', read_only=True)
    # Display the target type and primary key for client-side routing
    target_type = serializers.SerializerMethodField()
    target_id = serializers.IntegerField(source='object_id', read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor_username', 'verb', 'target_type', 'target_id', 'timestamp', 'is_read']
        read_only_fields = fields

    def get_target_type(self, obj):
        return obj.content_type.model