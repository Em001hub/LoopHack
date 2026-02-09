# LoopHack - Quick Start Script
# This script starts both backend and frontend

Write-Host "`n🚀 Starting LoopHack Intelligence Platform...`n" -ForegroundColor Cyan

# Check if services are already running
$backendRunning = Get-NetTCPConnection -LocalPort 8002 -ErrorAction SilentlyContinue
$frontendRunning = Get-NetTCPConnection -LocalPort 5173 -ErrorAction SilentlyContinue

if ($backendRunning) {
    Write-Host "⚠️  Backend already running on port 8002" -ForegroundColor Yellow
    Write-Host "   Kill it with: Get-Process -Id (Get-NetTCPConnection -LocalPort 8002).OwningProcess | Stop-Process" -ForegroundColor Yellow
    exit 1
}

if ($frontendRunning) {
    Write-Host "⚠️  Frontend already running on port 5173" -ForegroundColor Yellow
    Write-Host "   Kill it with: Get-Process -Id (Get-NetTCPConnection -LocalPort 5173).OwningProcess | Stop-Process" -ForegroundColor Yellow
    exit 1
}

Write-Host "📖 Instructions to start LoopHack:`n" -ForegroundColor Green

Write-Host "Terminal 1 - Backend:" -ForegroundColor Yellow
Write-Host "  cd c:\Projects\LoopHack\services\intelligence-service" -ForegroundColor White
Write-Host "  .\.venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "  python -m uvicorn src.main:app --reload --port 8002`n" -ForegroundColor White

Write-Host "Terminal 2 - Frontend:" -ForegroundColor Yellow
Write-Host "  cd c:\Projects\LoopHack\frontend" -ForegroundColor White
Write-Host "  npm run dev`n" -ForegroundColor White

Write-Host "Then open: http://localhost:5173`n" -ForegroundColor Cyan

Write-Host "💡 Tip: You need to run these in separate terminal windows" -ForegroundColor Green
Write-Host "📚 Full guide: See STARTUP_GUIDE.md`n" -ForegroundColor Green
