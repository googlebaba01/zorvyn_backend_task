@echo off
REM Deployment Script for Finance Backend
REM This script prepares the project for deployment

echo ========================================
echo Finance Backend - Deployment Preparation
echo ========================================
echo.

REM Step 1: Collect static files
echo [1/4] Collecting static files...
python manage.py collectstatic --noinput
if errorlevel 1 (
    echo ERROR: Failed to collect static files
    pause
    exit /b 1
)
echo ✓ Static files collected
echo.

REM Step 2: Run migrations
echo [2/4] Running database migrations...
python manage.py migrate
if errorlevel 1 (
    echo ERROR: Failed to run migrations
    pause
    exit /b 1
)
echo ✓ Migrations applied
echo.

REM Step 3: Create superuser prompt
echo [3/4] Would you like to create a superuser? (Y/N)
set /p CREATE_SUPER=
if /i "%CREATE_SUPER%"=="Y" (
    python manage.py createsuperuser
)
echo.

REM Step 4: Git setup
echo [4/4] Setting up Git repository...
if not exist .git (
    git init
    echo ✓ Git initialized
) else (
    echo ✓ Git already initialized
)

echo.
echo ========================================
echo Deployment Preparation Complete!
echo ========================================
echo.
echo Next Steps:
echo 1. Add your files: git add .
echo 2. Commit: git commit -m "Initial commit"
echo 3. Add remote: git remote add origin YOUR_REPO_URL
echo 4. Push: git push -u origin main
echo.
pause
