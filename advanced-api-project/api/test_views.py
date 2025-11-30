from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase # Used for DRF API testing
from django.contrib.auth.models import User
from api.models import Book 
from api.serializers import BookSerializer 
# Note: A separate test database is automatically configured by APITestCase.

class BookAPITests(APITestCase):
    """
    Comprehensive tests for the Book model's generic API endpoints.
    """
    def setUp(self):
        # 1. Create a non-admin user for authenticated access tests
        self.user = User.objects.create_user(username='tester', password='testpassword')
        
        # 2. Create sample Book instances for detail/list tests
        self.book1 = Book.objects.create(
            title="The Test Book", 
            author="Test Author", 
            isbn="1234567890123", 
            publication_year=2020
        )
        self.book2 = Book.objects.create(
            title="Another Test Title", 
            author="Jane Doe", 
            isbn="0987654321098", 
            publication_year=2021
        )
        
        # 3. Define the URLs for use in tests
        self.list_create_url = reverse('book-list-create') # /api/books/
        self.detail_url = reverse('book-detail-rud', kwargs={'pk': self.book1.pk}) # /api/books/1/
        self.invalid_detail_url = reverse('book-detail-rud', kwargs={'pk': 999})
        
        # 4. Define data payload for creation/update
        self.valid_payload = {
            'title': 'New Sci-Fi Title',
            'author': 'A. Clarke',
            'isbn': '9998887776665',
            'publication_year': 2023
        }
        self.updated_payload = {
            'title': 'Updated Fantasy Title',
            'author': self.book1.author,
            'isbn': self.book1.isbn,
            'publication_year': 2022
        }


## --- 1. GET (READ) Tests: Public Access ---

    def test_list_books_unauthenticated(self):
        """Ensure unauthenticated users can retrieve the list of books (ListView)."""
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
    def test_retrieve_book_detail_unauthenticated(self):
        """Ensure unauthenticated users can retrieve a single book (DetailView)."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


## --- 2. POST (CREATE) Tests: Requires Authentication ---

    def test_create_book_authenticated(self):
        """Ensure authenticated users can create a new book (CreateView)."""
        # Using force_authenticate for DRF API testing
        self.client.force_authenticate(user=self.user) 
        initial_book_count = Book.objects.count()
        response = self.client.post(self.list_create_url, self.valid_payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), initial_book_count + 1)

    def test_create_book_unauthenticated_forbidden(self):
        """Ensure unauthenticated users cannot create a new book (Permission check)."""
        initial_book_count = Book.objects.count()
        response = self.client.post(self.list_create_url, self.valid_payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), initial_book_count)
        
    def test_create_book_with_invalid_data(self):
        """Ensure POST request with missing required field fails validation."""
        self.client.force_authenticate(user=self.user)
        invalid_payload = self.valid_payload.copy()
        invalid_payload.pop('title') 
        
        response = self.client.post(self.list_create_url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


## --- 3. PUT/PATCH (UPDATE) Tests: Requires Authentication ---

    def test_update_book_authenticated(self):
        """Ensure authenticated users can fully update a book (UpdateView - PUT)."""
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.detail_url, self.updated_payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, self.updated_payload['title'])

    def test_update_book_unauthenticated_forbidden(self):
        """Ensure unauthenticated users cannot update a book (Permission check)."""
        response = self.client.put(self.detail_url, self.updated_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


## --- 4. DELETE Tests: Requires Authentication ---

    def test_delete_book_authenticated(self):
        """Ensure authenticated users can delete a book (DestroyView)."""
        self.client.force_authenticate(user=self.user)
        initial_book_count = Book.objects.count()
        response = self.client.delete(self.detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), initial_book_count - 1)

    def test_delete_book_unauthenticated_forbidden(self):
        """Ensure unauthenticated users cannot delete a book (Permission check)."""
        initial_book_count = Book.objects.count()
        response = self.client.delete(self.detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), initial_book_count)