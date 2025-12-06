from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    CommentCreateView, 
    PostListView, 
    PostDetailView, 
    PostCreateView, 
    PostUpdateView, 
    PostDeleteView, 
    CommentUpdateView, 
    CommentDeleteView, 
    search, 
    PostTagListView
)

# Set application namespace
app_name = 'blog'

urlpatterns = [
    # --- 1. Blog Post CRUD URLs ---
    #path('tags/<slug:tag_slug>/', views.PostTagListView.as_view(), name='posts_by_tag'),

    path('', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    
    # Post Update (Uses the '/update/' structure)
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    
    # --- 2. Advanced Features (Search/Tagging) ---
    path('search/', views.search, name='search'),
    path('tags/<slug:tag_slug>/', views.PostTagListView.as_view(), name='posts_by_tag'), # Cleaned up duplicate
    
    # --- 3. Comment URLs ---
    path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='add_comment'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    
    # --- 4. User Authentication Views ---
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    
    # Built-in Auth Views
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'), 
    # CORRECT MAPPING:
    path('tags/<slug:tag_slug>/', views.PostByTagListView.as_view(), name='posts_by_tag'),

]