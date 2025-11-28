from django.contrib import admin
from .models import EngagementMetric, SensoryLog, AdaptiveRule


@admin.register(EngagementMetric)
class EngagementMetricAdmin(admin.ModelAdmin):
    """
    Admin interface for EngagementMetric model.
    """
    list_display = ['user', 'time_on_task', 'completion_rate', 'idle_ratio', 'timestamp']
    list_filter = ['timestamp', 'completion_rate']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Engagement Metrics', {
            'fields': ('time_on_task', 'completion_rate', 'idle_ratio')
        }),
        ('Timestamp', {
            'fields': ('timestamp',),
            'classes': ('collapse',)
        }),
    )


@admin.register(SensoryLog)
class SensoryLogAdmin(admin.ModelAdmin):
    """
    Admin interface for SensoryLog model.
    """
    list_display = ['user', 'mood_score', 'sensory_overload_flag', 'timestamp']
    list_filter = ['sensory_overload_flag', 'timestamp', 'mood_score']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Sensory State', {
            'fields': ('mood_score', 'sensory_overload_flag')
        }),
        ('Timestamp', {
            'fields': ('timestamp',),
            'classes': ('collapse',)
        }),
    )


@admin.register(AdaptiveRule)
class AdaptiveRuleAdmin(admin.ModelAdmin):
    """
    Admin interface for AdaptiveRule model.
    """
    list_display = ['name', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['name', 'condition']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Rule Information', {
            'fields': ('name', 'is_active')
        }),
        ('Rule Definition', {
            'fields': ('condition', 'action_payload')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
