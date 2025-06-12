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
        'date': '2024-01-16',
        'start_time': '15:00',
        'subject': 'Physics',
        'topic': 'Mechanics',
        'duration': 90,
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
        date='2024-01-15',
        start_time='14:00',
        subject='Math',
        topic='Algebra',
        duration=60,
        notes='Student 1 lesson',
    )
    lesson2 = Lesson(
        student_id=student2.id,
        date='2024-01-16',
        start_time='15:00',
        subject='Science',
        topic='Chemistry',
        duration=90,
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
        date='2024-01-15',
        start_time='14:00',
        subject='Math',
        topic='Algebra',
        duration=60,
        notes='First lesson',
    )
    lesson2 = Lesson(
        student_id=student.id,
        date='2024-01-16',
        start_time='15:00',
        subject='Math',
        topic='Geometry',
        duration=90,
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


def test_get_lessons_for_nonexistent_student(client: TestClient):
    """Test getting lessons for a non-existent student"""
    response = client.get('/api/lessons/student/999')
    assert response.status_code == 404


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
        date='2024-01-16',
        start_time='15:00',
        subject='Science',
        topic='Biology',
        duration=90,
        notes='Biology lesson',
        status=LessonStatus.COMPLETE,
    )
    session.add(lesson)
    session.commit()
    session.refresh(lesson)

    response = client.get(f'/api/lessons/{lesson.id}')
    assert response.status_code == 200
    data = response.json()
    assert data['subject'] == 'Science'
    assert data['topic'] == 'Biology'
    assert data['id'] == lesson.id
    assert data['status'] == 'complete'


def test_get_nonexistent_lesson(client: TestClient):
    """Test getting a non-existent lesson"""
    response = client.get('/api/lessons/999')
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
        date='2024-01-17',
        start_time='16:00',
        subject='English',
        topic='Literature',
        duration=45,
        notes='Original notes',
        status=LessonStatus.PLANNED,
    )
    session.add(lesson)
    session.commit()
    session.refresh(lesson)

    # Update lesson
    update_data = {
        'subject': 'English Literature',
        'topic': 'Shakespeare',
        'notes': 'Updated notes',
        'duration': 60,
    }
    response = client.put(f'/api/lessons/{lesson.id}', json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data['subject'] == 'English Literature'
    assert data['topic'] == 'Shakespeare'
    assert data['notes'] == 'Updated notes'
    assert data['duration'] == 60
    assert data['date'] == '2024-01-17'  # Should remain unchanged


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
        date='2024-01-18',
        start_time='14:00',
        subject='Science',
        topic='Chemistry',
        duration=60,
        notes='Chemistry lesson',
        status=LessonStatus.PLANNED,
    )
    session.add(lesson)
    session.commit()
    session.refresh(lesson)

    # Update status to cancelled
    update_data = {'status': 'cancelled'}
    response = client.put(f'/api/lessons/{lesson.id}', json=update_data)
    assert response.status_code == 200, response.json()
    data = response.json()
    assert data['status'] == 'cancelled'


def test_update_lesson_with_invalid_status(client: TestClient, session: Session):
    """Test updating a lesson with invalid status"""
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
        date='2024-01-19',
        start_time='14:00',
        subject='English',
        topic='Poetry',
        duration=60,
        notes='Poetry lesson',
        status=LessonStatus.PLANNED,
    )
    session.add(lesson)
    session.commit()
    session.refresh(lesson)

    # Update with invalid status
    update_data = {'status': 'invalid_status'}
    response = client.put(f'/api/lessons/{lesson.id}', json=update_data)
    assert response.status_code == 422  # Validation error


def test_update_nonexistent_lesson(client: TestClient):
    """Test updating a non-existent lesson"""
    update_data = {'notes': 'Updated notes'}
    response = client.put('/api/lessons/999', json=update_data)
    assert response.status_code == 404


def test_update_lesson_with_nonexistent_student(client: TestClient, session: Session):
    """Test updating a lesson with non-existent student"""
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
        date='2024-01-20',
        start_time='14:00',
        subject='Art',
        topic='Painting',
        duration=60,
        notes='Art lesson',
    )
    session.add(lesson)
    session.commit()
    session.refresh(lesson)

    # Try to update with non-existent student
    update_data = {'student_id': 999}
    response = client.put(f'/api/lessons/{lesson.id}', json=update_data)
    assert response.status_code == 404


def test_update_lesson_skills_ignored(client: TestClient, session: Session):
    """Test that skills and observations cannot be updated through the API"""
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
        grade='9th Grade',
    )
    session.add(student)
    session.commit()
    session.refresh(student)

    # Create a test lesson
    lesson = Lesson(
        student_id=student.id,
        date='2024-01-18',
        start_time='17:00',
        subject='Math',
        topic='Geometry',
        duration=60,
        notes='Geometry lesson',
        skills_practiced=['Calculating areas'],
        student_strengths_observed=['Good spatial awareness'],
    )
    session.add(lesson)
    session.commit()
    session.refresh(lesson)

    # Try to update skills and observations (should be ignored)
    update_data = {
        'subject': 'Advanced Math',
        'skills_practiced': ['New skills'],  # Should be ignored
        'student_strengths_observed': ['New strengths'],  # Should be ignored
        'tutor_tips': ['New tips'],  # Should be ignored
    }
    response = client.put(f'/api/lessons/{lesson.id}', json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data['subject'] == 'Advanced Math'  # Should be updated
    assert data['skills_practiced'] == ['Calculating areas']  # Should remain unchanged
    assert data['student_strengths_observed'] == ['Good spatial awareness']  # Should remain unchanged


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
        grade='8th Grade',
    )
    session.add(student)
    session.commit()
    session.refresh(student)

    # Create a test lesson
    lesson = Lesson(
        student_id=student.id,
        date='2024-01-19',
        start_time='18:00',
        subject='History',
        topic='World War I',
        duration=60,
        notes='History lesson',
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


def test_lesson_status_enum(client: TestClient, session: Session):
    """Test creating lessons with different status values"""
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
        grade='7th Grade',
    )
    session.add(student)
    session.commit()
    session.refresh(student)

    # Test different status values
    statuses = ['planned', 'complete', 'pending', 'cancelled', 'cancelled-but-chargeable']

    for status in statuses:
        lesson_data = {
            'student_id': student.id,
            'date': '2024-01-20',
            'start_time': '19:00',
            'subject': 'Test Subject',
            'topic': f'Test Topic for {status}',
            'duration': 60,
            'notes': f'Test lesson with {status} status',
            'status': status,
        }
        response = client.post('/api/lessons/', json=lesson_data)
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == status


def test_create_lesson_invalid_status(client: TestClient, session: Session):
    """Test creating a lesson with invalid status"""
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
        grade='6th Grade',
    )
    session.add(student)
    session.commit()
    session.refresh(student)

    lesson_data = {
        'student_id': student.id,
        'date': '2024-01-21',
        'start_time': '20:00',
        'subject': 'Test Subject',
        'topic': 'Test Topic',
        'duration': 60,
        'notes': 'Test lesson',
        'status': 'invalid_status',
    }
    response = client.post('/api/lessons/', json=lesson_data)
    assert response.status_code == 422  # Validation error
