from django.test import TestCase
from unittest.mock import patch
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

from books.models import Book, Author, Category, CartItem

User = get_user_model()

class BookAPITestCase(TestCase):
    """
    Test cases for the Book API endpoints.
    """

    def setUp(self):
        """
        Set up initial data for testing.
        """
        self.client = APIClient()
        self.email = 'testuser@gmail.com'
        self.password = 'password'
        self.user = self.create_user()
        self.login()
        
        # Create dummy authors and categories
        self.author = Author.objects.create(name='Test Author')
        self.category = Category.objects.create(name='Test Category')
        
        self.book = Book.objects.create(title='Test Book 1', 
                                        author=self.author, 
                                        published_date='2022-01-01', 
                                        isbn='1034567890012', 
                                        category=self.category, 
                                        price=100.00)

    def create_user(self):
        """
        Create a test user.
        """
        return User.objects.create_user(email=self.email, password=self.password)

    def login(self):
        """
        Log in the test user.
        """
        self.client.login(email=self.email, password=self.password)
    
    # Test cases for creating a book
    def test_create_book(self):
        """
        Test creating a new book.
        """
        data = {
            'title': 'Test Book 2', 
            'author': self.author.id,  # Use the ID of the pre-populated author
            'published_date': '2023-01-01', 
            'isbn': '1234567890123', 
            'category': self.category.id,  # Use the ID of the pre-populated category
            'price': 200.00
        }
        response = self.client.post('/books/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    # Test cases for retrieving book list and detail
    def test_get_book_list(self):
        """
        Test retrieving a list of books.
        """
        self.test_create_book()
        response = self.client.get('/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    def test_get_book_detail(self):
        """
        Test retrieving details of a book.
        """
        response = self.client.get(f'/books/{self.book.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # Test case for updating a book
    def test_update_book(self):
        """
        Test updating details of a book.
        """
        data = {
            'title': 'Updated Book Title', 
            'author': self.author.id,
            'published_date': '2022-01-01', 
            'isbn': '1034567890012', 
            'category': self.category.id, 
            'price': 150.00
        }
        response = self.client.put(f'/books/{self.book.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh the book instance from the database to get the updated data
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, data['title'])
        self.assertEqual(self.book.price, data['price'])
    
    # Test cases for adding, viewing, and removing items from the cart
    def test_add_to_cart(self):
        """
        Test adding a book to the shopping cart.
        """
        response = self.client.post(f'/cart/add/{self.book.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(CartItem.objects.filter(book=self.book, cart__user=self.user).exists())
        self.cart_item = CartItem.objects.get(book=self.book, cart__user=self.user)
        
    def test_view_cart(self):
        """
        Test viewing the shopping cart.
        """
        self.test_add_to_cart()
        response = self.client.get('/cart/view/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['book'], self.book.id)
    
    def test_remove_from_cart(self):
        """
        Test removing a book from the shopping cart.
        """
        self.test_add_to_cart()
        response = self.client.delete(f'/cart/remove/{self.cart_item.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CartItem.objects.filter(book=self.book).exists())
    
    # Test case for purchasing books in the cart
    @patch('books.tasks.send_purchase_notification.delay')
    def test_purchase_books(self, mock_send_purchase_notification):
        """
        Test purchasing books in the shopping cart.
        """
        self.test_add_to_cart()
        response = self.client.post('/cart/purchase/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_send_purchase_notification.assert_called_once_with(self.user.email, [cart_item.id for cart_item in CartItem.objects.all()])
        
    # Test case for deleting a book
    def test_delete_book(self):
        """
        Test deleting a book.
        """
        response = self.client.delete(f'/books/{self.book.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())
