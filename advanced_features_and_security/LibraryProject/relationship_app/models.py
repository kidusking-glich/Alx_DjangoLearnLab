from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser, BaseUserManager # Import AbstractUser
# ... (other imports: User, post_save, receiver, Book, Library, etc.)


# Create your models here.
# 1. Author Model (No relationship fields here)

class Author(models.Model):
    name = models.CharField(max_length=100)
    #birth_date = models.DateField()

    def __str__(self):
        return self.name
    
# 2. Book Model (ForeignKey)
# Demonstrates a One-to-Many relationship: One Author can write many Books.

class Book(models.Model):
    title = models.CharField( max_length=100)
    # ForeignKey creates a one-to-many link.
    # on_delete=models.CASCADE means if the Author is deleted, all their Books are also deleted.
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title
# 3. Library Model (ManyToManyField)
# Demonstrates a Many-to-Many relationship: A Library can have many Books, and a Book can be in many Libraries.

class Library(models.Model):
    name = models.CharField(max_length=100)
#many to many field creates  a link table to  manage the relationship between Library and Book instances.
    #books = models.ManyToManyField(Book, related_name='libraries')

    def __str__(self):
        return self.name
    
# 4. Librarian Model (OneToOneField)
# Demonstrates a One-to-One relationship: One Librarian manages exactly one Library, and vice-versa.
class Librarian(models.Model):
    name = models.CharField(max_length=100)

    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name='librarian')
    def __str__ (self):
        return self.name
    


class UserProfile(models.Model):

    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('LIBRARIAN', 'Librarian'),
        ('MEMBER', 'Member'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='MEMBER')

    def __str__(self):
        return f'{self.user.username} - {self.get_role_display()}' 
    
@receiver(post_save, sender = User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):

    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()


# relationship_app/models.py

#from django.db import models
# ... (other imports and models)

class Book(models.Model):
    # ... (Existing fields like title, publication_year, author, library) ...
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    #library = models.ManyToManyField('Library', related_name='books_in_library')

    # --- Custom Permissions Definition ---
    class Meta:
        permissions = [
            # ('code_name', 'Human readable description')
            ("can_add_book", "Can add new book entries"),
            ("can_change_book", "Can edit existing book entries"),
            ("can_delete_book", "Can delete book entries"),
        ]
        # Ensure the table name is correctly set if you use custom database names
        # db_table = 'relationship_app_book'
    # -----------------------------------

    def __str__(self):
        return self.title
    

# --- Custom User Manager (Step 3) ---

class CustomUserManager(BaseUserManager):

    def create_user(self, username, email, password = None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email= self.normalize_email(email)
        user = self.models(username = username, email =email, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user
    

    def create_superuser(self, username, email, password  = None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_supperuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('superuser must have is_supperuser = True')
        
        return self.create_user(username, email, password, **extra_fields)
    


class CustomUser(AbstractUser):
    # AbstractUser already provides: username, first_name, last_name, email, password, is_active, is_staff, is_superuser, last_login, date_joined

    date_of_birth = models.DateField(null = True, blank= True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null = True, blank= True)

    objects = CustomUserManager()

    def __str__(self):
        return self.username
    
# --- Update Existing Models to reference CustomUser (Step 5) ---

# Example: If you have a model that references the user, update it here.
# Since UserProfile is already linked to Django's built-in User, you must update it:
class UserProfile(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # ... (rest of UserProfile)