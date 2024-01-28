# books/models.py
from django.db import models
from django.contrib.auth import get_user_model

from django.utils import timezone

User = get_user_model()

class Author(models.Model):
    """
    Model representing an author.
    """
    name = models.CharField(max_length=100)
    
    def __str__(self):
        """
        String representation of the author.
        """
        return self.name

class Category(models.Model):
    """
    Model representing a category (genre).
    """
    name = models.CharField(max_length=100)
    
    def __str__(self):
        """
        String representation of the category.
        """
        return self.name

class Book(models.Model):
    """
    Model representing a book.
    """
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        """
        String representation of the book.
        """
        return self.title

class ShoppingCart(models.Model):
    """
    Model representing a shopping cart.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

class CartItem(models.Model):
    """
    Model representing an item in the shopping cart.
    """
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    @property
    def total_cost(self):
        """
        Calculate the total cost of the cart item.
        """
        return self.quantity * self.book.price
