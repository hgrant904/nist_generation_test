.PHONY: help install test test-unit test-integration run clean

help:
	@echo "Available commands:"
	@echo "  make install           - Install dependencies"
	@echo "  make test              - Run all tests"
	@echo "  make test-unit         - Run unit tests only"
	@echo "  make test-integration  - Run integration tests"
	@echo "  make run               - Start the API server"
	@echo "  make clean             - Clean up generated files"

install:
	pip install -r requirements.txt

test:
	pytest

test-unit:
	pytest tests/unit/

test-integration:
	pytest tests/integration/

run:
	python run.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache htmlcov .coverage
	rm -f nist_csf.db
.PHONY: help install dev up down build restart logs clean test backend-test frontend-test backend-shell frontend-shell db-shell

help:
	@echo "NIST Reports - Available Commands"
	@echo "===================================="
	@echo "make install         - Install all dependencies (backend and frontend)"
	@echo "make dev             - Start all services in development mode"
	@echo "make up              - Start all services (detached)"
	@echo "make down            - Stop all services"
	@echo "make build           - Build all Docker images"
	@echo "make restart         - Restart all services"
	@echo "make logs            - Show logs from all services"
	@echo "make clean           - Remove all containers, volumes, and cache"
	@echo "make test            - Run all tests"
	@echo "make backend-test    - Run backend tests"
	@echo "make frontend-test   - Run frontend tests"
	@echo "make backend-shell   - Open shell in backend container"
	@echo "make frontend-shell  - Open shell in frontend container"
	@echo "make db-shell        - Open PostgreSQL shell"

install:
	@echo "Installing backend dependencies..."
	cd backend && pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	cd frontend && npm install
	@echo "Dependencies installed successfully!"

dev:
	@echo "Starting development environment..."
	docker-compose up

up:
	@echo "Starting services in detached mode..."
	docker-compose up -d

down:
	@echo "Stopping services..."
	docker-compose down

build:
	@echo "Building Docker images..."
	docker-compose build

rebuild:
	@echo "Rebuilding Docker images from scratch..."
	docker-compose build --no-cache

restart:
	@echo "Restarting services..."
	docker-compose restart

logs:
	docker-compose logs -f

clean:
	@echo "Cleaning up containers, volumes, and cache..."
	docker-compose down -v
	rm -rf backend/__pycache__ backend/.pytest_cache backend/.mypy_cache
	rm -rf frontend/.next frontend/node_modules
	@echo "Cleanup complete!"

test: backend-test frontend-test

backend-test:
	@echo "Running backend tests..."
	cd backend && pytest

frontend-test:
	@echo "Running frontend tests..."
	cd frontend && npm test

backend-shell:
	docker-compose exec backend /bin/bash

frontend-shell:
	docker-compose exec frontend /bin/sh

db-shell:
	docker-compose exec postgres psql -U nist_user -d nist_reports

# Database migration commands
db-migrate:
	docker-compose exec backend alembic upgrade head

db-rollback:
	docker-compose exec backend alembic downgrade -1

db-reset:
	docker-compose down -v
	docker-compose up -d postgres
	sleep 5
	docker-compose up -d backend
