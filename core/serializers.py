from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
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
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        """Check if email is already registered."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered.")
        return value

    def create(self, validated_data):
        """Create a new user with hashed password."""
        # Use email as username (or generate a unique username)
        email = validated_data['email']
        username = email.split('@')[0]  # Use email prefix as username
        
        # Ensure username is unique
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=validated_data['password'],
            role='student'  # Students are not admins
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

        if email and password:
            # Find user by email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError(
                    "Incorrect email or password.",
                    code='authorization'
                )
            
            # Authenticate user
            user = authenticate(username=user.username, password=password)
            if not user:
                raise serializers.ValidationError(
                    "Incorrect email or password.",
                    code='authorization'
                )
            
            attrs['user'] = user
        else:
            raise serializers.ValidationError(
                "Must include 'email' and 'password'.",
                code='authorization'
            )

        return attrs


class TokenSerializer(serializers.Serializer):
    """
    Serializer for the token response ('Digital Key').
    Data model for the token response.
    """
    access_token = serializers.CharField()
    token_type = serializers.CharField(default='bearer')
    expires_in_minutes = serializers.IntegerField(default=30)

