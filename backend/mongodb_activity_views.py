"""
MongoDB-based views for activity management.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
import mongodb_auth


class MongoDBActivityListView(APIView):
    """
    API view for listing and creating activities using MongoDB.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        """
        Get activities for the current user.
        """
        try:
            # Get user ID from token
            token = request.headers.get('Authorization', '').replace('Bearer ', '')
            if not token:
                return Response({
                    'success': False,
                    'message': 'Authentication required'
                }, status=status.HTTP_401_UNAUTHORIZED)

            user_data = mongodb_auth.get_user_by_token(token)
            if not user_data:
                return Response({
                    'success': False,
                    'message': 'Invalid token'
                }, status=status.HTTP_401_UNAUTHORIZED)

            # Get optional challenge filter
            challenge_id = request.GET.get('challenge_id')

            # Get activities
            result = mongodb_auth.get_user_activities(user_data['id'], challenge_id)

            if result['success']:
                return Response({
                    'success': True,
                    'data': result['activities']
                }, status=status.HTTP_200_OK)
            else:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """
        Log a new activity.
        """
        try:
            # Get user ID from token
            token = request.headers.get('Authorization', '').replace('Bearer ', '')
            if not token:
                return Response({
                    'success': False,
                    'message': 'Authentication required'
                }, status=status.HTTP_401_UNAUTHORIZED)

            user_data = mongodb_auth.get_user_by_token(token)
            if not user_data:
                return Response({
                    'success': False,
                    'message': 'Invalid token'
                }, status=status.HTTP_401_UNAUTHORIZED)

            # Extract activity data
            challenge_id = request.data.get('challenge_id')
            value = request.data.get('value')
            notes = request.data.get('notes', '')

            # Validate required fields
            if not challenge_id or value is None:
                return Response({
                    'success': False,
                    'message': 'challenge_id and value are required'
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                value = float(value)
                if value <= 0:
                    raise ValueError("Value must be positive")
            except (ValueError, TypeError):
                return Response({
                    'success': False,
                    'message': 'Value must be a positive number'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Log activity
            result = mongodb_auth.log_activity(
                user_id=user_data['id'],
                challenge_id=challenge_id,
                value=value,
                notes=notes
            )

            if result['success']:
                return Response({
                    'success': True,
                    'message': result['message'],
                    'data': {
                        'new_progress': result['new_progress'],
                        'completed': result['completed']
                    }
                }, status=status.HTTP_201_CREATED)
            else:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MongoDBActivityChallengeView(APIView):
    """
    API view for getting activities for a specific challenge.
    """
    permission_classes = [AllowAny]

    def get(self, request, challenge_id):
        """
        Get activities for a specific challenge.
        """
        try:
            # Get user ID from token
            token = request.headers.get('Authorization', '').replace('Bearer ', '')
            if not token:
                return Response({
                    'success': False,
                    'message': 'Authentication required'
                }, status=status.HTTP_401_UNAUTHORIZED)

            user_data = mongodb_auth.get_user_by_token(token)
            if not user_data:
                return Response({
                    'success': False,
                    'message': 'Invalid token'
                }, status=status.HTTP_401_UNAUTHORIZED)

            # Get activities for the specific challenge
            result = mongodb_auth.get_user_activities(user_data['id'], challenge_id)

            if result['success']:
                return Response({
                    'success': True,
                    'data': result['activities']
                }, status=status.HTTP_200_OK)
            else:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MongoDBActivityLogView(APIView):
    """
    API view for logging activities to a specific challenge.
    """
    permission_classes = [AllowAny]

    def post(self, request, challenge_id):
        """
        Log an activity to a specific challenge.
        """
        try:
            # Get user ID from token
            token = request.headers.get('Authorization', '').replace('Bearer ', '')
            if not token:
                return Response({
                    'success': False,
                    'message': 'Authentication required'
                }, status=status.HTTP_401_UNAUTHORIZED)

            user_data = mongodb_auth.get_user_by_token(token)
            if not user_data:
                return Response({
                    'success': False,
                    'message': 'Invalid token'
                }, status=status.HTTP_401_UNAUTHORIZED)

            # Extract activity data
            value = request.data.get('value')
            notes = request.data.get('notes', '')

            # Validate required fields
            if value is None:
                return Response({
                    'success': False,
                    'message': 'value is required'
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                value = float(value)
                if value <= 0:
                    raise ValueError("Value must be positive")
            except (ValueError, TypeError):
                return Response({
                    'success': False,
                    'message': 'Value must be a positive number'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Log activity
            result = mongodb_auth.log_activity(
                user_id=user_data['id'],
                challenge_id=challenge_id,
                value=value,
                notes=notes
            )

            if result['success']:
                return Response({
                    'success': True,
                    'message': result['message'],
                    'data': {
                        'new_progress': result['new_progress'],
                        'completed': result['completed']
                    }
                }, status=status.HTTP_201_CREATED)
            else:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
