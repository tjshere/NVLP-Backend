from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404, render
from .models import User, Course, Progress, NeuroProfile, Message, PomodoroTimerModel, TaskChunkingModel, TaskStepModel
from .serializers import (
    CourseSerializer,
    ProgressSerializer,
    UserSerializer,
    NeuroProfileSerializer,
    UserCreateSerializer,
    UserLoginSerializer,
    TokenSerializer,
    MessageSerializer,
    PomodoroTimerSerializer,
    TaskChunkingSerializer
)


def home(request):
    """
    Simple function view to render the homepage.
    """
    return render(request, 'core/home.html')


class CourseListView(generics.ListAPIView):
    """
    API view to list all courses.
    GET /api/courses/
    Requires authentication.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]


class CourseDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve course details.
    GET /api/courses/{id}/
    Requires authentication.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]


class ProgressViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Progress model.
    Provides list, create, retrieve, update, and destroy operations.
    All operations require authentication and only operate on data belonging to the authenticated user.
    
    GET /api/progress/ - List all progress records for the authenticated user
    POST /api/progress/ - Create a new progress record for the authenticated user
    GET /api/progress/{id}/ - Retrieve a specific progress record
    PUT /api/progress/{id}/ - Update a specific progress record
    PATCH /api/progress/{id}/ - Partially update a specific progress record
    DELETE /api/progress/{id}/ - Delete a specific progress record
    """
    serializer_class = ProgressSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter progress records to show only those belonging to the authenticated user."""
        return Progress.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Automatically set the user to the authenticated user when creating."""
        serializer.save(user=self.request.user)


class AuthProfileView(APIView):
    """
    API view to fetch and update authenticated user's profile data.
    GET /api/auth/profile/ - Get user profile
    PATCH /api/auth/profile/ - Update user profile (including preferences)
    Requires authentication.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Retrieve the authenticated user's profile including user data and neuro profile.
        """
        user = request.user
        
        # Serialize user data
        user_serializer = UserSerializer(user)
        
        return Response(user_serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request):
        """
        Update the authenticated user's profile.
        Supports updating preferences (stored in NeuroProfile.sensory_preferences).
        """
        user = request.user
        data = request.data
        
        # Handle preferences update
        if 'preferences' in data:
            preferences_data = data['preferences']
            
            # Get or create NeuroProfile for the user
            neuro_profile, created = NeuroProfile.objects.get_or_create(user=user)
            
            # Update sensory preferences
            neuro_profile.sensory_preferences = preferences_data
            neuro_profile.save()
            
            print(f"Updated preferences for {user.email}: {preferences_data}")
        
        # Handle other user fields (first_name, last_name, etc.)
        updateable_fields = ['first_name', 'last_name']
        for field in updateable_fields:
            if field in data:
                setattr(user, field, data[field])
        
        # Save user model if any changes were made
        if any(field in data for field in updateable_fields):
            user.save()
        
        # Return updated user data
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data, status=status.HTTP_200_OK)


# --- Authentication Views ---

