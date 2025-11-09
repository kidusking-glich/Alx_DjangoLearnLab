# relationship_app/query_samples.py

import os
import sys 

# ADD PROJECT ROOT TO SYS.PATH
# Get the directory of the script and its parent (the project root)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

from django.core.exceptions import ObjectDoesNotExist

# Configure Django settings (MUST be done before importing models)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings') # Replace 'django_models' with your project name
import django
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

print("--- Data Setup ---")
# 1. Create Data
# Authors
author1, created = Author.objects.get_or_create(name="Harper Lee")
author2, created = Author.objects.get_or_create(name="George Orwell")

# Books
book1, created = Book.objects.get_or_create(title="To Kill a Mockingbird", author=author1)
book2, created = Book.objects.get_or_create(title="Go Set a Watchman", author=author1)
book3, created = Book.objects.get_or_create(title="1984", author=author2)
book4, created = Book.objects.get_or_create(title="Animal Farm", author=author2)

# Libraries
library1, created = Library.objects.get_or_create(name="City Central Library")
library2, created = Library.objects.get_or_create(name="University Archives")

# Add Books to Libraries (ManyToMany relationship)
library1.books.add(book1, book3) # City Central has Mockingbird and 1984
library2.books.add(book3, book4, book2) # University Archives has 1984, Animal Farm, and Watchman

# Librarians (OneToOne relationship)
librarian1, created = Librarian.objects.get_or_create(name="Alice Smith", library=library1)
librarian2, created = Librarian.objects.get_or_create(name="Bob Johnson", library=library2)


print("\n--- Sample Queries ---")

# --- Query 1: Query all books by a specific author (ForeignKey/One-to-Many) ---
author_name = "Harper Lee"
try:
    # Use the related_name ('books') on the Author model for reverse lookup
    author = Author.objects.get(name=author_name)
    author_books = Book.objects.filter(author=author)
    #author_books = target_author.books.all()
    print(f"1. Books by **{author_name}**:")
    for book in author_books:
        print(f"   - {book.title}")
except ObjectDoesNotExist:
    print(f"1. Author '{author_name}' not found.")


# --- Query 2: List all books in a library (ManyToMany) ---
library_name = "City Central Library"
try:
    target_library = Library.objects.get(name=library_name)
    # Access the books through the ManyToMany field
    library_books = target_library.books.all()
    print(f"\n2. Books in **{library_name}**:")
    for book in library_books:
        print(f"   - {book.title}")
except ObjectDoesNotExist:
    print(f"2. Library '{library_name}' not found.")


# --- Query 3: Retrieve the librarian for a library (OneToOne) ---
target_library_name = "University Archives"
try:
    target_library = Library.objects.get(name=target_library_name)
    # Access the related Librarian using the related_name ('librarian') on the Library instance
    target_librarian = target_library.librarian
    print(f"\n3. Librarian for **{target_library_name}**:")
    print(f"   - {target_librarian.name}")
except ObjectDoesNotExist:
    print(f"3. Librarian not found for Library '{target_library_name}' (or Library not found).")