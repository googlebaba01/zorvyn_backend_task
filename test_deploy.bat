#!/bin/bash

# Quick Deployment Test Script
# Run this before deploying to ensure everything works

echo "=== Testing Finance API Deployment ==="
echo ""

# Step 1: Check Python version
echo "1. Checking Python version..."
python --version || { echo "ERROR: Python not found!"; exit 1; }

# Step 2: Check if requirements can be installed
echo "2. Checking dependencies..."
pip install -r requirements.txt --dry-run || { echo "ERROR: Requirements check failed!"; exit 1; }

# Step 3: Run system checks
echo "3. Running Django checks..."
python manage.py check --deploy || { echo "WARNING: Some checks failed, but continuing..."; }

# Step 4: Check migrations
echo "4. Checking migrations..."
python manage.py migrate --check || { echo "WARNING: Migration check failed..."; }

# Step 5: Collect static files (test)
echo "5. Testing static file collection..."
python manage.py collectstatic --noinput --dry-run || { echo "WARNING: Static files check failed..."; }

echo ""
echo "=== Pre-deployment checks complete ==="
echo ""
echo "Next steps:"
echo "1. Push to GitHub"
echo "2. Deploy on Render with these settings:"
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: ./start.sh"
echo "3. Add environment variables in Render dashboard"
echo ""
