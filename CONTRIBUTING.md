# Contributing Guide

## Development Setup

### Prerequisites

- Python 3.8 or higher
- pip
- virtualenv (optional but recommended)

### Initial Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd nist_generation_test
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
uvicorn app.main:app --reload
```

## Project Structure

```
.
├── app/
│   ├── models/              # SQLAlchemy database models
│   │   ├── questionnaire.py
│   │   ├── question.py
│   │   ├── assessment_session.py
│   │   └── response.py
│   ├── schemas/             # Pydantic validation schemas
│   │   ├── questionnaire.py
│   │   ├── question.py
│   │   └── assessment.py
│   ├── services/            # Business logic layer
│   │   ├── questionnaire_service.py
│   │   ├── question_service.py
│   │   └── assessment_service.py
│   ├── routers/             # API route handlers
│   │   ├── questionnaires.py
│   │   ├── questions.py
│   │   └── assessments.py
│   ├── database.py          # Database configuration
│   └── main.py              # FastAPI application
├── tests/
│   ├── unit/                # Unit tests
│   └── integration/         # Integration tests
├── requirements.txt
├── README.md
└── API_DOCUMENTATION.md
```

## Architecture

### Layered Architecture

1. **Models Layer**: SQLAlchemy ORM models define database schema
2. **Schemas Layer**: Pydantic models for request/response validation
3. **Services Layer**: Business logic and database operations
4. **Routers Layer**: HTTP endpoints and request handling

### Key Design Patterns

- **Dependency Injection**: FastAPI's dependency system for database sessions
- **Repository Pattern**: Services abstract database operations
- **DTO Pattern**: Pydantic schemas separate API contracts from database models

## Coding Standards

### Python Style

- Follow PEP 8
- Use type hints for function parameters and return values
- Maximum line length: 100 characters
- Use docstrings for classes and complex functions

### Naming Conventions

- **Classes**: PascalCase (e.g., `QuestionnaireService`)
- **Functions/Methods**: snake_case (e.g., `create_questionnaire`)
- **Variables**: snake_case (e.g., `questionnaire_id`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `MAX_PAGE_SIZE`)

### Database Models

- Use descriptive table names in plural form
- Define relationships explicitly
- Use appropriate indexes for foreign keys
- Add constraints for data integrity

### API Endpoints

- Use RESTful conventions
- Version APIs in production (e.g., `/api/v1/`)
- Include comprehensive OpenAPI documentation
- Return appropriate HTTP status codes

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/unit/test_assessment_service.py

# Run specific test
pytest tests/unit/test_assessment_service.py::test_start_assessment
```

### Writing Tests

#### Unit Tests

Test individual functions and methods in isolation:

```python
def test_create_questionnaire(db_session):
    questionnaire_data = QuestionnaireCreate(
        title="Test",
        description="Test description"
    )
    
    questionnaire = QuestionnaireService.create_questionnaire(
        db_session, questionnaire_data
    )
    
    assert questionnaire.id is not None
    assert questionnaire.title == "Test"
```

#### Integration Tests

Test complete API workflows:

```python
def test_complete_assessment_flow(client):
    # Create questionnaire
    questionnaire_response = client.post(
        "/api/questionnaires/",
        json={"title": "Test", "description": "Test"}
    )
    
    # Add questions
    # Start assessment
    # Submit responses
    # Verify completion
```

### Test Coverage

- Aim for at least 80% code coverage
- Test both success and failure scenarios
- Test edge cases and boundary conditions
- Mock external dependencies

## Adding New Features

### 1. Add Database Model

Create or modify model in `app/models/`:

```python
from sqlalchemy import Column, Integer, String
from app.database import Base

class NewModel(Base):
    __tablename__ = "new_models"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
```

### 2. Add Pydantic Schemas

Create schemas in `app/schemas/`:

```python
from pydantic import BaseModel

class NewModelCreate(BaseModel):
    name: str

class NewModelResponse(NewModelCreate):
    id: int
    
    model_config = {"from_attributes": True}
```

### 3. Add Service Layer

Create service in `app/services/`:

```python
from sqlalchemy.orm import Session

class NewModelService:
    @staticmethod
    def create(db: Session, data: NewModelCreate):
        db_model = NewModel(**data.model_dump())
        db.add(db_model)
        db.commit()
        db.refresh(db_model)
        return db_model
```

### 4. Add API Router

Create router in `app/routers/`:

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/new-models", tags=["New Models"])

@router.post("/", response_model=NewModelResponse, status_code=201)
def create(data: NewModelCreate, db: Session = Depends(get_db)):
    return NewModelService.create(db, data)
```

### 5. Register Router

Add to `app/main.py`:

```python
from app.routers import new_models_router

app.include_router(new_models_router)
```

### 6. Add Tests

Create unit tests in `tests/unit/` and integration tests in `tests/integration/`.

## Database Migrations

For production use, implement Alembic migrations:

```bash
# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Add new table"

