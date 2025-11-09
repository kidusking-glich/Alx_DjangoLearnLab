

from django.urls import path, include
from django.contrib.auth import views as auth_views # Import Django's auth views
from . import views
from .views import list_books
from .views import LibraryDetailView, register_user

app_name = 'relationship_app'

urlpatterns = [
    # Function-based View (FBV) URL
    # URL: /relationship/books/
    path('books/', views.list_all_books, name='list_books'),
    
    # Class-based View (CBV) URL
    # URL: /relationship/library/1/ (where 1 is the primary key of the Library)
    # The <int:pk> captures the primary key required by the DetailView
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    # --- New Authentication URLs ---
    
    # 1. Registration (Custom FBV)
    path('register/', views.register_user, name='register'),
    
    # 2. Login (Built-in View) - Uses the provided 'login.html' template
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    
    # 3. Logout (Built-in View) - Uses the provided 'logout.html' template
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
]
