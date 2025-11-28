from django.contrib import admin
from .models import AI_Persona, ChatMessage


@admin.register(AI_Persona)
class AI_PersonaAdmin(admin.ModelAdmin):
    """
    Admin interface for AI_Persona model.
    """
    list_display = ['name', 'full_name', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', 'full_name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Persona Information', {
            'fields': ('name', 'full_name', 'system_prompt')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    """
    Admin interface for ChatMessage model.
    """
    list_display = ['user', 'ai_persona', 'is_from_bot', 'timestamp', 'message_preview']
    list_filter = ['ai_persona', 'is_from_bot', 'timestamp']
    search_fields = ['user__username', 'user__email', 'message', 'ai_persona__name']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'
    
    fieldsets = (
        ('Message Information', {
            'fields': ('user', 'ai_persona', 'message', 'is_from_bot', 'timestamp')
        }),
    )
    
    def message_preview(self, obj):
        """Display a preview of the message (first 50 characters)."""
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message Preview'
