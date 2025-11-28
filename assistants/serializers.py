from rest_framework import serializers
from .models import ChatMessage, AI_Persona


class ChatMessageSerializer(serializers.ModelSerializer):
    """
    Serializer for ChatMessage model.
    Includes id, message, is_from_bot, timestamp.
    Also accepts a write-only persona_name field to choose the AI persona.
    """
    persona_name = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Name of the AI persona (e.g., DANI or LUCAS)'
    )
    
    class Meta:
        model = ChatMessage
        fields = ['id', 'message', 'is_from_bot', 'timestamp', 'persona_name']
        read_only_fields = ['id', 'is_from_bot', 'timestamp']
    
    def validate_persona_name(self, value):
        """Validate that the persona_name exists."""
        try:
            AI_Persona.objects.get(name=value.upper())
        except AI_Persona.DoesNotExist:
            raise serializers.ValidationError(
                f"AI persona '{value}' does not exist. Available personas: {', '.join([p.name for p in AI_Persona.objects.all()])}"
            )
        return value.upper()

