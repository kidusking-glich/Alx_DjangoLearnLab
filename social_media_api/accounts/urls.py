# accounts/urls.py

from django.urls import path
from .views import RegisterUserView, LoginUserView, UserProfileView, TokenRetrievalView
from .views import FollowAPIView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('token/', TokenRetrievalView.as_view(), name='token'),
    path('follow/<int:user_id>/', FollowAPIView.as_view(), name='follow-toggle'),
]
