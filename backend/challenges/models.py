"""
Models for the challenges app.
"""
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Challenge(models.Model):
    """
    Model for fitness challenges.
    """
    CHALLENGE_TYPES = [
        ('Walking', 'Walking'),
        ('Running', 'Running'),
        ('Cycling', 'Cycling'),
        ('Steps', 'Steps Count'),
        ('Workout', 'Workout Minutes'),
    ]
    
    UNIT_CHOICES = [
        ('km', 'Kilometers'),
        ('miles', 'Miles'),
        ('steps', 'Steps'),
        ('minutes', 'Minutes'),
        ('hours', 'Hours'),
    ]
    
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=50, choices=CHALLENGE_TYPES)
    description = models.TextField()
    goal = models.FloatField(help_text="Target value to achieve")
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_challenges')
    participants = models.ManyToManyField(User, through='ChallengeParticipant', related_name='joined_challenges')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    @property
    def participant_count(self):
        """
        Get the number of participants in the challenge.
        """
        return self.participants.count()


class ChallengeParticipant(models.Model):
    """
    Model for tracking user participation in challenges.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    current_progress = models.FloatField(default=0.0)
    joined_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('user', 'challenge')
    
    def __str__(self):
        return f"{self.user.name} - {self.challenge.name}"
    
    @property
    def progress_percentage(self):
        """
        Calculate the progress percentage.
        """
        if self.challenge.goal <= 0:
            return 0
        return min(round((self.current_progress / self.challenge.goal) * 100), 100)
