"""
API views for direct MongoDB authentication.
"""
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
import json
import mongodb_auth

class MongoDBRegisterView(APIView):
    """
    API view for user registration using direct MongoDB.
    """
    permission_classes = [AllowAny]

    def options(self, request):
        """
        Handle OPTIONS requests for CORS preflight.
        """
        response = Response()
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response

    def post(self, request):
        """
        Handle POST requests for user registration.
        """
        try:
            print("MongoDBRegisterView: Received registration request")
            print("Request body:", request.body)

            # Get request data
            data = json.loads(request.body)
            print("Parsed data:", data)

            name = data.get('name', '')
            email = data.get('email', '')
            password = data.get('password', '')  # Don't print password
            username = data.get('username', '')

            print(f"Registration data: name={name}, email={email}, username={username}")

            # Validate data
            if not name:
                print("Validation error: Name is required")
                return Response({
                    'success': False,
                    'error': {'name': ['Name is required']}
                }, status=status.HTTP_400_BAD_REQUEST)

            if not email:
                print("Validation error: Email is required")
                return Response({
                    'success': False,
                    'error': {'email': ['Email is required']}
                }, status=status.HTTP_400_BAD_REQUEST)

            if not password:
                print("Validation error: Password is required")
                return Response({
                    'success': False,
                    'error': {'password': ['Password is required']}
                }, status=status.HTTP_400_BAD_REQUEST)

            # Register user
            print("Calling mongodb_auth.register_user")
            result = mongodb_auth.register_user(name, email, password, username)
            print("Registration result:", result)

            if result['success']:
                print("Registration successful")
                response = Response(result, status=status.HTTP_201_CREATED)
                # Add CORS headers
                response["Access-Control-Allow-Origin"] = "*"
                response["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
                response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
                return response
            else:
                print("Registration failed:", result)
                response = Response(result, status=status.HTTP_400_BAD_REQUEST)
                # Add CORS headers
                response["Access-Control-Allow-Origin"] = "*"
                response["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
                response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
                return response
        except Exception as e:
            print(f"Registration exception: {str(e)}")
            import traceback
            traceback.print_exc()
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MongoDBLoginView(APIView):
    """
    API view for user login using direct MongoDB.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle POST requests for user login.
        """
        try:
            # Get request data
            data = json.loads(request.body)
            email = data.get('email', '')
            password = data.get('password', '')

            # Validate data
            if not email:
                return Response({
                    'success': False,
                    'error': {'email': ['Email is required']}
                }, status=status.HTTP_400_BAD_REQUEST)

            if not password:
                return Response({
                    'success': False,
                    'error': {'password': ['Password is required']}
                }, status=status.HTTP_400_BAD_REQUEST)

            # Login user
            result = mongodb_auth.login_user(email, password)

            if result['success']:
                return Response(result, status=status.HTTP_200_OK)
            else:
                return Response(result, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MongoDBValidateTokenView(APIView):
    """
    API view for token validation using direct MongoDB.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        """
        Handle GET requests for token validation.
        """
        try:
            # Get token from header
            auth_header = request.headers.get('Authorization', '')

            if not auth_header or not auth_header.startswith('Bearer '):
                return Response({
                    'success': False,
                    'message': 'Invalid token'
                }, status=status.HTTP_401_UNAUTHORIZED)

            token = auth_header.split(' ')[1]

            # Get user by token
            user = mongodb_auth.get_user_by_token(token)

            if user:
                return Response({
                    'success': True,
                    'message': 'Token is valid',
                    'user': user
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'message': 'Invalid token'
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
