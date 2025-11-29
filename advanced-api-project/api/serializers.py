# From api/serializers.py
# api/serializers.py

from rest_framework import serializers # <- Must be present
from .models import Author, Book # <- Must be present
# ... (rest of the file)
books = BookSerializer(many=True, read_only=True)