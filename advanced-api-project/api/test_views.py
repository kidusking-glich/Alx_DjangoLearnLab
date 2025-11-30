from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from api.models import Book # Assuming 'api' is your app name and Book is your model
from api.serializers import BookSerializer # Assuming BookSerializer is defined

# Note: APITestCase automatically uses a separate test database.

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


## --- 1. GET (READ) Tests: Public Access (IsAuthenticatedOrReadOnly) ---

    def test_list_books_unauthenticated(self):
        """
        Ensure unauthenticated users can retrieve the list of books (ListView).
        """
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
    def test_retrieve_book_detail_unauthenticated(self):
        """
        Ensure unauthenticated users can retrieve a single book (DetailView).
        """
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
        
    def test_retrieve_non_existent_book(self):
        """
        Ensure retrieving a non-existent book returns 404.
        """
        response = self.client.get(self.invalid_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


## --- 2. POST (CREATE) Tests: Requires Authentication ---

    def test_create_book_authenticated(self):
        """
        Ensure authenticated users can create a new book (CreateView).
        """
        self.client.force_authenticate(user=self.user)
        initial_book_count = Book.objects.count()
        response = self.client.post(self.list_create_url, self.valid_payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), initial_book_count + 1)
        self.assertEqual(response.data['title'], self.valid_payload['title'])

    def test_create_book_unauthenticated_forbidden(self):
        """
        Ensure unauthenticated users cannot create a new book (Permission check).
        """
        initial_book_count = Book.objects.count()
        response = self.client.post(self.list_create_url, self.valid_payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), initial_book_count)
        
    def test_create_book_with_invalid_data(self):
        """
        Ensure POST request with missing required field fails validation.
        """
        self.client.force_authenticate(user=self.user)
        invalid_payload = self.valid_payload.copy()
        invalid_payload.pop('title') # Remove required field
        
        response = self.client.post(self.list_create_url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data) # Check that the error message relates to 'title'


## --- 3. PUT/PATCH (UPDATE) Tests: Requires Authentication ---

    def test_update_book_authenticated(self):
        """
        Ensure authenticated users can fully update a book (UpdateView - PUT).
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.detail_url, self.updated_payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, self.updated_payload['title'])
        self.assertEqual(self.book1.publication_year, 2022) # Verify update occurred

    def test_partial_update_book_authenticated(self):
        """
        Ensure authenticated users can partially update a book (UpdateView - PATCH).
        """
        self.client.force_authenticate(user=self.user)
        partial_payload = {'title': 'Only the Title Changed'}
        response = self.client.patch(self.detail_url, partial_payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, partial_payload['title'])
        # Ensure other fields are unchanged
        self.assertEqual(self.book1.author, "Test Author")

    def test_update_book_unauthenticated_forbidden(self):
        """
        Ensure unauthenticated users cannot update a book (Permission check).
        """
        response = self.client.put(self.detail_url, self.updated_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Verify no change occurred
        self.book1.refresh_from_db()
        self.assertNotEqual(self.book1.title, self.updated_payload['title'])


## --- 4. DELETE Tests: Requires Authentication ---

    def test_delete_book_authenticated(self):
        """
        Ensure authenticated users can delete a book (DestroyView).
        """
        self.client.force_authenticate(user=self.user)
        initial_book_count = Book.objects.count()
        response = self.client.delete(self.detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), initial_book_count - 1)
        self.assertFalse(Book.objects.filter(pk=self.book1.pk).exists())

    def test_delete_book_unauthenticated_forbidden(self):
        """
        Ensure unauthenticated users cannot delete a book (Permission check).
        """
        initial_book_count = Book.objects.count()
        response = self.client.delete(self.detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), initial_book_count)
        self.assertTrue(Book.objects.filter(pk=self.book1.pk).exists())