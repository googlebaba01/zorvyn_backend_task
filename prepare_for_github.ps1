# Prepare Finance API for GitHub Push
# This script cleans up unnecessary files and prepares only essential files

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Preparing Finance API for GitHub Push" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Rename README_GITHUB.md to README.md
Write-Host "[1/8] Renaming README_GITHUB.md to README.md..." -ForegroundColor Yellow
if (Test-Path "README_GITHUB.md") {
    if (Test-Path "README.md") {
        Remove-Item "README.md" -Force
        Write-Host "  Removed old README.md" -ForegroundColor Gray
    }
    Move-Item "README_GITHUB.md" "README.md"
    Write-Host "  ✓ README.md ready" -ForegroundColor Green
} else {
    Write-Host "  ⚠ README_GITHUB.md not found, skipping..." -ForegroundColor Yellow
}

# Step 2: Rename SUBMISSION_GUIDE_FINAL.md to SUBMISSION_GUIDE.md
Write-Host "[2/8] Renaming SUBMISSION_GUIDE_FINAL.md to SUBMISSION_GUIDE.md..." -ForegroundColor Yellow
if (Test-Path "SUBMISSION_GUIDE_FINAL.md") {
    Move-Item "SUBMISSION_GUIDE_FINAL.md" "SUBMISSION_GUIDE.md"
    Write-Host "  ✓ SUBMISSION_GUIDE.md ready" -ForegroundColor Green
} else {
    Write-Host "  ⚠ SUBMISSION_GUIDE_FINAL.md not found, skipping..." -ForegroundColor Yellow
}

# Step 3: Remove unnecessary documentation
Write-Host "[3/8] Removing unnecessary documentation..." -ForegroundColor Yellow
$unnecessaryDocs = @(
    "README_SIMPLE.md",
    "CLEANUP_SUMMARY.md",
    "FILES_TO_COMMIT.txt",
    ".gitignore.clean"
)

foreach ($doc in $unnecessaryDocs) {
    if (Test-Path $doc) {
        Remove-Item $doc -Force
        Write-Host "  ✓ Removed $doc" -ForegroundColor Green
    }
}

# Step 4: Clean up Python cache and temporary files
Write-Host "[4/8] Cleaning Python cache and temporary files..." -ForegroundColor Yellow

# Remove __pycache__ directories
Get-ChildItem -Recurse -Directory -Filter "__pycache__" | ForEach-Object {
    Remove-Item $_.FullName -Recurse -Force
    Write-Host "  ✓ Removed $($_.FullName)" -ForegroundColor Gray
}

# Remove .pyc files
Get-ChildItem -Recurse -Filter "*.pyc" | ForEach-Object {
    Remove-Item $_.FullName -Force
    Write-Host "  ✓ Removed $($_.FullName)" -ForegroundColor Gray
}

# Remove .log files
Get-ChildItem -Recurse -Filter "*.log" | ForEach-Object {
    Remove-Item $_.FullName -Force
    Write-Host "  ✓ Removed $($_.FullName)" -ForegroundColor Gray
}

Write-Host "  ✓ Cache cleanup complete" -ForegroundColor Green

# Step 5: Verify .gitignore exists
Write-Host "[5/8] Checking .gitignore..." -ForegroundColor Yellow
if (Test-Path ".gitignore") {
    Write-Host "  ✓ .gitignore found" -ForegroundColor Green
} else {
    Write-Host "  ✗ ERROR: .gitignore not found!" -ForegroundColor Red
    exit 1
}

# Step 6: Check essential files exist
Write-Host "[6/8] Verifying essential files..." -ForegroundColor Yellow
$essentialFiles = @(
    "manage.py",
    "requirements.txt",
    "render.yaml",
    "start.sh",
    "README.md",
    "DEPLOYMENT_CHECKLIST.md",
    "POSTMAN_QUICK_GUIDE.md",
    "SUBMISSION_GUIDE.md"
)

$allGood = $true
foreach ($file in $essentialFiles) {
    if (Test-Path $file) {
        Write-Host "  ✓ $file exists" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $file MISSING!" -ForegroundColor Red
        $allGood = $false
    }
}

if (-not $allGood) {
    Write-Host ""
    Write-Host "ERROR: Some essential files are missing!" -ForegroundColor Red
    exit 1
}

# Step 7: Show git status
Write-Host "[7/8] Checking git status..." -ForegroundColor Yellow
Write-Host ""
git status
Write-Host ""

# Step 8: Summary
Write-Host "[8/8] Preparation Summary:" -ForegroundColor Yellow
Write-Host ""
Write-Host "✓ Repository is ready for GitHub push!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Review git status above" -ForegroundColor White
Write-Host "  2. Run: git add ." -ForegroundColor White
Write-Host "  3. Run: git commit -m 'Production-ready Finance API'" -ForegroundColor White
Write-Host "  4. Run: git push origin main" -ForegroundColor White
Write-Host ""
Write-Host "Files to be committed:" -ForegroundColor Cyan
Write-Host "  - Core Django project files" -ForegroundColor Gray
Write-Host "  - All app files (users, records, dashboard)" -ForegroundColor Gray
Write-Host "  - Migrations" -ForegroundColor Gray
Write-Host "  - requirements.txt" -ForegroundColor Gray
Write-Host "  - render.yaml" -ForegroundColor Gray
Write-Host "  - start.sh" -ForegroundColor Gray
Write-Host "  - README.md" -ForegroundColor Gray
Write-Host "  - DEPLOYMENT_CHECKLIST.md" -ForegroundColor Gray
Write-Host "  - POSTMAN_QUICK_GUIDE.md" -ForegroundColor Gray
Write-Host "  - SUBMISSION_GUIDE.md" -ForegroundColor Gray
Write-Host "  - .env.example" -ForegroundColor Gray
Write-Host ""
Write-Host "Files NOT committed (in .gitignore):" -ForegroundColor Cyan
Write-Host "  - .env (contains secrets)" -ForegroundColor Gray
Write-Host "  - db.sqlite3 (database)" -ForegroundColor Gray
Write-Host "  - venv/ (virtual environment)" -ForegroundColor Gray
Write-Host "  - staticfiles/" -ForegroundColor Gray
Write-Host "  - __pycache__/" -ForegroundColor Gray
Write-Host "  - *.pyc, *.log" -ForegroundColor Gray
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Ready to push! 🚀" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
