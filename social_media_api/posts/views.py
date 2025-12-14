# posts/views.py

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework_nested import routers

from django.shortcuts import get_object_or_404
from django.db.models import Prefetch

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly # You must create this file/class

# --- Post ViewSet ---
class PostViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for Posts.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    # Optimized QuerySet Implementation
    def get_queryset(self):
        """
        Returns the queryset for the view.
        Uses select_related to join the 'author' and prefetch_related for 'comments'
        to solve the N+1 query problem and optimize performance.
        """
        # 
        return Post.objects.select_related('author').prefetch_related(
            Prefetch(
                'comments',
                queryset=Comment.objects.select_related('author') # Optimizes comment author lookup too
            )
        ).all()
        
    def perform_create(self, serializer):
        # Automatically set the author to the currently logged-in user
        serializer.save(author=self.request.user)

# --- Comment ViewSet ---
class CommentViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for Comments nested under a Post.
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    
    # Retrieves the post ID from the URL (set by the nested router)
    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_pk']).select_related('author')

    def perform_create(self, serializer):
        # 1. Get the parent Post object
        post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        # 2. Automatically set the author and the parent post
        serializer.save(author=self.request.user, post=post)