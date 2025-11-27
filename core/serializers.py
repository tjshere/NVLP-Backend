from rest_framework import serializers
from .models import User, NeuroProfile, Course, Progress


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    Includes ID, username, email, and role.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']


class NeuroProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for NeuroProfile model.
    Includes sensory_preferences, learning_style, and ef_needs.
    """
    class Meta:
        model = NeuroProfile
        fields = ['sensory_preferences', 'learning_style', 'ef_needs']


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for Course model.
    Includes title, description, and content_metadata.
    """
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'content_metadata']


class ProgressSerializer(serializers.ModelSerializer):
    """
    Serializer for Progress model.
    Includes completion_rate and engagement_time.
    """
    class Meta:
        model = Progress
        fields = ['completion_rate', 'engagement_time']

