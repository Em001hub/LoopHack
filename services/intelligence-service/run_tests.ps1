# Test Runner Script for Intelligence Service
# Run this to execute all tests and see results

Write-Host "🧪 Intelligence Service - Test Suite" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment is activated
if (-not $env:VIRTUAL_ENV) {
    Write-Host "⚠️  Virtual environment not activated!" -ForegroundColor Yellow
    Write-Host "Activating .venv..." -ForegroundColor Yellow
    & .\.venv\Scripts\Activate.ps1
}

Write-Host "✅ Virtual environment: $env:VIRTUAL_ENV" -ForegroundColor Green
Write-Host ""

# Install test dependencies if needed
Write-Host "📦 Checking dependencies..." -ForegroundColor Cyan
pip install -q pytest pytest-asyncio pytest-cov httpx

Write-Host ""
Write-Host "🏃 Running tests..." -ForegroundColor Cyan
Write-Host ""

# Run tests with verbose output
pytest tests/ -v --tb=short --color=yes

Write-Host ""
Write-Host "📊 Generating coverage report..." -ForegroundColor Cyan
pytest tests/ --cov=src --cov-report=term --cov-report=html --quiet

Write-Host ""
Write-Host "✅ Tests complete! Coverage report: htmlcov/index.html" -ForegroundColor Green
