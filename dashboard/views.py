"""
Dashboard Views Module

This module contains view classes for dashboard analytics endpoints.

Classes:
    DashboardSummaryView: Overall financial summary
    CategoryBreakdownView: Category-wise breakdown
    MonthlyTrendsView: Monthly trends analysis
    RecentActivityView: Recent transactions feed
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count, Avg, F, ExpressionWrapper, DecimalField, Q, Case, When
from django.db.models.functions import TruncMonth, Coalesce
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal, DivisionByZero
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from records.models import FinancialRecord
from .serializers import (
    DashboardSummarySerializer,
    CategoryBreakdownSerializer,
    MonthlyTrendSerializer,
    RecentActivitySerializer,
)


class DashboardSummaryView(APIView):
    """
    API View for dashboard summary statistics.
    
    Provides high-level financial metrics including total income,
    total expenses, net balance, and record counts.
    
    Endpoint:
        GET /api/dashboard/summary/
    
    Query Parameters:
        - date_from: Filter from date (YYYY-MM-DD)
        - date_to: Filter to date (YYYY-MM-DD)
        - record_type: Filter by 'income' or 'expense'
    
    Returns:
        - total_income: Sum of all income
        - total_expense: Sum of all expenses
        - net_balance: Income - Expense
        - record_count: Total number of records
        - average_income: Average income amount
        - average_expense: Average expense amount
    """
    
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="Get dashboard summary",
        operation_description="Retrieve overall financial summary with totals and averages.",
        manual_parameters=[
            openapi.Parameter(
                'date_from',
                openapi.IN_QUERY,
                description="Filter from date (YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
                format='date'
            ),
            openapi.Parameter(
                'date_to',
                openapi.IN_QUERY,
                description="Filter to date (YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
                format='date'
            ),
            openapi.Parameter(
                'record_type',
                openapi.IN_QUERY,
                description="Filter by type (income/expense)",
                type=openapi.TYPE_STRING,
                enum=['income', 'expense']
            ),
        ],
        responses={
            200: openapi.Response('Dashboard summary', DashboardSummarySerializer),
            401: 'Unauthorized',
        }
    )
    def get(self, request):
        """
        Retrieve dashboard summary statistics.
        
        Args:
            request: HTTP request with optional query parameters
            
        Returns:
            Response: Summary statistics
        """
        # Get query parameters
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        record_type = request.query_params.get('record_type')
        
        # Base queryset - filter based on user role
        queryset = FinancialRecord.objects.filter(is_deleted=False)
        
        # Viewers can only see their own records
        if request.user.role == 'viewer':
            queryset = queryset.filter(created_by=request.user)
        
        # Apply date filters
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
        
        # Apply type filter
        if record_type:
            queryset = queryset.filter(record_type=record_type)
        
        # Calculate aggregates
        income_queryset = queryset.filter(record_type='income')
        expense_queryset = queryset.filter(record_type='expense')
        
        income_data = income_queryset.aggregate(
            total=Coalesce(Sum('amount'), Decimal('0.00')),
            count=Count('id'),
            average=Coalesce(Avg('amount'), Decimal('0.00'))
        )
        
        expense_data = expense_queryset.aggregate(
            total=Coalesce(Sum('amount'), Decimal('0.00')),
            count=Count('id'),
            average=Coalesce(Avg('amount'), Decimal('0.00'))
        )
        
        # Prepare response data
        total_income = income_data['total'] or 0
        total_expense = expense_data['total'] or 0
        
        summary_data = {
            'total_income': total_income,
            'total_expense': total_expense,
            'net_balance': total_income - total_expense,
            'record_count': queryset.count(),
            'income_count': income_data['count'] or 0,
            'expense_count': expense_data['count'] or 0,
            'average_income': income_data['average'] or 0,
            'average_expense': expense_data['average'] or 0,
        }
        
        serializer = DashboardSummarySerializer(summary_data, context={'request': request})
        return Response(serializer.data)


class CategoryBreakdownView(APIView):
    """
    API View for category-wise breakdown.
    
    Provides detailed breakdown of income and expenses by category,
    including totals, counts, and percentages.
    
    Endpoint:
        GET /api/dashboard/category-breakdown/
    
    Query Parameters:
        - date_from: Filter from date
        - date_to: Filter to date
        - record_type: Filter by 'income' or 'expense'
    
    Returns:
        List of categories with:
        - total_amount
        - record_count
        - percentage of total
        - average_amount
    """
    
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="Get category breakdown",
        operation_description="Retrieve category-wise financial breakdown with percentages.",
        manual_parameters=[
            openapi.Parameter(
                'date_from',
                openapi.IN_QUERY,
                description="Filter from date (YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
                format='date'
            ),
            openapi.Parameter(
                'date_to',
                openapi.IN_QUERY,
                description="Filter to date (YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
                format='date'
            ),
            openapi.Parameter(
                'record_type',
                openapi.IN_QUERY,
                description="Filter by type (income/expense)",
                type=openapi.TYPE_STRING,
                enum=['income', 'expense']
            ),
        ],
        responses={
            200: openapi.Response('Category breakdown', CategoryBreakdownSerializer(many=True)),
            401: 'Unauthorized',
        }
    )
    def get(self, request):
        """
        Retrieve category-wise breakdown.
        
        Args:
            request: HTTP request with optional query parameters
            
        Returns:
            Response: Category breakdown list
        """
        # Get query parameters
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        record_type = request.query_params.get('record_type')
        
        # Base queryset
        queryset = FinancialRecord.objects.filter(is_deleted=False)
        
        # Viewers can only see their own records
        if request.user.role == 'viewer':
            queryset = queryset.filter(created_by=request.user)
        
        # Apply filters
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
        if record_type:
            queryset = queryset.filter(record_type=record_type)
        
        # Group by category
        category_data = queryset.values('category', 'record_type').annotate(
            total_amount=Sum('amount'),
            record_count=Count('id'),
            average_amount=Avg('amount')
        ).order_by('-total_amount')
        
        # Calculate total for percentage
        total = queryset.aggregate(total=Sum('amount'))['total'] or 0
        
        # Format response
        result = []
        for item in category_data:
            percentage = (item['total_amount'] / total * 100) if total > 0 else 0
            
            result.append({
                'category': item['category'],
                'category_display': dict(FinancialRecord.CATEGORY_CHOICES).get(item['category']),
                'total_amount': item['total_amount'],
                'record_count': item['record_count'],
                'percentage': round(percentage, 2),
                'record_type': item['record_type'],
                'average_amount': item['average_amount'] or 0,
            })
        
        serializer = CategoryBreakdownSerializer(result, many=True)
        return Response(serializer.data)


class MonthlyTrendsView(APIView):
    """
    API View for monthly trend analysis.
    
    Provides month-by-month breakdown of income and expenses,
    showing trends over time.
    
    Endpoint:
        GET /api/dashboard/monthly-trends/
    
    Query Parameters:
        - months: Number of months to include (default: 12)
        - year: Specific year to analyze
    
    Returns:
        List of months with:
        - income total
        - expense total
        - net (income - expense)
        - savings rate
        - record count
    """
    
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="Get monthly trends",
        operation_description="Retrieve month-by-month financial trends.",
        manual_parameters=[
            openapi.Parameter(
                'months',
                openapi.IN_QUERY,
                description="Number of months to include",
                type=openapi.TYPE_INTEGER,
                default=12
            ),
            openapi.Parameter(
                'year',
                openapi.IN_QUERY,
                description="Specific year to analyze",
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={
            200: openapi.Response('Monthly trends', MonthlyTrendSerializer(many=True)),
            401: 'Unauthorized',
        }
    )
    def get(self, request):
        """
        Retrieve monthly trend data.
        
        Args:
            request: HTTP request with optional query parameters
            
        Returns:
            Response: Monthly trend data
        """
        # Get query parameters
        months_param = request.query_params.get('months', '12')
        # Handle trailing slash or other non-numeric characters
        try:
            months = int(months_param.rstrip('/'))
        except (ValueError, AttributeError):
            months = 12
        year = request.query_params.get('year')
        
        # Base queryset
        queryset = FinancialRecord.objects.filter(is_deleted=False)
        
        # Viewers can only see their own records
        if request.user.role == 'viewer':
            queryset = queryset.filter(created_by=request.user)
        
        # Filter by year if specified
        if year:
            queryset = queryset.filter(date__year=year)
        else:
            # Default to last N months
            cutoff_date = timezone.now().date() - timedelta(days=months * 30)
            queryset = queryset.filter(date__gte=cutoff_date)
        
        # Annotate by month
        monthly_data = queryset.annotate(
            month=TruncMonth('date')
        ).values('month').annotate(
            income=Sum(Case(
                when=Q(record_type='income'), then='amount'
            ), output_field=DecimalField()),
            expense=Sum(Case(
                when=Q(record_type='expense'), then='amount'
            ), output_field=DecimalField()),
            record_count=Count('id')
        ).order_by('month')
        
        # Format response
        result = []
        for item in monthly_data:
            income = item['income'] or Decimal('0.00')
            expense = item['expense'] or Decimal('0.00')
            net = income - expense
            savings_rate = ((income - expense) / income * 100) if income and income > 0 else Decimal('0.00')
            
            result.append({
                'month': item['month'].strftime('%B'),
                'month_number': item['month'].month,
                'year': item['month'].year,
                'income': income,
                'expense': expense,
                'net': net,
                'savings_rate': round(savings_rate, 2),
                'record_count': item['record_count'],
            })
        
        serializer = MonthlyTrendSerializer(result, many=True)
        return Response(serializer.data)


class RecentActivityView(APIView):
    """
    API View for recent activity feed.
    
    Provides a list of most recent transactions for the activity feed.
    
    Endpoint:
        GET /api/dashboard/recent-activity/
    
    Query Parameters:
        - limit: Number of records to return (default: 10)
    
    Returns:
        List of recent transactions with basic details
    """
    
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="Get recent activity",
        operation_description="Retrieve most recent financial transactions.",
        manual_parameters=[
            openapi.Parameter(
                'limit',
                openapi.IN_QUERY,
                description="Number of records to return",
                type=openapi.TYPE_INTEGER,
                default=10
            ),
        ],
        responses={
            200: openapi.Response('Recent activity', RecentActivitySerializer(many=True)),
            401: 'Unauthorized',
        }
    )
    def get(self, request):
        """
        Retrieve recent activity feed.
        
        Args:
            request: HTTP request with optional limit parameter
            
        Returns:
            Response: Recent transactions list
        """
        limit = int(request.query_params.get('limit', 10))
        
        # Base queryset
        queryset = FinancialRecord.objects.filter(is_deleted=False)
        
        # Viewers can only see their own records
        if request.user.role == 'viewer':
            queryset = queryset.filter(created_by=request.user)
        
        # Get recent records
        recent_records = queryset.select_related('created_by').order_by('-created_at')[:limit]
        
        # Format response
        result = []
        for record in recent_records:
            result.append({
                'id': record.id,
                'amount': record.amount,
                'formatted_amount': record.formatted_amount,
                'record_type': record.record_type,
                'category': record.category,
                'category_display': record.get_category_display(),
                'description': record.description,
                'date': record.date,
                'created_by_username': record.created_by.username,
                'created_at': record.created_at,
            })
        
        serializer = RecentActivitySerializer(result, many=True)
        return Response(serializer.data)
