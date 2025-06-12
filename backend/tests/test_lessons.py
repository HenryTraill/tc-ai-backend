from datetime import datetime, timezone

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models.client import Client
from app.models.lesson import Lesson, LessonStatus
from app.models.student import Student


def test_create_lesson(client: TestClient, session: Session):
    """Test creating a new lesson"""
    # Create a test client
    test_client = Client(first_name='John', last_name='Doe', email='john.doe@example.com', phone='+1234567890')
    session.add(test_client)
    session.commit()
    session.refresh(test_client)

    # Create a test student
    student = Student(
        client_id=test_client.id,
        first_name='Alice',
        last_name='Smith',
        email='alice.smith@example.com',
        phone='+1111111111',
        grade='10th Grade',
    )
    session.add(student)
    session.commit()
    session.refresh(student)

    lesson_data = {
        'student_id': student.id,
        'start_dt': '2024-01-15T14:00:00Z',
        'end_dt': '2024-01-15T15:00:00Z',
        'subject': 'Mathematics',
        'topic': 'Algebra',
        'notes': 'Student showed good progress',
        'skills_practiced': ['Solving equations', 'Graphing'],
        'main_subjects_covered': ['Linear equations', 'Quadratic functions'],
        'student_strengths_observed': ['Quick learner', 'Good at problem-solving'],
        'student_weaknesses_observed': ['Struggles with word problems'],
        'tutor_tips': ['Practice more word problems', 'Use visual aids'],
    }
    response = client.post(client.app.url_path_for('create_lesson'), json=lesson_data)
    assert response.status_code == 200
    data = response.json()
    assert data['student_id'] == student.id
    assert data['start_dt'] == '2024-01-15T14:00:00'
    assert data['end_dt'] == '2024-01-15T15:00:00'
    assert data['subject'] == lesson_data['subject']
    assert data['topic'] == lesson_data['topic']
    assert data['notes'] == lesson_data['notes']
    assert data['skills_practiced'] == lesson_data['skills_practiced']
    assert data['main_subjects_covered'] == lesson_data['main_subjects_covered']
    assert data['status'] == 'planned'  # Default status
    assert 'id' in data
    assert 'created_at' in data


def test_create_lesson_with_specific_status(client: TestClient, session: Session):
    """Test creating a lesson with a specific status"""
    # Create a test client
    test_client = Client(first_name='John', last_name='Doe', email='john.doe@example.com', phone='+1234567890')
    session.add(test_client)
    session.commit()
    session.refresh(test_client)

    # Create a test student
    student = Student(
        client_id=test_client.id,
        first_name='Alice',
        last_name='Smith',
        email='alice.smith@example.com',
        phone='+1111111111',
        grade='11th Grade',
    )
    session.add(student)
    session.commit()
    session.refresh(student)

    lesson_data = {
        'student_id': student.id,
        'start_dt': '2024-01-16T15:00:00Z',
        'end_dt': '2024-01-16T16:30:00Z',
        'subject': 'Physics',
        'topic': 'Mechanics',
        'notes': 'Completed lesson',
        'status': 'complete',
    }
    response = client.post('/api/lessons/', json=lesson_data)
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'complete'


def test_create_lesson_invalid_student_id(client: TestClient):
    """Test creating a lesson with invalid student_id"""
    lesson_data = {
        'student_id': 999,  # Non-existent student
        'start_dt': '2024-01-15T14:00:00Z',
        'end_dt': '2024-01-15T15:00:00Z',
        'subject': 'Mathematics',
        'topic': 'Algebra',
        'notes': 'Test lesson',
    }
    response = client.post(client.app.url_path_for('create_lesson'), json=lesson_data)
    # Should return 404 when student doesn't exist
    assert response.status_code == 404
    assert 'Student not found' in response.json()['detail']


