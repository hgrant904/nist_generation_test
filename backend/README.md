# NIST Report Backend

FastAPI backend for NIST security report automation with async SQLAlchemy and database connectivity.

## Features

- **FastAPI** framework with async/await support
- **SQLAlchemy 2.0** with async engine and session management
- **Alembic** for database migrations
- **Pydantic v2** for settings management and data validation
- **Application factory pattern** with lifespan management
- **Structured logging** configuration
- Health check and database status endpoints
- Comprehensive test suite with pytest
- Code quality tools (Black, Ruff, Mypy)

## Project Structure

```
backend/
├── app/
│   ├── api/              # API route handlers
│   │   └── health.py     # Health check endpoints
│   ├── core/             # Core configuration
│   │   ├── settings.py   # Pydantic settings
│   │   └── logging_config.py
│   ├── db/               # Database configuration
│   │   ├── base.py       # SQLAlchemy base
│   │   └── session.py    # Async session management
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   │   └── health.py
│   └── main.py           # Application factory
├── alembic/              # Database migrations
│   ├── versions/         # Migration files
│   └── env.py            # Alembic environment
├── tests/                # Test suite
│   ├── conftest.py       # Pytest fixtures
│   ├── test_health.py    # Health endpoint tests
│   └── test_main.py      # Main app tests
├── .env.example          # Example environment variables
├── alembic.ini           # Alembic configuration
├── pyproject.toml        # Poetry dependencies
├── requirements.txt      # Pip dependencies
└── requirements-dev.txt  # Development dependencies
```

## Prerequisites

- Python 3.11+
- PostgreSQL 12+ (for production)
- pip or Poetry package manager

## Installation

### Using pip

1. Create and activate a virtual environment:
# NIST Reports Backend

FastAPI-based backend service for NIST security report automation.

## Technology Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Python Version**: 3.11+
- **Package Management**: Poetry (optional) or pip

## Development Setup

### Local Development (without Docker)

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
cd backend
pip install -r requirements-dev.txt
```

### Using Poetry

```bash
cd backend
poetry install
poetry shell
```

## Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` with your database credentials and settings:
```env
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_USER=postgres
DATABASE_PASSWORD=your_password
DATABASE_NAME=nist_reports
```

## Database Setup

### Create Database

```bash
# Using psql
createdb nist_reports

# Or connect to PostgreSQL
psql -U postgres
CREATE DATABASE nist_reports;
```

### Run Migrations

```bash
# Generate initial migration (if models exist)
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## Running the Application

### Development Server

```bash
# Using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or with custom settings
uvicorn app.main:app --reload --log-level debug
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive docs**: http://localhost:8000/docs
- **Alternative docs**: http://localhost:8000/redoc

### Health Check Endpoints

Test the endpoints:
```bash
# Basic health check
curl http://localhost:8000/api/v1/health

# Database connectivity check
curl http://localhost:8000/api/v1/health/db
```

## Testing

### Run All Tests

```bash
# Run tests with coverage
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_health.py

# Run with coverage report
pytest --cov=app --cov-report=html
```

### Run Tests in Watch Mode

```bash
# Install pytest-watch
pip install pytest-watch

# Run in watch mode
ptw
```

## Code Quality

### Linting and Formatting

```bash
# Format code with Black
black app tests

# Lint with Ruff
ruff check app tests

# Fix linting issues automatically
ruff check --fix app tests

# Type checking with Mypy
mypy app
```

### Pre-commit Setup

```bash
# Install pre-commit
pip install pre-commit

# Install git hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

## Database Migrations

### Create a New Migration

```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "Add new table"

# Create empty migration
alembic revision -m "Custom migration"
```

### Apply Migrations

```bash
# Upgrade to latest
alembic upgrade head

# Upgrade by steps
alembic upgrade +1

# Downgrade by steps
alembic downgrade -1

# Show current revision
alembic current

# Show migration history
alembic history
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PROJECT_NAME` | Application name | "NIST Report Backend" |
| `VERSION` | Application version | "0.1.0" |
| `API_V1_PREFIX` | API prefix | "/api/v1" |
| `DEBUG` | Debug mode | false |
| `LOG_LEVEL` | Logging level | "INFO" |
| `DATABASE_HOST` | Database host | "localhost" |
| `DATABASE_PORT` | Database port | 5432 |
| `DATABASE_USER` | Database user | "postgres" |
| `DATABASE_PASSWORD` | Database password | "postgres" |
| `DATABASE_NAME` | Database name | "nist_reports" |
| `DATABASE_URL` | Full database URL | Auto-generated |
| `DATABASE_POOL_SIZE` | Connection pool size | 5 |
| `DATABASE_MAX_OVERFLOW` | Max overflow connections | 10 |
| `DATABASE_ECHO` | Echo SQL queries | false |

## Docker Support (Coming Soon)

```bash
# Build image
docker build -t nist-backend .

# Run container
docker run -p 8000:8000 --env-file .env nist-backend
```

## Troubleshooting

### Database Connection Issues

1. Verify PostgreSQL is running:
```bash
pg_isready -h localhost -p 5432
```

2. Check database exists:
```bash
psql -U postgres -l
```

3. Test connection:
```bash
psql -U postgres -d nist_reports -c "SELECT 1;"
```

### Migration Issues

1. Reset migrations (development only):
```bash
alembic downgrade base
rm alembic/versions/*.py
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### Import Errors

Ensure the backend directory is in your Python path:
```bash
export PYTHONPATH="${PYTHONPATH}:/path/to/backend"
```

## Development Workflow

1. Create a new branch for your feature
2. Make changes to code
3. Write/update tests
4. Run linters and formatters: `black app tests && ruff check app tests`
5. Run tests: `pytest`
6. Create database migration if needed: `alembic revision --autogenerate -m "Description"`
7. Commit and push changes

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

## License

[Add your license here]

## Contributing

[Add contributing guidelines here]
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp ../.env.example .env
# Edit .env with your configuration
```

4. Run the application:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Running Tests

```bash
pytest
pytest --cov=app tests/  # With coverage
```

## API Documentation

Once the server is running, access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application entry point
│   ├── config.py         # Configuration management
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   ├── api/              # API routes
│   ├── services/         # Business logic
│   └── utils/            # Utility functions
├── tests/
│   └── test_main.py
├── Dockerfile
├── requirements.txt
└── pyproject.toml
```
