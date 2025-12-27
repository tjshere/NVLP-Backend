from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User, NeuroProfile, Course, Progress, Message, PomodoroTimerModel, TaskChunkingModel, TaskStepModel


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    Includes ID, email, role, and preferences from NeuroProfile.
    """
    preferences = serializers.SerializerMethodField()
    first_name = serializers.CharField(required=False, allow_blank=True, default='')
    last_name = serializers.CharField(required=False, allow_blank=True, default='')
    username = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'first_name', 'last_name', 'username', 'is_active', 'preferences']
    
    def get_preferences(self, obj):
        """Get preferences from NeuroProfile or return default preferences."""
        try:
            neuro_profile = obj.neuro_profile
            return neuro_profile.sensory_preferences or {
                'dark_mode': False,
                'low_audio': False,
                'reduce_animations': False,
            }
        except NeuroProfile.DoesNotExist:
            return {
                'dark_mode': False,
                'low_audio': False,
                'reduce_animations': False,
            }
    
    def get_username(self, obj):
        """Generate a display name from first_name, last_name, or email."""
        if hasattr(obj, 'first_name') and hasattr(obj, 'last_name') and obj.first_name and obj.last_name:
            return f"{obj.first_name} {obj.last_name}"
        elif hasattr(obj, 'first_name') and obj.first_name:
            return obj.first_name
        else:
            # Return the part before @ in the email
            return obj.email.split('@')[0].replace('.', ' ').title()


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
    Includes nested course details for reads and write-only course ID for updates.
    """
    # Add a nested serializer for read operations
    course_detail = CourseSerializer(source='course', read_only=True)
    
    # Add a write-only PrimaryKey field for creating/linking a new Progress record to a Course ID
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), write_only=True)

    class Meta:
        model = Progress
        fields = ['id', 'course', 'course_detail', 'completion_rate', 'engagement_time', 'updated_at']
        read_only_fields = ['id', 'course_detail', 'updated_at']


# --- Authentication Serializers ---

class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration request.
    Data model for user registration request.
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        min_length=8,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate_email(self, value):
        """Check if email is already registered."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered.")
        return value

    def create(self, validated_data):
        """Create a new user with hashed password."""
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            role='student'
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login request.
    Data model for user login request.
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        """Validate user credentials."""
        email = attrs.get('email')
        password = attrs.get('password')

        # Authenticate user using email and password
        # Django's authenticate() will use USERNAME_FIELD='email' from the User model
        user = authenticate(request=None, username=email, password=password)
        
        if not user:
            raise serializers.ValidationError("Invalid credentials provided.")
        
        attrs['user'] = user
        return attrs


class TokenSerializer(serializers.Serializer):
    """
    Serializer for the token response ('Digital Key').
    Data model for the token response.
    """
    access_token = serializers.CharField()
    token_type = serializers.CharField(default='bearer')
    expires_in_minutes = serializers.IntegerField(default=30)


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message model.
    Includes sender_email, recipient_email, content, and timestamp.
    The sender field is automatically set to the authenticated user and is read-only.
    The recipient field is write-only for message creation.
    """
    sender_email = serializers.CharField(source='sender.email', read_only=True)
    recipient_email = serializers.CharField(source='recipient.email', read_only=True)
    recipient = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        help_text='The recipient user ID (write-only)'
    )
    
    class Meta:
        model = Message
        fields = ['id', 'sender_email', 'recipient_email', 'recipient', 'content', 'timestamp']
        read_only_fields = ['timestamp']


# --- EF Toolkit Serializers ---

class TaskStepSerializer(serializers.ModelSerializer):
    """
    Serializer for TaskStepModel.
    Basic serializer for individual task steps.
    """
    class Meta:
        model = TaskStepModel
        fields = ['id', 'step_description', 'is_step_complete', 'order']
        read_only_fields = ['id']


class TaskChunkingSerializer(serializers.ModelSerializer):
    """
    Serializer for TaskChunkingModel.
    Includes nested TaskStepSerializer as a writable field (steps) to allow
    creating/updating steps when the main task is handled.
    """
    steps = TaskStepSerializer(many=True, required=False)
    
    class Meta:
        model = TaskChunkingModel
        fields = ['id', 'main_task_title', 'is_complete', 'created_at', 'steps']
        read_only_fields = ['id', 'created_at']
    
    def create(self, validated_data):
        """Create TaskChunkingModel with nested steps."""
        steps_data = validated_data.pop('steps', [])
        task_chunk = TaskChunkingModel.objects.create(**validated_data)
        
        for step_data in steps_data:
            TaskStepModel.objects.create(task_chunk=task_chunk, **step_data)
        
        return task_chunk
    
    def update(self, instance, validated_data):
        """Update TaskChunkingModel and handle nested steps."""
        steps_data = validated_data.pop('steps', None)
        
        # Update main task fields
        instance.main_task_title = validated_data.get('main_task_title', instance.main_task_title)
        instance.is_complete = validated_data.get('is_complete', instance.is_complete)
        instance.save()
        
        # Handle steps update if provided
        if steps_data is not None:
            # Delete existing steps
            instance.steps.all().delete()
            
            # Create new steps
            for step_data in steps_data:
                TaskStepModel.objects.create(task_chunk=instance, **step_data)
        
        return instance


class PomodoroTimerSerializer(serializers.ModelSerializer):
    """
    Serializer for PomodoroTimerModel.
    Basic serializer for Pomodoro timer settings and state.
    """
    class Meta:
        model = PomodoroTimerModel
        fields = [
            'id', 'work_duration', 'break_duration', 'long_break_duration',
            'cycles_to_long_break', 'current_status', 'session_start_time',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

