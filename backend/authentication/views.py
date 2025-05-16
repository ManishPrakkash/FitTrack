import jwt
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework import status, views, permissions
from rest_framework.response import Response
from users.models import User
from users.serializers import UserSerializer


class RegisterView(views.APIView):
    """
    API view for user registration.
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        """
        Handle POST requests for user registration.
        """
        serializer = UserSerializer(data=request.data)
        
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


class LoginView(views.APIView):
    """
    API view for user login.
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        """
        Handle POST requests for user login.
        """
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response({
                'success': False,
                'message': 'Please provide both email and password'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({
                'success': False,
                'message': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        if not user.check_password(password):
            return Response({
                'success': False,
                'message': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Generate JWT token
        token_lifetime = settings.JWT_ACCESS_TOKEN_LIFETIME
        payload = {
            'user_id': str(user.id),
            'exp': datetime.utcnow() + token_lifetime,
            'iat': datetime.utcnow()
        }
        
        token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm='HS256')
        
        # Return user data and token
        user_data = UserSerializer(user).data
        
        return Response({
            'success': True,
            'token': token,
            'user': user_data
        }, status=status.HTTP_200_OK)


class ValidateTokenView(views.APIView):
    """
    API view for token validation.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """
        Handle GET requests for token validation.
        """
        return Response({
            'success': True,
            'message': 'Token is valid',
            'user': UserSerializer(request.user).data
        }, status=status.HTTP_200_OK)
