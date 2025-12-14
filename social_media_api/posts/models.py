from django.db import models
from django.conf import settings # Use settings.AUTH_USER_MODEL for ForeignKeys to User


# Create your models here.
# posts/models.py



class Post(models.Model):
    # ForeignKey to CustomUser (the author)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    
    # Optional: For future image/media posts
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} by {self.author.username}'

class Comment(models.Model):
    # ForeignKey to Post
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments' # Access comments via post.comments.all()
    )
    # ForeignKey to CustomUser (the author of the comment)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.author.username} on Post ID {self.post.id}'