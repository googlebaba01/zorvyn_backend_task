"""
User Models Module

This module defines the custom User model with role-based access control.

Models:
    User: Custom user model with role and status fields

Roles:
    - VIEWER: Read-only access to dashboard and records
    - ANALYST: Can view and create records, access analytics
    - ADMIN: Full system access including user management
"""

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    """
    Custom manager for the User model.
    
    Provides methods for creating users and superusers
    with proper field handling and validation.
    """
    
    def create_user(self, username, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        
        Args:
            username (str): Unique username
            email (str): Email address
            password (str): Plain text password (will be hashed)
            **extra_fields: Additional fields like role, first_name, etc.
        
        Returns:
            User: Created user instance
        
        Raises:
            ValueError: If email is not provided
        """
        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        Create and return a superuser (Admin role).
        
        Args:
            username (str): Unique username
            email (str): Email address
            password (str): Plain text password (will be hashed)
            **extra_fields: Additional fields (role forced to 'admin')
        
        Returns:
            User: Created superuser instance
        """
        # Force admin role and permissions for superuser
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model with role-based access control.
    
    This model extends Django's AbstractBaseUser to provide:
    - Role-based permissions (Viewer, Analyst, Admin)
    - User status tracking (active/inactive)
    - Timestamp tracking
    - Email-based authentication
    
    Attributes:
        username (str): Unique identifier for the user
        email (str): Unique email address
        role (str): User role (viewer, analyst, admin)
        is_active (bool): Account status
        is_staff (bool): Staff status for admin panel access
        date_joined (datetime): Account creation timestamp
        last_login (datetime): Last login timestamp
        updated_at (datetime): Last update timestamp
    
    Methods:
        get_full_name(): Return full name or username
        get_short_name(): Return username
        has_role(role): Check if user has specific role
        can_create_records(): Check if user can create records
        can_delete_records(): Check if user can delete records
        can_manage_users(): Check if user can manage other users
    """
    
    # Role choices
    ROLE_VIEWER = 'viewer'
    ROLE_ANALYST = 'analyst'
    ROLE_ADMIN = 'admin'
    
    ROLE_CHOICES = [
        (ROLE_VIEWER, 'Viewer'),
        (ROLE_ANALYST, 'Analyst'),
        (ROLE_ADMIN, 'Admin'),
    ]
    
    # Basic fields
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    
    # Role and status
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_VIEWER,
        help_text="User's role in the system (determines permissions)"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this user account is active"
    )
    is_staff = models.BooleanField(
        default=False,
        help_text="Whether the user can access the admin site"
    )
    
    # Timestamps
    date_joined = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Custom manager
    objects = UserManager()
    
    # Field used for authentication
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    class Meta:
        """Meta options for User model."""
        db_table = 'users'
        ordering = ['-date_joined']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        """Return string representation of the user."""
        return f"{self.username} ({self.get_role_display()})"
    
    def get_full_name(self):
        """
        Return the user's full name.
        
        Returns:
            str: Full name if available, otherwise username
        """
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        return self.username
    
    def get_short_name(self):
        """
        Return the user's short name.
        
        Returns:
            str: Username
        """
        return self.username
    
    def has_role(self, role):
        """
        Check if user has a specific role.
        
        Args:
            role (str): Role to check against
            
        Returns:
            bool: True if user has the specified role
        """
        return self.role == role
    
    def can_create_records(self):
        """
        Check if user can create financial records.
        
        Returns:
            bool: True if user is Analyst or Admin
        """
        return self.role in [self.ROLE_ANALYST, self.ROLE_ADMIN]
    
    def can_delete_records(self):
        """
        Check if user can delete financial records.
        
        Returns:
            bool: True if user is Admin
        """
        return self.role == self.ROLE_ADMIN
    
    def can_update_any_record(self):
        """
        Check if user can update any record (not just their own).
        
        Returns:
            bool: True if user is Admin
        """
        return self.role == self.ROLE_ADMIN
    
    def can_manage_users(self):
        """
        Check if user can manage other users.
        
        Returns:
            bool: True if user is Admin
        """
        return self.role == self.ROLE_ADMIN
    
    def can_view_analytics(self):
        """
        Check if user can view dashboard analytics.
        
        Returns:
            bool: True for all authenticated users
        """
        return True  # All authenticated users can view analytics
    
    @property
    def full_name(self):
        """
        Property alias for get_full_name().
        
        Returns:
            str: Full name
        """
        return self.get_full_name()
