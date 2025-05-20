"""
JWT Authentication for the authentication app.
"""
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()


def generate_token(user_id):
    """
    Generate a JWT token for the given user ID.
    """
    payload = {
        'id': str(user_id),
        'exp': datetime.utcnow() + timedelta(days=7),
        'iat': datetime.utcnow()
    }
    
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    
    return token


class JWTAuthentication(authentication.BaseAuthentication):
    """
    Custom JWT authentication for the API.
    """
    def authenticate(self, request):
        """
        Authenticate the request and return a two-tuple of (user, token).
        """
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return None
            
        try:
            # Get the token
            token = auth_header.split(' ')[1]
            
            # Decode the token
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            
            # Get the user
            user_id = payload['id']
            user = User.objects.get(id=user_id)
            
            return (user, token)
            
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired. Please log in again.')
        except jwt.DecodeError:
            raise AuthenticationFailed('Invalid token. Please log in again.')
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found.')
        
        return None
