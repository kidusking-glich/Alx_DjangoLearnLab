from django.urls import path
from .views import BookListCreateView, BookRetrieveUpdateDestroyView

urlpatterns = [
    # Route for retrieving all books (GET) and creating a new book (POST)
    # Corresponds to: ListView and CreateView
    path('books/', BookListCreateView.as_view(), name='book-list-create'),

    # Route for retrieving, updating, or deleting a single book (GET, PUT, PATCH, DELETE)
    # The <int:pk> captures the primary key from the URL.
    # Corresponds to: DetailView, UpdateView, and DeleteView
    path('books/<int:pk>/', BookRetrieveUpdateDestroyView.as_view(), name='book-detail-rud'),
]