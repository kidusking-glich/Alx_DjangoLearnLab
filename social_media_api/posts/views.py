# posts/views.py

from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework_nested import routers
from rest_framework.decorators import action # Import action

from django.shortcuts import get_object_or_404
from django.db.models import Prefetch

from django.contrib.contenttypes.models import ContentType # Import ContentType
from notifications.models import Notification # Import Notification

from .models import Post, Comment, Like
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


    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        post = generics.get_object_or_404(Post, pk=pk)
        user = request.user
        
        # 1. Create Like
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        
        if not created:
            return Response({"detail": "Post already liked."}, status=status.HTTP_409_CONFLICT)

        # 2. Create Notification (Only if the user isn't liking their own post)
        if post.author != user:
            Notification.objects.create(
                recipient=post.author,
                actor=user,
                verb="liked",
                target=post
            )
        
        return Response({"detail": "Post liked.", "likes_count": post.total_likes}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, pk=None):
        post = generics.get_object_or_404(Post, pk=pk)
        user = request.user
        
        # 1. Delete Like
        deleted_count, _ = Like.objects.filter(user=user, post=post).delete()
        
        if deleted_count == 0:
            return Response({"detail": "Post was not liked by this user."}, status=status.HTTP_404_NOT_FOUND)

        # 2. OPTIONAL: Delete the associated notification (often skipped, but cleaner)
        Notification.objects.filter(
            recipient=post.author,
            actor=user,
            verb="liked",
            content_type=ContentType.objects.get_for_model(Post),
            object_id=post.id
        ).delete()
        
        return Response({"detail": "Post unliked.", "likes_count": post.total_likes}, status=status.HTTP_204_NO_CONTENT)

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


class UserFeedAPIView(generics.ListAPIView):
    """
    Generates a personalized feed of posts from users the current user follows.
    """
    serializer_class = PostSerializer # Use your existing optimized PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Get the IDs of all users the current user follows
        following_users = self.request.user.following.all()
        
        # Get all posts from those users, ordered by creation date
        # 
        queryset = Post.objects.filter(author__in=following_users).order_by('-created_at')
        
        # Apply optimization using select_related and prefetch_related
        return queryset.select_related('author').prefetch_related(
            Prefetch(
                'comments',
                queryset=Comment.objects.select_related('author')
            )
        ).all()



