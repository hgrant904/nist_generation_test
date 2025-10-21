# Changelog

All notable changes to the NIST Reports project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial monorepo structure with backend, frontend, and docs directories
- FastAPI backend service with health endpoint and CORS configuration
- Next.js 14 frontend with TypeScript and App Router
- PostgreSQL database configuration with Docker Compose
- Docker Compose orchestration for all services with networking and volumes
- Comprehensive documentation:
  - Main README with quick start guide
  - SETUP.md with detailed setup instructions
  - CONTRIBUTING.md with contribution guidelines
  - PROJECT_STRUCTURE.md with structure documentation
  - QUICK_REFERENCE.md with command reference
  - docs/architecture.md with system architecture
  - docs/development.md with development guide
- Development tooling:
  - Makefile with 15+ convenience commands
  - scripts/init-project.sh for automated setup
  - scripts/health-check.sh for service verification
  - scripts/db-init.sql for database initialization
- Configuration files:
  - .env.example with all environment variables
  - .gitignore for Python, Node.js, and Docker
  - docker-compose.yml with three services
  - Backend: Dockerfile, requirements.txt, pyproject.toml
  - Frontend: package.json, tsconfig.json, next.config.js, Dockerfiles
- Code quality tools:
  - Backend: Black, Ruff, mypy, pytest
  - Frontend: ESLint, Prettier, TypeScript
- MIT License
- Backend test suite with basic API tests
- Hot-reload support for development

### Infrastructure
- PostgreSQL 16 Alpine container with health checks
- FastAPI backend container with volume mounts
- Next.js frontend container with development setup
- Custom Docker network (nist-network) for service communication
- Persistent volumes for database and caching

### Documentation
- Complete project documentation (2,500+ lines)
- API documentation auto-generation (Swagger/ReDoc)
- Backend and frontend READMEs
- Scripts documentation
- Contribution guidelines with code style standards

## [0.1.0] - 2024-10-15

### Initial Release
- Project scaffolding and monorepo structure
- Development environment setup
- Basic backend and frontend applications
- Docker containerization
- Comprehensive documentation
