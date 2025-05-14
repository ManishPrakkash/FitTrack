from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserLoginSerializer
from django.contrib.auth.hashers import check_password
from .mongodb_utils import create_user, authenticate_user, get_user_by_email
import json

class RegisterView(APIView):
    def post(self, request):
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')

        # Validate input
        if not name or not email or not password:
            return Response({
                'success': False,
                'error': {'message': 'Name, email, and password are required'}
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check if email already exists
        if get_user_by_email(email):
            return Response({
                'success': False,
                'error': {'message': 'Email already exists'}
            }, status=status.HTTP_400_BAD_REQUEST)

        # Create user in MongoDB
        user = create_user(name, email, password)

        if user:
            return Response({
                'success': True,
                'message': 'User registered successfully'
            }, status=status.HTTP_201_CREATED)

        return Response({
            'success': False,
            'error': {'message': 'Failed to create user'}
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Validate input
        if not email or not password:
            return Response({
                'success': False,
                'message': 'Email and password are required'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate user
        user = authenticate_user(email, password)

        if user:
            return Response({
                'success': True,
                'user': user
            }, status=status.HTTP_200_OK)

        # Check if user exists
        if get_user_by_email(email):
            return Response({
                'success': False,
                'message': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'success': False,
                'message': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)
