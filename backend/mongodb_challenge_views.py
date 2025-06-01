"""
MongoDB-based views for challenge management.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authentication import BasicAuthentication
import mongodb_auth


class MongoDBChallengeListView(APIView):
    """
    API view for listing and creating challenges using MongoDB.
    """
    authentication_classes = []  # Disable DRF authentication for MongoDB endpoints
    permission_classes = [AllowAny]

    def get(self, request):
        """
        Get all challenges or user-specific challenges.
        """
        try:
            # Get user ID from token if provided
            user_id = None
            token = request.headers.get('Authorization', '').replace('Bearer ', '')
            if token:
                user_data = mongodb_auth.get_user_by_token(token)
                if user_data:
                    user_id = user_data['id']

            challenge_type = request.GET.get('type', 'all')  # all, joined, available
            
            if user_id and challenge_type in ['joined', 'available']:
                result = mongodb_auth.get_user_challenges(user_id, challenge_type)
            else:
                result = mongodb_auth.get_all_challenges()

            if result['success']:
                return Response({
                    'success': True,
                    'data': result['challenges']
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
        Create a new challenge.
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

            # Extract challenge data
            name = request.data.get('name')
            challenge_type = request.data.get('type')
            description = request.data.get('description')
            goal = request.data.get('goal')
            unit = request.data.get('unit')

            # Validate required fields
            if not all([name, challenge_type, description, goal, unit]):
                return Response({
                    'success': False,
                    'message': 'All fields are required: name, type, description, goal, unit'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Create challenge
            result = mongodb_auth.create_challenge(
                name=name,
                challenge_type=challenge_type,
                description=description,
                goal=goal,
                unit=unit,
                created_by_id=user_data['id']
            )

            if result['success']:
                # Format the response
                challenge = result['challenge']
                # Defensive serialization for all fields
                challenge['id'] = str(challenge.get('_id', ''))
                challenge['created_by'] = str(challenge.get('created_by', ''))
                if 'created_at' in challenge and hasattr(challenge['created_at'], 'isoformat'):
                    challenge['created_at'] = challenge['created_at'].isoformat()
                else:
                    challenge['created_at'] = str(challenge.get('created_at', ''))
                if 'updated_at' in challenge and hasattr(challenge['updated_at'], 'isoformat'):
                    challenge['updated_at'] = challenge['updated_at'].isoformat()
                else:
                    challenge['updated_at'] = str(challenge.get('updated_at', ''))
                challenge['participants'] = 0

                # Remove any non-serializable fields
                challenge.pop('_id', None)

                return Response({
                    'success': True,
                    'data': challenge,
                    'message': result['message']
                }, status=status.HTTP_201_CREATED)
            else:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            import traceback
            return Response({
                'success': False,
                'error': str(e),
                'trace': traceback.format_exc()
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MongoDBChallengeDetailView(APIView):
    """
    API view for retrieving, updating, and deleting specific challenges.
    """
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request, challenge_id):
        """
        Get a specific challenge by ID.
        """
        try:
            result = mongodb_auth.get_challenge_by_id(challenge_id)

            if result['success']:
                return Response({
                    'success': True,
                    'data': result['challenge']
                }, status=status.HTTP_200_OK)
            else:
                return Response(result, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, challenge_id):
        """
        Update a challenge.
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

            # Update challenge
            result = mongodb_auth.update_challenge(
                challenge_id=challenge_id,
                name=request.data.get('name'),
                challenge_type=request.data.get('type'),
                description=request.data.get('description'),
                goal=request.data.get('goal'),
                unit=request.data.get('unit')
            )

            if result['success']:
                return Response(result, status=status.HTTP_200_OK)
            else:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, challenge_id):
        """
        Delete a challenge.
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

            # Delete challenge
            result = mongodb_auth.delete_challenge(challenge_id)

            if result['success']:
                return Response(result, status=status.HTTP_200_OK)
            else:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MongoDBChallengeJoinView(APIView):
    """
    API view for joining challenges.
    """
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, challenge_id):
        """
        Join a challenge.
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

            # Join challenge
            result = mongodb_auth.join_challenge(user_data['id'], challenge_id)

            if result['success']:
                return Response(result, status=status.HTTP_201_CREATED)
            else:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MongoDBChallengeLeaderboardView(APIView):
    """
    API view for challenge leaderboards.
    """
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request, challenge_id):
        """
        Get leaderboard for a challenge.
        """
        try:
            result = mongodb_auth.get_challenge_leaderboard(challenge_id)

            if result['success']:
                return Response({
                    'success': True,
                    'data': result['leaderboard']
                }, status=status.HTTP_200_OK)
            else:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
