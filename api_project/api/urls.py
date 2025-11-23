# api/urls.py

from django.urls import include, path
from .views import BookList, BookViewSet
from rest_framework.routers import DefaultRouter # Import DefaultRouter


# 1. Initialize the router
router = DefaultRouter()

# 2. Register the ViewSet
# This generates URLs for: list, create, retrieve, update, partial_update, and destroy.
# The base URL will be /api/books_all/ (due to the include in api_project/urls.py)
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    # Maps /api/books/ (when included) to the BookList view
    path('books/', BookList.as_view(), name='book-list'), 
    path('', include(router.urls)),
]