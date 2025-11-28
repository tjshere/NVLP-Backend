from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timedelta


def default_timedelta():
    """Default function for DurationField that returns zero timedelta."""
    return timedelta(0)


class User(AbstractUser):
    """
    Custom User model that extends Django's AbstractUser.
    Adds a role field to distinguish between student, educator, and parent.
    """
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('educator', 'Educator'),
        ('parent', 'Parent'),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='student',
        help_text='User role in the platform'
    )
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class NeuroProfile(models.Model):
    """
    NeuroProfile model stores neurodivergent learning preferences and needs.
    One-to-One relationship with User.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='neuro_profile',
        help_text='The user this profile belongs to'
    )
    
    sensory_preferences = models.JSONField(
        default=dict,
        blank=True,
        help_text='JSON field storing sensory preferences (e.g., visual, auditory, kinesthetic)'
    )
    
    learning_style = models.CharField(
        max_length=100,
        blank=True,
        help_text='Preferred learning style'
    )
    
    ef_needs = models.TextField(
        blank=True,
        help_text='Executive function needs and accommodations'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"NeuroProfile for {self.user.username}"


class Course(models.Model):
    """
    Course model stores course information and content metadata.
    """
    title = models.CharField(
        max_length=200,
        help_text='Course title'
    )
    
    description = models.TextField(
        blank=True,
        help_text='Course description'
    )
    
    content_metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text='JSON field storing course content metadata (modules, lessons, resources, etc.)'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title


class Progress(models.Model):
    """
    Progress model tracks user progress through courses.
    Links User to Course and tracks completion and engagement metrics.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='progress_records',
        help_text='The user whose progress is being tracked'
    )
    
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='progress_records',
        help_text='The course being tracked'
    )
    
    completion_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        help_text='Completion rate as a percentage (0.00 to 100.00)'
    )
    
    engagement_time = models.DurationField(
        default=default_timedelta,
        help_text='Total time spent engaging with the course'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'course']
        verbose_name_plural = 'Progress records'
    
    def __str__(self):
        return f"{self.user.username} - {self.course.title} ({self.completion_rate}%)"


class Message(models.Model):
    """
    Message model for user-to-user messaging.
    Stores messages with sender and recipient foreign keys.
    """
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        help_text='The user who sent the message'
    )
    
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages',
        help_text='The user who received the message'
    )
    
    content = models.TextField(
        help_text='The message content'
    )
    
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text='When the message was created'
    )
    
    class Meta:
        ordering = ['-timestamp']  # Newest first
        indexes = [
            models.Index(fields=['recipient', 'timestamp']),
            models.Index(fields=['sender', 'timestamp']),
        ]
    
    def __str__(self):
        return f"From {self.sender.username} to {self.recipient.username}: {self.content[:50]}..."
