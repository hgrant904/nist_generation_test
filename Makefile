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
