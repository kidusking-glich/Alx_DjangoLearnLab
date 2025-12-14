

# posts/urls.py

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import PostViewSet, CommentViewSet, UserFeedAPIView

# 1. Root Router for Posts
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

# 2. Nested Router for Comments (Nested within Posts)
# Routes look like: /posts/{post_pk}/comments/
posts_router = routers.NestedSimpleRouter(router, r'posts', lookup='post')
posts_router.register(r'comments', CommentViewSet, basename='post-comments')

urlpatterns = [
    # Include both routers
    *router.urls,
    *posts_router.urls,
    # Feed Endpoint
    path('feed/', UserFeedAPIView.as_view(), name='user-feed'),
    
    # Explicit URL patterns for liking and unliking posts
    path('<int:pk>/like/', PostViewSet.as_view({'post': 'like'}), name='post-like'),
    path('<int:pk>/unlike/', PostViewSet.as_view({'delete': 'unlike'}), name='post-unlike'),
    
    # Post and Comment URLs
    path('', include(router.urls)),
    path('', include(posts_router.urls)),
    
]
