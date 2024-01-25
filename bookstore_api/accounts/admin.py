from django.contrib import admin
from accounts.models import CustomUser
from books.models import Book, Author, Category, ShoppingCart, CartItem

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(ShoppingCart)
admin.site.register(CartItem)