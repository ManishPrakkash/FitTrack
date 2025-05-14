from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ChallengeSerializer, UserProgressSerializer, LeaderboardEntrySerializer
from .mongodb_utils import (
    create_challenge, get_all_challenges, get_challenge_by_id, delete_challenge,
    create_or_update_progress, get_user_progress, get_challenge_leaderboard
)

class ChallengeListView(APIView):
    def get(self, request):
        """Get all challenges"""
        challenges = get_all_challenges()
        return Response({
            'success': True,
            'challenges': challenges
        })

    def post(self, request):
        """Create a new challenge"""
        serializer = ChallengeSerializer(data=request.data)
        if serializer.is_valid():
            challenge = create_challenge(
                name=serializer.validated_data['name'],
                type=serializer.validated_data['type'],
                description=serializer.validated_data['description'],
                goal=serializer.validated_data['goal'],
                unit=serializer.validated_data['unit'],
                created_by=serializer.validated_data['created_by']
            )
            if challenge:
                return Response({
                    'success': True,
                    'challenge': challenge
                }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'error': {'message': 'Invalid challenge data'}
        }, status=status.HTTP_400_BAD_REQUEST)

class ChallengeDetailView(APIView):
    def get(self, request, challenge_id):
        """Get a specific challenge"""
        challenge = get_challenge_by_id(challenge_id)
        if challenge:
            return Response({
                'success': True,
                'challenge': challenge
            })
        return Response({
            'success': False,
            'error': {'message': 'Challenge not found'}
        }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, challenge_id):
        """Delete a challenge"""
        result = delete_challenge(challenge_id)
        if result:
            return Response({
                'success': True,
                'message': 'Challenge deleted successfully'
            })
        return Response({
            'success': False,
            'error': {'message': 'Challenge not found'}
        }, status=status.HTTP_404_NOT_FOUND)

class UserProgressView(APIView):
    def get(self, request, user_id):
        """Get progress for a specific user"""
        progress = get_user_progress(user_id)
        return Response({
            'success': True,
            'progress': progress
        })

    def post(self, request):
        """Create or update user progress"""
        serializer = UserProgressSerializer(data=request.data)
        if serializer.is_valid():
            progress = create_or_update_progress(
                user_id=serializer.validated_data['user_id'],
                challenge_id=serializer.validated_data['challenge_id'],
                current_value=serializer.validated_data['current_value']
            )
            if progress:
                return Response({
                    'success': True,
                    'progress': progress
                })
        return Response({
            'success': False,
            'error': {'message': 'Invalid progress data'}
        }, status=status.HTTP_400_BAD_REQUEST)

class LeaderboardView(APIView):
    def get(self, request, challenge_id):
        """Get leaderboard for a specific challenge"""
        leaderboard = get_challenge_leaderboard(challenge_id)
        return Response({
            'success': True,
            'leaderboard': leaderboard
        })
