# LibraryProject/bookshelf/urls.py

from django.urls import path
from . import views # Imports all view functions from bookshelf/views.py

app_name = 'bookshelf'

urlpatterns = [
    # 1. Secured View (Requires 'bookshelf.can_view' permission)
    path('books/', views.list_books, name='list_books'), 
    
    # 2. Secured Create (Requires 'bookshelf.can_create' permission)
    path('books/create/', views.create_book, name='create_book'),
    
    # 3. Secured Edit (Requires 'bookshelf.can_edit' permission)
    path('books/edit/<int:pk>/', views.edit_book, name='edit_book'),
    
    # 4. Secured Delete (Requires 'bookshelf.can_delete' permission)
    path('books/delete/<int:pk>/', views.delete_book, name='delete_book'),
    
    # Add any other required URLs here (like login, register, etc.)
]