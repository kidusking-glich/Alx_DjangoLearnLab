from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from api.models import Book 

class BookAPITests(APITestCase):
    """
    Revised comprehensive tests using self.client.login() for authentication.
    """
    def setUp(self):
        # 1. Create a user
        self.user = User.objects.create_user(username='tester', password='testpassword')
        
        # 2. Create sample Book instances
        self.book1 = Book.objects.create(
            title="The Test Book", 
            author="Test Author", 
            isbn="1234567890123", 
            publication_year=2020
        )
        # Credentials for login
        self.credentials = {
            'username': 'tester',
            'password': 'testpassword'
        }
        
        # 3. Define the URLs
        self.list_create_url = reverse('book-list-create')
        self.detail_url = reverse('book-detail-rud', kwargs={'pk': self.book1.pk})
        
        # 4. Define data payload for update
        self.updated_payload = {
            'title': 'Updated Title After Login',
            'author': self.book1.author,
            'isbn': self.book1.isbn,
            'publication_year': 2022
        }


## --- Test Cases Requiring Authentication ---

    def test_create_book_authenticated_via_login(self):
        """
        Ensure users logged in via session can create a new book (POST).
        """
        # ✅ Using self.client.login() as required
        login_success = self.client.login(**self.credentials)
        self.assertTrue(login_success)

        initial_book_count = Book.objects.count()
        response = self.client.post(self.list_create_url, self.updated_payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), initial_book_count + 1)
        # Optional: Log out after test if needed for session cleanup, though APITestCase often handles this.
        self.client.logout()

    def test_update_book_authenticated_via_login(self):
        """
        Ensure users logged in via session can update a book (PUT).
        """
        # ✅ Using self.client.login() as required
        self.client.login(**self.credentials)
        
        response = self.client.put(self.detail_url, self.updated_payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, self.updated_payload['title'])
        self.client.logout()

    def test_delete_book_authenticated_via_login(self):
        """
        Ensure users logged in via session can delete a book (DELETE).
        """
        # ✅ Using self.client.login() as required
        self.client.login(**self.credentials)
        
        initial_book_count = Book.objects.count()
        response = self.client.delete(self.detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), initial_book_count - 1)
        self.client.logout()

# --- Unauthenticated tests (GET and unauthorized POST/PUT/DELETE) remain unchanged ---

    def test_create_book_unauthenticated_forbidden(self):
        """
        Ensure unauthenticated users cannot create a new book (Permission check).
        """
        initial_book_count = Book.objects.count()
        # No login before the POST request
        response = self.client.post(self.list_create_url, self.updated_payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), initial_book_count)