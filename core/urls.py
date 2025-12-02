from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourseListView,
    CourseDetailView,
    ProgressView,
    AuthProfileView,
    RegisterStudentView,
    LoginForAccessTokenView,
    ProtectedRouteView,
    MessageSendView,
    InboxListView,
    SentListView,
    PomodoroTimerViewSet,
    TaskChunkingViewSet
)

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'pomodoro-timers', PomodoroTimerViewSet, basename='pomodoro-timer')
router.register(r'task-chunkings', TaskChunkingViewSet, basename='task-chunking')

app_name = 'core'

urlpatterns = [
    # Course endpoints
    path('api/courses/', CourseListView.as_view(), name='course-list'),
    path('api/courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    
    # Progress endpoint
    path('api/progress/<int:user_id>/', ProgressView.as_view(), name='progress'),
    
    # Authentication endpoints
    path('api/auth/register/', RegisterStudentView.as_view(), name='register-student'),
    path('api/auth/login/', LoginForAccessTokenView.as_view(), name='login'),
    path('api/auth/profile/', AuthProfileView.as_view(), name='auth-profile'),
    path('api/protected/', ProtectedRouteView.as_view(), name='protected-route'),
    
    # Message endpoints
    path('api/messages/send/', MessageSendView.as_view(), name='message-send'),
    path('api/messages/inbox/', InboxListView.as_view(), name='message-inbox'),
    path('api/messages/sent/', SentListView.as_view(), name='message-sent'),
    
    # EF Toolkit endpoints (via router)
    path('api/', include(router.urls)),
]

