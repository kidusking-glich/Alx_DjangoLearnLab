# posts/urls.py

from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import PostViewSet, CommentViewSet

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
    *posts_router.urls
]