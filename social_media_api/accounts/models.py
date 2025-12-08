from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    # ManyToMany field referencing itself, symmetrical=False for unidirectional following
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following', # Reverse relationship: user.following lists who the user follows
        blank=True
    )

    def __str__(self):
        return self.username