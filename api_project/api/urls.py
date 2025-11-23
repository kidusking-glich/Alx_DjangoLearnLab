# api/urls.py

from django.db import router
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BookList, BookViewSet
# 1. Initialize the router
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')


urlpatterns = [
    # Maps /api/books/ (when included) to the BookList view
    path('books/', BookList.as_view(), name='book-list'), 
    path('', include(router.urls)), 

]