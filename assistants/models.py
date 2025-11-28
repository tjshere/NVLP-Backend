from django.db import models
from core.models import User


class AI_Persona(models.Model):
    """
    AI Persona model representing different AI assistant personalities.
    Stores the name, full name (acronym definition), and system prompt.
    """
    name = models.CharField(
        max_length=50,
        unique=True,
        help_text='Short name/identifier for the AI persona (e.g., DANI, LUCAS)'
    )
    
    full_name = models.CharField(
        max_length=200,
        help_text='Full name or acronym definition (e.g., "Discover, Adapt, Nurture & Inspire")'
    )
    
    system_prompt = models.TextField(
        help_text='System prompt that defines the AI persona\'s behavior and personality'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'AI Persona'
        verbose_name_plural = 'AI Personas'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.full_name}"


class ChatMessage(models.Model):
    """
    ChatMessage model representing individual messages in a conversation
    between a User and an AI_Persona.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='chat_messages',
        help_text='The user who sent or received this message'
    )
    
    ai_persona = models.ForeignKey(
        AI_Persona,
        on_delete=models.CASCADE,
        related_name='chat_messages',
        help_text='The AI persona involved in this conversation'
    )
    
    message = models.TextField(
        help_text='The message content'
    )
    
    is_from_bot = models.BooleanField(
        default=False,
        help_text='True if message is from the AI bot, False if from the user'
    )
    
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text='When the message was created'
    )
    
    class Meta:
        ordering = ['timestamp']
        indexes = [
            models.Index(fields=['user', 'ai_persona', 'timestamp']),
        ]
    
    def __str__(self):
        sender = self.ai_persona.name if self.is_from_bot else self.user.username
        return f"{sender}: {self.message[:50]}..."
