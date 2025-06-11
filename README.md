# TutorCruncher AI

A full-stack application for managing tutoring sessions, student profiles, and lesson tracking.

## Tech Stack

**Backend:**
- FastAPI (Python)
- SQLModel + PostgreSQL
- uv for package management

**Frontend:**
- React + TypeScript
- React Router
- Tailwind CSS

## Getting Started

### Prerequisites
- Python 3.12+
- Node.js 18+
- PostgreSQL

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   make install-dev
   ```

3. Set up your database connection by creating a `.env` file:
   ```bash
   cp env.example .env
   # Edit .env with your database credentials
   ```

4. Create the database:
   ```bash
   make reset-db
   ```

5. Start the development server:
   ```bash
   make run-dev
   ```

The backend API will be available at `http://localhost:8000`
- API docs: `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:5173`

## API Endpoints

### Students
- `GET /students` - Get all students
- `GET /students/{id}` - Get student by ID
- `POST /students` - Create new student
- `PUT /students/{id}` - Update student
- `DELETE /students/{id}` - Delete student

### Lessons
- `GET /lessons` - Get all lessons (optional: `?student_id=X`)
- `GET /lessons/{id}` - Get lesson by ID
- `GET /lessons/student/{student_id}` - Get lessons for specific student
- `POST /lessons` - Create new lesson
- `PUT /lessons/{id}` - Update lesson
- `DELETE /lessons/{id}` - Delete lesson

## Development

### Backend Commands
```bash
# Install dependencies
make install-dev

# Run development server
make run-dev

# Run tests
make test

# Format code
make format

# Lint code
make lint

# Reset database
make reset-db
```

### Frontend Commands
```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Features

- **Student Management**: Create, view, edit, and delete student profiles
- **Lesson Tracking**: Record detailed lesson information including skills practiced, subjects covered, and tutor observations
- **Progress Monitoring**: Track student strengths, weaknesses, and lesson completion
- **Dashboard**: Overview of lessons, statistics, and recent activity
- **Responsive Design**: Works on desktop and mobile devices 