from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Author, Category, Book, ShoppingCart, CartItem
from .serializers import AuthorSerializer, CategorySerializer, BookSerializer, CartItemSerializer
from .tasks import send_purchase_notification

class AuthorListCreate(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating authors.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class AuthorRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting authors.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class CategoryListCreate(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class BookListCreate(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class AddToCartAPIView(APIView):
    """
    API endpoint for adding a book to the shopping cart.
    """
    def post(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        cart, _ = ShoppingCart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return Response({'message': 'Book added to cart successfully'}, status=status.HTTP_200_OK)


class ViewCartAPIView(APIView):
    """
    API endpoint for viewing the shopping cart.
    """
    def get(self, request):
        try:
            cart = ShoppingCart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart)
        except ShoppingCart.DoesNotExist:
            cart_items = []
        
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class RemoveFromCartAPIView(APIView):
    """
    API endpoint for removing a book from the shopping cart.
    """
    def delete(self, request, cart_item_id):
        cart_item = get_object_or_404(CartItem, pk=cart_item_id)
        if cart_item.cart.user != request.user:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        
        cart_item.delete()
        return Response({'message': 'Item removed from cart successfully'}, status=status.HTTP_204_NO_CONTENT)


class PurchaseBooksAPIView(APIView):
    """
    API endpoint for purchasing books from the shopping cart.
    """
    def post(self, request):
        try:
            cart = ShoppingCart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart)
        except ShoppingCart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Get primary keys of cart items
        cart_item_ids = list(cart_items.values_list('id', flat=True))
        send_purchase_notification.delay(request.user.email, cart_item_ids)
        return Response({'message': 'Books purchased successfully'}, status=status.HTTP_200_OK)
