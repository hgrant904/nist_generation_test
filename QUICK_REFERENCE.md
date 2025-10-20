# Quick Reference Guide

Essential commands and information for NIST Reports development.

## 🚀 Getting Started

```bash
# Clone and setup
git clone <repo-url>
cd nist_generation_test
cp .env.example .env

# Start everything (Docker)
make dev

# Or without Make
docker-compose up
```

## 📦 Common Commands

### Using Make (Recommended)

```bash
make help            # Show all available commands
make dev             # Start development environment
make up              # Start services (detached)
make down            # Stop all services
make restart         # Restart all services
make logs            # Show logs from all services
make build           # Build Docker images
make rebuild         # Rebuild from scratch
make clean           # Remove containers and volumes
make test            # Run all tests
make backend-test    # Run backend tests only
make frontend-test   # Run frontend tests only
make backend-shell   # Open shell in backend container
make frontend-shell  # Open shell in frontend container
make db-shell        # Open PostgreSQL shell
```

### Docker Compose (Without Make)

```bash
docker-compose up              # Start services (foreground)
docker-compose up -d           # Start services (background)
docker-compose down            # Stop services
docker-compose down -v         # Stop and remove volumes
docker-compose logs -f         # Follow logs
docker-compose ps              # Show running services
docker-compose build           # Build images
docker-compose restart         # Restart services
docker-compose exec backend bash    # Backend shell
docker-compose exec frontend sh     # Frontend shell
docker-compose exec postgres psql -U nist_user -d nist_reports  # DB shell
```

## 🔧 Backend Commands

```bash
cd backend

# Virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
deactivate

# Dependencies
pip install -r requirements.txt
pip freeze > requirements.txt

# Run server
uvicorn app.main:app --reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Testing
pytest                       # Run all tests
pytest -v                    # Verbose output
pytest --cov=app tests/      # With coverage
pytest tests/test_main.py    # Specific file

# Code quality
black .                      # Format code
black --check .              # Check formatting
ruff check .                 # Lint code
ruff check --fix .           # Fix linting issues
mypy .                       # Type checking
```

## 💻 Frontend Commands

```bash
cd frontend

# Dependencies
npm install                  # Install dependencies
npm update                   # Update dependencies
npm outdated                 # Check outdated packages

# Development
npm run dev                  # Start dev server
npm run build                # Build for production
npm start                    # Start production server

# Code quality
npm run lint                 # Lint code
npm run lint -- --fix        # Fix linting issues
npm run format               # Format code
npm run type-check           # TypeScript type checking

# Testing (when configured)
npm test                     # Run tests
npm test -- --watch          # Watch mode
npm test -- --coverage       # With coverage
```

## 🗄️ Database Commands

```bash
# Access database shell
docker-compose exec postgres psql -U nist_user -d nist_reports

# Common SQL commands
\l                          # List databases
\dt                         # List tables
\d table_name              # Describe table
\q                          # Quit

# Backup and restore
docker-compose exec postgres pg_dump -U nist_user nist_reports > backup.sql
docker-compose exec -T postgres psql -U nist_user nist_reports < backup.sql

# Database migrations (Alembic)
docker-compose exec backend alembic revision --autogenerate -m "description"
docker-compose exec backend alembic upgrade head
docker-compose exec backend alembic downgrade -1
docker-compose exec backend alembic history
docker-compose exec backend alembic current
```

## 🌐 URLs

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation (Swagger): http://localhost:8000/docs
- API Documentation (ReDoc): http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

## 📁 Important Files

```
.env                        # Environment variables (create from .env.example)
docker-compose.yml          # Service orchestration
Makefile                    # Convenience commands
backend/requirements.txt    # Python dependencies
backend/app/main.py        # Backend entry point
frontend/package.json       # Node dependencies
frontend/src/app/page.tsx  # Frontend home page
```

## 🔍 Debugging

```bash
# View logs
docker-compose logs -f                    # All services
docker-compose logs -f backend            # Backend only
docker-compose logs -f frontend           # Frontend only
docker-compose logs -f postgres           # Database only

# Check service health
./scripts/health-check.sh

# Inspect containers
docker-compose ps                         # List containers
docker inspect nist-reports-backend       # Inspect container
docker stats                              # Resource usage

# Network debugging
docker network ls                         # List networks
docker network inspect nist-network       # Inspect network
```

