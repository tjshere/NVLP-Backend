from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404, render
from .models import User, Course, Progress, NeuroProfile, Message
from .serializers import (
    CourseSerializer,
    ProgressSerializer,
    UserSerializer,
    NeuroProfileSerializer,
    UserCreateSerializer,
    UserLoginSerializer,
    TokenSerializer,
    MessageSerializer
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
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve course details.
    GET /api/courses/{id}/
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'pk'


class ProgressView(APIView):
    """
    API view to retrieve progress summary for a user.
    GET /api/progress/{user_id}/
    """
    def get(self, request, user_id):
        """
        Retrieve all progress records for a specific user.
        Returns a list of progress records with course information.
        """
        user = get_object_or_404(User, id=user_id)
        progress_records = Progress.objects.filter(user=user)
        
        # Serialize progress records
        serializer = ProgressSerializer(progress_records, many=True)
        
        # Include course information in the response
        progress_data = []
        for progress in progress_records:
            course_serializer = CourseSerializer(progress.course)
            progress_serializer = ProgressSerializer(progress)
            progress_data.append({
                'course': course_serializer.data,
                'completion_rate': progress.completion_rate,
                'engagement_time': str(progress.engagement_time),
            })
        
        return Response({
            'user_id': user_id,
            'username': user.username,
            'progress': progress_data
        }, status=status.HTTP_200_OK)


class AuthProfileView(APIView):
    """
    API view to fetch authenticated user's profile data.
    GET /api/auth/profile/
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
        
        # Get neuro profile if it exists
        neuro_profile_data = None
        try:
            neuro_profile = user.neuro_profile
            neuro_profile_serializer = NeuroProfileSerializer(neuro_profile)
            neuro_profile_data = neuro_profile_serializer.data
        except NeuroProfile.RelatedObjectDoesNotExist:
            # User doesn't have a neuro profile yet
            # RelatedObjectDoesNotExist is raised for missing OneToOne reverse relations
            neuro_profile_data = None
        
        return Response({
            'user': user_serializer.data,
            'neuro_profile': neuro_profile_data
        }, status=status.HTTP_200_OK)


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
            'email': user.email,
            'username': user.username
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
