# API Documentation

## Overview

The NIST Questionnaire Engine API provides comprehensive endpoints for creating and managing questionnaires with intelligent branching logic. This document provides detailed information about all available endpoints.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API does not require authentication. For production use, implement JWT or OAuth2 authentication.

## Endpoints

### Questionnaires

#### Create Questionnaire

Create a new questionnaire to organize questions.

```http
POST /api/questionnaires/
```

**Request Body:**
```json
{
  "title": "NIST 800-53 Security Assessment",
  "description": "Comprehensive security controls assessment",
  "category": "security",
  "version": "1.0",
  "is_active": true
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "title": "NIST 800-53 Security Assessment",
  "description": "Comprehensive security controls assessment",
  "category": "security",
  "version": "1.0",
  "is_active": true,
  "created_at": "2025-10-15T12:00:00",
  "updated_at": null
}
```

#### List Questionnaires

Retrieve a paginated list of questionnaires with optional filtering.

```http
GET /api/questionnaires/?page=1&page_size=10&category=security&is_active=true
```

**Query Parameters:**
- `page` (integer, default: 1): Page number
- `page_size` (integer, default: 10, max: 100): Items per page
- `category` (string, optional): Filter by category
- `is_active` (boolean, optional): Filter by active status

**Response (200 OK):**
```json
{
  "items": [...],
  "total": 50,
  "page": 1,
  "page_size": 10,
  "total_pages": 5
}
```

#### Get Questionnaire

Retrieve a specific questionnaire by ID.

```http
GET /api/questionnaires/{questionnaire_id}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "NIST 800-53 Security Assessment",
  "description": "Comprehensive security controls assessment",
  "category": "security",
  "version": "1.0",
  "is_active": true,
  "created_at": "2025-10-15T12:00:00",
  "updated_at": null
}
```

#### Update Questionnaire

Update specific fields of a questionnaire.

```http
PATCH /api/questionnaires/{questionnaire_id}
```

**Request Body:**
```json
{
  "title": "Updated Title",
  "is_active": false
}
```

**Response (200 OK):** Returns updated questionnaire

#### Delete Questionnaire

Delete a questionnaire and all associated questions and sessions.

```http
DELETE /api/questionnaires/{questionnaire_id}
```

**Response (204 No Content)**

### Questions

#### Create Question

Create a new question within a questionnaire.

```http
POST /api/questions/
```

**Request Body:**
```json
{
  "questionnaire_id": 1,
  "question_text": "Do you have a dedicated security team?",
  "question_type": "yes_no",
  "order_index": 0,
  "is_required": true,
  "options": null,
  "branching_rules": [
    {
      "condition": "equals",
      "value": "yes",
      "next_question_id": 3
    }
  ],
  "depends_on_question_id": null,
  "depends_on_answer": null,
  "question_metadata": {
    "nist_control": "AC-2"
  }
}
```

**Question Types:**
- `text` - Free-form text input
- `multiple_choice` - Select from predefined options
- `yes_no` - Binary choice
- `rating` - Numeric rating scale
- `number` - Numeric input

**Branching Rule Conditions:**
- `equals` - Next question if answer equals value
- `not_equals` - Next question if answer doesn't equal value
- `contains` - Next question if answer contains value

**Response (201 Created):**
```json
{
  "id": 1,
  "questionnaire_id": 1,
  "question_text": "Do you have a dedicated security team?",
  "question_type": "yes_no",
  "order_index": 0,
  "is_required": true,
  "options": null,
  "branching_rules": [...],
  "depends_on_question_id": null,
  "depends_on_answer": null,
  "question_metadata": {...}
}
```

#### List Questions for Questionnaire

Retrieve all questions for a specific questionnaire.

```http
GET /api/questions/questionnaire/{questionnaire_id}?skip=0&limit=100
```

**Query Parameters:**
- `skip` (integer, default: 0): Number of items to skip
- `limit` (integer, default: 100, max: 1000): Maximum items to return

**Response (200 OK):** Array of question objects

#### Get Question

Retrieve a specific question by ID.

```http
GET /api/questions/{question_id}
```

