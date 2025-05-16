import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from users.models import User


class JWTAuthentication(authentication.BaseAuthentication):
    """
    Custom JWT authentication for the FitTrack API.
    """
    
    def authenticate(self, request):
        """
        Authenticate the request and return a tuple of (user, token).
        """
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return None
        
        try:
            # Get the token from the Authorization header
            token = auth_header.split(' ')[1]
            payload = jwt.decode(
                token, 
                settings.JWT_SECRET_KEY, 
                algorithms=['HS256']
            )
            
            # Get the user from the payload
            user_id = payload.get('user_id')
            if not user_id:
                raise exceptions.AuthenticationFailed('Invalid token')
            
            user = User.objects.get(id=user_id)
            if not user.is_active:
                raise exceptions.AuthenticationFailed('User is inactive')
            
            return (user, token)
            
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired')
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed('Invalid token')
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found')
        except Exception as e:
            raise exceptions.AuthenticationFailed(f'Authentication failed: {str(e)}')
