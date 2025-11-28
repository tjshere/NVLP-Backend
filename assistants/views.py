from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.conf import settings
from openai import OpenAI
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
        # Initialize OpenAI client
        if not settings.OPENAI_API_KEY:
            return Response(
                {'error': 'OpenAI API key is not configured'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Get message and persona_name from request
        serializer = ChatMessageSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        message_text = serializer.validated_data['message']
        persona_name = serializer.validated_data['persona_name']
        
        # Fetch the AI_Persona object (DANI or LUCAS)
        ai_persona = get_object_or_404(AI_Persona, name=persona_name)
        
        # Save the User's message to the database
        user_message = ChatMessage.objects.create(
            user=request.user,
            ai_persona=ai_persona,
            message=message_text,
            is_from_bot=False
        )
        
        # Call OpenAI API
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": ai_persona.system_prompt},
                    {"role": "user", "content": message_text}
                ]
            )
            
            # Extract the response content
            bot_response_text = response.choices[0].message.content
            
        except Exception as e:
            # Handle API errors gracefully
            return Response(
                {'error': f'OpenAI API error: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Save the Bot's message to the database
        bot_message = ChatMessage.objects.create(
            user=request.user,
            ai_persona=ai_persona,
            message=bot_response_text,
            is_from_bot=True
        )
        
        # Return the Bot's message as the response
        return Response(
            {
                'message': bot_response_text,
                'persona': ai_persona.name,
                'persona_full_name': ai_persona.full_name,
                'timestamp': bot_message.timestamp
            },
            status=status.HTTP_201_CREATED
        )
