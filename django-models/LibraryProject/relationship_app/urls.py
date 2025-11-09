

from django.urls import path, include
from . import views
from .views import LibraryDetailView

app_name = 'relationship_app'

urlpatterns = [
    # Function-based View (FBV) URL
    # URL: /relationship/books/
    path('books/', views.list_all_books, name='list_books'),
    
    # Class-based View (CBV) URL
    # URL: /relationship/library/1/ (where 1 is the primary key of the Library)
    # The <int:pk> captures the primary key required by the DetailView
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]
