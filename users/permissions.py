"""
Custom Permission Classes Module

This module defines custom permission classes for role-based access control.

Classes:
    IsAdminUser: Only admin users
    IsAdminOrAnalyst: Admin or analyst users
    IsViewerReadOnly: Viewers can only read
    CanCreateRecords: Users who can create records
    CanDeleteRecords: Users who can delete records
    CanManageUsers: Users who can manage other users
"""

from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    Permission class that allows only admin users.
    
    Use this for operations that should only be accessible to admins,
    such as user management or system configuration.
    """
    
    def has_permission(self, request, view):
        """
        Check if the requesting user is an admin.
        
        Args:
            request (Request): HTTP request object
            view (View): Current view being accessed
            
        Returns:
            bool: True if user is admin and authenticated
        """
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == 'admin'
        )


class IsAdminOrAnalyst(permissions.BasePermission):
    """
    Permission class that allows admin and analyst users.
    
    Use this for operations that analysts and admins can perform,
    such as creating or updating financial records.
    """
    
    def has_permission(self, request, view):
        """
        Check if the requesting user is admin or analyst.
        
        Args:
            request (Request): HTTP request object
            view (View): Current view being accessed
            
        Returns:
            bool: True if user is admin/analyst and authenticated
        """
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role in ['admin', 'analyst']
        )


class IsViewerReadOnly(permissions.BasePermission):
    """
    Permission class for viewer role with read-only access.
    
    Viewers can only perform safe methods (GET, HEAD, OPTIONS).
    They cannot create, update, or delete any data.
    """
    
    def has_permission(self, request, view):
        """
        Check if viewer can perform the action.
        
        Args:
            request (Request): HTTP request object
            view (View): Current view being accessed
            
        Returns:
            bool: True if action is read-only
        """
        # Safe methods are read-only
        return request.method in permissions.SAFE_METHODS


class CanCreateRecords(permissions.BasePermission):
    """
    Permission class for creating financial records.
    
    Allows analysts and admins to create new records.
    Viewers are denied.
    """
    
    def has_permission(self, request, view):
        """
        Check if user can create records.
        
        Args:
            request (Request): HTTP request object
            view (View): Current view being accessed
            
        Returns:
            bool: True if user can create records
        """
        return (
            request.user and
            request.user.is_authenticated and
            request.user.can_create_records()
        )


class CanDeleteRecords(permissions.BasePermission):
    """
    Permission class for deleting financial records.
    
    Only admins can delete records.
    """
    
    def has_permission(self, request, view):
        """
        Check if user can delete records.
        
        Args:
            request (Request): HTTP request object
            view (View): Current view being accessed
            
        Returns:
            bool: True if user is admin
        """
        return (
            request.user and
            request.user.is_authenticated and
            request.user.can_delete_records()
        )


class CanManageUsers(permissions.BasePermission):
    """
    Permission class for managing users.
    
    Only admins can create, update, or delete users.
    """
    
    def has_permission(self, request, view):
        """
        Check if user can manage other users.
        
        Args:
            request (Request): HTTP request object
            view (View): Current view being accessed
            
        Returns:
            bool: True if user is admin
        """
        return (
            request.user and
            request.user.is_authenticated and
            request.user.can_manage_users()
        )


class IsActiveUser(permissions.BasePermission):
    """
    Permission class that checks if user account is active.
    
    Even if a user has valid credentials, they should not be able
    to access the API if their account has been deactivated.
    """
    
    def has_permission(self, request, view):
        """
        Check if the user account is active.
        
        Args:
            request (Request): HTTP request object
            view (View): Current view being accessed
            
        Returns:
            bool: True if user is active
        """
        return (
            request.user and
            request.user.is_authenticated and
            request.user.is_active
        )
