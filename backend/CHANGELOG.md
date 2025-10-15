# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-10-15

### Added
- Initial FastAPI backend foundation
- Application factory pattern with main.py
- Async SQLAlchemy 2.0 integration with PostgreSQL
- Alembic database migration scaffolding
- Pydantic v2 settings management from environment variables
- Structured logging configuration
- Database session management with async engine
- Health check endpoints (`/api/v1/health` and `/api/v1/health/db`)
- Comprehensive test suite with pytest and pytest-asyncio
- Code quality tools integration (Black, Ruff, Mypy)
- Docker and docker-compose configuration
- Development scripts (start.sh, test.sh)
- Project documentation (README.md, CONTRIBUTING.md)
- Example environment configuration (.env.example)

### Infrastructure
- Python 3.11+ support
- Virtual environment setup
- Requirements files for pip (requirements.txt, requirements-dev.txt)
- Poetry configuration (pyproject.toml)
- Makefile for common tasks
- .gitignore and .dockerignore files

### Testing
- Smoke tests for health endpoints
- Test fixtures with in-memory SQLite database
- 79% code coverage

### Documentation
- Comprehensive README with setup and usage instructions
- Contributing guidelines
- API documentation via Swagger UI and ReDoc
- Inline code documentation and docstrings
