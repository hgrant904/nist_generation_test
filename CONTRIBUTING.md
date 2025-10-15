# Contributing to NIST Reports

Thank you for your interest in contributing to the NIST Reports project! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone <your-fork-url>`
3. Add upstream remote: `git remote add upstream <original-repo-url>`
4. Create a branch: `git checkout -b feature/your-feature-name`

## Development Setup

Follow the setup instructions in the [README.md](README.md) to get your development environment running.

## Code Style Guidelines

### Python (Backend)

- Follow [PEP 8](https://pep8.org/) style guide
- Use [Black](https://github.com/psf/black) for code formatting (line length: 100)
- Use [Ruff](https://github.com/astral-sh/ruff) for linting
- Add type hints where possible
- Write docstrings for functions and classes
- Maximum line length: 100 characters

```python
# Good
def generate_report(user_id: int, report_type: str) -> dict:
    """Generate a NIST security report for a user.
    
    Args:
        user_id: The ID of the user requesting the report
        report_type: The type of report to generate
        
    Returns:
        A dictionary containing the report data
    """
    pass
```

### TypeScript (Frontend)

- Follow the project's ESLint configuration
- Use [Prettier](https://prettier.io/) for code formatting
- Use TypeScript types instead of `any` when possible
- Use functional components with hooks
- Maximum line length: 100 characters

```typescript
// Good
interface ReportProps {
  reportId: string;
  onComplete: (report: Report) => void;
}

export default function ReportComponent({ reportId, onComplete }: ReportProps) {
  // Component logic
}
```

## Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples
```
feat(backend): add NIST API integration
fix(frontend): resolve report rendering issue
docs: update installation instructions
test(backend): add unit tests for report generation
```

## Pull Request Process

1. **Update your branch** with the latest changes from upstream:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Test your changes**:
   ```bash
   make test
   ```

3. **Ensure code quality**:
   ```bash
   # Backend
   cd backend
   black .
   ruff check .
   mypy .
   
   # Frontend
   cd frontend
   npm run lint
   npm run type-check
   ```

4. **Push your branch**:
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request** on GitHub with:
   - Clear title and description
   - Reference to any related issues
   - Screenshots (if UI changes)
   - Test results

6. **Address review comments** and update your PR as needed

## Testing Guidelines

### Backend Tests

- Write tests for all new features
- Aim for at least 80% code coverage
- Use pytest fixtures for common test data
- Test both success and error cases

```python
def test_generate_report_success():
    response = client.post("/api/reports", json={"type": "security"})
    assert response.status_code == 200
    assert "report_id" in response.json()

def test_generate_report_invalid_type():
    response = client.post("/api/reports", json={"type": "invalid"})
    assert response.status_code == 400
```

### Frontend Tests

- Write tests for components and utilities
- Test user interactions and edge cases
- Use meaningful test descriptions

## Documentation

- Update README.md if you change setup or usage
- Update API documentation for new endpoints
- Add inline comments for complex logic
- Update architecture docs for significant changes

## Questions or Issues?

- Check existing issues before creating a new one
- Provide detailed information in issue reports
- Use issue templates when available
- Be respectful and constructive in discussions

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).
