"""
Production Settings for Finance API

This module contains production-specific settings.
It extends the base settings and overrides for production environment.

Usage:
    - Deploy to Render.com
    - Deploy to Heroku
    - Any other production server
    
Environment Variables Required:
    - SECRET_KEY (required)
    - DEBUG (should be False)
    - ALLOWED_HOSTS (required)
    - DATABASE_URL (for PostgreSQL on Render)
    - CORS_ALLOWED_ORIGINS (your frontend domain)
"""

import os
from .settings import *  # Import base settings

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# Security settings
SECURE_SSL_REDIRECT = True  # Force HTTPS
SESSION_COOKIE_SECURE = True  # Secure cookies
CSRF_COOKIE_SECURE = True  # Secure CSRF cookies
SECURE_BROWSER_XSS_FILTER = True  # XSS protection
SECURE_CONTENT_TYPE_NOSNIFF = True  # Content type sniffing protection
X_FRAME_OPTIONS = 'DENY'  # Clickjacking protection

# Allowed hosts - must be set in production
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# CORS - Update with your actual frontend domain
# Get CORS allowed origins from environment variable
_cors_origins_raw = os.environ.get(
    'CORS_ALLOWED_ORIGINS',
    default='https://your-frontend-domain.com'
)
# Parse and validate CORS origins - filter out empty strings and wildcards
CORS_ALLOWED_ORIGINS = [
    origin.strip() for origin in _cors_origins_raw.split(',')
    if origin.strip() and origin.strip() != '*'
]
# Fallback if no valid origins provided
if not CORS_ALLOWED_ORIGINS:
    CORS_ALLOWED_ORIGINS = ['https://your-frontend-domain.com']

# CSRF Settings
# Get CSRF trusted origins from environment variable
_csrf_origins_raw = os.environ.get(
    'CSRF_TRUSTED_ORIGINS',
    default='https://your-frontend-domain.com'
)
# Parse and validate CSRF origins - filter out empty strings and wildcards
CSRF_TRUSTED_ORIGINS = [
    origin.strip() for origin in _csrf_origins_raw.split(',')
    if origin.strip() and origin.strip() != '*'
]
# Fallback if no valid origins provided
if not CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS = ['https://your-frontend-domain.com']

# Database - Use PostgreSQL in production
# Render provides DATABASE_URL automatically
if 'DATABASE_URL' in os.environ:
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }

# Static files - WhiteNoise handles this
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Logging - More verbose for production
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

# JWT Settings - Longer token lifetime in production
SIMPLE_JWT = {
    **SIMPLE_JWT,
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=int(os.environ.get('JWT_ACCESS_TOKEN_LIFETIME', 60))),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=int(os.environ.get('JWT_REFRESH_TOKEN_LIFETIME', 7))),
}