# Apply migration
alembic upgrade head
```

## Common Issues

### Import Errors

- Ensure virtual environment is activated
- Check `PYTHONPATH` includes project root
- Verify all dependencies are installed

### Database Errors

- Delete `questionnaire.db` and restart to reset database
- Check SQLAlchemy connection string
- Verify table relationships are correctly defined

### Test Failures

- Ensure test database is clean (use fixtures)
- Check for test interdependencies
- Verify mock data is valid

## Pull Request Process

1. Create a feature branch from `main`
2. Make your changes with clear commit messages
3. Add/update tests for your changes
4. Ensure all tests pass
5. Update documentation if needed
6. Submit pull request with description of changes

## Code Review Checklist

- [ ] Code follows project style guidelines
- [ ] Tests added/updated and passing
- [ ] Documentation updated
- [ ] No unnecessary dependencies added
- [ ] Error handling is appropriate
- [ ] API changes are backward compatible
- [ ] OpenAPI documentation is complete

## Performance Guidelines

- Use pagination for list endpoints
- Add database indexes for frequently queried fields
- Use `db.flush()` instead of `db.commit()` when checking intermediate state
- Avoid N+1 queries (use eager loading)
- Cache static data when appropriate

## Security Guidelines

- Validate all user input
- Use parameterized queries (SQLAlchemy handles this)
- Implement authentication for production
- Add rate limiting
- Log security-relevant events
- Don't expose sensitive data in error messages

## Documentation

- Keep README.md up to date
- Document all API endpoints with OpenAPI tags
- Add docstrings to complex functions
- Update API_DOCUMENTATION.md for endpoint changes
- Include usage examples in documentation

## Questions?

Open an issue or contact the maintainers.
# Contributing to NIST Reports

Thank you for your interest in contributing to the NIST Reports project! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone <your-fork-url>`
3. Add upstream remote: `git remote add upstream <original-repo-url>`
4. Create a branch: `git checkout -b feature/your-feature-name`

## Development Setup

Follow the setup instructions in the [README.md](README.md) to get your development environment running.

## Code Style Guidelines

### Python (Backend)

- Follow [PEP 8](https://pep8.org/) style guide
- Use [Black](https://github.com/psf/black) for code formatting (line length: 100)
- Use [Ruff](https://github.com/astral-sh/ruff) for linting
- Add type hints where possible
- Write docstrings for functions and classes
- Maximum line length: 100 characters

```python
# Good
def generate_report(user_id: int, report_type: str) -> dict:
    """Generate a NIST security report for a user.
    
    Args:
        user_id: The ID of the user requesting the report
        report_type: The type of report to generate
        
    Returns:
        A dictionary containing the report data
    """
    pass
```

### TypeScript (Frontend)

- Follow the project's ESLint configuration
- Use [Prettier](https://prettier.io/) for code formatting
- Use TypeScript types instead of `any` when possible
- Use functional components with hooks
- Maximum line length: 100 characters

```typescript
// Good
interface ReportProps {
  reportId: string;
  onComplete: (report: Report) => void;
}

export default function ReportComponent({ reportId, onComplete }: ReportProps) {
  // Component logic
}
```

## Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples
```
feat(backend): add NIST API integration
fix(frontend): resolve report rendering issue
docs: update installation instructions
test(backend): add unit tests for report generation
```

## Pull Request Process

1. **Update your branch** with the latest changes from upstream:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Test your changes**:
   ```bash
   make test
   ```

3. **Ensure code quality**:
   ```bash
   # Backend
   cd backend
   black .
   ruff check .
   mypy .
   
   # Frontend
   cd frontend
   npm run lint
   npm run type-check
   ```

4. **Push your branch**:
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request** on GitHub with:
   - Clear title and description
   - Reference to any related issues
   - Screenshots (if UI changes)
   - Test results

6. **Address review comments** and update your PR as needed

## Testing Guidelines

### Backend Tests

- Write tests for all new features
- Aim for at least 80% code coverage
- Use pytest fixtures for common test data
- Test both success and error cases

```python
def test_generate_report_success():
    response = client.post("/api/reports", json={"type": "security"})
    assert response.status_code == 200
    assert "report_id" in response.json()

def test_generate_report_invalid_type():
    response = client.post("/api/reports", json={"type": "invalid"})
    assert response.status_code == 400
```

### Frontend Tests

- Write tests for components and utilities
- Test user interactions and edge cases
- Use meaningful test descriptions

## Documentation

- Update README.md if you change setup or usage
- Update API documentation for new endpoints
- Add inline comments for complex logic
- Update architecture docs for significant changes

## Questions or Issues?

- Check existing issues before creating a new one
- Provide detailed information in issue reports
- Use issue templates when available
- Be respectful and constructive in discussions

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).
