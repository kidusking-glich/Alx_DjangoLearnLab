# api/serializers.py

from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    """
    Serializes the Book model fields (title and author) into JSON format.
    """
    class Meta:
        model = Book
        # '__all__' includes all fields defined in the Book model
        fields = '__all__' 
        # Alternatively, list them explicitly: fields = ['id', 'title', 'author']