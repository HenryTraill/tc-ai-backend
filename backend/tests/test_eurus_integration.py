from datetime import UTC, datetime, timedelta
from unittest.mock import patch

import pytest
from httpx import Request, Response
from sqlmodel import Session

from app.core.config import settings
from app.models import Lesson, LessonStudent, LessonTutor, Student, User


@pytest.fixture
def test_students(session: Session) -> list[Student]:
    """Create test students for the lesson."""
    students = [
        Student(
            client_id=1,
            first_name=f'Student{i}',
            last_name=f'Test{i}',
            email=f'student{i}@example.com',
            phone='1234567890',
            grade='A',  # Provide a dummy grade
            company_id=None,
            tc_path=None,
            strengths=[],
            weaknesses=[],
            created_at=datetime.now(),
        )
        for i in range(3)
    ]
    session.add_all(students)
    session.commit()
    return students


@pytest.fixture
def test_lesson(session: Session, test_tutor: User, test_students: list[Student]) -> Lesson:
    """Create a test lesson with multiple students."""
    lesson = Lesson(
        subject='Math',
        topic='Algebra',
        notes='Test lesson',
        start_dt=datetime.now(UTC) + timedelta(hours=1),
        end_dt=datetime.now(UTC) + timedelta(hours=2),
    )
    session.add(lesson)
    session.commit()
    session.refresh(lesson)

    # Add students to lesson
    for student in test_students:
        lesson_student = LessonStudent(lesson_id=lesson.id, student_id=student.id)
        session.add(lesson_student)

    # Add tutor to lesson
    lesson_tutor = LessonTutor(lesson_id=lesson.id, tutor_id=test_tutor.id)
    session.add(lesson_tutor)

    session.commit()
    session.refresh(lesson)
    return lesson


def test_create_eurus_space_success(auth_client, test_lesson: Lesson, test_students: list[Student]):
    """Test successful creation of a Eurus space."""
    mock_response = {
        'space_id': '123',
        'lesson_id': str(test_lesson.id),
        'tutor_spaces': [
            {
                'user_id': str(auth_client.user.id),
                'name': f'{auth_client.user.first_name} {auth_client.user.last_name}',
                'role': 'tutor',
                'space_url': 'https://eurus.example.com/tutor/123',
            }
        ],
        'student_spaces': [
            {
                'user_id': str(student.id),
                'name': f'{student.first_name} {student.last_name}',
                'role': 'student',
                'space_url': f'https://eurus.example.com/student/{student.id}/123',
            }
            for student in test_students
        ],
    }

    with patch('httpx.AsyncClient.post') as mock_post:
        mock_post.return_value = Response(200, json=mock_response, request=Request('POST', 'http://testserver'))
        response = auth_client.post(auth_client.app.url_path_for('create_eurus_space', lesson_id=test_lesson.id))

    assert response.status_code == 200
    data = response.json()
    assert data == mock_response

    # Verify the request to Eurus
    mock_post.assert_called_once()
    call_args = mock_post.call_args
    assert call_args[0][0] == f'{settings.eurus_api_url}/api/space/'

    expected_request_data = {
        'lesson_id': str(test_lesson.id),
        'tutors': [
            {
                'user_id': str(auth_client.user.id),
                'name': f'{auth_client.user.first_name} {auth_client.user.last_name}',
                'email': auth_client.user.email if hasattr(auth_client.user, 'email') else None,
                'is_leader': True,
            }
        ],
        'students': [
            {
                'user_id': str(student.id),
                'name': f'{student.first_name} {student.last_name}',
                'email': student.email if hasattr(student, 'email') else None,
            }
            for student in test_students
        ],
        'not_before': test_lesson.start_dt.isoformat() if test_lesson.start_dt else None,
    }

    assert call_args[1]['json'] == expected_request_data


def test_create_eurus_space_lesson_not_found(auth_client):
    """Test creating a Eurus space for a non-existent lesson."""
    response = auth_client.post(auth_client.app.url_path_for('create_eurus_space', lesson_id=999))
    assert response.status_code == 404
    assert response.json()['detail'] == 'Lesson not found'


def test_create_eurus_space_no_students(auth_client, session: Session, test_tutor: User):
    """Test creating a Eurus space for a lesson with no students."""
    # Create a lesson without any students
    lesson = Lesson(
        subject='Math',
        topic='Algebra',
        notes='Test lesson',
        start_dt=datetime.now(UTC) + timedelta(hours=1),
        end_dt=datetime.now(UTC) + timedelta(hours=2),
    )
    session.add(lesson)
    session.commit()
    session.refresh(lesson)

    # Add tutor to lesson
    lesson_tutor = LessonTutor(lesson_id=lesson.id, tutor_id=test_tutor.id)
    session.add(lesson_tutor)
    session.commit()

    response = auth_client.post(auth_client.app.url_path_for('create_eurus_space', lesson_id=lesson.id))
    assert response.status_code == 404
    assert response.json()['detail'] == 'No students found for this lesson'


def test_create_eurus_space_api_error(auth_client, test_lesson: Lesson):
    """Test handling of Eurus API errors."""
    with patch('httpx.AsyncClient.post') as mock_post:
        mock_post.return_value = Response(
            500, json={'error': 'API Error'}, request=Request('POST', 'http://testserver')
        )
        response = auth_client.post(auth_client.app.url_path_for('create_eurus_space', lesson_id=test_lesson.id))

    assert response.status_code == 500
    assert 'Failed to create Eurus space' in response.json()['detail']


def test_create_eurus_space_unauthorized_access(client, test_lesson: Lesson):
    """Test that unauthenticated users cannot create Eurus spaces."""
    response = client.post(client.app.url_path_for('create_eurus_space', lesson_id=test_lesson.id))
    assert response.status_code == 401