## 🐛 Troubleshooting

```bash
# Port already in use
lsof -i :8000                             # Find process using port
kill -9 <PID>                            # Kill process

# Permission issues
sudo chown -R $USER:$USER .              # Fix ownership

# Docker issues
docker system prune                       # Clean up unused resources
docker system prune -a --volumes         # Clean everything
docker-compose down -v && docker-compose up --build  # Fresh start

# Backend issues
cd backend && rm -rf __pycache__ .pytest_cache
cd backend && pip install -r requirements.txt --force-reinstall

# Frontend issues
cd frontend && rm -rf node_modules .next package-lock.json
cd frontend && npm install

# Database issues
docker-compose down -v                    # Remove database
docker volume rm nist_generation_test_postgres_data
docker-compose up -d postgres            # Recreate database
```

## 🧪 Testing Endpoints

```bash
# Using curl
curl http://localhost:8000/
curl http://localhost:8000/health

# Using httpie (if installed)
http GET http://localhost:8000/
http GET http://localhost:8000/health

# Using Python
python -c "import requests; print(requests.get('http://localhost:8000/health').json())"
```

## 📝 Git Commands

```bash
# Branch management
git checkout -b feature/my-feature        # Create and switch to branch
git branch -a                             # List all branches
git push origin feature/my-feature        # Push branch

# Commit
git add .                                 # Stage changes
git commit -m "feat: add new feature"    # Commit with message
git push                                  # Push to remote

# Update
git fetch origin                          # Fetch updates
git pull origin main                      # Pull from main
git rebase origin/main                    # Rebase on main

# Cleanup
git branch -d feature/my-feature         # Delete local branch
git push origin --delete feature/my-feature  # Delete remote branch
```

## 🔐 Environment Variables

Key variables to configure in `.env`:

```bash
# Database
POSTGRES_DB=nist_reports
POSTGRES_USER=nist_user
POSTGRES_PASSWORD=your_secure_password

# Backend
BACKEND_PORT=8000
DEBUG=true
SECRET_KEY=your-secret-key

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
FRONTEND_PORT=3000

# CORS
ALLOWED_ORIGINS=http://localhost:3000
```

## 📊 Project Statistics

```bash
# Line counts
find backend -name "*.py" | xargs wc -l
find frontend/src -name "*.tsx" -o -name "*.ts" | xargs wc -l

# File counts
find backend -type f -name "*.py" | wc -l
find frontend/src -type f | wc -l

# Dependencies
pip list                                  # Python packages
npm list --depth=0                        # Node packages
```

## 🔄 Update Dependencies

```bash
# Backend
cd backend
pip list --outdated                       # Check outdated packages
pip install --upgrade package_name        # Update specific package

# Frontend
cd frontend
npm outdated                              # Check outdated packages
npm update                                # Update all packages
npm install package@latest                # Update specific package
```

## 📚 Documentation Locations

- Main README: `./README.md`
- Setup Guide: `./SETUP.md`
- Architecture: `./docs/architecture.md`
- Development Guide: `./docs/development.md`
- Contributing: `./CONTRIBUTING.md`
- Project Structure: `./PROJECT_STRUCTURE.md`
- Backend Docs: `./backend/README.md`
- Frontend Docs: `./frontend/README.md`

## 🆘 Get Help

```bash
# Show help
make help                                 # Makefile commands
docker-compose --help                     # Docker Compose help
pytest --help                             # Pytest help
npm --help                                # npm help

# Check versions
python --version
node --version
docker --version
docker-compose --version
```

## 💡 Pro Tips

1. Use `make` commands for consistency
2. Keep Docker images updated: `docker-compose pull`
3. Use `.env` for local customization
4. Check health before debugging: `./scripts/health-check.sh`
5. Read logs when something fails: `docker-compose logs -f`
6. Use `-v` flag for verbose output when debugging
7. Keep dependencies updated regularly
8. Run tests before committing: `make test`
9. Format code before committing: `black .` and `npm run format`
10. Use interactive API docs: http://localhost:8000/docs
