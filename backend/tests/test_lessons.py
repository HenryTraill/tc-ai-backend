from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models.client import Client
from app.models.lesson import Lesson
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
        'date': '2024-01-15',
        'start_time': '14:00',
        'subject': 'Mathematics',
        'topic': 'Algebra',
        'duration': 60,
        'notes': 'Student showed good progress',
        'skills_practiced': ['Solving equations', 'Graphing'],
        'main_subjects_covered': ['Linear equations', 'Quadratic functions'],
        'student_strengths_observed': ['Quick learner', 'Good at problem-solving'],
        'student_weaknesses_observed': ['Struggles with word problems'],
        'tutor_tips': ['Practice more word problems', 'Use visual aids'],
    }
    response = client.post('/api/lessons/', json=lesson_data)
    assert response.status_code == 200
    data = response.json()
    assert data['student_id'] == student.id
    assert data['date'] == lesson_data['date']
    assert data['start_time'] == lesson_data['start_time']
    assert data['subject'] == lesson_data['subject']
    assert data['topic'] == lesson_data['topic']
    assert data['duration'] == lesson_data['duration']
    assert data['notes'] == lesson_data['notes']
    assert data['skills_practiced'] == lesson_data['skills_practiced']
    assert data['main_subjects_covered'] == lesson_data['main_subjects_covered']
    assert 'id' in data
    assert 'created_at' in data


def test_create_lesson_invalid_student_id(client: TestClient):
    """Test creating a lesson with invalid student_id"""
    lesson_data = {
        'student_id': 999,  # Non-existent student
        'date': '2024-01-15',
        'start_time': '14:00',
        'subject': 'Mathematics',
        'topic': 'Algebra',
        'duration': 60,
        'notes': 'Test lesson',
    }
    response = client.post('/api/lessons/', json=lesson_data)
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
        date='2024-01-15',
        start_time='14:00',
        subject='Mathematics',
        topic='Algebra',
        duration=60,
        notes='Test lesson',
    )
    session.add(lesson)
    session.commit()

    response = client.get('/api/lessons/')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['subject'] == 'Mathematics'
    assert data[0]['topic'] == 'Algebra'


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
        grade='10th Grade',
    )
    session.add(student)
    session.commit()
    session.refresh(student)

    # Create a test lesson
    lesson = Lesson(
        student_id=student.id,
        date='2024-01-15',
        start_time='14:00',
        subject='Mathematics',
        topic='Algebra',
        duration=60,
        notes='Test lesson',
    )
    session.add(lesson)
    session.commit()
    session.refresh(lesson)

    response = client.get(f'/api/lessons/{lesson.id}')
    assert response.status_code == 200
    data = response.json()
    assert data['subject'] == 'Mathematics'
    assert data['id'] == lesson.id


def test_get_nonexistent_lesson(client: TestClient):
    """Test getting a non-existent lesson"""
    response = client.get('/api/lessons/999')
    assert response.status_code == 404


def test_update_lesson_basic_fields(client: TestClient, session: Session):
    """Test updating basic lesson fields"""
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
        date='2024-01-15',
        start_time='14:00',
        subject='Mathematics',
        topic='Algebra',
        duration=60,
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

    # Update basic fields
    update_data = {'subject': 'Physics', 'topic': 'Mechanics', 'duration': 90, 'notes': 'Updated notes'}
    response = client.put(f'/api/lessons/{lesson.id}', json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data['subject'] == 'Physics'
    assert data['topic'] == 'Mechanics'
    assert data['duration'] == 90
    assert data['notes'] == 'Updated notes'
    assert data['date'] == '2024-01-15'  # Should remain unchanged


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
        date='2024-01-15',
        start_time='14:00',
        subject='Mathematics',
        topic='Algebra',
        duration=60,
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
        'subject': 'Physics',  # Should be updated
        'skills_practiced': ['Advanced physics'],  # Should be ignored
        'main_subjects_covered': ['Thermodynamics'],  # Should be ignored
        'student_strengths_observed': ['Excellent student'],  # Should be ignored
        'student_weaknesses_observed': ['No weaknesses'],  # Should be ignored
        'tutor_tips': ['Keep it up'],  # Should be ignored
    }
    response = client.put(f'/api/lessons/{lesson.id}', json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data['subject'] == 'Physics'  # Should be updated
    assert data['skills_practiced'] == ['Basic algebra']  # Should remain unchanged
    assert data['main_subjects_covered'] == ['Linear equations']  # Should remain unchanged
    assert data['student_strengths_observed'] == ['Quick learner']  # Should remain unchanged
    assert data['student_weaknesses_observed'] == ['Struggles with word problems']  # Should remain unchanged
    assert data['tutor_tips'] == ['Practice more']  # Should remain unchanged


def test_delete_lesson(client: TestClient, session: Session):
    """Test deleting a lesson"""
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
        date='2024-01-15',
        start_time='14:00',
        subject='Mathematics',
        topic='Algebra',
        duration=60,
        notes='Test lesson',
    )
    session.add(lesson)
    session.commit()
    session.refresh(lesson)

    response = client.delete(f'/api/lessons/{lesson.id}')
    assert response.status_code == 200
    data = response.json()
    assert data['message'] == 'Lesson deleted successfully'

    # Verify lesson is deleted
    response = client.get(f'/api/lessons/{lesson.id}')
    assert response.status_code == 404


def test_delete_nonexistent_lesson(client: TestClient):
    """Test deleting a non-existent lesson"""
    response = client.delete('/api/lessons/999')
    assert response.status_code == 404
