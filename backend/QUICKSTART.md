# Quick Start Guide

Get the NIST Report Backend up and running in 5 minutes.

## Prerequisites

- Python 3.11 or higher
- PostgreSQL 12+ (optional for development - tests use SQLite)
- pip or Poetry package manager

## Installation

```bash
# Clone and navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements-dev.txt
```

## Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env if needed (optional for testing)
# The default values work for local development
```

## Run Tests

```bash
# Run all tests
pytest

# Or use the test script
bash scripts/test.sh
```

## Start Development Server

```bash
# Start the server
uvicorn app.main:app --reload

# Server will be available at:
# - API: http://localhost:8000
# - Docs: http://localhost:8000/docs
```

## Test the API

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Expected response:
# {"status":"healthy","version":"0.1.0"}

# Database health check
curl http://localhost:8000/api/v1/health/db

# Expected response (with SQLite for testing):
# {"database":"postgresql","status":"connected"}
```

## Using Docker (Optional)

```bash
# Start with Docker Compose
docker-compose up

# Server will be available at http://localhost:8000
# PostgreSQL at localhost:5432
```

## Common Commands

```bash
# Run tests with coverage
pytest --cov=app

# Format code
black app tests

# Lint code
ruff check app tests

# Type check
mypy app

# Run all checks
bash scripts/test.sh

# Create database migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head
```

## Next Steps

1. Read the full [README.md](README.md) for detailed documentation
2. Check [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines
3. Explore the API documentation at http://localhost:8000/docs
4. Start building your features!

## Troubleshooting

### Import Errors
```bash
# Make sure you're in the virtual environment
source venv/bin/activate
```

### Port Already in Use
```bash
# Use a different port
uvicorn app.main:app --reload --port 8001
```

### Database Connection Issues
The tests use in-memory SQLite by default, so no PostgreSQL setup is required for development. For production deployment, configure the database settings in `.env`.

## Support

- Check the [README.md](README.md) for detailed documentation
- Review [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines
- Open an issue on GitHub for bugs or feature requests
