# From api/serializers.py
# api/serializers.py

# from rest_framework import serializers # <- Must be present
# from .models import Author, Book # <- Must be present
# # ... (rest of the file)
# books = BookSerializer(many=True, read_only=True)

from rest_framework import serializers
from .models import Book, Author  # Assuming these models are defined in models.py
from datetime import datetime

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'  # Serializes all fields of the Book model

    def validate_publication_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)  # Nested BookSerializer for related books

    class Meta:
        model = Author
        fields = ['name', 'books']
