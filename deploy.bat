@echo off
REM Quick Deployment Script for Render.com
REM This script commits all changes and pushes to GitHub for automatic deployment

echo ================================================
echo   Finance Data Processing API - Deploy to Render
echo ================================================
echo.

REM Step 1: Check git status
echo [1/4] Checking git status...
git status
if %errorlevel% neq 0 (
    echo ERROR: Not in a git repository or git not installed!
    pause
    exit /b 1
)

REM Step 2: Add all changes
echo.
echo [2/4] Adding all changes to git...
git add .
echo Done!

REM Step 3: Commit with message
echo.
echo [3/4] Committing changes...
set COMMIT_MSG=Production deployment - %date% %time%
git commit -m "%COMMIT_MSG%"
if %errorlevel% neq 0 (
    echo No changes to commit or commit failed.
)

REM Step 4: Push to main
echo.
echo [4/4] Pushing to main branch...
git push origin main
if %errorlevel% neq 0 (
    echo ERROR: Push failed! Check your git configuration.
    pause
    exit /b 1
)

echo.
echo ================================================
echo   SUCCESS! Code pushed to GitHub
echo.
echo   Next Steps:
echo   1. Go to https://dashboard.render.com
echo   2. Select your service: finance-data-api
echo   3. Click "Manual Deploy" if auto-deploy is disabled
echo   4. Wait 2-3 minutes for deployment
echo   5. Test: https://finance-data-api-saav.onrender.com/
echo ================================================
echo.
pause