**Response (200 OK):** Question object

#### Update Question

Update specific fields of a question.

```http
PATCH /api/questions/{question_id}
```

**Request Body:** Partial question object

**Response (200 OK):** Updated question

#### Delete Question

Delete a question.

```http
DELETE /api/questions/{question_id}
```

**Response (204 No Content)**

### Assessments

#### Start Assessment Session

Create a new assessment session for a questionnaire.

```http
POST /api/assessments/start
```

**Request Body:**
```json
{
  "questionnaire_id": 1,
  "user_id": "user123"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "questionnaire_id": 1,
  "user_id": "user123",
  "session_token": "a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6",
  "status": "in_progress",
  "current_question_id": null,
  "started_at": "2025-10-15T12:00:00",
  "completed_at": null,
  "last_activity_at": "2025-10-15T12:00:00"
}
```

#### Get Assessment Session

Retrieve the current state of an assessment session.

```http
GET /api/assessments/sessions/{session_token}
```

**Response (200 OK):** Session object

#### Get Next Question

Resolve and return the next question based on branching logic.

```http
GET /api/assessments/sessions/{session_token}/next-question
```

**Response (200 OK):**
```json
{
  "id": 1,
  "question_text": "Do you have a dedicated security team?",
  "question_type": "yes_no",
  "is_required": true,
  "options": null,
  "question_metadata": {...}
}
```

Returns `null` when assessment is complete.

#### Submit Response

Submit an answer to a question in an assessment session.

```http
POST /api/assessments/responses
```

**Request Body:**
```json
{
  "session_token": "a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6",
  "question_id": 1,
  "answer_value": "yes"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "session_id": 1,
  "question_id": 1,
  "answer_value": "yes",
  "answered_at": "2025-10-15T12:05:00"
}
```

**Validation:**
- Session must exist and be in progress
- Question must belong to the session's questionnaire
- Question dependencies must be met
- Existing responses can be updated

#### Get Session Responses

Retrieve all responses submitted in an assessment session.

```http
GET /api/assessments/sessions/{session_token}/responses
```

**Response (200 OK):** Array of response objects

#### Resume Session

Resume a paused or in-progress assessment session.

```http
POST /api/assessments/sessions/{session_token}/resume
```

**Response (200 OK):** Updated session object

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Error message describing the problem"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "Error message",
      "type": "error_type"
    }
  ]
}
```

## Session Status Values

- `in_progress` - Session is active
- `completed` - All questions answered
- `abandoned` - Session expired or cancelled

## Complete Workflow Example

### 1. Create a Questionnaire
```bash
curl -X POST "http://localhost:8000/api/questionnaires/" \
  -H "Content-Type: application/json" \
  -d '{"title":"Security Assessment","description":"Test"}'
```

### 2. Add Questions
```bash
# Question 1
curl -X POST "http://localhost:8000/api/questions/" \
  -H "Content-Type: application/json" \
  -d '{"questionnaire_id":1,"question_text":"Have security team?","question_type":"yes_no","order_index":0}'

# Question 2 (conditional)
curl -X POST "http://localhost:8000/api/questions/" \
  -H "Content-Type: application/json" \
  -d '{"questionnaire_id":1,"question_text":"Team size?","question_type":"number","order_index":1,"depends_on_question_id":1,"depends_on_answer":"yes"}'
```

### 3. Start Assessment
```bash
curl -X POST "http://localhost:8000/api/assessments/start" \
  -H "Content-Type: application/json" \
  -d '{"questionnaire_id":1,"user_id":"user123"}'
```

### 4. Get First Question
```bash
curl "http://localhost:8000/api/assessments/sessions/{TOKEN}/next-question"
```

### 5. Submit Answer
```bash
curl -X POST "http://localhost:8000/api/assessments/responses" \
  -H "Content-Type: application/json" \
  -d '{"session_token":"{TOKEN}","question_id":1,"answer_value":"yes"}'
```

### 6. Continue Until Complete
Repeat steps 4-5 until next-question returns null.

## Interactive Documentation

Visit the following URLs when the server is running:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`
