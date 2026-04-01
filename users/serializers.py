"""
User Serializers Module

This module handles serialization/deserialization of User model data.

Classes:
    UserSerializer: For regular user operations
    UserCreateSerializer: For user registration
    UserDetailSerializer: For detailed user views
    UserStatusUpdateSerializer: For toggling user status
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Basic user serializer for listing and general operations.
    
    Provides field validation and read-only access to sensitive fields.
    """
    
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
            'is_active',
            'date_joined',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'date_joined',
            'updated_at',
        ]
    
    def validate_email(self, value):
        """
        Validate email format and uniqueness.
        
        Args:
            value (str): Email address to validate
            
        Returns:
            str: Normalized email address
            
        Raises:
            serializers.ValidationError: If email is invalid or exists
        """
        return value.lower().strip()
    
    def validate_username(self, value):
        """
        Validate username format.
        
        Args:
            value (str): Username to validate
            
        Returns:
            str: Cleaned username
            
        Raises:
            serializers.ValidationError: If username is invalid
        """
        if len(value) < 3:
            raise serializers.ValidationError(
                "Username must be at least 3 characters long"
            )
        if not value.isalnum():
            raise serializers.ValidationError(
                "Username can only contain letters and numbers"
            )
        return value
    
    def validate_role(self, value):
        """
        Validate role assignment.
        
        Only admins can assign roles. This validation ensures
        the role is one of the valid choices.
        
        Args:
            value (str): Role to assign
            
        Returns:
            str: Validated role
            
        Raises:
            serializers.ValidationError: If role is invalid
        """
        valid_roles = [choice[0] for choice in User.ROLE_CHOICES]
        if value not in valid_roles:
            raise serializers.ValidationError(
                f"Invalid role. Must be one of: {', '.join(valid_roles)}"
            )
        return value


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new users.
    
    Includes password field and handles user creation with proper validation.
    """
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        style={'input_type': 'password'},
        help_text="Password must be at least 8 characters long"
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        style={'input_type': 'password'},
        help_text="Confirm your password"
    )
    
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password_confirm',
            'first_name',
            'last_name',
            'role',
        ]
    
    def validate_password(self, value):
        """
        Validate password strength.
        
        Args:
            value (str): Password to validate
            
        Returns:
            str: Validated password
            
        Raises:
            serializers.ValidationError: If password is too weak
        """
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long"
            )
        
        # Check for common passwords
        common_passwords = ['password', '12345678', 'qwerty', 'admin123']
        if value.lower() in common_passwords:
            raise serializers.ValidationError(
                "Password is too common. Please choose a stronger password"
            )
        
        return value
    
    def validate(self, attrs):
        """
        Validate that passwords match.
        
        Args:
            attrs (dict): All serializer attributes
            
        Returns:
            dict: Validated attributes
            
        Raises:
            serializers.ValidationError: If passwords don't match
        """
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError(
                {"password_confirm": "Passwords do not match"}
            )
        
        # Remove password_confirm from attrs as it's not needed for user creation
        attrs.pop('password_confirm')
        return attrs
    
    def create(self, validated_data):
        """
        Create a new user instance.
        
        Args:
            validated_data (dict): Validated user data
            
        Returns:
            User: Created user instance
        """
        # Extract password before removing it from validated_data
        password = validated_data.pop('password')
        
        # Create user using manager's create_user method
        user = User.objects.create_user(password=password, **validated_data)
        
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Detailed user serializer for retrieving user information.
    
    Includes additional computed fields and role permissions info.
    """
    
    full_name = serializers.CharField(read_only=True)
    can_create_records = serializers.BooleanField(read_only=True)
    can_delete_records = serializers.BooleanField(read_only=True)
    can_manage_users = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'full_name',
            'first_name',
            'last_name',
            'role',
            'is_active',
            'date_joined',
            'updated_at',
            'can_create_records',
            'can_delete_records',
            'can_manage_users',
        ]
        read_only_fields = fields


class UserStatusUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user status (active/inactive).
    
    Used by admins to toggle user accounts without modifying other fields.
    """
    
    class Meta:
        model = User
        fields = ['is_active']
    
    def validate_is_active(self, value):
        """
        Validate status update.
        
        Prevent deactivating own account.
        
        Args:
            value (bool): New active status
            
        Returns:
            bool: Validated status
            
        Raises:
            serializers.ValidationError: If trying to deactivate self
        """
        # Check if user is trying to deactivate themselves
        request = self.context.get('request')
        if request and request.user == self.instance:
            if value is False:
                raise serializers.ValidationError(
                    "You cannot deactivate your own account"
                )
        return value


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing user password.
    
    Validates current password and sets new password.
    """
    
    old_password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        min_length=8,
        style={'input_type': 'password'}
    )
    new_password_confirm = serializers.CharField(
        required=True,
        write_only=True,
        min_length=8,
        style={'input_type': 'password'}
    )
    
    def validate_new_password(self, value):
        """Validate new password strength."""
        if len(value) < 8:
            raise serializers.ValidationError(
                "New password must be at least 8 characters long"
            )
        return value
    
    def validate(self, attrs):
        """Validate that new passwords match."""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError(
                {"new_password_confirm": "New passwords do not match"}
            )
        
        # Check old password
        user = self.context['request'].user
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError(
                {"old_password": "Current password is incorrect"}
            )
        
        # Remove confirm field
        attrs.pop('new_password_confirm')
        return attrs
