from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import User, Course, Progress, NeuroProfile
from .serializers import (
    CourseSerializer,
    ProgressSerializer,
    UserSerializer,
    NeuroProfileSerializer
)


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
        except NeuroProfile.DoesNotExist:
            neuro_profile_data = None
        
        return Response({
            'user': user_serializer.data,
            'neuro_profile': neuro_profile_data
        }, status=status.HTTP_200_OK)
