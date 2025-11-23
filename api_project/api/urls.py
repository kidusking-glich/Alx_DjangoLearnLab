# api/urls.py

from django.urls import path
from .views import BookList

urlpatterns = [
    # Maps /api/books/ (when included) to the BookList view
    path('books/', BookList.as_view(), name='book-list'), 
]