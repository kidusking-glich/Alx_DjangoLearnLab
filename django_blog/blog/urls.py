from django.urls import path
from django.contrib.auth import views as auth_views # Built-in Auth Views
from . import views
from .views import CommentCreateView, PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, CommentUpdateView, CommentDeleteView, search, PostTagListView
# Set application namespace
app_name = 'blog'

urlpatterns = [
    # --- Blog Post CRUD URLs ---
    path('', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    # path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    # --- Custom Auth Views ---
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    # --- Comment URLs ---
    # Comment Creation (uses a function view, attached to the post PK)
    #path('post/<int:pk>/comment/add/', views.add_comment_to_post, name='add_comment'),
    path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='add_comment'),
    # Comment Editing (uses the comment's PK)
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment_update'),
    # Comment Deletion (uses the comment's PK)
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    # --- Django Built-in Auth Views ---
    # Login uses the default form and logic, but we map it to our custom template
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    
    # Logout uses the default view, but we specify a redirect URL after logout
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'), 
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    # --- New Functionality URLs ---
    path('search/', views.search, name='search'),
    # NEW TAGGING URL:
    path('tags/<slug:tag_slug>/', views.PostTagListView.as_view(), name='posts_by_tag'),

    # Example: Base path for the blog (e.g., list of posts)
    # path('', views.post_list, name='post_list'),
]