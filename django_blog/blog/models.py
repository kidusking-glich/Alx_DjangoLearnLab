from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    """
    Represents a single blog post entry.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now=True)
    # ForeignKey to User model (built-in Django Auth)
    # on_delete=models.CASCADE means if the User is deleted, 
    # their posts are also deleted.
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """
        Returns a string representation of the model (the post's title).
        """
        return self.title