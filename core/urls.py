from django.urls import path
from .views import (
    CourseListView,
    CourseDetailView,
    ProgressView,
    AuthProfileView
)

app_name = 'core'

urlpatterns = [
    # Course endpoints
    path('api/courses/', CourseListView.as_view(), name='course-list'),
    path('api/courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    
    # Progress endpoint
    path('api/progress/<int:user_id>/', ProgressView.as_view(), name='progress'),
    
    # Authentication/profile endpoint
    path('api/auth/profile/', AuthProfileView.as_view(), name='auth-profile'),
]

