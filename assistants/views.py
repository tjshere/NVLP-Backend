from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import AI_Persona, ChatMessage
from .serializers import ChatMessageSerializer


class ChatView(APIView):
    """
    API view to handle chat messages with AI personas.
    POST /api/chat/
    Requires authentication.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Handle POST request to send a message to an AI persona.
        
        Expected payload:
        {
            "message": "User's message text",
            "persona_name": "DANI" or "LUCAS"
        }
        
        Returns the bot's response message.
        """
        # Get message and persona_name from request
        serializer = ChatMessageSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        message_text = serializer.validated_data['message']
        persona_name = serializer.validated_data['persona_name']
        
        # Find the correct AI_Persona
        ai_persona = get_object_or_404(AI_Persona, name=persona_name)
        
        # Save the User's message to the database
        user_message = ChatMessage.objects.create(
            user=request.user,
            ai_persona=ai_persona,
            message=message_text,
            is_from_bot=False
        )
        
        # Generate a Dummy Response
        bot_response_text = (
            f"Hello {request.user.username}, I am {ai_persona.name} ({ai_persona.full_name}). "
            f"I received your message: {message_text}"
        )
        
        # Save the Bot's message to the database
        bot_message = ChatMessage.objects.create(
            user=request.user,
            ai_persona=ai_persona,
            message=bot_response_text,
            is_from_bot=True
        )
        
        # Return the Bot's message as the response
        response_serializer = ChatMessageSerializer(bot_message)
        return Response(
            {
                'message': bot_response_text,
                'persona': ai_persona.name,
                'persona_full_name': ai_persona.full_name,
                'timestamp': bot_message.timestamp
            },
            status=status.HTTP_201_CREATED
        )
