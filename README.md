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
# NIST Security Report Automation

Automate NIST security report generation for end users to easily generate comprehensive security reports.

## 🏗️ Project Structure

This is a monorepo containing the following components:

```
nist_generation_test/
├── backend/              # FastAPI backend service
│   ├── app/             # Application code
│   ├── tests/           # Backend tests
│   ├── Dockerfile       # Backend container configuration
│   └── requirements.txt # Python dependencies
├── frontend/            # Next.js frontend application
│   ├── src/            # Source code
│   ├── public/         # Static assets
│   ├── Dockerfile.dev  # Development container
│   └── package.json    # Node dependencies
├── docs/               # Project documentation
├── docker-compose.yml  # Docker orchestration
├── Makefile           # Development commands
└── .env.example       # Environment variable template
```

## 🚀 Quick Start

### Prerequisites

Before you begin, ensure you have the following installed:
- **Docker** (20.10+) and **Docker Compose** (2.0+)
- **Node.js** (20+) and **npm** (for local development without Docker)
- **Python** (3.11+) and **pip** (for local development without Docker)
- **Make** (optional, for convenience commands)

### Getting Started with Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd nist_generation_test
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration (optional for development)
   ```

3. **Start the services**
   ```bash
   make dev
   # Or without Make:
   docker-compose up
   ```

4. **Access the applications**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Local Development without Docker

#### Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp ../.env.example .env
# Edit .env with your configuration

# Start the backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp ../.env.example .env.local
# Edit .env.local with your configuration

# Start the development server
npm run dev
```

#### Database Setup

For local development without Docker, you'll need to install and run PostgreSQL:

```bash
# On macOS with Homebrew
brew install postgresql@16
brew services start postgresql@16

# On Ubuntu/Debian
sudo apt-get install postgresql-16
sudo systemctl start postgresql

# Create database and user
psql postgres
CREATE DATABASE nist_reports;
CREATE USER nist_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE nist_reports TO nist_user;
\q
```

## 📦 Available Commands

If you have Make installed, you can use these convenience commands:

```bash
make help            # Show all available commands
make dev             # Start development environment
make up              # Start services in detached mode
make down            # Stop all services
make build           # Build Docker images
make rebuild         # Rebuild images from scratch
make restart         # Restart all services
make logs            # Show service logs
make clean           # Remove containers, volumes, and cache
make test            # Run all tests
make backend-test    # Run backend tests only
make frontend-test   # Run frontend tests only
make backend-shell   # Open shell in backend container
make frontend-shell  # Open shell in frontend container
make db-shell        # Open PostgreSQL shell
```

## 🔧 Configuration

### Environment Variables

The project uses environment variables for configuration. Copy `.env.example` to `.env` and customize:

**Backend Configuration:**
- `BACKEND_PORT`: Backend server port (default: 8000)
- `DATABASE_URL`: PostgreSQL connection string
- `DEBUG`: Enable debug mode (default: true)
- `SECRET_KEY`: Application secret key
- `ALLOWED_ORIGINS`: CORS allowed origins

**Frontend Configuration:**
- `NEXT_PUBLIC_API_URL`: Backend API URL (default: http://localhost:8000)
- `FRONTEND_PORT`: Frontend server port (default: 3000)

**Database Configuration:**
- `POSTGRES_HOST`: Database host (default: postgres)
- `POSTGRES_PORT`: Database port (default: 5432)
- `POSTGRES_DB`: Database name (default: nist_reports)
- `POSTGRES_USER`: Database user
- `POSTGRES_PASSWORD`: Database password

## 🧪 Testing

### Running Tests

```bash
# Run all tests
make test

# Backend tests only
make backend-test
# Or: cd backend && pytest

# Frontend tests only
make frontend-test
# Or: cd frontend && npm test

# Backend tests with coverage
cd backend && pytest --cov=app tests/
```

## 📖 API Documentation

Once the backend is running, you can access interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🏗️ Technology Stack

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.11+
- **Database**: PostgreSQL 16
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Testing**: pytest

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Package Manager**: npm
- **HTTP Client**: Axios

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Database**: PostgreSQL 16
- **Reverse Proxy**: (To be added)

## 🔄 Development Workflow

1. **Create a new branch** for your feature or bugfix
2. **Make your changes** following the coding standards
3. **Test your changes** locally
4. **Commit your changes** with descriptive commit messages
5. **Push your branch** and create a pull request

### Code Style

**Backend (Python):**
- Follow PEP 8 guidelines
- Use Black for formatting: `black .`
- Use Ruff for linting: `ruff check .`
- Type hints are encouraged

**Frontend (TypeScript):**
- Follow the project's ESLint configuration
- Use Prettier for formatting: `npm run format`
- Run type checking: `npm run type-check`

## 🐳 Docker Services

The `docker-compose.yml` defines three services:

1. **postgres**: PostgreSQL database with persistent volume
2. **backend**: FastAPI application with hot-reload
3. **frontend**: Next.js application with hot-reload

All services are connected via a custom bridge network `nist-network`.

### Volumes
- `postgres_data`: Persistent database storage
- `backend_cache`: Python cache directory

## 📝 Project Roadmap

- [x] Initial project setup
- [x] Docker containerization
- [x] Basic backend API structure
- [x] Basic frontend structure
- [ ] Database models and migrations
- [ ] Authentication system
- [ ] NIST API integration
- [ ] Report generation logic
- [ ] User dashboard
- [ ] Export functionality
- [ ] Deployment configuration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For questions or issues, please:
- Open an issue on GitHub
- Contact the development team
- Refer to the documentation in the `docs/` directory

## 🙏 Acknowledgments

- NIST for providing security standards and guidelines
- FastAPI and Next.js communities for excellent frameworks
