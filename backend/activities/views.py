"""
Views for the activities app.
"""
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from challenges.models import Challenge, ChallengeParticipant
from .models import Activity
from .serializers import ActivitySerializer, ActivityLogSerializer


class ActivityViewSet(viewsets.ModelViewSet):
    """
    API endpoint for activities.
    """
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Return activities for the current user.
        """
        user = self.request.user
        return Activity.objects.filter(user=user).order_by('-created_at')
    
    @action(detail=False, methods=['post'])
    def log(self, request):
        """
        Log an activity for a challenge.
        """
        serializer = ActivityLogSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            activity = serializer.save()
            
            # Get the updated participant data
            participant = ChallengeParticipant.objects.get(
                user=request.user,
                challenge_id=request.data.get('challenge_id')
            )
            
            # Get the challenge
            challenge = Challenge.objects.get(pk=request.data.get('challenge_id'))
            
            return Response({
                'success': True,
                'message': 'Activity logged successfully.',
                'data': {
                    'activity_id': activity.id,
                    'challenge_id': challenge.id,
                    'challenge_name': challenge.name,
                    'value': activity.value,
                    'current_progress': participant.current_progress,
                    'progress_percentage': participant.progress_percentage,
                    'completed': participant.completed
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'success': False,
            'message': 'Failed to log activity.',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def challenge(self, request):
        """
        Get activities for a specific challenge.
        """
        challenge_id = request.query_params.get('challenge_id')
        
        if not challenge_id:
            return Response({
                'success': False,
                'message': 'Challenge ID is required.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the challenge exists
        challenge = get_object_or_404(Challenge, pk=challenge_id)
        
        # Get activities for the challenge
        activities = Activity.objects.filter(
            user=request.user,
            challenge=challenge
        ).order_by('-created_at')
        
        serializer = ActivitySerializer(activities, many=True)
        
        return Response({
            'success': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)
