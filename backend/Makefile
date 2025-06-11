.PHONY: install install-dev dev test lint format clean seed reset-db

# Install dependencies (normal packages only)
install:
	uv sync

# Install dependencies (including dev packages)
install-dev:
	uv sync --extra dev

# Run development server
dev:
	uv run python scripts/run_dev.py

# Run tests
test:
	uv run pytest

# Run tests with coverage
test-cov:
	uv run coverage run -m pytest
	uv run coverage report

# Lint code
lint:
	uv run ruff check .
	uv run ruff format --check .

# Format code
format:
	uv run ruff check --fix .
	uv run ruff format .

# Reset database
reset-db:
	psql -h localhost -U postgres -c "DROP DATABASE IF EXISTS tc-ai"
	psql -h localhost -U postgres -c "CREATE DATABASE tc-ai"

# Run Celery worker
celery:
	uv run celery -A app.core.celery_app worker --loglevel=info

# Run Celery beat
celery-beat:
	uv run celery -A app.core.celery_app beat --loglevel=info

# Seed database with sample data
seed:
	uv run python scripts/seed_data.py

# Clean up cache files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".coverage" -delete

# Help
help:
	@echo "Available commands:"
	@echo "  install     - Install dependencies (normal packages only)"
	@echo "  install-dev - Install dependencies (including dev packages)"
	@echo "  dev         - Run development server"
	@echo "  test        - Run tests"
	@echo "  test-cov    - Run tests with coverage"
	@echo "  lint        - Lint code"
	@echo "  format      - Format code"
	@echo "  reset-db    - Reset database (drop and create tc-ai database)"
	@echo "  celery      - Run Celery worker"
	@echo "  celery-beat - Run Celery beat scheduler"
	@echo "  seed        - Seed database with sample data"
	@echo "  clean       - Clean up cache files" 