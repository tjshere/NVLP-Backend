from django.urls import path
from .views import (
    CourseListView,
    CourseDetailView,
    ProgressView,
    AuthProfileView,
    RegisterStudentView,
    LoginForAccessTokenView,
    ProtectedRouteView
)

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
]

