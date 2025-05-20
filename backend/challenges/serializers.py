"""
Serializers for the challenges app.
"""
from rest_framework import serializers
from .models import Challenge, ChallengeParticipant
from authentication.serializers import UserSerializer


class ChallengeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Challenge model.
    """
    participants = serializers.IntegerField(source='participant_count', read_only=True)
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Challenge
        fields = [
            'id', 'name', 'type', 'description', 'goal', 'unit',
            'participants', 'created_by', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def create(self, validated_data):
        """
        Create and return a new challenge.
        """
        user = self.context['request'].user
        challenge = Challenge.objects.create(created_by=user, **validated_data)
        return challenge


class ChallengeParticipantSerializer(serializers.ModelSerializer):
    """
    Serializer for the ChallengeParticipant model.
    """
    user = UserSerializer(read_only=True)
    challenge = ChallengeSerializer(read_only=True)
    progress_percentage = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = ChallengeParticipant
        fields = [
            'id', 'user', 'challenge', 'current_progress',
            'progress_percentage', 'joined_at', 'completed', 'completed_at'
        ]
        read_only_fields = ['id', 'joined_at', 'completed', 'completed_at']


class ChallengeDetailSerializer(ChallengeSerializer):
    """
    Serializer for detailed challenge information including user's participation.
    """
    is_joined = serializers.SerializerMethodField()
    current_progress = serializers.SerializerMethodField()
    progress_percentage = serializers.SerializerMethodField()
    
    class Meta(ChallengeSerializer.Meta):
        fields = ChallengeSerializer.Meta.fields + ['is_joined', 'current_progress', 'progress_percentage']
    
    def get_is_joined(self, obj):
        """
        Check if the current user has joined the challenge.
        """
        user = self.context['request'].user
        return ChallengeParticipant.objects.filter(user=user, challenge=obj).exists()
    
    def get_current_progress(self, obj):
        """
        Get the current user's progress in the challenge.
        """
        user = self.context['request'].user
        try:
            participant = ChallengeParticipant.objects.get(user=user, challenge=obj)
            return participant.current_progress
        except ChallengeParticipant.DoesNotExist:
            return 0
    
    def get_progress_percentage(self, obj):
        """
        Get the current user's progress percentage in the challenge.
        """
        user = self.context['request'].user
        try:
            participant = ChallengeParticipant.objects.get(user=user, challenge=obj)
            return participant.progress_percentage
        except ChallengeParticipant.DoesNotExist:
            return 0
