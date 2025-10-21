# NIST Security Report Automation

Automate NIST security report generation for end users to easily generate comprehensive security assessments and compliance reports.

## Overview

This system provides a comprehensive framework for conducting security assessments based on NIST Cybersecurity Framework (CSF) 2.0 and other NIST standards. It includes database models, migrations, seed data, and a service layer for managing controls, assessments, and responses.

## Features

- **NIST CSF 2.0 Support**: Complete taxonomy of control families and controls
- **Implementation Tiers**: Support for NIST's 4-tier maturity model
- **Flexible Questionnaires**: Multiple question types (multiple choice, text, rating, yes/no, file upload)
- **Assessment Management**: Full lifecycle management from draft to completion
- **Evidence Collection**: Metadata tracking for supporting evidence and artifacts
- **Version Support**: Handle multiple framework versions simultaneously
- **Repository Pattern**: Clean separation of data access and business logic
- **Database Migrations**: Alembic-based schema versioning

## Architecture

```
src/nist_automation/
├── models/              # SQLAlchemy ORM models
│   ├── control_family.py
│   ├── control.py
│   ├── implementation_tier.py
│   ├── question.py
│   ├── option.py
│   ├── assessment.py
│   ├── assessment_session.py
│   ├── response.py
│   └── evidence.py
├── repositories/        # Data access layer
│   └── base.py
├── services/           # Business logic layer
│   └── crud_service.py
├── seeds/              # Seed data and loaders
│   ├── nist_csf_data.py
│   └── seed_runner.py
├── config.py           # Application configuration
└── database.py         # Database setup and session management

alembic/
├── versions/           # Database migration files
│   └── 001_initial_schema.py
├── env.py              # Alembic environment
└── script.py.mako      # Migration template

docs/
└── DATA_LOADING.md     # Comprehensive data loading documentation
```

## Installation

### Prerequisites

- Python 3.9+
- PostgreSQL 12+

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd nist_generation_test
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e .
```

4. Configure database:
Create a `.env` file:
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/nist_automation
ECHO_SQL=false
ENVIRONMENT=development
```

5. Create database:
```bash
createdb nist_automation
```

6. Run migrations:
```bash
alembic upgrade head
```

7. Load seed data:
```bash
python -m src.nist_automation.seeds.seed_runner
```

## Database Models

### Core Entities

- **ControlFamily**: NIST CSF categories (Govern, Identify, Protect, Detect, Respond, Recover)
- **Control**: Individual security controls within families
- **ImplementationTier**: Maturity levels (Partial, Risk Informed, Repeatable, Adaptive)
- **Question**: Assessment questions linked to controls
- **Option**: Response options for multiple choice questions
- **Assessment**: Assessment instance with metadata
- **AssessmentSession**: User session tracking
- **Response**: User responses to questions
- **Evidence**: Evidence file metadata

### Key Features

- **Versioning**: Support for multiple framework versions
- **Hierarchical Controls**: Self-referencing parent-child relationships
- **Flexible Questions**: Multiple question types with scoring
- **Cascade Deletes**: Proper referential integrity
- **Performance Indices**: Optimized for common query patterns

## Usage

### Using the Service Layer

```python
from src.nist_automation.database import SessionLocal
from src.nist_automation.services import CRUDService

# Initialize
db = SessionLocal()
service = CRUDService(db)

# Get control families
families = service.get_control_families(framework="NIST_CSF")

# Get controls for a family
controls = service.get_controls(family_id=family.id)

# Create assessment
assessment = service.create_assessment(
    name="Q4 2024 Security Assessment",
    framework="NIST_CSF",
    framework_version="2.0",
    organization_name="Acme Corp",
    status="DRAFT"
)

# Get questions for a control
questions = service.get_questions(control_id=control.id)

# Submit response
response = service.create_response(
    assessment_id=assessment.id,
    question_id=question.id,
    option_id=option.id,
    version="1.0"
)

# Add evidence
evidence = service.create_evidence(
    response_id=response.id,
    file_name="policy_document.pdf",
    file_size=1048576,
    mime_type="application/pdf"
)

db.close()
```

### Using the Repository Layer

```python
from src.nist_automation.repositories import BaseRepository
from src.nist_automation.models import Control
from src.nist_automation.database import SessionLocal

db = SessionLocal()
control_repo = BaseRepository(Control, db)

# Get by filters
active_controls = control_repo.get_by_filters(
    {"is_active": True, "priority": "high"}
)

# Bulk create
controls = control_repo.bulk_create([
    {"code": "CTRL-1", "name": "Control 1", ...},
    {"code": "CTRL-2", "name": "Control 2", ...},
])

# Count
total = control_repo.count({"framework": "NIST_CSF"})

db.close()
```

## Seed Data

The system includes seed data for NIST CSF 2.0:

- **6 Control Families**: Complete NIST CSF 2.0 function taxonomy
- **15 Sample Controls**: Representative controls from each family
- **4 Implementation Tiers**: NIST maturity model
- **7 Sample Questions**: Demonstrating all question types

### Extending Seed Data

To add more controls:

1. Edit `src/nist_automation/seeds/nist_csf_data.py`
2. Add entries to `NIST_CSF_CONTROLS` list
3. Run seed script:
```bash
python -m src.nist_automation.seeds.seed_runner
```

## Database Migrations

### Common Commands

```bash
# Apply all migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Check current version
alembic current

# View history
alembic history

# Create new migration
alembic revision --autogenerate -m "Description"
```

### Migration Structure

Migrations include:
- Table creation with proper types
- Foreign key constraints with cascades
- Unique constraints on codes
- Performance indices
- Enum types for status fields

## Configuration

### Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `ECHO_SQL`: Enable SQLAlchemy query logging (true/false)
- `ENVIRONMENT`: Environment name (development/production)

### Database Connection

Default: `postgresql://postgres:postgres@localhost:5432/nist_automation`

Configure via environment variable or `.env` file.

## Documentation

- [Data Loading Workflow](docs/DATA_LOADING.md): Comprehensive guide to data loading, migrations, and CRUD operations

## Development

### Project Structure

- `src/nist_automation/`: Main application code
- `alembic/`: Database migrations
- `docs/`: Documentation
- `requirements.txt`: Python dependencies
- `pyproject.toml`: Project metadata and build configuration

### Adding New Models

1. Create model file in `src/nist_automation/models/`
2. Import in `src/nist_automation/models/__init__.py`
3. Generate migration: `alembic revision --autogenerate -m "Add model"`
4. Review and apply: `alembic upgrade head`

### Adding New Seeds

1. Add data to `src/nist_automation/seeds/nist_csf_data.py`
2. Update `seed_runner.py` if new entity types
3. Run seeds: `python -m src.nist_automation.seeds.seed_runner`

## Testing

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests (when implemented)
pytest

# Type checking
mypy src/

# Code formatting
black src/

# Linting
flake8 src/
```

## Roadmap

- [ ] Complete NIST 800-53 Rev. 5 control catalog
- [ ] Control mapping between frameworks (CSF ↔ 800-53 ↔ ISO 27001)
- [ ] REST API for assessments
- [ ] Web UI for assessment completion
- [ ] Report generation (PDF, DOCX)
- [ ] Risk scoring and analytics
- [ ] User authentication and authorization
- [ ] Audit trail and versioning
- [ ] OSCAL import/export
- [ ] Multi-tenant support

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Submit pull request

## License

[License information to be added]

## References

- [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework)
- [NIST SP 800-53 Rev. 5](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
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
