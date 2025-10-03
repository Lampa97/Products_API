#!/bin/bash
# Development startup script

echo "🚀 Starting Products API in development mode..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Build and start services
echo "📦 Building and starting services..."
docker-compose up --build

echo "✅ Development environment started!"
echo "📍 API available at: http://localhost:8000"
echo "📖 API docs available at: http://localhost:8000/docs"
echo "🗄️  PostgreSQL available at: localhost:5432"
echo "🔴 Redis available at: localhost:6379"