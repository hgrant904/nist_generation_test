# NIST Generation Test

Automate NIST security report generation for end users to easily create reports.

## Project Structure

```
.
├── backend/          # FastAPI backend application
└── README.md         # This file
```

## Backend

The backend is built with FastAPI and provides REST APIs for NIST report automation.

### Quick Start

```bash
cd backend

# Install dependencies
pip install -r requirements-dev.txt

# Configure environment
cp .env.example .env
# Edit .env with your database credentials

# Run database migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload
```

### Features

- ✅ FastAPI with async/await support
- ✅ SQLAlchemy 2.0 with async engine
- ✅ Alembic database migrations
- ✅ Pydantic v2 settings management
- ✅ Health check endpoints
- ✅ Comprehensive test suite
- ✅ Code quality tools (Black, Ruff, Mypy)

### API Documentation

Once the server is running:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Testing

```bash
cd backend
pytest
```

For more details, see [backend/README.md](backend/README.md).

## Development

This project uses:
- Python 3.11+
- PostgreSQL 12+
- FastAPI
- SQLAlchemy (async)
- Alembic

## License

[Add your license here]
