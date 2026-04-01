"""
User URL Configuration Module

This module defines URL routing for user management endpoints.

Endpoints:
    /api/users/ - List/Create users
    /api/users/{id}/ - Retrieve/Update/Delete user
    /api/users/{id}/status/ - Update user status
    /api/users/{id}/change-password/ - Change password
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

# Create router and register viewset
router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')

# URL patterns
urlpatterns = [
    path('', include(router.urls)),
]
