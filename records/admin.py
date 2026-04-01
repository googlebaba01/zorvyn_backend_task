"""
Financial Records Admin Configuration Module

This module configures the Django admin panel for financial records.
"""

from django.contrib import admin
from .models import FinancialRecord


@admin.register(FinancialRecord)
class FinancialRecordAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for FinancialRecord model.
    
    Provides interface for managing financial records in admin panel.
    """
    
    list_display = [
        'amount',
        'record_type',
        'category',
        'date',
        'created_by',
        'is_deleted',
        'created_at',
    ]
    list_filter = ['record_type', 'category', 'is_deleted', 'date', 'created_at']
    search_fields = ['description', 'notes', 'created_by__username']
    date_hierarchy = 'date'
    ordering = ['-date', '-created_at']
    
    fieldsets = (
        ('Transaction Details', {
            'fields': (
                'amount',
                'record_type',
                'category',
                'date',
                'description',
                'notes',
            )
        }),
        ('User & Status', {
            'fields': (
                'created_by',
                'is_deleted',
                'deleted_at',
            )
        }),
        ('Timestamps', {
            'fields': (
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',),
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'deleted_at']
    
    actions = ['mark_as_deleted', 'restore_records']
    
    def mark_as_deleted(self, request, queryset):
        """Soft delete selected records."""
        from django.utils import timezone
        updated = queryset.update(is_deleted=True, deleted_at=timezone.now())
        self.message_user(request, f'{updated} records marked as deleted.')
    mark_as_deleted.short_description = "Mark selected records as deleted"
    
    def restore_records(self, request, queryset):
        """Restore selected deleted records."""
        updated = queryset.update(is_deleted=False, deleted_at=None)
        self.message_user(request, f'{updated} records restored.')
    restore_records.short_description = "Restore selected records"
