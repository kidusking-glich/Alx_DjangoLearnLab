from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.
# notifications/models.py



class Notification(models.Model):
    # The user who should receive the notification
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        db_index=True
    )

    # The user who performed the action (e.g., the user who liked the post)
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='actions'
    )

    # A short phrase describing the action (e.g., 'liked', 'commented', 'followed')
    verb = models.CharField(max_length=255)

    # Generic Foreign Key setup to point to any model (Post, Comment, etc.)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    target = GenericForeignKey('content_type', 'object_id')

    # Status and Time
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.actor.username} {self.verb} {self.target} for {self.recipient.username}"