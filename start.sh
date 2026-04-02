#!/bin/bash

# Production Startup Script for Render.com
# This script handles database migrations, static files, and server startup

echo "=== Starting Finance Data Processing API ==="

# Exit on error
set -o errexit

# Echo commands for debugging
set -x

echo "Step 1: Applying database migrations..."
python manage.py migrate --noinput || {
    echo "ERROR: Migration failed!"
    exit 1
}

echo "Step 2: Collecting static files..."
python manage.py collectstatic --noinput --clear || {
    echo "Warning: Static file collection failed, continuing..."
}

echo "Step 3: Checking database connection..."
python manage.py check --deploy || {
    echo "Warning: Some deployment checks failed"
}

echo "Step 4: Creating superuser (if not exists)..."
python manage.py shell <<EOF || true
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    try:
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print('Superuser created successfully!')
    except Exception as e:
        print(f'Superuser creation failed: {e}')
else:
    print('Superuser already exists.')
EOF

echo "Step 5: Starting Gunicorn server..."
exec gunicorn finance_api.wsgi:application --bind "0.0.0.0:$PORT" --workers 3 --threads 2 --timeout 30
