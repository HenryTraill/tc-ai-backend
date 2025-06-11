from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models.client import Client
from app.models.student import Student


def test_create_student(client: TestClient, session: Session):
    """Test creating a new student"""
    # First create a client
    test_client = Client(first_name='John', last_name='Doe', email='john.doe@example.com', phone='+1234567890')
    session.add(test_client)
    session.commit()
    session.refresh(test_client)

    student_data = {
        'client_id': test_client.id,
        'first_name': 'Alice',
        'last_name': 'Smith',
        'email': 'alice.smith@example.com',
        'phone': '+1111111111',
        'grade': '9th Grade',
        'strengths': ['Math', 'Science'],
        'weaknesses': ['Writing', 'History'],
    }
    response = client.post('/api/students/', json=student_data)
    assert response.status_code == 200
    data = response.json()
    assert data['client_id'] == test_client.id
    assert data['first_name'] == student_data['first_name']
    assert data['last_name'] == student_data['last_name']
    assert data['email'] == student_data['email']
    assert data['phone'] == student_data['phone']
    assert data['grade'] == student_data['grade']
    assert data['lessons_completed'] == 0


def test_create_student_invalid_client_id(client: TestClient):
    """Test creating a student with invalid client_id"""
    student_data = {
        'client_id': 999,  # Non-existent client
        'first_name': 'Alice',
        'last_name': 'Smith',
        'email': 'alice.smith@example.com',
        'phone': '+1111111111',
        'grade': '9th Grade',
    }
    response = client.post('/api/students/', json=student_data)
    # This might return 500 or 400 depending on database constraints
    assert response.status_code in [400, 422, 500]


def test_get_students(client: TestClient, session: Session):
    """Test getting all students"""
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
        strengths=['Math'],
        weaknesses=['English'],
    )
    session.add(student)
    session.commit()

    response = client.get('/api/students/')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['first_name'] == 'Alice'
    assert data[0]['last_name'] == 'Smith'


def test_get_student_by_id(client: TestClient, session: Session):
    """Test getting a specific student by ID"""
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
        strengths=['Science'],
        weaknesses=['Math'],
    )
    session.add(student)
    session.commit()
    session.refresh(student)

    response = client.get(f'/api/students/{student.id}')
    assert response.status_code == 200
    data = response.json()
    assert data['first_name'] == 'Alice'
    assert data['last_name'] == 'Smith'
    assert data['id'] == student.id


def test_get_nonexistent_student(client: TestClient):
    """Test getting a non-existent student"""
    response = client.get('/api/students/999')
    assert response.status_code == 404


def test_update_student(client: TestClient, session: Session):
    """Test updating a student"""
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
        strengths=['Math'],
        weaknesses=['English'],
    )
    session.add(student)
    session.commit()
    session.refresh(student)

    # Update student
    update_data = {'first_name': 'Alicia', 'grade': '11th Grade', 'email': 'alicia.smith@example.com'}
    response = client.put(f'/api/students/{student.id}', json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data['first_name'] == 'Alicia'
    assert data['grade'] == '11th Grade'
    assert data['email'] == 'alicia.smith@example.com'
    assert data['last_name'] == 'Smith'  # Should remain unchanged


def test_update_student_strengths_weaknesses_ignored(client: TestClient, session: Session):
    """Test that strengths and weaknesses cannot be updated through the API"""
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
        strengths=['Math'],
        weaknesses=['English'],
    )
    session.add(student)
    session.commit()
    session.refresh(student)

    # Try to update strengths and weaknesses (should be ignored)
    update_data = {
        'first_name': 'Alicia',
        'strengths': ['Science', 'Physics'],  # Should be ignored
        'weaknesses': ['History'],  # Should be ignored
    }
    response = client.put(f'/api/students/{student.id}', json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data['first_name'] == 'Alicia'  # Should be updated
    assert data['strengths'] == ['Math']  # Should remain unchanged
    assert data['weaknesses'] == ['English']  # Should remain unchanged


def test_delete_student(client: TestClient, session: Session):
    """Test deleting a student"""
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

    response = client.delete(f'/api/students/{student.id}')
    assert response.status_code == 200
    data = response.json()
    assert data['message'] == 'Student deleted successfully'

    # Verify student is deleted
    response = client.get(f'/api/students/{student.id}')
    assert response.status_code == 404
