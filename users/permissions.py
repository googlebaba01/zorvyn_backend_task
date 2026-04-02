"""
Custom Permission Classes for role-based access control.
"""

from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """Permission class that allows only admin users."""
    
    def has_permission(self, request, view):
        """Check if the requesting user is an admin."""
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == 'admin'
        )


class IsAdminOrAnalyst(permissions.BasePermission):
    """Permission class that allows admin and analyst users."""
    
    def has_permission(self, request, view):
        """Check if the requesting user is admin or analyst."""
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role in ['admin', 'analyst']
        )


class IsViewerReadOnly(permissions.BasePermission):
    """Permission class for viewer role with read-only access."""
    
    def has_permission(self, request, view):
        """Check if viewer can perform the action."""
        return request.method in permissions.SAFE_METHODS


class CanCreateRecords(permissions.BasePermission):
    """Permission class for creating financial records."""
    
    def has_permission(self, request, view):
        """Check if user can create records."""
        return (
            request.user and
            request.user.is_authenticated and
            request.user.can_create_records()
        )


class CanDeleteRecords(permissions.BasePermission):
    """Permission class for deleting financial records. Admin only."""
    
    def has_permission(self, request, view):
        """Check if user can delete records."""
        return (
            request.user and
            request.user.is_authenticated and
            request.user.can_delete_records()
        )


class CanManageUsers(permissions.BasePermission):
    """Permission class for managing users. Admin only."""
    
    def has_permission(self, request, view):
        """Check if user can manage other users."""
        return (
            request.user and
            request.user.is_authenticated and
            request.user.can_manage_users()
        )


class IsActiveUser(permissions.BasePermission):
    """Permission class that checks if user account is active."""
    
    def has_permission(self, request, view):
        """Check if the user account is active."""
        return (
            request.user and
            request.user.is_authenticated and
            request.user.is_active
        )
