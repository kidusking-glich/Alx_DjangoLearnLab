
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser 

from rest_framework import generics
from rest_framework import mixins
# ✅ CRITICAL: Importing the necessary permission classes
from .models import Book
from .serializers import BookSerializer

# --- BookListCreateView (Handles List and Create - ListView & CreateView) ---
class BookListCreateView(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         generics.GenericAPIView):
    """
    Handles: GET (List all books) and POST (Create a new book).
    
    Permissions: IsAuthenticatedOrReadOnly
    * GET requests are allowed for everyone (Read-Only).
    * POST requests (Create) require an authenticated user.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    # Step 4: Applying Permissions
    permission_classes = [IsAuthenticatedOrReadOnly] 
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

# --- BookRetrieveUpdateDestroyView (Handles Detail, Update, and Delete) ---
class BookRetrieveUpdateDestroyView(mixins.RetrieveModelMixin,
                                    mixins.UpdateModelMixin,
                                    mixins.DestroyModelMixin,
                                    generics.GenericAPIView):
    """
    Handles: GET (Retrieve), PUT/PATCH (Update), DELETE (Remove).
    
    Permissions: IsAuthenticatedOrReadOnly
    * GET requests are allowed for everyone (Read-Only).
    * PUT, PATCH, DELETE requests require an authenticated user.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    # Step 4: Applying Permissions
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)






# from django.shortcuts import render
# # api/views.py
# from rest_framework import generics
# from rest_framework import mixins
# from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser

# from api.models import Book
# from .serializers import BookSerializer, AuthorSerializer
# # ... rest of your views code

# # Create your views here.
# # --- BookListCreateView (Handles List and Create - ListView & CreateView) ---
# # Combines ListModelMixin and CreateModelMixin with GenericAPIView
# class BookListCreateView(mixins.ListModelMixin,
#                          mixins.CreateModelMixin,
#                          generics.GenericAPIView):
#     """
#     Handles: GET (List all books) and POST (Create a new book).
#     Permissions: Read-only for unauthenticated users (GET).
#                  Authenticated users only for writing (POST).
#     """
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
    
#     # Step 4: Permissions Setup
#     # Allows GET requests without authentication, but requires authentication for POST, PUT, DELETE.
#     permission_classes = [IsAuthenticatedOrReadOnly] 
    
#     # ListView implementation
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     # CreateView implementation (POST)
#     def post(self, request, *args, **kwargs):
#         # Step 3: Customization - Data validation is handled automatically by the CreateModelMixin 
#         # using the defined serializer_class.
#         return self.create(request, *args, **kwargs)

# # --- BookRetrieveUpdateDestroyView (Handles Detail, Update, and Delete - DetailView, UpdateView, DeleteView) ---
# # Combines RetrieveModelMixin, UpdateModelMixin, and DestroyModelMixin with GenericAPIView
# class BookRetrieveUpdateDestroyView(mixins.RetrieveModelMixin,
#                                     mixins.UpdateModelMixin,
#                                     mixins.DestroyModelMixin,
#                                     generics.GenericAPIView):
#     """
#     Handles: GET (Retrieve single book by ID), PUT/PATCH (Update book), DELETE (Remove book).
#     Permissions: Read-only for unauthenticated users (GET).
#                  Authenticated users only for writing/deletion (PUT/PATCH/DELETE).
#     """
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
    
#     # Step 4: Permissions Setup
#     permission_classes = [IsAuthenticatedOrReadOnly]

#     # DetailView implementation (GET by ID)
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     # UpdateView implementation (PUT/PATCH by ID)
#     def put(self, request, *args, **kwargs):
#         # Step 3: Customization - UpdateModelMixin handles validation and saving.
#         return self.update(request, *args, **kwargs)

#     def patch(self, request, *args, **kwargs):
#         return self.partial_update(request, *args, **kwargs)

#     # DeleteView implementation (DELETE by ID)
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

# # Optional: Using the built-in generic views for even less code (Alternative approach)
# # class BookListCreateAPIView(generics.ListCreateAPIView):
# #     queryset = Book.objects.all()
# #     serializer_class = BookSerializer
# #     permission_classes = [IsAuthenticatedOrReadOnly]
    
# # class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
# #     queryset = Book.objects.all()
# #     serializer_class = BookSerializer
# #     permission_classes = [IsAuthenticatedOrReadOnly]
# permission_classes = [IsAuthenticatedOrReadOnly]