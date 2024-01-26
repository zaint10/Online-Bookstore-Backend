"""
URL configuration for bookstore_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from accounts.views import UserRegisterAPIView, UserLoginAPIView, UserLogoutAPIView, CustomObtainAuthToken
from books.views import AuthorListCreate, AuthorRetrieveUpdateDestroy, CategoryListCreate,\
    CategoryRetrieveUpdateDestroy, BookListCreate, BookRetrieveUpdateDestroy,\
    AddToCartAPIView, ViewCartAPIView, RemoveFromCartAPIView, PurchaseBooksAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', UserRegisterAPIView.as_view()),
    path('login/', UserLoginAPIView.as_view()),
    path('api-token-auth/', CustomObtainAuthToken.as_view(), name='api_token_auth'),
    path('logout/', UserLogoutAPIView.as_view()),
    path('authors/', AuthorListCreate.as_view()),
    path('authors/<int:pk>/', AuthorRetrieveUpdateDestroy.as_view()),
    path('categories/', CategoryListCreate.as_view()),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroy.as_view()),
    path('books/', BookListCreate.as_view()),
    path('books/<int:pk>/', BookRetrieveUpdateDestroy.as_view()),
    path('cart/add/<int:book_id>/', AddToCartAPIView.as_view()),
    path('cart/view/', ViewCartAPIView.as_view()),
    path('cart/remove/<int:cart_item_id>/', RemoveFromCartAPIView.as_view()),
    path('cart/purchase/', PurchaseBooksAPIView.as_view()),
]
