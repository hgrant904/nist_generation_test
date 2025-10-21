# Setup Checklist

This document provides a comprehensive checklist for setting up the NIST Reports project.

## ✅ Prerequisites Checklist

Before starting, ensure you have the following installed:

- [ ] **Docker** (version 20.10+)
  ```bash
  docker --version
  ```

- [ ] **Docker Compose** (version 2.0+)
  ```bash
  docker-compose --version
  ```

- [ ] **Git**
  ```bash
  git --version
  ```

- [ ] **Make** (optional but recommended)
  ```bash
  make --version
  ```

For local development without Docker:

- [ ] **Node.js** (version 20+)
  ```bash
  node --version
  ```

- [ ] **Python** (version 3.11+)
  ```bash
  python --version
  ```

- [ ] **PostgreSQL** (version 16+)
  ```bash
  psql --version
  ```

## 🚀 Quick Setup (Docker - Recommended)

### Step 1: Clone and Navigate

```bash
git clone <repository-url>
cd nist_generation_test
```

### Step 2: Environment Configuration

```bash
cp .env.example .env
# Review and update .env if needed (optional for development)
```

### Step 3: Initialize Project

Option A - Using the initialization script:
```bash
./scripts/init-project.sh
```

Option B - Manual setup:
```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# Check health
./scripts/health-check.sh
```

### Step 4: Verify Setup

- [ ] Frontend accessible at http://localhost:3000
- [ ] Backend accessible at http://localhost:8000
- [ ] API docs accessible at http://localhost:8000/docs
- [ ] Health endpoint returns 200: http://localhost:8000/health

## 🔧 Local Setup (Without Docker)

### Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp ../.env.example .env
   # Edit .env with your local configuration
   ```

5. Ensure PostgreSQL is running and create database:
   ```bash
   createdb nist_reports
   ```

6. Run the backend:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

7. Verify: http://localhost:8000/health

### Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables:
   ```bash
   cp ../.env.example .env.local
   # Edit .env.local with your configuration
   ```

4. Run the frontend:
   ```bash
   npm run dev
   ```

5. Verify: http://localhost:3000

## 🧪 Verify Installation

Run these commands to verify everything is working:

```bash
# Check all services
make logs

# Run backend tests
cd backend && pytest

# Run frontend type checking
cd frontend && npm run type-check

# Check API health
curl http://localhost:8000/health
```

Expected outputs:
- [ ] All Docker containers are running
- [ ] Backend tests pass
- [ ] Frontend has no type errors
- [ ] API health check returns `{"status": "healthy"}`

## 🔍 Troubleshooting

### Docker Issues

**Port conflicts:**
```bash
# Check what's using the port
lsof -i :8000  # or :3000, :5432

# Stop conflicting service or change port in .env
```

**Permission issues:**
```bash
# Add user to docker group
sudo usermod -aG docker $USER
# Log out and back in
```

**Services not starting:**
```bash
# View logs
docker-compose logs -f

# Rebuild images
docker-compose build --no-cache

# Remove all containers and volumes
docker-compose down -v
```

### Backend Issues

**Import errors:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

**Database connection errors:**
```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Check environment variables
cat .env | grep POSTGRES
```

### Frontend Issues

**Module not found:**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Build errors:**
```bash
# Clear Next.js cache
rm -rf .next

# Rebuild
npm run build
```

## 📚 Next Steps

After successful setup:

1. **Read the documentation:**
   - [README.md](README.md) - Project overview
   - [docs/development.md](docs/development.md) - Development guide
   - [docs/architecture.md](docs/architecture.md) - System architecture
   - [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines

2. **Explore the API:**
   - Visit http://localhost:8000/docs for interactive API documentation

3. **Start developing:**
   - Create a new branch: `git checkout -b feature/your-feature`
   - Make your changes
   - Run tests: `make test`
   - Commit and push

4. **Join the team:**
   - Review open issues
   - Check the project roadmap in README.md
   - Reach out with questions

## 🆘 Getting Help

If you encounter issues not covered here:

1. Check the [docs/development.md](docs/development.md) for common issues
2. Search existing GitHub issues
3. Create a new issue with:
   - Your operating system
   - Versions of Docker, Node, Python
   - Steps to reproduce the problem
   - Error messages and logs

## ✨ Success!

If you've completed all the steps above, you're ready to start developing! 🎉

Access your applications:
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
