from rest_framework import serializers
from .models import Challenge, UserProgress

class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = ['id', 'name', 'type', 'description', 'goal', 'unit', 'created_by', 'created_at', 'updated_at']

class UserProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProgress
        fields = ['id', 'user_id', 'challenge_id', 'current_value', 'joined_at', 'last_updated']

class LeaderboardEntrySerializer(serializers.Serializer):
    user_id = serializers.CharField()
    name = serializers.CharField()
    avatar_text = serializers.CharField()
    score = serializers.FloatField()
    unit = serializers.CharField()
