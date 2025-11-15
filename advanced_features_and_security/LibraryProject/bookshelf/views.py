from django.shortcuts import render
from django.db.models import Q

from LibraryProject.bookshelf.models import Book

# Create your views here.
def secure_search_books(request):
    """
    Securely searches books using the ORM (Prevents SQL Injection).
    """
    query = request.GET.get('q', '')
    
    if query:
        # The Django ORM handles sanitization and parameterization automatically,
        # ensuring the 'query' variable is treated as a safe parameter.
        books = Book.objects.filter(
            Q(title__icontains=query) | Q(author__name__icontains=query)
        )
    else:
        books = Book.objects.all()
        
    return render(request, 'bookshelf/book_list.html', {'books': books, 'query': query})

# --- Example of UNSAFE code to AVOID: ---
# from django.db import connection
# def unsafe_search(request):
#     user_input = request.GET.get('q', '')
#     with connection.cursor() as cursor:
#         # NEVER DO THIS - VULNERABLE TO SQL INJECTION
#         cursor.execute(f"SELECT * FROM bookshelf_book WHERE title = '{user_input}';") 
#         results = cursor.fetchall()
#     return results