def test_get_lessons(client: TestClient, session: Session):
    """Test getting all lessons"""
    # Create a test client
    test_client = Client(first_name='John', last_name='Doe', email='john.doe@example.com', phone='+1234567890')
    session.add(test_client)
    session.commit()
    session.refresh(test_client)

    # Create a test student
    student = Student(
        client_id=test_client.id,
        first_name='Alice',
        last_name='Smith',
        email='alice.smith@example.com',
        phone='+1111111111',
        grade='10th Grade',
    )
    session.add(student)
    session.commit()
    session.refresh(student)

    # Create a test lesson
    lesson = Lesson(
        student_id=student.id,
        start_dt=datetime(2024, 1, 15, 14, 0, tzinfo=timezone.utc),
        end_dt=datetime(2024, 1, 15, 15, 0, tzinfo=timezone.utc),
        subject='Mathematics',
        topic='Algebra',
        notes='Test lesson',
    )
    session.add(lesson)
    session.commit()

    response = client.get(client.app.url_path_for('get_lessons'))
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['subject'] == 'Mathematics'
    assert data[0]['topic'] == 'Algebra'


def test_get_lessons_with_student_filter(client: TestClient, session: Session):
    """Test getting lessons filtered by student ID"""
    # Create a test client
    test_client = Client(first_name='John', last_name='Doe', email='john.doe@example.com', phone='+1234567890')
    session.add(test_client)
    session.commit()
    session.refresh(test_client)

    # Create two students
    student1 = Student(
        client_id=test_client.id,
        first_name='Alice',
        last_name='Smith',
        email='alice.smith@example.com',
        phone='+1111111111',
        grade='10th Grade',
    )
    student2 = Student(
        client_id=test_client.id,
        first_name='Bob',
        last_name='Jones',
        email='bob.jones@example.com',
        phone='+2222222222',
        grade='11th Grade',
    )
    session.add_all([student1, student2])
    session.commit()
    session.refresh(student1)
    session.refresh(student2)

    # Create lessons for both students
    lesson1 = Lesson(
        student_id=student1.id,
        start_dt=datetime(2024, 1, 15, 14, 0, tzinfo=timezone.utc),
        end_dt=datetime(2024, 1, 15, 15, 0, tzinfo=timezone.utc),
        subject='Math',
        topic='Algebra',
        notes='Student 1 lesson',
    )
    lesson2 = Lesson(
        student_id=student2.id,
        start_dt=datetime(2024, 1, 16, 15, 0, tzinfo=timezone.utc),
        end_dt=datetime(2024, 1, 16, 16, 30, tzinfo=timezone.utc),
        subject='Science',
        topic='Chemistry',
        notes='Student 2 lesson',
    )
    session.add_all([lesson1, lesson2])
    session.commit()

    # Test filtering by student1
    response = client.get(f'/api/lessons/?student_id={student1.id}')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['student_id'] == student1.id
    assert data[0]['subject'] == 'Math'


def test_get_student_lessons(client: TestClient, session: Session):
    """Test getting all lessons for a specific student"""
    # Create a test client
    test_client = Client(first_name='John', last_name='Doe', email='john.doe@example.com', phone='+1234567890')
    session.add(test_client)
    session.commit()
    session.refresh(test_client)

    # Create a test student
    student = Student(
        client_id=test_client.id,
        first_name='Alice',
        last_name='Smith',
        email='alice.smith@example.com',
        phone='+1111111111',
        grade='10th Grade',
    )
    session.add(student)
    session.commit()
    session.refresh(student)

    # Create multiple lessons for the student
    lesson1 = Lesson(
        student_id=student.id,
        start_dt=datetime(2024, 1, 15, 14, 0, tzinfo=timezone.utc),
        end_dt=datetime(2024, 1, 15, 15, 0, tzinfo=timezone.utc),
        subject='Math',
        topic='Algebra',
        notes='First lesson',
    )
    lesson2 = Lesson(
        student_id=student.id,
        start_dt=datetime(2024, 1, 16, 15, 0, tzinfo=timezone.utc),
        end_dt=datetime(2024, 1, 16, 16, 30, tzinfo=timezone.utc),
        subject='Math',
        topic='Geometry',
        notes='Second lesson',
    )
    session.add_all([lesson1, lesson2])
    session.commit()

    # Get lessons for the student
    response = client.get(f'/api/lessons/student/{student.id}')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    for lesson in data:
        assert lesson['student_id'] == student.id
        assert lesson['subject'] == 'Math'


