# Contributing to NIST Report Backend

Thank you for your interest in contributing to the NIST Report Backend project!

## Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd backend
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your local configuration
   ```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_health.py

# Run with verbose output
pytest -v
```

## Code Quality

Before submitting a pull request, ensure your code passes all checks:

```bash
# Format code
black app tests

# Lint code
ruff check app tests

# Fix linting issues automatically
ruff check --fix app tests

# Type checking
mypy app

# Run all checks
bash scripts/test.sh
```

## Making Changes

1. **Create a new branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, readable code
   - Follow existing code style
   - Add tests for new functionality
   - Update documentation as needed

3. **Test your changes**
   ```bash
   bash scripts/test.sh
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

   Use conventional commit messages:
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation changes
   - `test:` for test updates
   - `refactor:` for code refactoring
   - `chore:` for maintenance tasks

5. **Push to your branch**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a pull request**
   - Provide a clear description of your changes
   - Reference any related issues
   - Ensure all CI checks pass

## Database Migrations

When making changes to database models:

1. **Create a migration**
   ```bash
   alembic revision --autogenerate -m "Description of changes"
   ```

2. **Review the migration**
   - Check the generated migration file in `alembic/versions/`
   - Ensure it captures all intended changes

3. **Test the migration**
   ```bash
   # Apply migration
   alembic upgrade head
   
   # Test rollback
   alembic downgrade -1
   
   # Re-apply
   alembic upgrade head
   ```

## Project Structure

```
backend/
├── app/
│   ├── api/          # API endpoints
│   ├── core/         # Core configuration
│   ├── db/           # Database setup
│   ├── models/       # SQLAlchemy models
│   ├── schemas/      # Pydantic schemas
│   └── main.py       # Application factory
├── tests/            # Test suite
├── alembic/          # Database migrations
└── scripts/          # Utility scripts
```

## Code Style

- **Line length**: 88 characters (Black default)
- **Python version**: 3.11+
- **Import order**: stdlib, third-party, local (enforced by Ruff)
- **Type hints**: Required for all functions and methods
- **Docstrings**: Required for all public functions and classes

## Best Practices

1. **Write tests** for all new functionality
2. **Keep functions small** and focused on a single task
3. **Use type hints** for better code clarity
4. **Write clear commit messages** using conventional commits
5. **Update documentation** when changing functionality
6. **Handle errors gracefully** with proper exception handling
7. **Log appropriately** using the configured logger

## Getting Help

If you have questions or need help:
- Open an issue on GitHub
- Check existing documentation
- Ask in project discussions

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.
