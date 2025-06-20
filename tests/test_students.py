from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models import Client, Company, Student, TutorStudent, User
from tests.conftest import AuthenticatedTestClient


def test_create_student(auth_client: AuthenticatedTestClient, session: Session):
    """Test creating a new student"""
    # First create a client
    client = Client(
        first_name='John',
        last_name='Doe',
        email='john.doe@example.com',
        phone='+1234567890',
    )
    session.add(client)
    session.commit()
    session.refresh(client)

    student_data = {
        'client_id': client.id,
        'first_name': 'Alice',
        'last_name': 'Smith',
        'email': 'alice.smith@example.com',
        'phone': '+1234567890',
        'grade': '10th Grade',
    }
    r = auth_client.post(auth_client.app.url_path_for('create_student'), json=student_data)
    assert r.status_code == 200, r.json()
    expected = {
        'client_id': client.id,
        'first_name': 'Alice',
        'last_name': 'Smith',
        'email': 'alice.smith@example.com',
        'phone': '+1234567890',
        'grade': '10th Grade',
    }
    for k, v in expected.items():
        assert r.json()[k] == v


def test_create_student_invalid_client_id(auth_client: AuthenticatedTestClient):
    """Test creating a student with invalid client_id"""
    student_data = {
        'client_id': 999,  # Non-existent client
        'first_name': 'Alice',
        'last_name': 'Smith',
        'email': 'alice.smith@example.com',
        'phone': '+1111111111',
        'grade': '10th Grade',
    }
    r = auth_client.post(auth_client.app.url_path_for('create_student'), json=student_data)
    assert r.status_code == 404, r.json()
    assert 'Client not found' in r.json()['detail']


def test_create_student_duplicate_email(auth_client: AuthenticatedTestClient, session: Session):
    """Test creating a student with duplicate email"""
    # First create a client
    client = Client(
        first_name='John',
        last_name='Doe',
        email='john.doe@example.com',
        phone='+1234567890',
    )
    session.add(client)
    session.commit()
    session.refresh(client)

    # Create first student
    student = Student(
        client_id=client.id,
        first_name='Alice',
        last_name='Smith',
        email='alice.smith@example.com',
        phone='+1111111111',
        grade='10th Grade',
    )
    session.add(student)
    session.commit()

    # Try to create another student with the same email
    student_data = {
        'client_id': client.id,
        'first_name': 'Bob',
        'last_name': 'Smith',
        'email': 'alice.smith@example.com',  # Same email
        'phone': '+2222222222',
        'grade': '10th Grade',
    }
    r = auth_client.post(auth_client.app.url_path_for('create_student'), json=student_data)
    assert r.status_code == 400, r.json()
    assert 'Email already registered' in r.json()['detail']


def test_get_students(auth_client: AuthenticatedTestClient, session: Session):
    """Test getting all students (tutor must be linked to students)."""

    # First create a client
    client = Client(
        first_name='John',
        last_name='Doe',
        email='john.doe@example.com',
        phone='+1234567890',
    )
    session.add(client)
    session.commit()
    session.refresh(client)

    # Create some test students
    students = [
        Student(
            client_id=client.id,
            first_name='Alice',
            last_name='Smith',
            email='alice.smith@example.com',
            phone='+1111111111',
            grade='10th Grade',
        ),
        Student(
            client_id=client.id,
            first_name='Bob',
            last_name='Jones',
            email='bob.jones@example.com',
            phone='+2222222222',
            grade='10th Grade',
        ),
    ]
    for student in students:
        session.add(student)
    session.commit()
    for student in students:
        session.refresh(student)
        session.add(TutorStudent(tutor_id=auth_client.user.id, student_id=student.id))
    session.commit()

    r = auth_client.get(auth_client.app.url_path_for('get_students'))
    assert r.status_code == 200, r.json()
    data = r.json()
    returned_ids = {s['id'] for s in data}
    expected_ids = {student.id for student in students}
    assert returned_ids == expected_ids


