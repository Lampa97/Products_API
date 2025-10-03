# Development startup script for Windows

Write-Host "🚀 Starting Products API in development mode..." -ForegroundColor Green

# Check if Docker is running
try {
    docker info | Out-Null
} catch {
    Write-Host "❌ Docker is not running. Please start Docker first." -ForegroundColor Red
    exit 1
}

# Build and start services
Write-Host "📦 Building and starting services..." -ForegroundColor Yellow
docker-compose up --build

Write-Host "✅ Development environment started!" -ForegroundColor Green
Write-Host "📍 API available at: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📖 API docs available at: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "🗄️  PostgreSQL available at: localhost:5432" -ForegroundColor Cyan
Write-Host "🔴 Redis available at: localhost:6379" -ForegroundColor Cyan