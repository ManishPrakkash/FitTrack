"""
Serializers for the activities app.
"""
from rest_framework import serializers
from .models import Activity
from challenges.models import Challenge, ChallengeParticipant
from challenges.serializers import ChallengeSerializer


class ActivitySerializer(serializers.ModelSerializer):
    """
    Serializer for the Activity model.
    """
    challenge_name = serializers.CharField(source='challenge.name', read_only=True)
    challenge_unit = serializers.CharField(source='challenge.unit', read_only=True)
    
    class Meta:
        model = Activity
        fields = [
            'id', 'challenge', 'challenge_name', 'challenge_unit',
            'value', 'date', 'notes', 'created_at'
        ]
        read_only_fields = ['id', 'date', 'created_at']
    
    def validate(self, data):
        """
        Validate that the user has joined the challenge.
        """
        user = self.context['request'].user
        challenge = data.get('challenge')
        
        if not challenge:
            raise serializers.ValidationError("Challenge is required.")
        
        # Check if the user has joined the challenge
        if not ChallengeParticipant.objects.filter(user=user, challenge=challenge).exists():
            raise serializers.ValidationError("You must join the challenge before logging activities.")
        
        return data
    
    def create(self, validated_data):
        """
        Create and return a new activity.
        """
        user = self.context['request'].user
        activity = Activity.objects.create(user=user, **validated_data)
        return activity


class ActivityLogSerializer(serializers.Serializer):
    """
    Serializer for logging an activity for a challenge.
    """
    challenge_id = serializers.IntegerField()
    value = serializers.FloatField(min_value=0.1)
    notes = serializers.CharField(required=False, allow_blank=True)
    
    def validate_challenge_id(self, value):
        """
        Validate that the challenge exists.
        """
        try:
            challenge = Challenge.objects.get(pk=value)
            return value
        except Challenge.DoesNotExist:
            raise serializers.ValidationError("Challenge not found.")
    
    def validate(self, data):
        """
        Validate that the user has joined the challenge.
        """
        user = self.context['request'].user
        challenge_id = data.get('challenge_id')
        
        # Check if the user has joined the challenge
        if not ChallengeParticipant.objects.filter(user=user, challenge_id=challenge_id).exists():
            raise serializers.ValidationError("You must join the challenge before logging activities.")
        
        return data
    
    def create(self, validated_data):
        """
        Create and return a new activity.
        """
        user = self.context['request'].user
        challenge_id = validated_data.pop('challenge_id')
        challenge = Challenge.objects.get(pk=challenge_id)
        
        activity = Activity.objects.create(
            user=user,
            challenge=challenge,
            **validated_data
        )
        
        return activity
