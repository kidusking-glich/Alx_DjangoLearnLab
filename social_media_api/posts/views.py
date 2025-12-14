# posts/views.py

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework_nested import routers

from django.shortcuts import get_object_or_404
from django.db.models import Prefetch

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly # (from posts/permissions.py)

# --- Post ViewSet ---
class PostViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for Posts.
    Post.objects.all() is implemented via the optimized get_queryset method below.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    # Post.objects.all() is functionally implemented and optimized here:
    def get_queryset(self):
        """
        Returns the optimized queryset for Posts.
        """
        return Post.objects.select_related('author').prefetch_related(
            Prefetch(
                'comments',
                queryset=Comment.objects.select_related('author') # Optimizes comment author lookup
            )
        ).all()
        
    def perform_create(self, serializer):
        # Automatically set the author to the currently logged-in user
        serializer.save(author=self.request.user)

# --- Comment ViewSet ---
class CommentViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for Comments nested under a Post.
    Comment.objects.all() is implemented via the filtered get_queryset method below.
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    
    # Comment.objects.all() is implemented here, filtered by the parent Post:
    def get_queryset(self):
        """
        Returns the queryset for Comments, filtered by the parent post_pk.
        """
        # filters comments by the ID from the URL and optimizes the author lookup
        return Comment.objects.filter(post_id=self.kwargs['post_pk']).select_related('author')

    def perform_create(self, serializer):
        # 1. Get the parent Post object using the ID from the URL
        post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        # 2. Automatically set the author and the parent post
        serializer.save(author=self.request.user, post=post)