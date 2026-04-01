"""
Records URL Configuration Module

This module defines URL routing for financial record endpoints.

Endpoints:
    /api/records/ - List/Create records
    /api/records/{id}/ - Retrieve/Update/Delete record
    /api/records/{id}/restore/ - Restore deleted record
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FinancialRecordViewSet

# Create router and register viewset
router = DefaultRouter()
router.register(r'', FinancialRecordViewSet, basename='financial-record')

# URL patterns
urlpatterns = [
    path('', include(router.urls)),
]
