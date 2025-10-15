#!/bin/bash

echo "🔍 Checking service health..."
echo ""

# Check if Docker Compose is running
if ! docker-compose ps | grep -q "Up"; then
    echo "❌ Services are not running. Start them with: make dev"
    exit 1
fi

# Check Backend
echo "Backend API (http://localhost:8000):"
if curl -s -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "  ✅ Healthy"
else
    echo "  ❌ Not responding"
fi

# Check Frontend
echo ""
echo "Frontend (http://localhost:3000):"
if curl -s -f http://localhost:3000 > /dev/null 2>&1; then
    echo "  ✅ Healthy"
else
    echo "  ❌ Not responding"
fi

# Check Database
echo ""
echo "PostgreSQL Database:"
if docker-compose exec -T postgres pg_isready -U nist_user > /dev/null 2>&1; then
    echo "  ✅ Healthy"
else
    echo "  ❌ Not responding"
fi

echo ""
echo "📊 Container Status:"
docker-compose ps
