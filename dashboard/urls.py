"""
Dashboard URL Configuration Module

This module defines URL routing for dashboard analytics endpoints.

Endpoints:
    /api/dashboard/summary/ - Overall financial summary
    /api/dashboard/category-breakdown/ - Category-wise breakdown
    /api/dashboard/monthly-trends/ - Monthly trends
    /api/dashboard/recent-activity/ - Recent transactions
"""

from django.urls import path
from .views import (
    DashboardSummaryView,
    CategoryBreakdownView,
    MonthlyTrendsView,
    RecentActivityView,
)

urlpatterns = [
    path('summary/', DashboardSummaryView.as_view(), name='dashboard-summary'),
    path('category-breakdown/', CategoryBreakdownView.as_view(), name='category-breakdown'),
    path('monthly-trends/', MonthlyTrendsView.as_view(), name='monthly-trends'),
    path('recent-activity/', RecentActivityView.as_view(), name='recent-activity'),
]
