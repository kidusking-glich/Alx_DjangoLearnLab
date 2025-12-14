# posts/serializers.py

from rest_framework import serializers
from .models import Post, Comment
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