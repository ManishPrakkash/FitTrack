"""
Models for the fitness app.
"""
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class ActivityType(models.Model):
    """
    Model for different types of fitness activities.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    met_value = models.FloatField(help_text="Metabolic Equivalent of Task value for calorie calculation", default=1.0)
    icon = models.CharField(max_length=50, blank=True, null=True, help_text="Icon identifier for the frontend")
    
    def __str__(self):
        return self.name


class Activity(models.Model):
    """
    Model for tracking user fitness activities.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.ForeignKey(ActivityType, on_delete=models.CASCADE, related_name='activities')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True, help_text="Duration in minutes")
    distance = models.FloatField(blank=True, null=True, help_text="Distance in kilometers")
    calories_burned = models.IntegerField(blank=True, null=True)
    heart_rate_avg = models.IntegerField(blank=True, null=True, help_text="Average heart rate during activity")
    heart_rate_max = models.IntegerField(blank=True, null=True, help_text="Maximum heart rate during activity")
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Activities"
        ordering = ['-date', '-start_time']
    
    def __str__(self):
        return f"{self.user.name}'s {self.activity_type.name} on {self.date}"
    
    def save(self, *args, **kwargs):
        """
        Calculate calories burned if not provided.
        """
        if not self.calories_burned and self.duration:
            # Simple calorie calculation based on MET value, duration, and user weight
            try:
                weight = self.user.profile.weight or 70  # Default to 70kg if weight not provided
                duration_hours = self.duration.total_seconds() / 3600
                self.calories_burned = int(self.activity_type.met_value * weight * duration_hours)
            except:
                pass
        super().save(*args, **kwargs)


class Challenge(models.Model):
    """
    Model for fitness challenges.
    """
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
        ('expert', 'Expert')
    ]
    
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    activity_type = models.ForeignKey(ActivityType, on_delete=models.CASCADE, related_name='challenges')
    start_date = models.DateField()
    end_date = models.DateField()
    goal_value = models.FloatField(help_text="Goal value (e.g., distance in km, duration in minutes)")
    goal_unit = models.CharField(max_length=50, help_text="Unit of measurement (e.g., km, minutes)")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='upcoming')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_challenges')
    participants = models.ManyToManyField(User, through='ChallengeParticipant', related_name='challenges')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title


class ChallengeParticipant(models.Model):
    """
    Model for tracking user participation in challenges.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    current_progress = models.FloatField(default=0.0, help_text="Current progress towards the goal")
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        unique_together = ('user', 'challenge')
    
    def __str__(self):
        return f"{self.user.name} - {self.challenge.title}"
