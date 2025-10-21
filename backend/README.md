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
