from django.db import models
import uuid

class Challenge(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    description = models.TextField()
    goal = models.FloatField()
    unit = models.CharField(max_length=20)
    created_by = models.CharField(max_length=100)  # User ID who created the challenge
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class UserProgress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=100)  # User ID who is tracking progress
    challenge_id = models.CharField(max_length=100)  # Challenge ID
    current_value = models.FloatField(default=0)
    joined_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user_id', 'challenge_id')

    def __str__(self):
        return f"{self.user_id} - {self.challenge_id}"
