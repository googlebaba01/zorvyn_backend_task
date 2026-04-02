"""
Dashboard Views Module

API views for dashboard analytics endpoints.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count, Avg, F, ExpressionWrapper, DecimalField, Q, Case, When
from django.db.models.functions import TruncMonth, Coalesce
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal, DivisionByZero

from records.models import FinancialRecord
from .serializers import (
    DashboardSummarySerializer,
    CategoryBreakdownSerializer,
    MonthlyTrendSerializer,
    RecentActivitySerializer,
)


class DashboardSummaryView(APIView):
    """API View for dashboard summary statistics."""
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Retrieve dashboard summary statistics."""
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        record_type = request.query_params.get('record_type')
        
        queryset = FinancialRecord.objects.filter(is_deleted=False)
        
        if request.user.role == 'viewer':
            queryset = queryset.filter(created_by=request.user)
        
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
        if record_type:
            queryset = queryset.filter(record_type=record_type)
        
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
    """API View for category-wise breakdown."""
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Retrieve category-wise breakdown."""
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        record_type = request.query_params.get('record_type')
        
        queryset = FinancialRecord.objects.filter(is_deleted=False)
        
        if request.user.role == 'viewer':
            queryset = queryset.filter(created_by=request.user)
        
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
        if record_type:
            queryset = queryset.filter(record_type=record_type)
        
        category_data = queryset.values('category', 'record_type').annotate(
            total_amount=Sum('amount'),
            record_count=Count('id'),
            average_amount=Avg('amount')
        ).order_by('-total_amount')
        
        total = queryset.aggregate(total=Sum('amount'))['total'] or 0
        
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
    """API View for monthly trend analysis."""
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Retrieve monthly trend data."""
        months_param = request.query_params.get('months', '12')
        try:
            months = int(months_param.rstrip('/'))
        except (ValueError, AttributeError):
            months = 12
        year = request.query_params.get('year')
        
        queryset = FinancialRecord.objects.filter(is_deleted=False)
        
        if request.user.role == 'viewer':
            queryset = queryset.filter(created_by=request.user)
        
        if year:
            queryset = queryset.filter(date__year=year)
        else:
            cutoff_date = timezone.now().date() - timedelta(days=months * 30)
            queryset = queryset.filter(date__gte=cutoff_date)
        
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
    """API View for recent activity feed."""
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Retrieve recent activity feed."""
        limit = int(request.query_params.get('limit', 10))
        
        queryset = FinancialRecord.objects.filter(is_deleted=False)
        
        if request.user.role == 'viewer':
            queryset = queryset.filter(created_by=request.user)
        
        recent_records = queryset.select_related('created_by').order_by('-created_at')[:limit]
        
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
