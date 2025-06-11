# TutorCruncher AI Backend

FastAPI backend for the TutorCruncher AI tutoring management system.

## Features

- **FastAPI** - Modern, fast web framework for building APIs
- **SQLModel** - SQL databases in Python, designed for simplicity, compatibility, and robustness
- **Celery** - Distributed task queue for background jobs
- **PostgreSQL** - Production database
- **Redis** - Caching and Celery message broker
- **Logfire** - Observability and monitoring
- **Sentry** - Error tracking and performance monitoring
- **Ruff** - Fast Python linter and formatter
- **Pytest** - Testing framework

## Quick Start

### Prerequisites

- Python 3.12+
- PostgreSQL
- Redis
- uv (Python package manager)

### Installation

1. Install dependencies:
```bash
uv sync
```

2. Copy environment variables:
```bash
cp env.example .env
```

3. Update `.env` with your database and service credentials

4. Run database migrations:
```bash
# Database tables will be created automatically on first run
```

### Running the Application

#### Development Server
```bash
# Using uv
uv run python scripts/run_dev.py

# Or directly with uvicorn
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Celery Worker
```bash
# In a separate terminal
uv run celery -A app.core.celery_app worker --loglevel=info
```

#### Celery Beat (for scheduled tasks)
```bash
# In another terminal
uv run celery -A app.core.celery_app beat --loglevel=info
```

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Students
- `GET /api/students/` - List all students
- `POST /api/students/` - Create a new student
- `GET /api/students/{id}` - Get student by ID
- `PUT /api/students/{id}` - Update student
- `DELETE /api/students/{id}` - Delete student

### Lessons
- `GET /api/lessons/` - List all lessons (with optional student filter)
- `POST /api/lessons/` - Create a new lesson
- `GET /api/lessons/{id}` - Get lesson by ID
- `PUT /api/lessons/{id}` - Update lesson
- `DELETE /api/lessons/{id}` - Delete lesson
- `GET /api/lessons/student/{student_id}` - Get all lessons for a student

## Testing

Run tests with pytest:
```bash
uv run pytest
```

Run tests with coverage:
```bash
uv run coverage run -m pytest
uv run coverage report
```

## Code Quality

Format code with ruff:
```bash
uv run ruff format .
```

Lint code:
```bash
uv run ruff check .
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:password@localhost/tutorcruncher` |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379/0` |
| `API_HOST` | API server host | `0.0.0.0` |
| `API_PORT` | API server port | `8000` |
| `DEBUG` | Enable debug mode | `True` |
| `ALLOWED_ORIGINS` | CORS allowed origins | `http://localhost:3000,http://localhost:5173` |
| `SENTRY_DSN` | Sentry error tracking DSN | `None` |
| `LOGFIRE_TOKEN` | Logfire monitoring token | `None` |

## Project Structure

```
backend/
├── app/
│   ├── api/           # API route handlers
│   ├── core/          # Core configuration and setup
│   ├── models/        # SQLModel database models
│   └── tasks/         # Celery background tasks
├── tests/             # Test files
├── scripts/           # Utility scripts
└── pyproject.toml     # Project configuration
```

## Background Tasks

The application includes Celery for background task processing:

- **Email Tasks**: Send lesson reminders and notifications
- **Analytics Tasks**: Generate student reports and analytics

## Monitoring

- **Sentry**: Error tracking and performance monitoring
- **Logfire**: Observability and structured logging

## Development

### Adding New Models

1. Create model in `app/models/`
2. Add to `app/models/__init__.py`
3. Create API routes in `app/api/`
4. Add tests in `tests/`

### Adding Background Tasks

1. Create task in `app/tasks/`
2. Add to `app/tasks/__init__.py`
3. Import in `app/core/celery_app.py`

## Production Deployment

For production deployment, consider:

1. Use a production WSGI server (e.g., Gunicorn)
2. Set up proper database migrations with Alembic
3. Configure environment variables securely
4. Set up monitoring and logging
5. Use a reverse proxy (e.g., Nginx)
6. Set up SSL/TLS certificates 