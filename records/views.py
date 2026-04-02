"""
Financial Record Views Module

ViewSet for financial record CRUD operations with role-based access control.
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
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
    """ViewSet for managing financial records with role-based access control."""
    
    queryset = FinancialRecord.objects.filter(is_deleted=False)
    permission_classes = [IsActiveUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = FinancialRecordFilter
    search_fields = ['description', 'notes']
    ordering_fields = ['date', 'amount', 'created_at', 'updated_at']
    ordering = ['-date', '-created_at']
    
    def get_queryset(self):
        """Filter queryset based on user role and permissions."""
        queryset = super().get_queryset()
        user = self.request.user
        
        if getattr(self, 'swagger_fake_view', False):
            return queryset
        
        if hasattr(user, 'role') and user.role == 'viewer':
            queryset = queryset.filter(created_by=user)
        
        if not self.request.query_params.get('is_deleted'):
            queryset = queryset.filter(is_deleted=False)
        
        return queryset
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return FinancialRecordCreateUpdateSerializer
        elif self.action in ['update', 'partial_update']:
            return FinancialRecordCreateUpdateSerializer
        elif self.action == 'list':
            return FinancialRecordListSerializer
        return FinancialRecordSerializer
    
    def get_permissions(self):
        """Set permissions based on action."""
        if self.action == 'create':
            self.permission_classes = [CanCreateRecords, IsActiveUser]
        elif self.action in ['destroy', 'restore']:
            self.permission_classes = [CanDeleteRecords, IsActiveUser]
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [IsActiveUser]
        else:
            self.permission_classes = [IsActiveUser]
        
        return [permission() for permission in self.permission_classes]
    
    def create(self, request, *args, **kwargs):
        """Create a new financial record."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            FinancialRecordSerializer(serializer.instance, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    
    def list(self, request, *args, **kwargs):
        """List financial records with filtering, searching, and pagination."""
        queryset = self.filter_queryset(self.get_queryset())
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        """Perform record creation with automatic user assignment."""
        serializer.save(created_by=self.request.user)
    
    def perform_update(self, serializer):
        """Perform record update with permission checks. Admins can update any, analysts only their own."""
        instance = serializer.instance
        user = self.request.user
        
        if user.role == 'admin':
            serializer.save()
            return
        
        if user.role == 'analyst' and instance.created_by == user:
            serializer.save()
            return
        
        self.permission_denied(
            request=self.request,
            message="You do not have permission to update this record"
        )
    
    def destroy(self, request, *args, **kwargs):
        """Soft delete a financial record. Admin only."""
        instance = self.get_object()
        instance.is_deleted = True
        instance.deleted_at = timezone.now()
        instance.save()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['patch'])
    def restore(self, request, pk=None):
        """Restore a soft-deleted financial record. Admin only."""
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
