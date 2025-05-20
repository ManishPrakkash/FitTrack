"""
Views for the authentication app.
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import (
    RegisterSerializer, UserSerializer, LoginSerializer,
    ProfileSerializer, ProfileUpdateSerializer
)
from .models import Profile
from .authentication import generate_token


class RegisterView(APIView):
    """
    API view for user registration.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle POST requests for user registration.
        """
        # Ensure username is provided or use email as username
        if 'username' not in request.data:
            request.data['username'] = request.data.get('email', '').split('@')[0]

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'User registered successfully'
            }, status=status.HTTP_201_CREATED)

        return Response({
            'success': False,
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    API view for user login.
    """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        """
        Handle POST requests for user login.
        """
        username = request.data.get('username', '')
        email = request.data.get('email', '')
        password = request.data.get('password', '')

        # Try to find user by email if email is provided
        if email and not username:
            try:
                user = User.objects.get(email=email)
                username = user.username
            except User.DoesNotExist:
                pass

        # Validate input
        if not username or not password:
            return Response({
                'success': False,
                'message': 'Please provide both username/email and password'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate user
        user = authenticate(username=username, password=password)

        if not user:
            return Response({
                'success': False,
                'message': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)

        # Generate token
        token = generate_token(user.id)

        # Serialize user data
        serializer = UserSerializer(user)

        return Response({
            'success': True,
            'token': token,
            'user': serializer.data
        }, status=status.HTTP_200_OK)


class ValidateTokenView(APIView):
    """
    API view for token validation.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Handle GET requests for token validation.
        """
        return Response({
            'success': True,
            'message': 'Token is valid',
            'user': UserSerializer(request.user).data
        }, status=status.HTTP_200_OK)


class ProfileView(APIView):
    """
    API view for user profile management.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Handle GET requests for user profile.
        """
        profile = request.user.profile
        serializer = ProfileSerializer(profile)

        return Response({
            'success': True,
            'profile': serializer.data
        }, status=status.HTTP_200_OK)

    def put(self, request):
        """
        Handle PUT requests for updating user profile.
        """
        profile = request.user.profile
        serializer = ProfileUpdateSerializer(profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            # Return the updated user with profile
            user_serializer = UserSerializer(request.user)

            return Response({
                'success': True,
                'message': 'Profile updated successfully',
                'user': user_serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            'success': False,
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
