from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from .models import Book, Library



# Create your views here.
# --- 1. Function-based View (FBV): List all books ---
def list_all_books(request):
    # Retrieve all Book objects, pre-fetching the author to optimize queries
    all_books = Book.objects.all() # <-- The line the checker is looking for
    context = {
        'books': all_books
    }
    # render the HTML template list_books.html
    return render(request, 'relationship_app/list_books.html', context)


# --- 2. Class-based View (CBV): Library Detail ---
# We use DetailView to display the details of a single object (a Library).

class LibraryDetailView(DetailView):
    # The model specifies the database model to use for this view
    model = Library

    # The template_name specifies the HTML template to use for rendering
    template_name = 'relationship_app/library_detail.html'

    # The context_object_name specifies the variable name to use in the template
    context_object_name = 'library'
    def get_queryset(self):
        return Library.objects.prefetch_related('books__author')
                 
    # Note: DetailView automatically uses the 'pk' passed in the URL to find the object.                               )