from django.shortcuts import render

# Create your views here.

# api/views.py

from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    """
    API view to list all Book objects.
    - queryset: Tells the view what data to retrieve.
    - serializer_class: Tells the view how to format the data.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer