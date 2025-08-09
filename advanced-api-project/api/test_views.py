from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Book, Author


class BookAPITestCase(TestCase):
    def setUp(self):
        # Initialize the API client
        self.client = APIClient()

        # Create a user for the 'owner' field
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword',
        )

        # Create authors and books associated with the user
        self.author1 = Author.objects.create(name='Test Author 1')
        self.author2 = Author.objects.create(name='Another Author')

        self.book1 = Book.objects.create(
            title='Test Book 1',
            author=self.author1,
            publication_year=2021,
            owner=self.user,
        )
        self.book2 = Book.objects.create(
            title='Second Book',
            author=self.author2,
            publication_year=2022,
            owner=self.user,
        )

        # Authenticate using session to exercise IsAuthenticated in views
        self.client.login(username='testuser', password='testpassword')

    def test_list_books(self):
        # Test listing books with proper authentication
        response = self.client.get('/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_book(self):
        # Test creating a new book
        data = {
            'title': 'New Book',
            'author': self.author1.id,
            'publication_year': 2023,
            'owner': self.user.id,
        }
        response = self.client.post('/books/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_update_book(self):
        # Test updating an existing book
        data = {
            'title': 'Updated Book',
            'author': self.author2.id,
            'publication_year': 2024,
            'owner': self.user.id,
        }
        response = self.client.put(f'/books/{self.book1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Book')

    def test_delete_book(self):
        # Test deleting a book
        response = self.client.delete(f'/books/{self.book1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_filter_books_by_author(self):
        # Test filtering books by author's name using author__name
        response = self.client.get('/books/', {'author__name': 'Test Author 1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Book 1')

    def test_search_books(self):
        # Test searching for books by title or author
        response = self.client.get('/books/', {'search': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should find at least the first book
        titles = [b['title'] for b in response.data]
        self.assertIn('Test Book 1', titles)

    def test_order_books_by_publication_year(self):
        # Test ordering books by publication year
        response = self.client.get('/books/', {'ordering': 'publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Test Book 1')
        self.assertEqual(response.data[1]['title'], 'Second Book')

    def test_unauthorized_access(self):
        # Log out the current user
        self.client.logout()

        # List view allows read-only access (IsAuthenticatedOrReadOnly)
        response = self.client.get('/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Creating requires auth
        response = self.client.post(
            '/books/',
            {
                'title': 'Unauth Book',
                'author': self.author1.id,
                'publication_year': 2020,
                'owner': self.user.id,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
