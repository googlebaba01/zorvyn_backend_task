"""
URL Configuration for finance_api project.

This module defines the main URL routing for the entire application.
It includes:
- API documentation endpoints (Swagger/Redoc)
- Authentication endpoints (JWT)
- User management routes
- Financial records routes
- Dashboard analytics routes
"""

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from finance_api import views as api_views

# Schema view for Swagger/OpenAPI documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Finance Data Processing API",
        default_version='v1',
        description="Backend API for managing financial data with role-based access control.",
        contact=openapi.Contact(email="admin@example.com"),
        license=openapi.License(name="Assessment Project"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Simple API info endpoint as fallback
def api_info(request):
    """Simple API information endpoint."""
    return JsonResponse({
        'title': 'Finance Data Processing API',
        'version': 'v1',
        'description': 'Backend API for managing financial data with role-based access control.',
        'endpoints': {
            'swagger': '/api/docs/',
            'redoc': '/api/redoc/',
            'openapi_json': '/api/schema.json',
            'health': '/health/',
        }
    })

# API URL patterns
urlpatterns = [
    # Root endpoint (health check and API info)
    path('', api_views.api_root, name='api_root'),
    path('health/', api_views.health_check, name='health_check'),
    path('api-info/', api_info, name='api_info'),
    
    # Admin panel
    path('admin/', admin.site.urls),
    
    # API Documentation - simplified
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/schema.json', schema_view.without_cache('openapi-schema'), name='schema-json'),
    
    # Authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # User management
    path('api/users/', include('users.urls')),
    
    # Financial records
    path('api/records/', include('records.urls')),
    
    # Dashboard analytics
    path('api/dashboard/', include('dashboard.urls')),
]

# Custom error pages - using Django defaults
