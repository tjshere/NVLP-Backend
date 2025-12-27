from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from core.views import AuthProfileView, CourseListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # User profile endpoint
    path('api/auth/profile/', AuthProfileView.as_view(), name='auth-profile'), 
    
    # Courses endpoint
    path('api/courses/', CourseListView.as_view(), name='course-list'),
    
    # Include core URLs for other endpoints (messages, EF toolkit, progress)
    path('api/', include('core.urls')),
    
    # Assistant/chat endpoints
    path('api/', include('assistants.urls')),
]

# Serve static files
if settings.DEBUG and settings.STATICFILES_DIRS:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])