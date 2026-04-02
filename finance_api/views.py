"""
Health check views for monitoring deployment status.
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import datetime


@api_view(['GET'])
def health_check(request):
    """
    Health check endpoint to verify the API is running.
    
    Returns:
        dict: Current timestamp and service status
    """
    return Response({
        'status': 'healthy',
        'message': 'Finance Data Processing API is running',
        'timestamp': datetime.datetime.now().isoformat(),
        'version': '1.0.0'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def api_root(request):
    """
    Root API endpoint with available endpoints.
    
    Returns:
        dict: List of available API endpoints
    """
    return Response({
        'message': 'Welcome to Finance Data Processing API',
        'available_endpoints': {
            'health': '/health/',
            'api_docs': '/api/docs/',
            'redoc': '/api/redoc/',
            'authentication': {
                'login': '/api/token/',
                'refresh': '/api/token/refresh/',
                'verify': '/api/token/verify/'
            },
            'users': '/api/users/',
            'records': '/api/records/',
            'dashboard': '/api/dashboard/',
            'admin': '/admin/'
        }
    }, status=status.HTTP_200_OK)
