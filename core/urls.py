from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    # Authentication views
    RegisterStudentView,
    LoginForAccessTokenView,
    # Core platform views
    CourseListView,
    CourseDetailView,
    AuthProfileView,
    # Messaging views
    MessageSendView,
    InboxListView,
    SentListView,
    # EF Toolkit viewsets
    PomodoroTimerViewSet,
    TaskChunkingViewSet
)

app_name = 'core'

# Create router and register ViewSets
router = DefaultRouter()
router.register(r'ef/timer', PomodoroTimerViewSet, basename='pomodoro-timer')
router.register(r'ef/tasks', TaskChunkingViewSet, basename='task-chunking')

urlpatterns = [
    # --- Authentication Endpoints ---
    path('auth/register/', RegisterStudentView.as_view(), name='register'),
    path('auth/login/', LoginForAccessTokenView.as_view(), name='login'),
    
    # --- Core Platform Endpoints (Courses & Profile) ---
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('user/profile/', AuthProfileView.as_view(), name='user-profile'),
    
    # --- Messaging Endpoints ---
    path('messages/send/', MessageSendView.as_view(), name='message-send'),
    path('messages/inbox/', InboxListView.as_view(), name='message-inbox'),
    path('messages/sent/', SentListView.as_view(), name='message-sent'),
    
    # --- Include ViewSet routes from router ---
    path('', include(router.urls)),
]