def test_get_students_by_client(auth_client, session):
    # Create two clients
    client1 = Client(
        first_name='John',
        last_name='Doe',
        email='john.doe@example.com',
        phone='+1234567890',
    )
    client2 = Client(
        first_name='Jane',
        last_name='Smith',
        email='jane.smith@example.com',
        phone='+0987654321',
    )
    session.add_all([client1, client2])
    session.commit()
    session.refresh(client1)
    session.refresh(client2)

    # Create students for each client
    student1 = Student(
        client_id=client1.id,
        first_name='Alice',
        last_name='Doe',
        email='alice.doe@example.com',
        phone='+1111111111',
        grade='10th Grade',
    )
    student2 = Student(
        client_id=client2.id,
        first_name='Bob',
        last_name='Smith',
        email='bob.smith@example.com',
        phone='+2222222222',
        grade='10th Grade',
    )
    session.add_all([student1, student2])
    session.commit()
    session.refresh(student1)
    session.refresh(student2)
    # Link both students to the test tutor
    session.add(TutorStudent(tutor_id=auth_client.user.id, student_id=student1.id))
    session.add(TutorStudent(tutor_id=auth_client.user.id, student_id=student2.id))
    session.commit()

    # Test getting students for client1
    r = auth_client.get(
        auth_client.app.url_path_for('get_students'),
        params={'client_id': client1.id},
    )
    assert r.status_code == 200, r.json()
    data = r.json()
    assert any(s['id'] == student1.id for s in data)
    assert all(s['client_id'] == client1.id for s in data)

    # Test getting students for client2
    r = auth_client.get(
        auth_client.app.url_path_for('get_students'),
        params={'client_id': client2.id},
    )
    assert r.status_code == 200, r.json()
    data = r.json()
    assert any(s['id'] == student2.id for s in data)
    assert all(s['client_id'] == client2.id for s in data)


def test_get_student_by_id(auth_client: AuthenticatedTestClient, session: Session):
    # Create a client and a student
    client = Client(
        first_name='John',
        last_name='Doe',
        email='john.doe@example.com',
        phone='+1234567890',
    )
    session.add(client)
    session.commit()
    session.refresh(client)
    student = Student(
        client_id=client.id,
        first_name='Alice',
        last_name='Smith',
        email='alice.smith@example.com',
        phone='+1111111111',
        grade='10th Grade',
    )
    session.add(student)
    session.commit()
    session.refresh(student)
    # Link student to test tutor
    session.add(TutorStudent(tutor_id=auth_client.user.id, student_id=student.id))
    session.commit()

    r = auth_client.get(auth_client.app.url_path_for('get_student', student_id=student.id))
    assert r.status_code == 200, r.json()
    data = r.json()
    assert data['id'] == student.id
    assert data['first_name'] == 'Alice'
    assert data['last_name'] == 'Smith'
    assert data['email'] == 'alice.smith@example.com'
    assert data['client_id'] == client.id


def test_get_nonexistent_student(auth_client: AuthenticatedTestClient):
    """Test getting a non-existent student"""
    r = auth_client.get(auth_client.app.url_path_for('get_student', student_id=999))
    assert r.status_code == 404, r.json()


def test_update_student(auth_client: AuthenticatedTestClient, session: Session):
    """Test updating a student"""
    # First create a client
    client = Client(
        first_name='John',
        last_name='Doe',
        email='john.doe@example.com',
        phone='+1234567890',
    )
    session.add(client)
    session.commit()
    session.refresh(client)

    # Create a test student
    student = Student(
        client_id=client.id,
        first_name='Alice',
        last_name='Smith',
        email='alice.smith@example.com',
        phone='+1111111111',
        grade='10th Grade',
    )
    session.add(student)
    session.commit()
    session.refresh(student)

    # Update student
    update_data = {
        'first_name': 'Alice',
        'last_name': 'Smith',
        'email': 'alice.smith.new@example.com',
        'phone': '+1111111111',
        'grade': '11th Grade',
    }
    r = auth_client.put(auth_client.app.url_path_for('update_student', student_id=student.id), json=update_data)
    assert r.status_code == 200, r.json()
    data = r.json()
    assert data['id'] == student.id
    assert data['first_name'] == 'Alice'
    assert data['email'] == 'alice.smith.new@example.com'
    assert data['grade'] == '11th Grade'


def test_update_student_duplicate_email(auth_client: AuthenticatedTestClient, session: Session):
    """Test updating a student with an email that's already in use"""
    # First create a client
    client = Client(
        first_name='John',
        last_name='Doe',
        email='john.doe@example.com',
        phone='+1234567890',
    )
    session.add(client)
    session.commit()
    session.refresh(client)

    # Create two test students
    student1 = Student(
        client_id=client.id,
        first_name='Alice',
        last_name='Smith',
        email='alice.smith@example.com',
        phone='+1111111111',
        grade='10th Grade',
    )
    student2 = Student(
        client_id=client.id,
        first_name='Bob',
        last_name='Jones',
        email='bob.jones@example.com',
        phone='+2222222222',
        grade='10th Grade',
    )
    session.add_all([student1, student2])
    session.commit()
    session.refresh(student1)
    session.refresh(student2)

    # Try to update student1 with student2's email
    update_data = {
        'first_name': 'Alice',
        'last_name': 'Smith',
        'email': 'bob.jones@example.com',  # student2's email
        'phone': '+1111111111',
        'grade': '10th Grade',
    }
    r = auth_client.put(auth_client.app.url_path_for('update_student', student_id=student1.id), json=update_data)
    assert r.status_code == 400, r.json()
    assert 'Email already registered' in r.json()['detail']


