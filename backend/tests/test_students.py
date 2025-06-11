from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models import Student


def test_create_student(client: TestClient):
    student_data = {
        'name': 'Test Student',
        'grade': '9th Grade',
        'strengths': ['Math', 'Science'],
        'weaknesses': ['Writing', 'History'],
    }
    response = client.post('/api/students/', json=student_data)
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == student_data['name']
    assert data['grade'] == student_data['grade']
    assert data['lessons_completed'] == 0


def test_get_students(client: TestClient, session: Session):
    # Create a test student
    student = Student(name='Test Student', grade='10th Grade', strengths=['Math'], weaknesses=['English'])
    session.add(student)
    session.commit()

    response = client.get('/api/students/')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['name'] == 'Test Student'


def test_get_student_by_id(client: TestClient, session: Session):
    # Create a test student
    student = Student(name='Test Student', grade='11th Grade', strengths=['Science'], weaknesses=['Math'])
    session.add(student)
    session.commit()
    session.refresh(student)

    response = client.get(f'/api/students/{student.id}')
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'Test Student'
    assert data['id'] == student.id


def test_get_nonexistent_student(client: TestClient):
    response = client.get('/api/students/999')
    assert response.status_code == 404
