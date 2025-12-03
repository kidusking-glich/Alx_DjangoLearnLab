from django.urls import path
from django.contrib.auth import views as auth_views # Built-in Auth Views
from . import views

# Set application namespace
app_name = 'blog'

urlpatterns = [
    # --- Custom Auth Views ---
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    
    # --- Django Built-in Auth Views ---
    # Login uses the default form and logic, but we map it to our custom template
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    
    # Logout uses the default view, but we specify a redirect URL after logout
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'), 

    # Example: Base path for the blog (e.g., list of posts)
    # path('', views.post_list, name='post_list'),
]