"""
User Views Module

This module contains viewsets for user management operations.

Classes:
    UserViewSet: CRUD operations for users with role-based access control
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserDetailSerializer,
    UserStatusUpdateSerializer,
    ChangePasswordSerializer,
)
from .permissions import (
    CanManageUsers,
    IsActiveUser,
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing users in the system.
    
    Provides CRUD operations with proper role-based access control.
    Only admin users can manage other users.
    
    Endpoints:
        GET /api/users/ - List all users (Admin only)
        POST /api/users/ - Create new user (Admin only)
        GET /api/users/{id}/ - Retrieve user details
        PUT /api/users/{id}/ - Update user (Admin only)
        DELETE /api/users/{id}/ - Delete user (Admin only)
        PATCH /api/users/{id}/status/ - Toggle user status (Admin only)
        POST /api/users/{id}/change-password/ - Change password
    
    Permissions:
        - List/Create: Admin only
        - Retrieve: Any authenticated user (own details or admin)
        - Update/Delete: Admin only
        - Status update: Admin only
    
    Filtering:
        - By role: ?role=admin
        - By status: ?is_active=true
        - Search: ?search=username or email
    
    Ordering:
        - By date_joined: ?ordering=-date_joined
        - By username: ?ordering=username
    """
    
    queryset = User.objects.all()
    permission_classes = [IsActiveUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['role', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['date_joined', 'username', 'email']
    ordering = ['-date_joined']
    
    def get_queryset(self):
        """
        Filter queryset based on user permissions.
        
        Regular users can only see their own details.
        Admins can see all users.
        
        Returns:
            QuerySet: Filtered user queryset
        """
        queryset = super().get_queryset()
        
        # Non-admin users can only see their own profile
        if not self.request.user.role == 'admin':
            queryset = queryset.filter(id=self.request.user.id)
        
        return queryset
    
    def get_serializer_class(self):
        """
        Return appropriate serializer class based on action.
        
        Returns:
            Serializer: Appropriate serializer for the action
        """
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'retrieve':
            return UserDetailSerializer
        elif self.action == 'update_status':
            return UserStatusUpdateSerializer
        elif self.action == 'change_password':
            return ChangePasswordSerializer
        return UserSerializer
    
    def get_permissions(self):
        """
        Set permissions based on action.
        
        Different actions require different permission levels.
        
        Returns:
            list: List of permission instances
        """
        if self.action in ['create', 'list', 'update', 'partial_update', 'destroy', 'update_status']:
            # Admin-only operations
            self.permission_classes = [CanManageUsers, IsActiveUser]
        elif self.action == 'change_password':
            # Users can change their own password
            self.permission_classes = [IsActiveUser]
        else:
            # Default permissions
            self.permission_classes = [IsActiveUser]
        
        return [permission() for permission in self.permission_classes]
    
    @swagger_auto_schema(
        operation_summary="Create a new user",
        operation_description="Create a new user account. Only admins can create users.",
        request_body=UserCreateSerializer,
        responses={
            201: openapi.Response('User created successfully', UserDetailSerializer),
            400: 'Bad Request - Invalid data',
            403: 'Forbidden - Admin access required',
        }
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new user.
        
        Only admin users can create new users. The creator can assign
        roles to the new user during creation.
        
        Args:
            request: HTTP request with user data
            
        Returns:
            Response: Created user details
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Return detailed response
        headers = self.get_success_headers(serializer.data)
        return Response(
            UserDetailSerializer(serializer.instance, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    
    @swagger_auto_schema(
        operation_summary="Get user details",
        operation_description="Retrieve detailed information about a specific user.",
        responses={
            200: openapi.Response('User details', UserDetailSerializer),
            404: 'User not found',
        }
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve user details.
        
        Users can view their own profile or admin can view any user.
        
        Args:
            request: HTTP request
            pk: Primary key of the user
            
        Returns:
            Response: User details
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'request': request})
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_summary="Update user",
        operation_description="Update user information. Only admins can update users.",
        request_body=UserSerializer,
        responses={
            200: openapi.Response('User updated', UserDetailSerializer),
            400: 'Bad Request - Invalid data',
            403: 'Forbidden - Admin access required',
            404: 'User not found',
        }
    )
    def update(self, request, *args, **kwargs):
        """
        Update user information.
        
        Only admin users can update other users.
        
        Args:
            request: HTTP request with updated data
            pk: Primary key of the user
            
        Returns:
            Response: Updated user details
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(UserDetailSerializer(instance, context={'request': request}).data)
    
    @swagger_auto_schema(
        operation_summary="Delete user",
        operation_description="Delete a user. Only admins can delete users.",
        responses={
            204: 'User deleted successfully',
            403: 'Forbidden - Admin access required',
            404: 'User not found',
        }
    )
    def destroy(self, request, *args, **kwargs):
        """
        Delete a user.
        
        Only admin users can delete other users.
        Cannot delete your own account.
        
        Args:
            request: HTTP request
            pk: Primary key of the user
            
        Returns:
            Response: Empty response with 204 status
        """
        instance = self.get_object()
        
        # Prevent self-deletion
        if instance.id == request.user.id:
            return Response(
                {'error': 'You cannot delete your own account'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['patch'], url_path='status')
    @swagger_auto_schema(
        operation_summary="Update user status",
        operation_description="Activate or deactivate a user account. Only admins can perform this action.",
        request_body=UserStatusUpdateSerializer,
        responses={
            200: openapi.Response('Status updated', UserDetailSerializer),
            400: 'Bad Request - Invalid status',
            403: 'Forbidden - Admin access required',
            404: 'User not found',
        }
    )
    def update_status(self, request, pk=None):
        """
        Update user active status.
        
        Admins can activate or deactivate user accounts.
        Users cannot deactivate their own accounts.
        
        Args:
            request: HTTP request with is_active field
            pk: Primary key of the user
            
        Returns:
            Response: Updated user details
        """
        user = self.get_object()
        
        serializer = UserStatusUpdateSerializer(
            user,
            data=request.data,
            context={'request': request},
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(UserDetailSerializer(user, context={'request': request}).data)
    
    @action(detail=True, methods=['post'], url_path='change-password')
    @swagger_auto_schema(
        operation_summary="Change password",
        operation_description="Change your password. Users can only change their own password.",
        request_body=ChangePasswordSerializer,
        responses={
            200: 'Password changed successfully',
            400: 'Bad Request - Invalid passwords',
            404: 'User not found',
        }
    )
    def change_password(self, request, pk=None):
        """
        Change user password.
        
        Users can only change their own password.
        Requires current password for verification.
        
        Args:
            request: HTTP request with old and new passwords
            pk: Primary key of the user (must match authenticated user)
            
        Returns:
            Response: Success message
        """
        user = self.get_object()
        
        # Users can only change their own password
        if user.id != request.user.id:
            return Response(
                {'error': 'You can only change your own password'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        
        # Set new password
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({'message': 'Password changed successfully'})
