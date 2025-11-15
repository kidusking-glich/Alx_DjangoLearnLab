from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib import messages
from LibraryProject.bookshelf.models import Book
from .forms import ExampleForm

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

--- Views Secured by Permission Decorators ---

# 1. VIEW (Viewing the list requires 'can_view')
# Note: You might use an alternative view for public access, but for enforcing the rule:
@permission_required('bookshelf.can_view', raise_exception=True, login_url='/login/')
def list_books(request):
    """View requires bookshelf.can_view permission."""
    books = Book.objects.all()
    # In a real app, you would render a list template here
    return HttpResponse(f"<h1>Book List</h1><p>You have permission to view {len(books)} books.</p>")


# 2. CREATE (Adding a book requires 'can_create')
@permission_required('bookshelf.can_create', raise_exception=True, login_url='/login/')
def create_book(request):
    """View requires bookshelf.can_create permission."""
    if request.method == 'POST':
        # ... (Handle form submission and creation) ...
        messages.success(request, "Book created.")
        return redirect('bookshelf:list_books')
    
    return HttpResponse("<h1>Create Book</h1><p>You have permission to create books.</p>")


# 3. EDIT (Editing a specific book requires 'can_edit')
@permission_required('bookshelf.can_edit', raise_exception=True, login_url='/login/')
def edit_book(request, pk):
    """View requires bookshelf.can_edit permission."""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        # ... (Handle form submission and update) ...
        messages.success(request, f"Book {book.title} edited.")
        return redirect('bookshelf:list_books')
        
    return HttpResponse(f"<h1>Edit Book: {book.title}</h1><p>You have permission to edit this book.</p>")


# 4. DELETE (Deleting a specific book requires 'can_delete')
@permission_required('bookshelf.can_delete', raise_exception=True, login_url='/login/')
def delete_book(request, pk):
    """View requires bookshelf.can_delete permission."""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        # book.delete()
        messages.success(request, f"Book {book.title} deleted.")
        return redirect('bookshelf:list_books')
        
    return HttpResponse(f"<h1>Delete Book: {book.title}</h1><p>You have permission to delete this book.</p>")


# ...

# --- SECURITY NOTE: PERMISSIONS AND GROUPS ---
# Permissions (can_view, can_create, can_edit, can_delete) are defined 
# in the Book model's Meta class. Access control is enforced using the 
# @permission_required decorator in views.
# 
# Groups are managed via the Django Admin:
# - Viewers: Assigned 'can_view' permission.
# - Editors: Assigned 'can_view', 'can_create', and 'can_edit' permissions.
# - Admins: Assigned all permissions, including 'can_delete'.
# ---------------------------------------------

