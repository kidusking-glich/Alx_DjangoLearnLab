from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer, PostCreateUpdateSerializer
from .permissions import IsAuthorOrReadOnly

# Create your views here.
# posts/views.py



# 1. Post ViewSet
class PostViewSet(viewsets.ModelViewSet):
    # Apply Filtering (Step 5)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['author__username', 'created_at']
    # Apply Searching (Step 5)
    search_fields = ['title', 'content'] 

    # Permissions: Only authenticated users can access. IsAuthorOrReadOnly applies for PUT/DELETE
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    # Customize the queryset
    def get_queryset(self):
        # Select related author data to avoid N+1 queries for author info
        return Post.objects.select_related('author').prefetch_related('comments')

    # Use different serializers for different actions
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PostCreateUpdateSerializer
        return PostSerializer

    # Logic to automatically set the author upon creation
    def perform_create(self, serializer):
        # The author is the current authenticated user
        serializer.save(author=self.request.user)


# 2. Comment ViewSet (Nested within a Post)
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    # Custom queryset to fetch comments only for a specific post
    def get_queryset(self):
        # We expect 'post_pk' (Post Primary Key) to be passed in the URL (router setup handles this)
        post_pk = self.kwargs.get('post_pk')
        if post_pk:
            # Select related author data to avoid N+1 queries for author info
            return Comment.objects.filter(post_id=post_pk).select_related('author')
        
        # If no post_pk is provided, return all comments (optional, but standard practice)
        return Comment.objects.all().select_related('author')

    # Logic to automatically set the post and author upon creation
    def perform_create(self, serializer):
        post_pk = self.kwargs.get('post_pk')
        post = Post.objects.get(pk=post_pk)

        # Set the author to the current user and the post to the retrieved post
        serializer.save(author=self.request.user, post=post)