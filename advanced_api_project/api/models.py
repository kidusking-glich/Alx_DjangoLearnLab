from django.db import models

# Create your models here.
# --- Author Model ---
class Author(models.Model):
    """
    Model representing an Author. A single Author can have multiple Books.
    """
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

# --- Book Model ---
class Book(models.Model):
    """
    Model representing a Book. A Book is linked to a single Author (ForeignKey).
    """
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    
    # ForeignKey links Book to Author (one Author to many Books)
    # related_name='books' allows us to access all books from an Author instance (author.books.all())
    author = models.ForeignKey(
        Author, 
        related_name='books', 
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.title} ({self.publication_year})"