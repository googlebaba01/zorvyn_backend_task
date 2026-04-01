"""
ASGI config for finance_api project.

It exposes the ASGI callable as a module-level variable named ``application``.

Reference:
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance_api.settings')

application = get_asgi_application()
