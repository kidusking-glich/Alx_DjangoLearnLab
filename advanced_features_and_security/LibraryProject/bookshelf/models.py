from django.db import models

class Book(models.Model):
    title = models.CharField(max_length = 200)
    author = models.CharField(max_length = 200)
    publication_year = models.IntegerField()

    def __str__(self):
        return f'"{self.title}" by {self.author} ({self.publication_year})'

# Create your models here.
# relationship_app/models.py

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.db import models
# ... (CustomUserManager class is defined above) ...

class CustomUser(AbstractUser):
    # Additional fields
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    
    # Custom Manager:
    # objects = CustomUserManager() # or BaseUserManager if you skipped the custom one

    def __str__(self):
        return self.username
    
class CustomUserManager(BaseUserManager):

    def create_user(self, username, email, password = None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email= self.normalize_email(email)
        user = self.models(username = username, email =email, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user
    def create_superuser(self, username, email, password=None, **extra_fields):
        # --- THIS METHOD IS REQUIRED ---
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.') # Check for the corrected spelling!

        return self.create_user(username, email, password, **extra_fields)
