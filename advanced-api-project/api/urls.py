from django.urls import path
from .views import BookListCreateView, BookRetrieveUpdateDestroyView



from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView, 
    UpdateAPIView, DestroyAPIView
)
from .views import (
    BookListAPIView, BookDetailAPIView, 
    BookCreateAPIView, BookUpdateAPIView, 
    BookDestroyAPIView
)

urlpatterns = [
    # Explicit URL patterns for all operations:
    path('books/', BookListAPIView.as_view(), name='book-list'),
    path('books/create/', BookCreateAPIView.as_view(), name='book-create'),
    path('books/<int:pk>/', BookDetailAPIView.as_view(), name='book-detail'),
    path('books/<int:pk>/update/', BookUpdateAPIView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', BookDestroyAPIView.as_view(), name='book-delete'),
]



# urlpatterns = [
#     # Route for retrieving all books (GET) and creating a new book (POST)
#     # Corresponds to: ListView and CreateView
#     path('books/', BookListCreateView.as_view(), name='book-list-create'),

#     # Route for retrieving, updating, or deleting a single book (GET, PUT, PATCH, DELETE)
#     # The <int:pk> captures the primary key from the URL.
#     # Corresponds to: DetailView, UpdateView, and DeleteView
#     path('books/<int:pk>/', BookRetrieveUpdateDestroyView.as_view(), name='book-detail-rud'),
# ]