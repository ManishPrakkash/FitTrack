"""
Views for the challenges app.
"""
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Challenge, ChallengeParticipant
from .serializers import ChallengeSerializer, ChallengeDetailSerializer, ChallengeParticipantSerializer


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to create or modify challenges.
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to admin users
        return request.user and request.user.is_admin


class ChallengeViewSet(viewsets.ModelViewSet):
    """
    API endpoint for challenges.
    """
    queryset = Challenge.objects.all().order_by('-created_at')
    serializer_class = ChallengeSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    
    def get_serializer_class(self):
        """
        Return appropriate serializer class.
        """
        if self.action == 'retrieve' or self.action == 'list':
            return ChallengeDetailSerializer
        return ChallengeSerializer
    
    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        """
        Join a challenge.
        """
        challenge = self.get_object()
        user = request.user
        
        # Check if the user has already joined the challenge
        if ChallengeParticipant.objects.filter(user=user, challenge=challenge).exists():
            return Response({
                'success': False,
                'message': 'You have already joined this challenge.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create a new participant
        participant = ChallengeParticipant.objects.create(
            user=user,
            challenge=challenge,
            current_progress=0.0
        )
        
        serializer = ChallengeParticipantSerializer(participant)
        
        return Response({
            'success': True,
            'message': 'Successfully joined the challenge.',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'])
    def participants(self, request, pk=None):
        """
        Get all participants of a challenge.
        """
        challenge = self.get_object()
        participants = ChallengeParticipant.objects.filter(challenge=challenge)
        serializer = ChallengeParticipantSerializer(participants, many=True)
        
        return Response({
            'success': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def joined(self, request):
        """
        Get all challenges joined by the current user.
        """
        user = request.user
        joined_challenges = Challenge.objects.filter(participants=user)
        serializer = ChallengeDetailSerializer(joined_challenges, many=True, context={'request': request})
        
        return Response({
            'success': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """
        Get all challenges not joined by the current user.
        """
        user = request.user
        available_challenges = Challenge.objects.exclude(participants=user)
        serializer = ChallengeDetailSerializer(available_challenges, many=True, context={'request': request})
        
        return Response({
            'success': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)
