# accounts/views.py
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model

from .serializers import UserRegisterSerializer, UserLoginSerializer, UserLogoutSerializer

User = get_user_model()

class UserRegisterAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            
            if User.objects.filter(email__iexact=email).exists():
                return Response({'error': 'User with Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
            
            user = User.objects.create_user(email=email, password=password)
            token, _ = Token.objects.get_or_create(user=user)
            
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            
            user = authenticate(email=email, password=password)
            if user is None:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutAPIView(APIView):
    serializer_class = UserLogoutSerializer
    
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
