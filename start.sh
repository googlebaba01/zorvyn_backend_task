#!/bin/bash

# Exit on error
set -o errexit

# Echo commands for debugging
set -x

# Apply database migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Start gunicorn
exec gunicorn finance_api.wsgi:application --bind "0.0.0.0:$PORT"
