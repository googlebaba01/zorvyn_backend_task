"""
Financial Record Models Module

Models for storing and managing financial records.
"""

from django.db import models
from django.utils import timezone
from django.conf import settings


class FinancialRecord(models.Model):
    """Model representing a financial record/transaction."""
    
    # Record type choices
    TYPE_INCOME = 'income'
    TYPE_EXPENSE = 'expense'
    
    TYPE_CHOICES = [
        (TYPE_INCOME, 'Income'),
        (TYPE_EXPENSE, 'Expense'),
    ]
    
    # Category choices
    CATEGORY_SALARY = 'salary'
    CATEGORY_FREELANCE = 'freelance'
    CATEGORY_INVESTMENT = 'investment'
    CATEGORY_BUSINESS = 'business'
    CATEGORY_RENTAL = 'rental'
    CATEGORY_OTHER_INCOME = 'other_income'
    
    CATEGORY_FOOD = 'food'
    CATEGORY_TRANSPORT = 'transport'
    CATEGORY_UTILITIES = 'utilities'
    CATEGORY_RENT = 'rent'
    CATEGORY_HEALTHCARE = 'healthcare'
    CATEGORY_ENTERTAINMENT = 'entertainment'
    CATEGORY_SHOPPING = 'shopping'
    CATEGORY_EDUCATION = 'education'
    CATEGORY_TRAVEL = 'travel'
    CATEGORY_INSURANCE = 'insurance'
    CATEGORY_MAINTENANCE = 'maintenance'
    CATEGORY_TAXES = 'taxes'
    CATEGORY_OTHER_EXPENSE = 'other_expense'
    
    CATEGORY_CHOICES = [
        # Income categories
        (CATEGORY_SALARY, 'Salary'),
        (CATEGORY_FREELANCE, 'Freelance'),
        (CATEGORY_INVESTMENT, 'Investment Returns'),
        (CATEGORY_BUSINESS, 'Business Income'),
        (CATEGORY_RENTAL, 'Rental Income'),
        (CATEGORY_OTHER_INCOME, 'Other Income'),
        
        # Expense categories
        (CATEGORY_FOOD, 'Food & Dining'),
        (CATEGORY_TRANSPORT, 'Transportation'),
        (CATEGORY_UTILITIES, 'Utilities'),
        (CATEGORY_RENT, 'Rent/Mortgage'),
        (CATEGORY_HEALTHCARE, 'Healthcare'),
        (CATEGORY_ENTERTAINMENT, 'Entertainment'),
        (CATEGORY_SHOPPING, 'Shopping'),
        (CATEGORY_EDUCATION, 'Education'),
        (CATEGORY_TRAVEL, 'Travel'),
        (CATEGORY_INSURANCE, 'Insurance'),
        (CATEGORY_MAINTENANCE, 'Maintenance'),
        (CATEGORY_TAXES, 'Taxes'),
        (CATEGORY_OTHER_EXPENSE, 'Other Expense'),
    ]
    
    # Core fields
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Transaction amount (must be positive)"
    )
    record_type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        help_text="Type of transaction: income or expense"
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        help_text="Category for classification"
    )
    date = models.DateField(
        default=timezone.now,
        help_text="Date of the transaction"
    )
    description = models.CharField(
        max_length=200,
        blank=True,
        help_text="Brief description of the transaction"
    )
    notes = models.TextField(
        blank=True,
        help_text="Additional notes or details"
    )
    
    # Relationships
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='financial_records',
        help_text="User who created this record"
    )
    
    # Status tracking
    is_deleted = models.BooleanField(
        default=False,
        help_text="Soft delete flag"
    )
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp when record was soft deleted"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        """Meta options for FinancialRecord model."""
        db_table = 'financial_records'
        ordering = ['-date', '-created_at']
        verbose_name = 'Financial Record'
        verbose_name_plural = 'Financial Records'
        indexes = [
            models.Index(fields=['record_type']),
            models.Index(fields=['category']),
            models.Index(fields=['date']),
            models.Index(fields=['is_deleted']),
            models.Index(fields=['created_by', '-date']),
        ]
    
    def __str__(self):
        """Return string representation of the record."""
        type_symbol = '+' if self.record_type == 'income' else '-'
        return f"{type_symbol} ${self.amount:.2f} - {self.get_category_display()} ({self.date})"
    
    def save(self, *args, **kwargs):
        """Override save to ensure amount is positive."""
        if self.amount < 0:
            self.amount = abs(self.amount)
        super().save(*args, **kwargs)
    
    def is_income(self):
        """Check if record is income type."""
        return self.record_type == self.TYPE_INCOME
    
    def is_expense(self):
        """Check if record is expense type."""
        return self.record_type == self.TYPE_EXPENSE
    
    def get_effect_amount(self):
        """Get signed amount based on record type."""
        if self.is_income():
            return self.amount
        return -self.amount
    
    @property
    def effect_amount(self):
        """Property alias for get_effect_amount()."""
        return self.get_effect_amount()
    
    @property
    def formatted_amount(self):
        """Get formatted amount with currency symbol."""
        prefix = '+' if self.is_income() else '-'
        return f"{prefix}${self.amount:,.2f}"
