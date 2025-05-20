"""
Leaderboard views for the challenges app.
"""
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from authentication.serializers import UserSerializer
from .models import Challenge, ChallengeParticipant


class LeaderboardView(APIView):
    """
    API view for challenge leaderboards.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, challenge_id=None):
        """
        Get the leaderboard for a specific challenge.
        """
        if not challenge_id:
            return Response({
                'success': False,
                'message': 'Challenge ID is required.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the challenge exists
        challenge = get_object_or_404(Challenge, pk=challenge_id)
        
        # Get all participants for the challenge
        participants = ChallengeParticipant.objects.filter(
            challenge=challenge
        ).order_by('-current_progress')
        
        # Build leaderboard data
        leaderboard = []
        for index, participant in enumerate(participants):
            user_data = UserSerializer(participant.user).data
            leaderboard.append({
                'rank': index + 1,
                'user': {
                    'id': user_data['id'],
                    'name': user_data['name'],
                    'email': user_data['email'],
                    'avatar_text': user_data['name'][0].upper() if user_data['name'] else '?'
                },
                'score': participant.current_progress,
                'unit': challenge.unit,
                'progress_percentage': participant.progress_percentage,
                'completed': participant.completed,
                'completed_at': participant.completed_at
            })
        
        return Response({
            'success': True,
            'challenge': {
                'id': challenge.id,
                'name': challenge.name,
                'type': challenge.type,
                'goal': challenge.goal,
                'unit': challenge.unit
            },
            'leaderboard': leaderboard
        }, status=status.HTTP_200_OK)
