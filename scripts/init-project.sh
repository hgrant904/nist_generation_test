#!/bin/bash
set -e

echo "🚀 Initializing NIST Reports Project..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Error: Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "✅ .env file created. Please review and update it with your configuration."
else
    echo "ℹ️  .env file already exists, skipping..."
fi

# Build Docker images
echo "🏗️  Building Docker images..."
docker-compose build

# Start the services
echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check if services are running
if docker-compose ps | grep -q "Up"; then
    echo ""
    echo "✅ Project initialized successfully!"
    echo ""
    echo "🌐 Access the applications:"
    echo "   - Frontend:  http://localhost:3000"
    echo "   - Backend:   http://localhost:8000"
    echo "   - API Docs:  http://localhost:8000/docs"
    echo ""
    echo "📚 Useful commands:"
    echo "   - View logs:        make logs"
    echo "   - Stop services:    make down"
    echo "   - Restart services: make restart"
    echo "   - Run tests:        make test"
    echo ""
else
    echo "❌ Error: Failed to start services. Check logs with 'docker-compose logs'"
    exit 1
fi
