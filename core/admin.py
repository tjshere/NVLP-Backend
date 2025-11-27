from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, NeuroProfile, Course, Progress


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom admin for User model that extends Django's UserAdmin.
    Adds the role field to the admin interface.
    """
    list_display = ['username', 'email', 'role', 'is_staff', 'is_active', 'date_joined']
    list_filter = ['role', 'is_staff', 'is_active', 'date_joined']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('NVLP Information', {'fields': ('role',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('NVLP Information', {'fields': ('role',)}),
    )


@admin.register(NeuroProfile)
class NeuroProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for NeuroProfile model.
    """
    list_display = ['user', 'learning_style', 'created_at', 'updated_at']
    list_filter = ['learning_style', 'created_at']
    search_fields = ['user__username', 'user__email', 'learning_style']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Learning Preferences', {
            'fields': ('sensory_preferences', 'learning_style', 'ef_needs')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Admin interface for Course model.
    """
    list_display = ['title', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Course Information', {
            'fields': ('title', 'description', 'content_metadata')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    """
    Admin interface for Progress model.
    """
    list_display = ['user', 'course', 'completion_rate', 'engagement_time', 'updated_at']
    list_filter = ['completion_rate', 'created_at', 'updated_at']
    search_fields = ['user__username', 'user__email', 'course__title']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Progress Information', {
            'fields': ('user', 'course', 'completion_rate', 'engagement_time')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
