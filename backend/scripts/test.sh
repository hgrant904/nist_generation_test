#!/bin/bash
set -e

echo "Running linters and formatters..."
black --check app tests
ruff check app tests

echo "Running type checks..."
mypy app

echo "Running tests..."
pytest

echo "All checks passed!"
