from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
book

# Expected Output (Will show the string representation of the object)
<Book: "1984" by George Orwell>