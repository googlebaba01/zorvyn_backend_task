"""
Financial Record Views Module

This module contains viewsets for financial record operations.

Classes:
    FinancialRecordViewSet: CRUD operations with filtering and permissions
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Sum, Count
from django.utils import timezone

from .models import FinancialRecord
from .serializers import (
    FinancialRecordSerializer,
    FinancialRecordListSerializer,
    FinancialRecordCreateUpdateSerializer,
)
from .filters import FinancialRecordFilter
from users.permissions import (
    CanCreateRecords,
    CanDeleteRecords,
    IsActiveUser,
)


class FinancialRecordViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing financial records.
    
    Provides comprehensive CRUD operations with role-based access control,
    advanced filtering, search, and pagination.
    
    Endpoints:
        GET /api/records/ - List records (with filtering)
        POST /api/records/ - Create new record (Analyst/Admin only)
        GET /api/records/{id}/ - Retrieve record details
        PUT /api/records/{id}/ - Update record (Admin or creator if Analyst)
        DELETE /api/records/{id}/ - Soft delete record (Admin only)
        PATCH /api/records/{id}/restore/ - Restore deleted record (Admin only)
    
    Permissions:
        - List: All authenticated users (filtered by role)
        - Create: Analyst and Admin only
        - Update: Admin or creator (if Analyst)
        - Delete: Admin only
    
    Filtering:
        - By type: ?record_type=income
        - By category: ?category=salary&category=food
        - By date range: ?date_from=2024-01-01&date_to=2024-12-31
        - By amount range: ?amount_min=100&amount_max=1000
        - By user: ?created_by=1 or ?is_mine=true
        - Search: ?search=description text
    
    Ordering:
        - By date: ?ordering=-date (default)
        - By amount: ?ordering=amount or ?ordering=-amount
        - By created_at: ?ordering=created_at
    """
    
    queryset = FinancialRecord.objects.filter(is_deleted=False)
    permission_classes = [IsActiveUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = FinancialRecordFilter
    search_fields = ['description', 'notes']
    ordering_fields = ['date', 'amount', 'created_at', 'updated_at']
    ordering = ['-date', '-created_at']
    
    def get_queryset(self):
        """
        Filter queryset based on user role and permissions.
        
        - Admins: Can see all non-deleted records
        - Analysts: Can see all non-deleted records
        - Viewers: Can only see their own records
        
        Returns:
            QuerySet: Filtered queryset
        """
        queryset = super().get_queryset()
        user = self.request.user
        
        # Viewers can only see their own records
        if user.role == 'viewer':
            queryset = queryset.filter(created_by=user)
        
        # Always exclude deleted records unless explicitly requested
        if not self.request.query_params.get('is_deleted'):
            queryset = queryset.filter(is_deleted=False)
        
        return queryset
    
    def get_serializer_class(self):
        """
        Return appropriate serializer based on action.
        
        Returns:
            Serializer: Appropriate serializer for the action
        """
        if self.action == 'create':
            return FinancialRecordCreateUpdateSerializer
        elif self.action in ['update', 'partial_update']:
            return FinancialRecordCreateUpdateSerializer
        elif self.action == 'list':
            return FinancialRecordListSerializer
        return FinancialRecordSerializer
    
    def get_permissions(self):
        """
        Set permissions based on action.
        
        Different actions require different permission levels.
        
        Returns:
            list: List of permission instances
        """
        if self.action == 'create':
            self.permission_classes = [CanCreateRecords, IsActiveUser]
        elif self.action in ['destroy', 'restore']:
            self.permission_classes = [CanDeleteRecords, IsActiveUser]
        elif self.action in ['update', 'partial_update']:
            # Custom permission logic in perform_update
            self.permission_classes = [IsActiveUser]
        else:
            self.permission_classes = [IsActiveUser]
        
        return [permission() for permission in self.permission_classes]
    
    @swagger_auto_schema(
        operation_summary="Create a new financial record",
        operation_description="Create a new financial record. Only Analysts and Admins can create records.",
        request_body=FinancialRecordCreateUpdateSerializer,
        responses={
            201: openapi.Response('Record created', FinancialRecordSerializer),
            400: 'Bad Request - Invalid data',
            403: 'Forbidden - Insufficient permissions',
        }
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new financial record.
        
        Only Analyst and Admin users can create records.
        The record is automatically associated with the creating user.
        
        Args:
            request: HTTP request with record data
            
        Returns:
            Response: Created record details
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            FinancialRecordSerializer(serializer.instance, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    
    @swagger_auto_schema(
        operation_summary="List financial records",
        operation_description="Retrieve paginated list of financial records with filtering options.",
        responses={
            200: openapi.Response('List of records', FinancialRecordListSerializer(many=True)),
        }
    )
    def list(self, request, *args, **kwargs):
        """
        List financial records with filtering, searching, and pagination.
        
        All authenticated users can list records, but the results are filtered
        based on their role and permissions.
        
        Args:
            request: HTTP request with optional query parameters
            
        Returns:
            Response: Paginated list of records
        """
        queryset = self.filter_queryset(self.get_queryset())
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        """
        Perform record creation with automatic user assignment.
        
        Args:
            serializer: Validated serializer instance
        """
        serializer.save(created_by=self.request.user)
    
    def perform_update(self, serializer):
        """
        Perform record update with permission checks.
        
        - Admins can update any record
        - Analysts can only update their own records
        - Viewers cannot update records
        
        Args:
            serializer: Validated serializer instance
            
        Raises:
            PermissionError: If user cannot update the record
        """
        instance = serializer.instance
        user = self.request.user
        
        # Admin can update any record
        if user.role == 'admin':
            serializer.save()
            return
        
        # Analyst can only update their own records
        if user.role == 'analyst' and instance.created_by == user:
            serializer.save()
            return
        
        # No permission to update
        self.permission_denied(
            request=self.request,
            message="You do not have permission to update this record"
        )
    
    @swagger_auto_schema(
        operation_summary="Delete a financial record",
        operation_description="Soft delete a financial record. Only Admins can delete records.",
        responses={
            204: 'Record deleted successfully',
            403: 'Forbidden - Admin access required',
            404: 'Record not found',
        }
    )
    def destroy(self, request, *args, **kwargs):
        """
        Soft delete a financial record.
        
        Only Admin users can delete records.
        The record is marked as deleted but not removed from database.
        
        Args:
            request: HTTP request
            pk: Primary key of the record
            
        Returns:
            Response: Empty response with 204 status
        """
        instance = self.get_object()
        instance.is_deleted = True
        instance.deleted_at = timezone.now()
        instance.save()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['patch'])
    @swagger_auto_schema(
        operation_summary="Restore a deleted record",
        operation_description="Restore a soft-deleted financial record. Only Admins can restore records.",
        responses={
            200: openapi.Response('Record restored', FinancialRecordSerializer),
            403: 'Forbidden - Admin access required',
            404: 'Record not found',
        }
    )
    def restore(self, request, pk=None):
        """
        Restore a soft-deleted financial record.
        
        Only Admin users can restore deleted records.
        
        Args:
            request: HTTP request
            pk: Primary key of the record
            
        Returns:
            Response: Restored record details
        """
        instance = self.get_object()
        
        if not instance.is_deleted:
            return Response(
                {'error': 'Record is not deleted'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        instance.is_deleted = False
        instance.deleted_at = None
        instance.save()
        
        return Response(FinancialRecordSerializer(instance, context={'request': request}).data)
