# TutorCruncher AI - Project Context

## Project Overview
TutorCruncher AI is a full-stack application designed for managing tutoring sessions, student profiles, and lesson tracking. The application provides a comprehensive platform for tutors to manage their students, track lessons, and monitor progress.

## Architecture

### Tech Stack
- **Backend**: FastAPI (Python 3.12+), SQLModel, PostgreSQL
- **Frontend**: React + TypeScript, React Router, Tailwind CSS
- **Package Management**: 
  - Backend: uv
  - Frontend: npm

### Project Structure
```
.
├── backend/                 # Python FastAPI backend
│   ├── app/                # Main application code
│   ├── tests/              # Backend tests
│   ├── scripts/            # Utility scripts
│   └── pyproject.toml      # Python project configuration
│
├── frontend/               # React frontend
│   ├── app/                # Main application code
│   ├── public/             # Static assets
│   └── package.json        # Node.js project configuration
│
├── frontend-minimal/       # Minimal frontend implementation
├── .github/                # GitHub workflows and configurations
└── .vscode/                # VS Code settings
```

## Core Features
1. **Student Management**
   - Create, view, edit, and delete student profiles
   - Track student information and progress

2. **Lesson Tracking**
   - Record detailed lesson information
   - Track skills practiced and subjects covered
   - Store tutor observations

3. **Progress Monitoring**
   - Track student strengths and weaknesses
   - Monitor lesson completion
   - Generate progress reports

4. **Dashboard**
   - Overview of lessons and statistics
   - Recent activity tracking
   - Responsive design for all devices

## API Structure
The backend provides RESTful endpoints for:

### Students
- `GET /students` - List all students
- `GET /students/{id}` - Get student details
- `POST /students` - Create new student
- `PUT /students/{id}` - Update student
- `DELETE /students/{id}` - Delete student

### Lessons
- `GET /lessons` - List all lessons
- `GET /lessons/{id}` - Get lesson details
- `GET /lessons/student/{student_id}` - Get student's lessons
- `POST /lessons` - Create new lesson
- `PUT /lessons/{id}` - Update lesson
- `DELETE /lessons/{id}` - Delete lesson

## Development Workflow

### Backend Development
- Uses Makefile for common commands
- Key commands:
  - `make install-dev` - Install dependencies
  - `make run-dev` - Start development server
  - `make test` - Run tests
  - `make format` - Format code
  - `make lint` - Lint code
  - `make reset-db` - Reset database

### Frontend Development
- Standard npm-based workflow
- Key commands:
  - `npm run dev` - Start development server
  - `npm run build` - Build for production
  - `npm run preview` - Preview production build

## Environment Setup
- Backend requires:
  - Python 3.12+
  - PostgreSQL
  - Environment variables in `.env` file
- Frontend requires:
  - Node.js 18+
  - npm

## Development URLs
- Backend API: `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- Frontend: `http://localhost:5173`

## Testing
- Backend uses pytest for testing
- Frontend testing setup available
- Coverage reports generated for backend

## Deployment
- Docker support available for both frontend and backend
- GitHub Actions workflows for CI/CD
- Environment-specific configurations

## Security
- Environment variables for sensitive data
- API authentication and authorization
- Secure database connections

## Future Considerations
- Scalability planning
- Performance optimization
- Additional feature development
- Enhanced monitoring and logging 