# NIST Questionnaire Engine API

Automate NIST security report generation with an intelligent questionnaire engine featuring branching logic and session management.

## Features

- **Dynamic Questionnaires**: Create and manage questionnaires with versioning and categorization
- **Intelligent Branching**: Questions adapt based on previous answers with dependency validation
- **Session Management**: Start, pause, and resume assessment sessions with full state persistence
- **Transactional Integrity**: All responses saved with ACID compliance
- **REST API**: Comprehensive OpenAPI-documented endpoints
- **Pagination & Filtering**: Efficient data retrieval for large questionnaires

## Quick Start

### Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Overview

### Questionnaires

- `POST /api/questionnaires/` - Create a new questionnaire
- `GET /api/questionnaires/` - List questionnaires (with pagination and filters)
- `GET /api/questionnaires/{id}` - Get questionnaire details
- `PATCH /api/questionnaires/{id}` - Update questionnaire
- `DELETE /api/questionnaires/{id}` - Delete questionnaire

### Questions

- `POST /api/questions/` - Create a new question
- `GET /api/questions/questionnaire/{id}` - List questions for a questionnaire
- `GET /api/questions/{id}` - Get question details
- `PATCH /api/questions/{id}` - Update question
- `DELETE /api/questions/{id}` - Delete question

### Assessments

- `POST /api/assessments/start` - Start a new assessment session
- `GET /api/assessments/sessions/{token}` - Get session details
- `GET /api/assessments/sessions/{token}/next-question` - Get next question based on branching logic
- `POST /api/assessments/responses` - Submit a response
- `GET /api/assessments/sessions/{token}/responses` - Get all responses for a session
- `POST /api/assessments/sessions/{token}/resume` - Resume a paused session

## Usage Examples

### Creating a Questionnaire

```bash
curl -X POST "http://localhost:8000/api/questionnaires/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "NIST 800-53 Security Assessment",
    "description": "Comprehensive security controls assessment",
    "category": "security",
    "version": "1.0"
  }'
```

### Adding Questions with Branching Logic

```bash
curl -X POST "http://localhost:8000/api/questions/" \
  -H "Content-Type: application/json" \
  -d '{
    "questionnaire_id": 1,
    "question_text": "Do you have a dedicated security team?",
    "question_type": "yes_no",
    "order_index": 0,
    "branching_rules": [
      {
        "condition": "equals",
        "value": "yes",
        "next_question_id": 3
      }
    ]
  }'
```

### Starting an Assessment

```bash
curl -X POST "http://localhost:8000/api/assessments/start" \
  -H "Content-Type: application/json" \
  -d '{
    "questionnaire_id": 1,
    "user_id": "user123"
  }'
```

### Submitting a Response

```bash
curl -X POST "http://localhost:8000/api/assessments/responses" \
  -H "Content-Type: application/json" \
  -d '{
    "session_token": "your-session-token",
    "question_id": 1,
    "answer_value": "yes"
  }'
```

## Question Types

- `text` - Free-form text input
- `multiple_choice` - Select from predefined options
- `yes_no` - Binary choice
- `rating` - Numeric rating scale
- `number` - Numeric input

## Branching Logic

Questions can have branching rules that determine the next question based on the answer:

- **equals**: Show next question if answer matches value
- **not_equals**: Show next question if answer doesn't match value
- **contains**: Show next question if answer contains value

## Dependencies

Questions can depend on previous questions:

```json
{
  "depends_on_question_id": 5,
  "depends_on_answer": "yes"
}
```

This ensures questions only appear when dependencies are met.

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/unit/test_assessment_service.py
```

## Database

By default, the application uses SQLite (`questionnaire.db`). For production, configure a PostgreSQL connection:

```bash
export DATABASE_URL="postgresql://user:password@localhost/dbname"
```

## Architecture

- **Models**: SQLAlchemy ORM models for database tables
- **Schemas**: Pydantic models for request/response validation
- **Services**: Business logic layer with transactional operations
- **Routers**: FastAPI route handlers with OpenAPI documentation

## License

MIT
