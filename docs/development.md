# Development Guide

This guide provides detailed information for developers working on the NIST Reports project.

## Development Environment Setup

### Prerequisites

Ensure you have the following installed:
- Docker 20.10+ and Docker Compose 2.0+
- Node.js 20+ (for local frontend development)
- Python 3.11+ (for local backend development)
- Git
- Make (optional but recommended)

### Initial Setup

1. Clone the repository and navigate to the project directory
2. Copy `.env.example` to `.env` and configure as needed
3. Run the initialization script: `./scripts/init-project.sh`
4. Verify services are running: `./scripts/health-check.sh`

## Development Workflow

### Starting Development

```bash
# Start all services
make dev

# Or start in detached mode
make up

# View logs
make logs
```

### Making Changes

1. Create a new branch: `git checkout -b feature/your-feature`
2. Make your changes in the appropriate directory (`backend/` or `frontend/`)
3. The development containers have hot-reload enabled, so changes are reflected immediately
4. Test your changes locally
5. Commit and push your changes

### Backend Development

#### Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI app initialization
│   ├── config.py         # Configuration settings
│   ├── models/           # SQLAlchemy models
│   │   └── __init__.py
│   ├── schemas/          # Pydantic schemas
│   │   └── __init__.py
│   ├── api/              # API endpoints
│   │   ├── __init__.py
│   │   └── v1/          # API version 1
│   │       ├── __init__.py
│   │       └── endpoints/
│   ├── services/         # Business logic
│   │   └── __init__.py
│   ├── db/              # Database utilities
│   │   ├── __init__.py
│   │   ├── session.py   # Database session
│   │   └── base.py      # Base model
│   └── utils/           # Utility functions
│       └── __init__.py
└── tests/
    ├── __init__.py
    ├── conftest.py      # Pytest fixtures
    └── api/             # API tests
```

#### Running Backend Locally (without Docker)

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL=postgresql://user:password@localhost:5432/nist_reports

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Running Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_main.py

# Run with verbose output
pytest -v
```

#### Code Quality Tools

```bash
cd backend

# Format code with Black
black .

# Lint code with Ruff
ruff check .

# Type checking with mypy
mypy .
```

### Frontend Development

#### Project Structure

```
frontend/
├── src/
│   └── app/
│       ├── layout.tsx        # Root layout
│       ├── page.tsx          # Home page
│       ├── api/             # API routes
│       ├── components/      # React components
│       ├── lib/            # Utility functions
│       ├── hooks/          # Custom React hooks
│       ├── types/          # TypeScript types
│       └── styles/         # Global styles
└── public/                 # Static assets
```

#### Running Frontend Locally (without Docker)

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

#### Running Frontend Tests

```bash
cd frontend

# Run tests
npm test

# Run tests in watch mode
npm test -- --watch

# Run type checking
npm run type-check
```

#### Code Quality Tools

```bash
cd frontend

# Lint code
npm run lint

# Format code
npm run format

# Type check
npm run type-check
```

## Database Management

### Accessing the Database

```bash
# Using Make
make db-shell

# Or directly with Docker
docker-compose exec postgres psql -U nist_user -d nist_reports
```

### Database Migrations (Alembic)

```bash
# Generate a new migration
docker-compose exec backend alembic revision --autogenerate -m "description"

# Apply migrations
docker-compose exec backend alembic upgrade head

# Rollback one migration
docker-compose exec backend alembic downgrade -1

# View migration history
docker-compose exec backend alembic history
```

## API Development

### Adding a New Endpoint

1. Create a new file in `backend/app/api/v1/endpoints/`
2. Define your endpoint using FastAPI decorators
3. Create Pydantic schemas in `backend/app/schemas/`
4. Add business logic in `backend/app/services/`
5. Write tests in `backend/tests/api/`
6. Update API documentation

Example:

```python
# backend/app/api/v1/endpoints/reports.py
from fastapi import APIRouter, Depends
from app.schemas.report import ReportCreate, ReportResponse

router = APIRouter()

@router.post("/", response_model=ReportResponse)
async def create_report(report: ReportCreate):
    # Implementation
    pass
```

### API Documentation

FastAPI automatically generates API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Frontend Development

### Adding a New Page

1. Create a new directory under `frontend/src/app/`
2. Add a `page.tsx` file for the page component
3. Optionally add a `layout.tsx` for page-specific layout
4. Update navigation components if needed

Example:

```typescript
// frontend/src/app/reports/page.tsx
export default function ReportsPage() {
  return (
    <main>
      <h1>Reports</h1>
      {/* Page content */}
    </main>
  );
}
```

### State Management

For simple state management, use React hooks (`useState`, `useContext`).
For complex state, consider adding a state management library (Redux, Zustand, etc.).

## Debugging

### Backend Debugging

#### Using print/logging

```python
import logging

logger = logging.getLogger(__name__)

@app.get("/debug")
async def debug_endpoint():
    logger.info("Debug info")
    return {"status": "ok"}
```

#### Using Python debugger

```python
import pdb

@app.get("/debug")
async def debug_endpoint():
    pdb.set_trace()  # Breakpoint
    return {"status": "ok"}
```

### Frontend Debugging

#### Browser DevTools

Use Chrome/Firefox DevTools for:
- Console logging
- Network inspection
- React DevTools
- Breakpoints

#### Debug logging

```typescript
console.log('Debug:', data);
console.error('Error:', error);
```

## Performance Optimization

### Backend

- Use async/await for I/O operations
- Implement database query optimization
- Add caching where appropriate
- Use connection pooling for database

### Frontend

- Implement code splitting
- Lazy load components
- Optimize images
- Use React.memo for expensive components

## Common Issues

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or change port in .env file
```

### Database Connection Issues

```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# View PostgreSQL logs
docker-compose logs postgres

# Restart database
docker-compose restart postgres
```

### Frontend Build Issues

```bash
# Clear Next.js cache
rm -rf frontend/.next

# Clear node_modules and reinstall
rm -rf frontend/node_modules
cd frontend && npm install
```

## Best Practices

1. **Always write tests** for new features
2. **Keep commits small** and focused
3. **Write descriptive commit messages** following conventions
4. **Update documentation** when changing functionality
5. **Run tests and linting** before committing
6. **Review your own PR** before requesting review
7. **Keep dependencies up to date** but test thoroughly
8. **Use environment variables** for configuration
9. **Never commit secrets** or sensitive data
10. **Follow the project's code style** guidelines
