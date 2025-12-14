# posts/serializers.py

from rest_framework import serializers
from .models import Post, Comment
from .models import Like, Post
from accounts.serializers import CustomUserProfileSerializer # To serialize author data

# 1. Comment Serializer (Detailed)
class CommentSerializer(serializers.ModelSerializer):
    # Read-only field to display the comment author's username
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_username', 'content', 'created_at']
        read_only_fields = ['author', 'post'] # Post and Author are set automatically in the View

# 2. Post Serializer (Detailed)
class PostSerializer(serializers.ModelSerializer):
    # Use the CustomUserProfileSerializer for a detailed author profile
    author = CustomUserProfileSerializer(read_only=True)
    
    # Nested field to display the count and list of comments
    comments = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'author', 'title', 'content', 'image', 
            'created_at', 'updated_at', 'comments', 'comment_count'
        ]
        read_only_fields = ['author'] # Author is set automatically in the View

    def get_comment_count(self, obj):
        # Efficiently get the comment count
        return obj.comments.count()

# 3. Post Creation/Update Serializer (Simplified for input)
class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']


class LikeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'username', 'post', 'created_at']
        read_only_fields = ['user', 'post']

# Update PostSerializer to include like count and status
class PostSerializer(serializers.ModelSerializer):
    # ... (Other fields)
    total_likes = serializers.IntegerField(read_only=True)
    # total_likes must be included in the fields list:
    # fields = ['id', 'author', 'content', 'created_at', 'total_likes', ...]

    # Optional: Check if the requesting user has liked the post
    has_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'created_at', 'total_likes', 'has_liked'] # Add total_likes and has_liked

    def get_has_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            # Check if a Like object exists for this user and this post
            return obj.likes.filter(user=user).exists()
        return False