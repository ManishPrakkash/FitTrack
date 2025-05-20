"""
Models for the activities app.
"""
from django.db import models
from django.conf import settings
from challenges.models import Challenge, ChallengeParticipant

User = settings.AUTH_USER_MODEL


class Activity(models.Model):
    """
    Model for tracking user activities.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='activities')
    value = models.FloatField(help_text="Activity value in the challenge's unit")
    date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Activities"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.name}'s activity for {self.challenge.name}"
    
    def save(self, *args, **kwargs):
        """
        Override save method to update challenge participant progress.
        """
        super().save(*args, **kwargs)
        
        # Update participant progress
        participant, created = ChallengeParticipant.objects.get_or_create(
            user=self.user,
            challenge=self.challenge,
            defaults={'current_progress': 0.0}
        )
        
        # Add the activity value to the current progress
        participant.current_progress += self.value
        
        # Check if the challenge is completed
        if participant.current_progress >= self.challenge.goal and not participant.completed:
            participant.completed = True
            participant.completed_at = self.created_at
        
        participant.save()
