"""
User Views Module

ViewSet for user management with role-based access control.
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend

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
    """ViewSet for managing users in the system."""
    
    queryset = User.objects.all()
    permission_classes = [IsActiveUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['role', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['date_joined', 'username', 'email']
    ordering = ['-date_joined']
    
    def get_queryset(self):
        """Filter queryset based on user permissions."""
        queryset = super().get_queryset()
        
        if getattr(self, 'swagger_fake_view', False):
            return queryset
        
        if hasattr(self.request.user, 'role') and not self.request.user.role == 'admin':
            queryset = queryset.filter(id=self.request.user.id)
        
        return queryset
    
    def get_serializer_class(self):
        """Return appropriate serializer class based on action."""
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
        """Set permissions based on action."""
        if self.action in ['create', 'list', 'update', 'partial_update', 'destroy', 'update_status']:
            self.permission_classes = [CanManageUsers, IsActiveUser]
        elif self.action == 'change_password':
            self.permission_classes = [IsActiveUser]
        else:
            self.permission_classes = [IsActiveUser]
        
        return [permission() for permission in self.permission_classes]
    
    def create(self, request, *args, **kwargs):
        """Create a new user."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            UserDetailSerializer(serializer.instance, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    
    def retrieve(self, request, *args, **kwargs):
        """Retrieve user details."""
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'request': request})
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        """Update user information."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(UserDetailSerializer(instance, context={'request': request}).data)
    
    def destroy(self, request, *args, **kwargs):
        """Delete a user. Prevents self-deletion."""
        instance = self.get_object()
        
        if instance.id == request.user.id:
            return Response(
                {'error': 'You cannot delete your own account'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['patch'], url_path='status')
    def update_status(self, request, pk=None):
        """Update user active status."""
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
    def change_password(self, request, pk=None):
        """Change user password. Users can only change their own password."""
        user = self.get_object()
        
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
        
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({'message': 'Password changed successfully'})
