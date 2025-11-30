from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from api.models import Book
from api.serializers import BookSerializer 

class BookAPITests(APITestCase):
    """
    Revised comprehensive tests using self.client.login() for authentication.
    """

    def test_list_books_unauthenticated_data_check(self):
        """
        Ensure unauthenticated users retrieve correct list data (ListView).
        """
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # ✅ Data Integrity Check: Compare response data with serialized objects
        expected_data = BookSerializer([self.book1, self.book2], many=True).data
        self.assertEqual(response.data, expected_data)
        
    def test_retrieve_book_detail_unauthenticated_data_check(self):
        """
        Ensure unauthenticated users retrieve correct detail data (DetailView).
        """
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # ✅ Data Integrity Check: Compare response data with serialized object
        expected_data = BookSerializer(self.book1).data
        self.assertEqual(response.data['title'], self.book1.title)
        self.assertEqual(response.data, expected_data)
        
        
## --- 2. POST (CREATE) Tests: Verifying response.data on Success ---

    def test_create_book_authenticated_data_check(self):
        """
        Ensure authenticated users create a book and receive correct 201 response data.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_create_url, self.valid_payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # ✅ Data Integrity Check: Verify key fields are returned and match payload
        self.assertEqual(response.data['title'], self.valid_payload['title'])
        self.assertIn('id', response.data) # Check that the primary key was assigned

    def test_create_book_with_invalid_data_error_message(self):
        """
        Ensure failed POST request returns 400 and clear error messages in response.data.
        """
        self.client.force_authenticate(user=self.user)
        invalid_payload = self.valid_payload.copy()
        invalid_payload['publication_year'] = 999 # Invalid year
        
        response = self.client.post(self.list_create_url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # ✅ Data Integrity Check: Ensure response.data contains validation error messages
        self.assertIn('publication_year', response.data)
        self.assertIsInstance(response.data['publication_year'], list)


## --- 3. PUT (UPDATE) Tests: Verifying response.data reflects changes ---

    def test_update_book_authenticated_data_check(self):
        """
        Ensure authenticated users update a book and receive correct 200 response data.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.detail_url, self.updated_payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # ✅ Data Integrity Check: Verify response data reflects the updated field
        self.assertEqual(response.data['title'], self.updated_payload['title'])
        self.assertEqual(response.data['publication_year'], 2022)

# --- DELETE Tests do not check response.data as they return 204 No Content ---

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