def test_update_nonexistent_student(auth_client: AuthenticatedTestClient):
    """Test updating a non-existent student"""
    update_data = {
        'first_name': 'Alice',
        'last_name': 'Smith',
        'email': 'alice.smith@example.com',
        'phone': '+1111111111',
        'grade': '10th Grade',
    }
    r = auth_client.put(auth_client.app.url_path_for('update_student', student_id=999), json=update_data)
    assert r.status_code == 404, r.json()


def test_delete_student(auth_client: AuthenticatedTestClient, session: Session, test_tutor: User):
    """Test deleting a student"""
    # First create a client
    client = Client(
        first_name='John',
        last_name='Doe',
        email='john.doe@example.com',
        phone='+1234567890',
    )
    session.add(client)
    session.commit()
    session.refresh(client)

    # Create a test student
    student = Student(
        client_id=client.id,
        first_name='Alice',
        last_name='Smith',
        email='alice.smith@example.com',
        phone='+1111111111',
        grade='10th Grade',
    )
    session.add(student)
    session.commit()
    session.refresh(student)

    r = auth_client.delete(auth_client.app.url_path_for('delete_student', student_id=student.id))
    assert r.status_code == 200, r.json()
    assert r.json()['message'] == 'Student deleted successfully'

    # Verify student is deleted
    r = auth_client.get(auth_client.app.url_path_for('get_student', student_id=student.id))
    assert r.status_code == 404, r.json()


def test_delete_nonexistent_student(auth_client: AuthenticatedTestClient):
    """Test deleting a non-existent student"""
    r = auth_client.delete(auth_client.app.url_path_for('delete_student', student_id=999))
    assert r.status_code == 404, r.json()


def test_unauthorized_access(client: TestClient):
    """Test accessing endpoints without authentication"""
    # Test create student
    r = client.post(client.app.url_path_for('create_student'), json={})
    assert r.status_code == 401

    # Test get students
    r = client.get(client.app.url_path_for('get_students'))
    assert r.status_code == 401

    # Test get student by id
    r = client.get(client.app.url_path_for('get_student', student_id=1))
    assert r.status_code == 401

    # Test update student
    r = client.put(client.app.url_path_for('update_student', student_id=1), json={})
    assert r.status_code == 401

    # Test delete student
    r = client.delete(client.app.url_path_for('delete_student', student_id=1))
    assert r.status_code == 401


def test_tutor_sees_only_their_students(auth_client, client, session):
    """Test that a tutor only sees students linked to them via TutorStudent."""
    from app.models import User, UserType
    from tests.conftest import create_authenticated_client_for_user

    # Create two tutors
    tutor1 = User(
        first_name='Tutor', last_name='One', email='tutor1@example.com', user_type=UserType.TUTOR, hashed_password='x'
    )
    tutor2 = User(
        first_name='Tutor', last_name='Two', email='tutor2@example.com', user_type=UserType.TUTOR, hashed_password='x'
    )
    session.add_all([tutor1, tutor2])
    session.commit()
    session.refresh(tutor1)
    session.refresh(tutor2)

    # Create a client and two students
    c = Client(first_name='Client', last_name='A', email='clienta@example.com', phone='+123')
    session.add(c)
    session.commit()
    session.refresh(c)
    student1 = Student(
        client_id=c.id, first_name='Student', last_name='One', email='student1@example.com', phone='+1', grade='10'
    )
    student2 = Student(
        client_id=c.id, first_name='Student', last_name='Two', email='student2@example.com', phone='+2', grade='10'
    )
    session.add_all([student1, student2])
    session.commit()
    session.refresh(student1)
    session.refresh(student2)

    # Link student1 to tutor1, student2 to tutor2
    session.add(TutorStudent(tutor_id=tutor1.id, student_id=student1.id))
    session.add(TutorStudent(tutor_id=tutor2.id, student_id=student2.id))
    session.commit()

    # Use authenticated client as tutor1
    tutor1_client = create_authenticated_client_for_user(client, tutor1)
    r = tutor1_client.get(tutor1_client.app.url_path_for('get_students'))
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]['id'] == student1.id
    assert data[0]['first_name'] == 'Student'
    assert data[0]['last_name'] == 'One'

    # Use authenticated client as tutor2
    tutor2_client = create_authenticated_client_for_user(client, tutor2)
    r = tutor2_client.get(tutor2_client.app.url_path_for('get_students'))
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]['id'] == student2.id
    assert data[0]['first_name'] == 'Student'
    assert data[0]['last_name'] == 'Two'


