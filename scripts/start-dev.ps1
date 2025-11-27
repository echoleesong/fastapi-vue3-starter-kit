# FastAPI Vue3 Starter Kit - Development Environment Startup Script

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "FastAPI Vue3 Starter Kit - Starting Dev Environment" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
try {
    docker info | Out-Null
    Write-Host "[OK] Docker is running" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Docker is not running. Please start Docker first." -ForegroundColor Red
    exit 1
}

# Check/Create .env file
if (-not (Test-Path ".env")) {
    Write-Host "[INFO] Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "[OK] .env file created. Please review and update if needed." -ForegroundColor Green
    Write-Host ""
}

# Start development environment
Write-Host "[INFO] Starting development environment..." -ForegroundColor Yellow
docker-compose up -d

# Wait for services to start
Write-Host ""
Write-Host "[INFO] Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Show service status
Write-Host ""
Write-Host "Service Status:" -ForegroundColor Cyan
docker-compose ps

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "[SUCCESS] Development environment started!" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Access URLs:" -ForegroundColor Yellow
Write-Host "  Frontend:     http://localhost:5173"
Write-Host "  Backend API:  http://localhost:8000/docs"
Write-Host "  Health Check: http://localhost:8000/api/v1/health"
Write-Host ""
Write-Host "View Logs:" -ForegroundColor Yellow
Write-Host "  docker-compose logs -f backend"
Write-Host "  docker-compose logs -f frontend"
Write-Host ""
Write-Host "Stop Services:" -ForegroundColor Yellow
Write-Host "  docker-compose down"
Write-Host ""