def test_get_lesson_by_id(client: TestClient, session: Session):
    """Test getting a specific lesson by ID"""
    # Create a test client
    test_client = Client(first_name='John', last_name='Doe', email='john.doe@example.com', phone='+1234567890')
    session.add(test_client)
    session.commit()
    session.refresh(test_client)

    # Create a test student
    student = Student(
        client_id=test_client.id,
        first_name='Alice',
        last_name='Smith',
        email='alice.smith@example.com',
        phone='+1111111111',
        grade='11th Grade',
    )
    session.add(student)
    session.commit()
    session.refresh(student)

    # Create a test lesson
    lesson = Lesson(
        student_id=student.id,
        start_dt=datetime(2024, 1, 16, 15, 0, tzinfo=timezone.utc),
        end_dt=datetime(2024, 1, 16, 16, 30, tzinfo=timezone.utc),
        subject='Science',
        topic='Biology',
        notes='Biology lesson',
        status=LessonStatus.COMPLETE,
    )
    session.add(lesson)
    session.commit()
    session.refresh(lesson)

    response = client.get(client.app.url_path_for('get_lesson', lesson_id=lesson.id))
    assert response.status_code == 200
    data = response.json()
    assert data['subject'] == 'Science'
    assert data['topic'] == 'Biology'
    assert data['id'] == lesson.id
    assert data['status'] == 'complete'


def test_get_nonexistent_lesson(client: TestClient):
    """Test getting a non-existent lesson"""
    response = client.get(client.app.url_path_for('get_lesson', lesson_id=999))
    assert response.status_code == 404


