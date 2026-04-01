"""
Financial Record Serializers Module

This module handles serialization/deserialization of FinancialRecord data.

Classes:
    FinancialRecordSerializer: Main serializer for CRUD operations
    FinancialRecordListSerializer: Optimized for listing
    FinancialRecordCreateUpdateSerializer: For create/update with validation
    CategoryBreakdownSerializer: For category-wise summaries
    MonthlyTrendSerializer: For monthly trend data
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import FinancialRecord

User = get_user_model()


class FinancialRecordSerializer(serializers.ModelSerializer):
    """
    Main serializer for FinancialRecord model.
    
    Provides comprehensive field access and validation.
    Includes computed fields for better frontend integration.
    """
    
    # Computed fields (read-only)
    formatted_amount = serializers.CharField(read_only=True)
    effect_amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        read_only=True,
        help_text="Signed amount: positive for income, negative for expense"
    )
    created_by_username = serializers.CharField(
        source='created_by.username',
        read_only=True
    )
    category_display = serializers.CharField(
        source='get_category_display',
        read_only=True
    )
    type_display = serializers.CharField(
        source='get_record_type_display',
        read_only=True
    )
    
    class Meta:
        model = FinancialRecord
        fields = [
            'id',
            'amount',
            'record_type',
            'category',
            'date',
            'description',
            'notes',
            'created_by',
            'created_by_username',
            'formatted_amount',
            'effect_amount',
            'category_display',
            'type_display',
            'is_deleted',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'created_by',
            'created_by_username',
            'formatted_amount',
            'effect_amount',
            'category_display',
            'type_display',
            'is_deleted',
            'created_at',
            'updated_at',
        ]
    
    def validate_amount(self, value):
        """
        Validate that amount is positive.
        
        Args:
            value (Decimal): Amount to validate
            
        Returns:
            Decimal: Validated amount
            
        Raises:
            serializers.ValidationError: If amount is negative or zero
        """
        if value <= 0:
            raise serializers.ValidationError(
                "Amount must be greater than zero"
            )
        if value > 999999999999.99:
            raise serializers.ValidationError(
                "Amount exceeds maximum allowed value"
            )
        return value
    
    def validate_date(self, value):
        """
        Validate that date is not in the future.
        
        Args:
            value (Date): Date to validate
            
        Returns:
            Date: Validated date
            
        Raises:
            serializers.ValidationError: If date is in the future
        """
        if value > timezone.now().date():
            raise serializers.ValidationError(
                "Transaction date cannot be in the future"
            )
        return value
    
    def validate(self, attrs):
        """
        Validate record type and category combination.
        
        Ensures that income categories are used with income type
        and expense categories with expense type.
        
        Args:
            attrs (dict): All attributes
            
        Returns:
            dict: Validated attributes
        """
        record_type = attrs.get('record_type')
        category = attrs.get('category')
        
        if record_type and category:
            # Define income and expense categories
            income_categories = [
                'salary', 'freelance', 'investment', 
                'business', 'rental', 'other_income'
            ]
            expense_categories = [
                'food', 'transport', 'utilities', 'rent',
                'healthcare', 'entertainment', 'shopping',
                'education', 'travel', 'insurance',
                'maintenance', 'taxes', 'other_expense'
            ]
            
            # Check consistency
            if record_type == 'income' and category in expense_categories:
                raise serializers.ValidationError(
                    f"Category '{category}' is an expense category. "
                    "Please use 'expense' as record type or choose an income category."
                )
            
            if record_type == 'expense' and category in income_categories:
                raise serializers.ValidationError(
                    f"Category '{category}' is an income category. "
                    "Please use 'income' as record type or choose an expense category."
                )
        
        return attrs
    
    def create(self, validated_data):
        """
        Create a new financial record.
        
        Automatically sets the created_by field from the request context.
        
        Args:
            validated_data (dict): Validated record data
            
        Returns:
            FinancialRecord: Created record instance
        """
        # Get user from context
        request = self.context.get('request')
        if request:
            validated_data['created_by'] = request.user
        
        return super().create(validated_data)


class FinancialRecordListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing records.
    
    Optimized for performance by including only essential fields.
    """
    
    formatted_amount = serializers.CharField(read_only=True)
    category_display = serializers.CharField(
        source='get_category_display',
        read_only=True
    )
    created_by_username = serializers.CharField(
        source='created_by.username',
        read_only=True
    )
    
    class Meta:
        model = FinancialRecord
        fields = [
            'id',
            'amount',
            'record_type',
            'category',
            'category_display',
            'date',
            'description',
            'formatted_amount',
            'created_by',
            'created_by_username',
            'created_at',
        ]


class FinancialRecordCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating records.
    
    Includes additional validation and user-friendly error messages.
    """
    
    class Meta:
        model = FinancialRecord
        fields = [
            'amount',
            'record_type',
            'category',
            'date',
            'description',
            'notes',
        ]
    
    def validate_amount(self, value):
        """
        Validate that amount is positive.
        
        Args:
            value (Decimal): Amount to validate
            
        Returns:
            Decimal: Validated amount
            
        Raises:
            serializers.ValidationError: If amount is negative or zero
        """
        if value <= 0:
            raise serializers.ValidationError(
                "Amount must be greater than zero"
            )
        if value > 999999999999.99:
            raise serializers.ValidationError(
                "Amount exceeds maximum allowed value"
            )
        return value
    
    def validate_date(self, value):
        """
        Validate that date is not in the future.
        
        Args:
            value (Date): Date to validate
            
        Returns:
            Date: Validated date
            
        Raises:
            serializers.ValidationError: If date is in the future
        """
        from django.utils import timezone
        if value > timezone.now().date():
            raise serializers.ValidationError(
                "Transaction date cannot be in the future"
            )
        return value
    
    def validate_description(self, value):
        """Validate description length."""
        if value and len(value) > 200:
            raise serializers.ValidationError(
                "Description cannot exceed 200 characters"
            )
        return value
    
    def validate_notes(self, value):
        """Validate notes length."""
        if value and len(value) > 2000:
            raise serializers.ValidationError(
                "Notes cannot exceed 2000 characters"
            )
        return value
    
    def validate(self, attrs):
        """
        Validate record type and category combination.
        
        Ensures that income categories are used with income type
        and expense categories with expense type.
        
        Args:
            attrs (dict): All attributes
            
        Returns:
            dict: Validated attributes
            
        Raises:
            serializers.ValidationError: If category and type don't match
        """
        record_type = attrs.get('record_type')
        category = attrs.get('category')
        
        if record_type and category:
            # Define income and expense categories
            income_categories = [
                'salary', 'freelance', 'investment', 
                'business', 'rental', 'other_income'
            ]
            expense_categories = [
                'food', 'transport', 'utilities', 'rent',
                'healthcare', 'entertainment', 'shopping',
                'education', 'travel', 'insurance',
                'maintenance', 'taxes', 'other_expense'
            ]
            
            # Check consistency
            if record_type == 'income' and category in expense_categories:
                raise serializers.ValidationError(
                    f"Category '{category}' is an expense category. "
                    "Please use 'expense' as record type or choose an income category."
                )
            
            if record_type == 'expense' and category in income_categories:
                raise serializers.ValidationError(
                    f"Category '{category}' is an income category. "
                    "Please use 'income' as record type or choose an expense category."
                )
        
        return attrs


class CategoryBreakdownSerializer(serializers.Serializer):
    """
    Serializer for category-wise breakdown data.
    
    Used in dashboard analytics to show totals per category.
    """
    
    category = serializers.CharField()
    category_display = serializers.CharField()
    total_amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    record_count = serializers.IntegerField()
    percentage = serializers.DecimalField(max_digits=5, decimal_places=2)
    record_type = serializers.CharField()


class MonthlyTrendSerializer(serializers.Serializer):
    """
    Serializer for monthly trend data.
    
    Used in dashboard to show income/expense trends over months.
    """
    
    month = serializers.CharField()
    year = serializers.IntegerField()
    income = serializers.DecimalField(max_digits=15, decimal_places=2)
    expense = serializers.DecimalField(max_digits=15, decimal_places=2)
    net = serializers.DecimalField(max_digits=15, decimal_places=2)
    record_count = serializers.IntegerField()
