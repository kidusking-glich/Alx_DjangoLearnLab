from django.db import models

# Create your models here.
# 1. Author Model (No relationship fields here)

class Author(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField()

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
    books = models.ManyToManyField(Book, related_name='libraries')

    def __str__(self):
        return self.name
    
# 4. Librarian Model (OneToOneField)
# Demonstrates a One-to-One relationship: One Librarian manages exactly one Library, and vice-versa.
class Librarian(models.Model):
    name = models.CharField(max_length=100)

    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name='librarian')
    def __str__ (self):
        return self.name