def test_update_lesson(client: TestClient, session: Session):
    """Test updating a lesson"""
    # Create a test client
    test_client = Client(first_name='John', last_name='Doe', email='john.doe@example.com', phone='+1234567890')
    session.add(test_client)
    session.commit()
    session.refresh(test_client)

    # Create a test student
    student = Student(
        client_id=test_client.id,
        first_name='Alice',
        last_name='Smith',
        email='alice.smith@example.com',
        phone='+1111111111',
        grade='12th Grade',
    )
    session.add(student)
    session.commit()
    session.refresh(student)

    # Create a test lesson
    lesson = Lesson(
        student_id=student.id,
        start_dt=datetime(2024, 1, 17, 16, 0, tzinfo=timezone.utc),
        end_dt=datetime(2024, 1, 17, 16, 45, tzinfo=timezone.utc),
        subject='English',
        topic='Literature',
        notes='Original notes',
        status=LessonStatus.PLANNED,
    )
    session.add(lesson)
    session.commit()
    session.refresh(lesson)

    # Update basic fields
    update_data = {
        'subject': 'Physics',
        'topic': 'Mechanics',
        'start_dt': '2024-01-17T16:00:00Z',
        'end_dt': '2024-01-17T17:30:00Z',
        'notes': 'Updated notes',
    }
    response = client.put(client.app.url_path_for('update_lesson', lesson_id=lesson.id), json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data['subject'] == 'Physics'
    assert data['topic'] == 'Mechanics'
    assert data['notes'] == 'Updated notes'
    assert data['start_dt'] == '2024-01-17T16:00:00'
    assert data['end_dt'] == '2024-01-17T17:30:00'


def test_update_lesson_protected_fields_ignored(client: TestClient, session: Session):
    """Test that protected fields cannot be updated through the API"""
    # Create a test client
    test_client = Client(first_name='John', last_name='Doe', email='john.doe@example.com', phone='+1234567890')
    session.add(test_client)
    session.commit()
    session.refresh(test_client)

    # Create a test student
    student = Student(
        client_id=test_client.id,
        first_name='Alice',
        last_name='Smith',
        email='alice.smith@example.com',
        phone='+1111111111',
        grade='10th Grade',
    )
    session.add(student)
    session.commit()
    session.refresh(student)

    # Create a test lesson
    lesson = Lesson(
        student_id=student.id,
        start_dt=datetime(2024, 1, 15, 14, 0, tzinfo=timezone.utc),
        end_dt=datetime(2024, 1, 15, 15, 0, tzinfo=timezone.utc),
        subject='Mathematics',
        topic='Algebra',
        notes='Original notes',
        skills_practiced=['Basic algebra'],
        main_subjects_covered=['Linear equations'],
        student_strengths_observed=['Quick learner'],
        student_weaknesses_observed=['Struggles with word problems'],
        tutor_tips=['Practice more'],
    )
    session.add(lesson)
    session.commit()
    session.refresh(lesson)

    # Try to update protected fields (should be ignored)
    update_data = {
        'subject': 'English Literature',
        'topic': 'Shakespeare',
        'notes': 'Updated notes',
        'start_dt': '2024-01-15T14:00:00Z',
        'end_dt': '2024-01-15T15:00:00Z',
    }
    response = client.put(client.app.url_path_for('update_lesson', lesson_id=lesson.id), json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data['subject'] == 'English Literature'
    assert data['topic'] == 'Shakespeare'
    assert data['notes'] == 'Updated notes'
    assert data['start_dt'] == '2024-01-15T14:00:00'
    assert data['end_dt'] == '2024-01-15T15:00:00'


def test_update_lesson_status_to_cancelled(client: TestClient, session: Session):
    """Test updating a lesson status to cancelled"""
    # Create a test client
    test_client = Client(first_name='John', last_name='Doe', email='john.doe@example.com', phone='+1234567890')
    session.add(test_client)
    session.commit()
    session.refresh(test_client)

    # Create a test student
    student = Student(
        client_id=test_client.id,
        first_name='Alice',
        last_name='Smith',
        email='alice.smith@example.com',
        phone='+1111111111',
        grade='10th Grade',
    )
    session.add(student)
    session.commit()
    session.refresh(student)

    # Create a test lesson
    lesson = Lesson(
        student_id=student.id,
        start_dt=datetime(2024, 1, 18, 14, 0, tzinfo=timezone.utc),
        end_dt=datetime(2024, 1, 18, 15, 0, tzinfo=timezone.utc),
        subject='Science',
        topic='Chemistry',
        notes='Chemistry lesson',
        status=LessonStatus.PLANNED,
    )
    session.add(lesson)
    session.commit()
    session.refresh(lesson)

    response = client.delete(client.app.url_path_for('delete_lesson', lesson_id=lesson.id))
    assert response.status_code == 200
    data = response.json()
    assert data['message'] == 'Lesson deleted successfully'

    # Verify lesson is deleted
    response = client.get(client.app.url_path_for('get_lesson', lesson_id=lesson.id))
    assert response.status_code == 404


def test_delete_nonexistent_lesson(client: TestClient):
    """Test deleting a non-existent lesson"""
    response = client.delete(client.app.url_path_for('delete_lesson', lesson_id=999))
    assert response.status_code == 404


def test_get_lessons_for_student(client: TestClient, session: Session):
    """Test getting all lessons for a specific student"""
    # Create a test client
    test_client = Client(first_name='John', last_name='Doe', email='john.doe@example.com', phone='+1234567890')
    session.add(test_client)
    session.commit()
    session.refresh(test_client)

    # Create a test student
    student = Student(
        client_id=test_client.id,
        first_name='Alice',
        last_name='Smith',
        email='alice.smith@example.com',
        phone='+1111111111',
        grade='10th Grade',
    )
    session.add(student)
    session.commit()
    session.refresh(student)

    # Create lessons for this student
    lesson1 = Lesson(
        student_id=student.id,
        start_dt=datetime(2024, 1, 15, 14, 0, tzinfo=timezone.utc),
        end_dt=datetime(2024, 1, 15, 15, 0, tzinfo=timezone.utc),
        subject='Mathematics',
        topic='Algebra',
        notes='Math lesson',
    )
    lesson2 = Lesson(
        student_id=student.id,
        start_dt=datetime(2024, 1, 16, 15, 0, tzinfo=timezone.utc),
        end_dt=datetime(2024, 1, 16, 16, 30, tzinfo=timezone.utc),
        subject='Physics',
        topic='Mechanics',
        notes='Physics lesson',
    )
    session.add(lesson1)
    session.add(lesson2)
    session.commit()

    response = client.get(client.app.url_path_for('get_lessons_for_student', student_id=student.id))
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    subjects = [lesson['subject'] for lesson in data]
    assert 'Mathematics' in subjects
    assert 'Physics' in subjects
    # Verify all lessons belong to the correct student
    for lesson in data:
        assert lesson['student_id'] == student.id


def test_get_lessons_for_nonexistent_student(client: TestClient):
    """Test getting lessons for a non-existent student"""
    response = client.get(client.app.url_path_for('get_lessons_for_student', student_id=999))
    assert response.status_code == 404
    assert 'Student not found' in response.json()['detail']
