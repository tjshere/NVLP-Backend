from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from core.models import User


class EngagementMetric(models.Model):
    """
    EngagementMetric model tracks user engagement metrics.
    Links to User and stores time on task, completion rate, and idle ratio.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='engagement_metrics',
        help_text='The user whose engagement is being tracked'
    )
    
    time_on_task = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0)],
        help_text='Time spent on task in minutes'
    )
    
    completion_rate = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text='Completion rate as a percentage (0.0 to 100.0)'
    )
    
    idle_ratio = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text='Ratio of idle time to active time (0.0 to 1.0)'
    )
    
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text='When this metric was recorded'
    )
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.timestamp.strftime('%Y-%m-%d %H:%M')} (Completion: {self.completion_rate}%)"


class SensoryLog(models.Model):
    """
    SensoryLog model tracks user sensory state and mood.
    Links to User and stores mood score and sensory overload flag.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sensory_logs',
        help_text='The user whose sensory state is being logged'
    )
    
    mood_score = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(-1.0), MaxValueValidator(1.0)],
        help_text='Mood score ranging from -1.0 (negative) to 1.0 (positive)'
    )
    
    sensory_overload_flag = models.BooleanField(
        default=False,
        help_text='True if user is experiencing sensory overload'
    )
    
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text='When this log entry was created'
    )
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
        ]
    
    def __str__(self):
        overload_status = "OVERLOAD" if self.sensory_overload_flag else "OK"
        return f"{self.user.username} - {self.timestamp.strftime('%Y-%m-%d %H:%M')} (Mood: {self.mood_score:.2f}, {overload_status})"


class AdaptiveRule(models.Model):
    """
    AdaptiveRule model defines rules for the adaptive engine.
    Stores rule name, condition description, and action payload (JSON).
    """
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text='Name of the adaptive rule (e.g., "Low Stimulus Trigger")'
    )
    
    condition = models.TextField(
        help_text='Text description of the condition that triggers this rule'
    )
    
    action_payload = models.JSONField(
        default=dict,
        help_text='JSON payload defining what action to take when rule is triggered (e.g., {"mode": "dark"})'
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text='Whether this rule is currently active'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        status = "Active" if self.is_active else "Inactive"
        return f"{self.name} ({status})"