class RegisterStudentView(APIView):
    """
    Registers a new student user.
    Hashes the password and saves the user to the database.
    Returns an access token immediately upon successful registration.
    POST /api/auth/register
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        Register a new student user and return JWT access token.
        """
        serializer = UserCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            # Create the user
            user = serializer.save()
            
            # Generate the 'Digital Key' (JWT Token)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            
            print(f"Registered new user: {user.email}")
            
            # Return token response
            token_data = {
                'access_token': access_token,
                'token_type': 'bearer',
                'expires_in_minutes': 30
            }
            
            return Response(
                token_data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginForAccessTokenView(APIView):
    """
    Authenticates the user credentials.
    If successful, generates and returns the JWT access token.
    POST /api/auth/login
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        Authenticate user and return JWT access token.
        """
        serializer = UserLoginSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Generate the 'Digital Key' (JWT Token)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            
            print(f"User logged in: {user.email}")
            
            # Return token response
            token_data = {
                'access_token': access_token,
                'token_type': 'bearer',
                'expires_in_minutes': 30
            }
            
            return Response(
                token_data,
                status=status.HTTP_200_OK
            )
        
        return Response(
            serializer.errors,
            status=status.HTTP_401_UNAUTHORIZED
        )


class ProtectedRouteView(APIView):
    """
    A protected route that requires a valid JWT access token.
    The request.user will contain the authenticated user if successful.
    GET /api/protected
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        A protected route that requires a valid JWT access token.
        Returns welcome message and user data.
        """
        user = request.user
        user_data = {
            'user_id': str(user.id),
            'email': user.email
        }
        
        return Response({
            'message': 'Welcome to the NVLP platform!',
            'user_data': user_data
        }, status=status.HTTP_200_OK)


# --- Message Views ---

class MessageSendView(generics.CreateAPIView):
    """
    API view to send a message.
    POST /api/messages/send/
    Requires authentication.
    The sender field is automatically set to the authenticated user.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        """Automatically set the sender to the authenticated user."""
        serializer.save(sender=self.request.user)


class InboxListView(generics.ListAPIView):
    """
    API view to list messages in the authenticated user's inbox.
    GET /api/messages/inbox/
    Requires authentication.
    Shows only messages where the authenticated user is the recipient.
    Ordered by timestamp (newest first).
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter messages to show only those received by the authenticated user."""
        return Message.objects.filter(recipient=self.request.user).order_by('-timestamp')


class SentListView(generics.ListAPIView):
    """
    API view to list messages sent by the authenticated user.
    GET /api/messages/sent/
    Requires authentication.
    Shows only messages where the authenticated user is the sender.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter messages to show only those sent by the authenticated user."""
        return Message.objects.filter(sender=self.request.user).order_by('-timestamp')


# --- EF Toolkit Views ---

class PomodoroTimerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for PomodoroTimerModel.
    Provides list, create, retrieve, update, and destroy operations.
    All operations require authentication and only operate on data belonging to the authenticated user.
    
    GET /api/pomodoro-timers/ - List all timers for the authenticated user
    POST /api/pomodoro-timers/ - Create a new timer for the authenticated user
    GET /api/pomodoro-timers/{id}/ - Retrieve a specific timer
    PUT /api/pomodoro-timers/{id}/ - Update a specific timer
    PATCH /api/pomodoro-timers/{id}/ - Partially update a specific timer
    DELETE /api/pomodoro-timers/{id}/ - Delete a specific timer
    """
    serializer_class = PomodoroTimerSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter timers to show only those belonging to the authenticated user."""
        return PomodoroTimerModel.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Automatically set the user to the authenticated user when creating."""
        serializer.save(user=self.request.user)


class TaskChunkingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for TaskChunkingModel.
    Provides list, create, retrieve, update, and destroy operations.
    All operations require authentication and only operate on data belonging to the authenticated user.
    Supports nested step creation/updates through the serializer.
    
    GET /api/ef/tasks/ - List all task chunkings for the authenticated user
    POST /api/ef/tasks/ - Create a new task chunking with nested steps
    GET /api/ef/tasks/{id}/ - Retrieve a specific task chunking with its steps
    PUT /api/ef/tasks/{id}/ - Update a task chunking and its steps
    PATCH /api/ef/tasks/{id}/ - Partially update a task chunking
    DELETE /api/ef/tasks/{id}/ - Delete a task chunking (cascades to steps)
    PATCH /api/ef/tasks/{task_id}/update_step/{step_id}/ - Update a specific step's completion status
    """
    serializer_class = TaskChunkingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter task chunkings to show only those belonging to the authenticated user."""
        return TaskChunkingModel.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Automatically set the user to the authenticated user when creating."""
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['patch'], url_path='update_step/(?P<step_id>[^/.]+)')
    def update_step(self, request, pk=None, step_id=None):
        """
        Custom action to update a specific step's completion status.
        This avoids race conditions and is more efficient than fetching/patching the entire task.
        
        PATCH /api/ef/tasks/{task_id}/update_step/{step_id}/
        Body: { "is_step_complete": true/false }
        """
        # Get the task (automatically filtered by user via get_queryset)
        task = self.get_object()
        
        # Get the step and verify it belongs to this task
        try:
            step = TaskStepModel.objects.get(id=step_id, task_chunk=task)
        except TaskStepModel.DoesNotExist:
            return Response(
                {'detail': 'Step not found or does not belong to this task.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Update the step
        is_complete = request.data.get('is_step_complete')
        if is_complete is not None:
            step.is_step_complete = is_complete
            step.save()
            
            # Check if all steps are complete and update task completion status
            all_steps_complete = task.steps.filter(is_step_complete=False).count() == 0
            if all_steps_complete and not task.is_complete:
                task.is_complete = True
                task.save()
            elif not all_steps_complete and task.is_complete:
                task.is_complete = False
                task.save()
            
            # Return updated task with all steps
            serializer = self.get_serializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {'detail': 'is_step_complete field is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