def test_admin_sees_only_their_company_students(auth_client, client, session):
    """Test that an admin only sees students for their companies."""
    from app.models import User, UserType
    from tests.conftest import create_authenticated_client_for_user

    # Create two companies
    company1 = Company(name='Company1', tc_id='c1', tutorcruncher_domain='https://c1')
    company2 = Company(name='Company2', tc_id='c2', tutorcruncher_domain='https://c2')
    session.add_all([company1, company2])
    session.commit()
    session.refresh(company1)
    session.refresh(company2)

    # Create two admins
    admin1 = User(
        first_name='Admin',
        last_name='One',
        email='admin1@example.com',
        user_type=UserType.ADMIN,
        hashed_password='x',
        company_ids=[company1.id],
    )
    admin2 = User(
        first_name='Admin',
        last_name='Two',
        email='admin2@example.com',
        user_type=UserType.ADMIN,
        hashed_password='x',
        company_ids=[company2.id],
    )
    session.add_all([admin1, admin2])
    session.commit()
    session.refresh(admin1)
    session.refresh(admin2)

    # Create a client and two students, each linked to a different company
    c = Client(first_name='Client', last_name='A', email='clienta@example.com', phone='+123')
    session.add(c)
    session.commit()
    session.refresh(c)
    student1 = Student(
        client_id=c.id,
        first_name='Student',
        last_name='One',
        email='student1c1@example.com',
        phone='+1',
        grade='10',
        company_id=company1.id,
    )
    student2 = Student(
        client_id=c.id,
        first_name='Student',
        last_name='Two',
        email='student2c2@example.com',
        phone='+2',
        grade='10',
        company_id=company2.id,
    )
    session.add_all([student1, student2])
    session.commit()
    session.refresh(student1)
    session.refresh(student2)

    # Use authenticated client as admin1
    admin1_client = create_authenticated_client_for_user(client, admin1)
    r = admin1_client.get(admin1_client.app.url_path_for('get_students'))
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]['id'] == student1.id
    assert data[0]['company_id'] == company1.id

    # Use authenticated client as admin2
    admin2_client = create_authenticated_client_for_user(client, admin2)
    r = admin2_client.get(admin2_client.app.url_path_for('get_students'))
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]['id'] == student2.id
    assert data[0]['company_id'] == company2.id


def test_no_cross_visibility_between_tutors_and_admins(auth_client, client, session):
    """Test that tutors do not see students for other tutors, and admins do not see students for other companies."""
    from app.models import User, UserType
    from tests.conftest import create_authenticated_client_for_user

    # Create company and users
    company = Company(name='Company', tc_id='c', tutorcruncher_domain='https://c')
    session.add(company)
    session.commit()
    session.refresh(company)
    tutor = User(
        first_name='Tutor', last_name='X', email='tutorx@example.com', user_type=UserType.TUTOR, hashed_password='x'
    )
    admin = User(
        first_name='Admin',
        last_name='Y',
        email='adminy@example.com',
        user_type=UserType.ADMIN,
        hashed_password='x',
        company_ids=[company.id],
    )
    session.add_all([tutor, admin])
    session.commit()
    session.refresh(tutor)
    session.refresh(admin)
    # Create client and students
    c = Client(first_name='Client', last_name='A', email='clienta@example.com', phone='+123')
    session.add(c)
    session.commit()
    session.refresh(c)
    student = Student(
        client_id=c.id,
        first_name='Student',
        last_name='Z',
        email='studentz@example.com',
        phone='+1',
        grade='10',
        company_id=company.id,
    )
    session.add(student)
    session.commit()
    session.refresh(student)
    # Link student to tutor
    session.add(TutorStudent(tutor_id=tutor.id, student_id=student.id))
    session.commit()
    # Tutor sees student
    tutor_client = create_authenticated_client_for_user(client, tutor)
    r = tutor_client.get(tutor_client.app.url_path_for('get_students'))
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]['id'] == student.id
    # Admin sees student
    admin_client = create_authenticated_client_for_user(client, admin)
    r = admin_client.get(admin_client.app.url_path_for('get_students'))
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]['id'] == student.id
    # New tutor sees no students
    tutor2 = User(
        first_name='Tutor', last_name='Q', email='tutorq@example.com', user_type=UserType.TUTOR, hashed_password='x'
    )
    session.add(tutor2)
    session.commit()
    session.refresh(tutor2)
    tutor2_client = create_authenticated_client_for_user(client, tutor2)
    r = tutor2_client.get(tutor2_client.app.url_path_for('get_students'))
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 0
    # New admin with no company_ids sees NO students
    admin2 = User(
        first_name='Admin',
        last_name='Z',
        email='adminz@example.com',
        user_type=UserType.ADMIN,
        hashed_password='x',
        company_ids=[],
    )
    session.add(admin2)
    session.commit()
    session.refresh(admin2)
    admin2_client = create_authenticated_client_for_user(client, admin2)
    r = admin2_client.get(admin2_client.app.url_path_for('get_students'))
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 0  # Should see no students
