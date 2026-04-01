"""
Dashboard Serializers Module

This module contains serializers for dashboard analytics data.

Classes:
    DashboardSummarySerializer: Overall financial summary
    CategoryBreakdownSerializer: Category-wise breakdown
    MonthlyTrendSerializer: Monthly trends
    RecentActivitySerializer: Recent transactions
"""

from rest_framework import serializers
from decimal import Decimal


class DashboardSummarySerializer(serializers.Serializer):
    """
    Serializer for overall dashboard summary.
    
    Provides high-level financial metrics for the dashboard.
    """
    
    total_income = serializers.DecimalField(
        max_digits=15,
        decimal_places=2,
        help_text="Total income across all records"
    )
    total_expense = serializers.DecimalField(
        max_digits=15,
        decimal_places=2,
        help_text="Total expense across all records"
    )
    net_balance = serializers.DecimalField(
        max_digits=15,
        decimal_places=2,
        help_text="Net balance (income - expense)"
    )
    record_count = serializers.IntegerField(
        help_text="Total number of records"
    )
    income_count = serializers.IntegerField(
        help_text="Number of income records"
    )
    expense_count = serializers.IntegerField(
        help_text="Number of expense records"
    )
    average_income = serializers.DecimalField(
        max_digits=15,
        decimal_places=2,
        help_text="Average income per transaction"
    )
    average_expense = serializers.DecimalField(
        max_digits=15,
        decimal_places=2,
        help_text="Average expense per transaction"
    )
    date_range = serializers.SerializerMethodField(
        help_text="Date range of the data"
    )
    
    def get_date_range(self, obj):
        """Get the date range from context."""
        request = self.context.get('request')
        if request:
            return {
                'from': request.query_params.get('date_from', 'All time'),
                'to': request.query_params.get('date_to', 'Present'),
            }
        return {'from': 'All time', 'to': 'Present'}


class CategoryBreakdownSerializer(serializers.Serializer):
    """
    Serializer for category-wise breakdown.
    
    Shows totals and percentages for each category.
    """
    
    category = serializers.CharField()
    category_display = serializers.CharField()
    total_amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    record_count = serializers.IntegerField()
    percentage = serializers.DecimalField(max_digits=5, decimal_places=2)
    record_type = serializers.CharField()
    average_amount = serializers.DecimalField(max_digits=15, decimal_places=2)


class MonthlyTrendSerializer(serializers.Serializer):
    """
    Serializer for monthly trend data.
    
    Shows income and expense trends over months.
    """
    
    month = serializers.CharField(help_text="Month name")
    month_number = serializers.IntegerField(help_text="Month number (1-12)")
    year = serializers.IntegerField()
    income = serializers.DecimalField(max_digits=15, decimal_places=2)
    expense = serializers.DecimalField(max_digits=15, decimal_places=2)
    net = serializers.DecimalField(max_digits=15, decimal_places=2)
    savings_rate = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Percentage of income saved"
    )
    record_count = serializers.IntegerField()


class RecentActivitySerializer(serializers.Serializer):
    """
    Serializer for recent activity feed.
    
    Shows most recent transactions.
    """
    
    id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    formatted_amount = serializers.CharField()
    record_type = serializers.CharField()
    category = serializers.CharField()
    category_display = serializers.CharField()
    description = serializers.CharField()
    date = serializers.DateField()
    created_by_username = serializers.CharField()
    created_at = serializers.DateTimeField()


class ComparisonSerializer(serializers.Serializer):
    """
    Serializer for period comparison data.
    
    Compares current period with previous period.
    """
    
    current_period = serializers.DictField(
        help_text="Current period statistics"
    )
    previous_period = serializers.DictField(
        help_text="Previous period statistics"
    )
    change_percentage = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Percentage change between periods"
    )
    trend = serializers.CharField(
        help_text="Trend direction: increasing, decreasing, or stable"
    )
