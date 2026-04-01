"""
Financial Record Filters Module

This module provides advanced filtering capabilities for financial records.

Classes:
    FinancialRecordFilter: Django Filter class for record filtering
    
Filter Fields:
    - record_type: Filter by income/expense
    - category: Filter by specific category
    - date_from: Start date filter
    - date_to: End date filter
    - amount_min: Minimum amount
    - amount_max: Maximum amount
    - created_by: Filter by user who created
    - is_mine: Filter to show only current user's records
"""

import django_filters
from django.db.models import Q
from django.contrib.auth import get_user_model
from .models import FinancialRecord

User = get_user_model()


class FinancialRecordFilter(django_filters.FilterSet):
    """
    Custom filter set for FinancialRecord model.
    
    Provides comprehensive filtering options for querying financial records.
    Supports date range filtering, category filtering, and custom filters.
    """
    
    # Date range filters
    date_from = django_filters.DateFilter(
        field_name='date',
        lookup_expr='gte',
        label="Start Date",
        help_text="Filter records from this date onwards (inclusive)"
    )
    date_to = django_filters.DateFilter(
        field_name='date',
        lookup_expr='lte',
        label="End Date",
        help_text="Filter records up to this date (inclusive)"
    )
    
    # Amount range filters
    amount_min = django_filters.NumberFilter(
        field_name='amount',
        lookup_expr='gte',
        label="Minimum Amount"
    )
    amount_max = django_filters.NumberFilter(
        field_name='amount',
        lookup_expr='lte',
        label="Maximum Amount"
    )
    
    # Category filter with multiple selection
    category = django_filters.MultipleChoiceFilter(
        field_name='category',
        choices=FinancialRecord.CATEGORY_CHOICES,
        label="Categories",
        help_text="Filter by one or more categories"
    )
    
    # Record type filter
    record_type = django_filters.ChoiceFilter(
        field_name='record_type',
        choices=FinancialRecord.TYPE_CHOICES,
        label="Record Type"
    )
    
    # Created by filter (for admins)
    created_by = django_filters.ModelChoiceFilter(
        field_name='created_by',
        queryset=User.objects.all(),
        label="Created By",
        help_text="Filter by user who created the record"
    )
    
    # Custom filter for user's own records
    is_mine = django_filters.BooleanFilter(
        method='filter_by_current_user',
        label="My Records Only",
        help_text="If true, show only records created by the current user"
    )
    
    # Search filter for description and notes
    search = django_filters.CharFilter(
        method='filter_search',
        label="Search",
        help_text="Search in description and notes fields"
    )
    
    # Exclude soft-deleted by default
    is_deleted = django_filters.BooleanFilter(
        field_name='is_deleted',
        initial=False,
        label="Include Deleted",
        help_text="Set to true to include soft-deleted records"
    )
    
    class Meta:
        model = FinancialRecord
        fields = [
            'record_type',
            'category',
            'date_from',
            'date_to',
            'amount_min',
            'amount_max',
            'created_by',
            'is_mine',
            'search',
        ]
    
    def filter_by_current_user(self, queryset, name, value):
        """
        Filter to show only current user's records.
        
        Args:
            queryset: Base queryset
            name: Filter name
            value: Boolean value
            
        Returns:
            QuerySet: Filtered queryset
        """
        if value:
            request = self.request
            if request and hasattr(request, 'user'):
                return queryset.filter(created_by=request.user)
        return queryset
    
    def filter_search(self, queryset, name, value):
        """
        Search in description and notes fields.
        
        Args:
            queryset: Base queryset
            name: Filter name
            value: Search term
            
        Returns:
            QuerySet: Filtered queryset
        """
        if value:
            return queryset.filter(
                Q(description__icontains=value) |
                Q(notes__icontains=value)
            )
        return queryset
