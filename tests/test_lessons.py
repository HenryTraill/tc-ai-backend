from datetime import datetime, timezone

from dirty_equals import IsDatetime
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.models import Client, Company, Lesson, LessonStudent, LessonTutor, Student, User, UserType
from tests.conftest import AuthenticatedTestClient


def test_create_lesson(auth_client: AuthenticatedTestClient, session: Session):
    """Test creating a new lesson"""
    # First create a client and student
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

    lesson_data = {
        'start_dt': '2024-01-15T14:00:00Z',
        'end_dt': '2024-01-15T15:00:00Z',
        'subject': 'Mathematics',
        'topic': 'Algebra',
        'notes': 'Math lesson',
        'student_ids': [student.id],
    }
    r = auth_client.post(auth_client.app.url_path_for('create_lesson'), json=lesson_data)
    assert r.status_code == 200, r.json()
    data = r.json()
    assert data['id'] == 1
    assert data['subject'] == 'Mathematics'
    assert data['topic'] == 'Algebra'
    assert data['notes'] == 'Math lesson'
    assert len(data['students']) == 1
    assert data['students'][0]['id'] == student.id
    assert data['created_at'] == IsDatetime(format_string='%Y-%m-%dT%H:%M:%S.%f')
    assert data['updated_at'] is None

    # Verify tutor association was created
    lesson_tutor = session.exec(select(LessonTutor).where(LessonTutor.lesson_id == data['id'])).first()
    assert lesson_tutor is not None
    assert lesson_tutor.tutor_id == auth_client.user.id


def test_create_lesson_with_company(auth_client: AuthenticatedTestClient, session: Session):
    """Test creating a lesson with a company"""
    # First create a client and student
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

    # Create a company
    company = Company(
        name='Test Company',
        tc_id='123',
        tutorcruncher_domain='https://test.tutorcruncher.com',
    )
    session.add(company)
    session.commit()
    session.refresh(company)

    # Add company to user's company_ids if admin
    if not auth_client.user.is_tutor:
        auth_client.user.company_ids.append(company.id)
        session.add(auth_client.user)
        session.commit()

    lesson_data = {
        'start_dt': '2024-01-15T14:00:00Z',
        'end_dt': '2024-01-15T15:00:00Z',
        'subject': 'Mathematics',
        'topic': 'Algebra',
        'notes': 'Math lesson',
        'student_ids': [student.id],
        'company_id': company.id,
    }
    r = auth_client.post(auth_client.app.url_path_for('create_lesson'), json=lesson_data)
    assert r.status_code == 200, r.json()
    data = r.json()
    assert data['company_id'] == company.id


def test_create_lesson_with_invalid_company(auth_client: AuthenticatedTestClient, session: Session):
    """Test creating a lesson with an invalid company ID"""
    # First create a client and student
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

    lesson_data = {
        'start_dt': '2024-01-15T14:00:00Z',
        'end_dt': '2024-01-15T15:00:00Z',
        'subject': 'Mathematics',
        'topic': 'Algebra',
        'notes': 'Math lesson',
        'student_ids': [student.id],
        'company_id': 999,  # Non-existent company
    }
    r = auth_client.post(auth_client.app.url_path_for('create_lesson'), json=lesson_data)
    assert r.status_code == 404, r.json()
    assert 'Company not found' in r.json()['detail']


def test_create_lesson_with_unauthorized_company(auth_client: AuthenticatedTestClient, session: Session):
    """Test creating a lesson with a company the admin doesn't have access to"""
    if auth_client.user.is_tutor:
        return  # Skip test for tutors

    # First create a client and student
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

    # Create a company
    company = Company(
        name='Test Company',
        tc_id='123',
        tutorcruncher_domain='https://test.tutorcruncher.com',
    )
    session.add(company)
    session.commit()
    session.refresh(company)

    # Ensure company is not in user's company_ids
    if company.id in auth_client.user.company_ids:
        auth_client.user.company_ids.remove(company.id)
        session.add(auth_client.user)
        session.commit()

    lesson_data = {
        'start_dt': '2024-01-15T14:00:00Z',
        'end_dt': '2024-01-15T15:00:00Z',
        'subject': 'Mathematics',
        'topic': 'Algebra',
        'notes': 'Math lesson',
        'student_ids': [student.id],
        'company_id': company.id,
    }
    r = auth_client.post(auth_client.app.url_path_for('create_lesson'), json=lesson_data)
    assert r.status_code == 403, r.json()
    assert 'Not authorized to create lessons for this company' in r.json()['detail']


def test_get_lessons_tutor_filtering(auth_client: AuthenticatedTestClient, session: Session):
    """Test that tutors can only see their own lessons"""
    # Ensure the user is a tutor
    if not auth_client.user.is_tutor:
        auth_client.user.is_tutor = True
        auth_client.user.is_admin = False
        session.add(auth_client.user)
        session.commit()

    # First create a client and student
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

    # Create two lessons
    lessons = [
        Lesson(
            start_dt=datetime(2024, 1, 15, 14, 0, tzinfo=timezone.utc),
            end_dt=datetime(2024, 1, 15, 15, 0, tzinfo=timezone.utc),
            subject='Mathematics',
            topic='Algebra',
            notes='Math lesson 1',
        ),
        Lesson(
            start_dt=datetime(2024, 1, 16, 15, 0, tzinfo=timezone.utc),
            end_dt=datetime(2024, 1, 16, 16, 0, tzinfo=timezone.utc),
            subject='Physics',
            topic='Mechanics',
            notes='Physics lesson',
        ),
    ]
    for lesson in lessons:
        session.add(lesson)
    session.commit()
    for lesson in lessons:
        session.refresh(lesson)

    # Associate student with lessons
    for lesson in lessons:
        lesson_student = LessonStudent(lesson_id=lesson.id, student_id=student.id)
        session.add(lesson_student)
    session.commit()

    # Associate only first lesson with current tutor
    lesson_tutor = LessonTutor(lesson_id=lessons[0].id, tutor_id=auth_client.user.id)
    session.add(lesson_tutor)
    session.commit()

    # Create another tutor and associate with second lesson
    other_tutor = User(
        email='other@example.com',
        hashed_password='dummy',
        is_tutor=True,
        is_admin=False,
        first_name='Other',
        last_name='Tutor',
        user_type=UserType.TUTOR,
    )
    session.add(other_tutor)
    session.commit()
    session.refresh(other_tutor)

    lesson_tutor = LessonTutor(lesson_id=lessons[1].id, tutor_id=other_tutor.id)
    session.add(lesson_tutor)
    session.commit()

    # Test getting lessons - should only see first lesson
    r = auth_client.get(auth_client.app.url_path_for('get_lessons'))
    assert r.status_code == 200, r.json()
    data = r.json()
    assert len(data) == 1
    assert data[0]['id'] == lessons[0].id
    assert data[0]['subject'] == 'Mathematics'


def test_get_lessons_admin_filtering(auth_client: AuthenticatedTestClient, session: Session):
    """Test that admins can only see lessons for their companies"""
    if auth_client.user.is_tutor:
        return  # Skip test for tutors

    # First create a client and student
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

    # Create two companies
    companies = [
        Company(
            name='Company 1',
            tc_id='123',
            tutorcruncher_domain='https://company1.tutorcruncher.com',
        ),
        Company(
            name='Company 2',
            tc_id='456',
            tutorcruncher_domain='https://company2.tutorcruncher.com',
        ),
    ]
    for company in companies:
        session.add(company)
    session.commit()
    for company in companies:
        session.refresh(company)

    # Add first company to user's company_ids
    auth_client.user.company_ids = [companies[0].id]
    session.add(auth_client.user)
    session.commit()

    # Create two lessons, one for each company
    lessons = [
        Lesson(
            start_dt=datetime(2024, 1, 15, 14, 0, tzinfo=timezone.utc),
            end_dt=datetime(2024, 1, 15, 15, 0, tzinfo=timezone.utc),
            subject='Mathematics',
            topic='Algebra',
            notes='Math lesson 1',
            company_id=companies[0].id,
        ),
        Lesson(
            start_dt=datetime(2024, 1, 16, 15, 0, tzinfo=timezone.utc),
            end_dt=datetime(2024, 1, 16, 16, 0, tzinfo=timezone.utc),
            subject='Physics',
            topic='Mechanics',
            notes='Physics lesson',
            company_id=companies[1].id,
        ),
    ]
    for lesson in lessons:
        session.add(lesson)
    session.commit()
    for lesson in lessons:
        session.refresh(lesson)

    # Associate student with lessons
    for lesson in lessons:
        lesson_student = LessonStudent(lesson_id=lesson.id, student_id=student.id)
        session.add(lesson_student)
    session.commit()

    # Test getting lessons - should only see first lesson
    r = auth_client.get(auth_client.app.url_path_for('get_lessons'))
    assert r.status_code == 200, r.json()
    data = r.json()
    assert len(data) == 1
    assert data[0]['id'] == lessons[0].id
    assert data[0]['subject'] == 'Mathematics'


def test_update_company_linked_lesson(auth_client: AuthenticatedTestClient, session: Session):
    """Test that company-linked lessons cannot be updated"""
    # First create a client and student
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

    # Create a company
    company = Company(
        name='Test Company',
        tc_id='123',
        tutorcruncher_domain='https://test.tutorcruncher.com',
    )
    session.add(company)
    session.commit()
    session.refresh(company)

    # Create a test lesson
    lesson = Lesson(
        start_dt=datetime(2024, 1, 15, 14, 0, tzinfo=timezone.utc),
        end_dt=datetime(2024, 1, 15, 15, 0, tzinfo=timezone.utc),
        subject='Mathematics',
        topic='Algebra',
        notes='Math lesson',
        company_id=company.id,
    )
    session.add(lesson)
    session.commit()
    session.refresh(lesson)

    # Associate student with lesson
    lesson_student = LessonStudent(lesson_id=lesson.id, student_id=student.id)
    session.add(lesson_student)
    session.commit()

    # Associate tutor with lesson
    lesson_tutor = LessonTutor(lesson_id=lesson.id, tutor_id=auth_client.user.id)
    session.add(lesson_tutor)
    session.commit()

    # Try to update lesson
    update_data = {
        'subject': 'Physics',
        'topic': 'Mechanics',
        'notes': 'Updated lesson',
    }
    r = auth_client.put(auth_client.app.url_path_for('update_lesson', lesson_id=lesson.id), json=update_data)
    assert r.status_code == 400, r.json()
    assert 'Cannot update lesson that is linked to a company' in r.json()['detail']


def test_delete_company_linked_lesson(auth_client: AuthenticatedTestClient, session: Session):
    """Test that company-linked lessons cannot be deleted"""
    # First create a client and student
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

    # Create a company
    company = Company(
        name='Test Company',
        tc_id='123',
        tutorcruncher_domain='https://test.tutorcruncher.com',
    )
    session.add(company)
    session.commit()
    session.refresh(company)

    # Create a test lesson
    lesson = Lesson(
        start_dt=datetime(2024, 1, 15, 14, 0, tzinfo=timezone.utc),
        end_dt=datetime(2024, 1, 15, 15, 0, tzinfo=timezone.utc),
        subject='Mathematics',
        topic='Algebra',
        notes='Math lesson',
        company_id=company.id,
    )
    session.add(lesson)
    session.commit()
    session.refresh(lesson)

    # Associate student with lesson
    lesson_student = LessonStudent(lesson_id=lesson.id, student_id=student.id)
    session.add(lesson_student)
    session.commit()

    # Associate tutor with lesson
    lesson_tutor = LessonTutor(lesson_id=lesson.id, tutor_id=auth_client.user.id)
    session.add(lesson_tutor)
    session.commit()

    # Try to delete lesson
    r = auth_client.delete(auth_client.app.url_path_for('delete_lesson', lesson_id=lesson.id))
    assert r.status_code == 400, r.json()
    assert 'Cannot delete lesson that is linked to a company' in r.json()['detail']


def test_create_lesson_with_multiple_students(auth_client: AuthenticatedTestClient, session: Session):
    """Test creating a lesson with multiple students"""
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

    # Create multiple students
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

    lesson_data = {
        'start_dt': '2024-01-15T14:00:00Z',
        'end_dt': '2024-01-15T15:00:00Z',
        'subject': 'Mathematics',
        'topic': 'Algebra',
        'notes': 'Group math lesson',
        'student_ids': [student.id for student in students],
    }
    r = auth_client.post(auth_client.app.url_path_for('create_lesson'), json=lesson_data)
    assert r.status_code == 200, r.json()
    data = r.json()
    assert len(data['students']) == 2
    student_ids = [student['id'] for student in data['students']]
    assert students[0].id in student_ids
    assert students[1].id in student_ids


def test_create_lesson_with_specific_status(auth_client: AuthenticatedTestClient, session: Session):
    """Test creating a lesson with a specific status"""
    # First create a client and student
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

    lesson_data = {
        'start_dt': '2024-01-15T14:00:00Z',
        'end_dt': '2024-01-15T15:00:00Z',
        'subject': 'Mathematics',
        'topic': 'Algebra',
        'notes': 'Math lesson',
        'student_ids': [student.id],
        'status': 'complete',
    }
    r = auth_client.post(auth_client.app.url_path_for('create_lesson'), json=lesson_data)
    assert r.status_code == 200, r.json()
    data = r.json()
    assert data['status'] == 'complete'


def test_create_lesson_with_invalid_student(auth_client: AuthenticatedTestClient, session: Session):
    """Test creating a lesson with an invalid student ID"""
    lesson_data = {
        'start_dt': '2024-01-15T14:00:00Z',
        'end_dt': '2024-01-15T15:00:00Z',
        'subject': 'Mathematics',
        'topic': 'Algebra',
        'notes': 'Math lesson',
        'student_ids': [999],  # Non-existent student
    }
    r = auth_client.post(auth_client.app.url_path_for('create_lesson'), json=lesson_data)
    assert r.status_code == 404, r.json()
    assert 'Student not found' in r.json()['detail']


def test_create_lesson_with_invalid_dates(auth_client: AuthenticatedTestClient, session: Session):
    """Test creating a lesson with invalid dates"""
    # First create a client and student
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

    # Test with end date before start date
    lesson_data = {
        'start_dt': '2024-01-15T15:00:00Z',
        'end_dt': '2024-01-15T14:00:00Z',  # End before start
        'subject': 'Mathematics',
        'topic': 'Algebra',
        'notes': 'Math lesson',
        'student_ids': [student.id],
    }
    r = auth_client.post(auth_client.app.url_path_for('create_lesson'), json=lesson_data)
    assert r.status_code == 400, r.json()
    assert 'End date must be after start date' in r.json()['detail']


def test_get_lessons(auth_client: AuthenticatedTestClient, session: Session):
    """Test getting all lessons"""
    # First create a client and student
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

    # Create some test lessons
    lessons = [
        Lesson(
            start_dt=datetime(2024, 1, 15, 14, 0, tzinfo=timezone.utc),
            end_dt=datetime(2024, 1, 15, 15, 0, tzinfo=timezone.utc),
            subject='Mathematics',
            topic='Algebra',
            notes='Math lesson 1',
        ),
        Lesson(
            start_dt=datetime(2024, 1, 16, 15, 0, tzinfo=timezone.utc),
            end_dt=datetime(2024, 1, 16, 16, 0, tzinfo=timezone.utc),
            subject='Physics',
            topic='Mechanics',
            notes='Physics lesson',
        ),
    ]
    for lesson in lessons:
        session.add(lesson)
    session.commit()
    for lesson in lessons:
        session.refresh(lesson)

    # Associate student with lessons
    for lesson in lessons:
        lesson_student = LessonStudent(lesson_id=lesson.id, student_id=student.id)
        session.add(lesson_student)
    session.commit()

    # Associate tutor with lessons
    for lesson in lessons:
        lesson_tutor = LessonTutor(lesson_id=lesson.id, tutor_id=auth_client.user.id)
        session.add(lesson_tutor)
    session.commit()

    r = auth_client.get(auth_client.app.url_path_for('get_lessons'))
    assert r.status_code == 200, r.json()
    data = r.json()
    assert len(data) == 2
    assert data[0]['subject'] == 'Mathematics'
    assert data[1]['subject'] == 'Physics'
    assert len(data[0]['students']) == 1
    assert len(data[1]['students']) == 1


def test_get_lessons_by_student(auth_client: AuthenticatedTestClient, session: Session):
    """Test getting lessons filtered by student ID"""
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

    # Create two students
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

    # Create lessons
    lessons = [
        Lesson(
            start_dt=datetime(2024, 1, 15, 14, 0, tzinfo=timezone.utc),
            end_dt=datetime(2024, 1, 15, 15, 0, tzinfo=timezone.utc),
            subject='Mathematics',
            topic='Algebra',
            notes='Math lesson',
        ),
        Lesson(
            start_dt=datetime(2024, 1, 16, 15, 0, tzinfo=timezone.utc),
            end_dt=datetime(2024, 1, 16, 16, 0, tzinfo=timezone.utc),
            subject='Physics',
            topic='Mechanics',
            notes='Physics lesson',
        ),
    ]
    for lesson in lessons:
        session.add(lesson)
    session.commit()
    for lesson in lessons:
        session.refresh(lesson)

    # Associate first lesson with first student, second lesson with both students
    lesson_students = [
        LessonStudent(lesson_id=lessons[0].id, student_id=students[0].id),
        LessonStudent(lesson_id=lessons[1].id, student_id=students[0].id),
        LessonStudent(lesson_id=lessons[1].id, student_id=students[1].id),
    ]
    for lesson_student in lesson_students:
        session.add(lesson_student)
    session.commit()

    # Associate tutor with lessons
    for lesson in lessons:
        lesson_tutor = LessonTutor(lesson_id=lesson.id, tutor_id=auth_client.user.id)
        session.add(lesson_tutor)
    session.commit()

    # Test getting lessons for first student
    r = auth_client.get(
        auth_client.app.url_path_for('get_lessons'),
        params={'student_id': students[0].id},
    )
    assert r.status_code == 200, r.json()
    data = r.json()
    assert len(data) == 2
    assert data[0]['subject'] == 'Mathematics'
    assert data[1]['subject'] == 'Physics'

    # Test getting lessons for second student
    r = auth_client.get(
        auth_client.app.url_path_for('get_lessons'),
        params={'student_id': students[1].id},
    )
    assert r.status_code == 200, r.json()
    data = r.json()
    assert len(data) == 1
    assert data[0]['subject'] == 'Physics'


def test_get_lesson_by_id(auth_client: AuthenticatedTestClient, session: Session):
    """Test getting a specific lesson by ID"""
    # First create a client and student
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

    # Create a test lesson
    lesson = Lesson(
        start_dt=datetime(2024, 1, 15, 14, 0, tzinfo=timezone.utc),
        end_dt=datetime(2024, 1, 15, 15, 0, tzinfo=timezone.utc),
        subject='Mathematics',
        topic='Algebra',
        notes='Math lesson',
    )
    session.add(lesson)
    session.commit()
    session.refresh(lesson)

    # Associate student with lesson
    lesson_student = LessonStudent(lesson_id=lesson.id, student_id=student.id)
    session.add(lesson_student)
    session.commit()

    # Associate tutor with lesson
    lesson_tutor = LessonTutor(lesson_id=lesson.id, tutor_id=auth_client.user.id)
    session.add(lesson_tutor)
    session.commit()

    r = auth_client.get(auth_client.app.url_path_for('get_lesson', lesson_id=lesson.id))
    assert r.status_code == 200, r.json()
    data = r.json()
    assert data['id'] == lesson.id
    assert data['subject'] == 'Mathematics'
    assert data['topic'] == 'Algebra'
    assert len(data['students']) == 1
    assert data['students'][0]['id'] == student.id


def test_get_nonexistent_lesson(auth_client: AuthenticatedTestClient):
    """Test getting a non-existent lesson"""
    r = auth_client.get(auth_client.app.url_path_for('get_lesson', lesson_id=999))
    assert r.status_code == 404, r.json()


def test_update_lesson(auth_client: AuthenticatedTestClient, session: Session):
    """Test updating a lesson"""
    # First create a client and student
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

    # Create a test lesson
    lesson = Lesson(
        start_dt=datetime(2024, 1, 15, 14, 0, tzinfo=timezone.utc),
        end_dt=datetime(2024, 1, 15, 15, 0, tzinfo=timezone.utc),
        subject='Mathematics',
        topic='Algebra',
        notes='Math lesson',
    )
    session.add(lesson)
    session.commit()
    session.refresh(lesson)

    # Associate student with lesson
    lesson_student = LessonStudent(lesson_id=lesson.id, student_id=student.id)
    session.add(lesson_student)
    session.commit()

    # Associate tutor with lesson
    lesson_tutor = LessonTutor(lesson_id=lesson.id, tutor_id=auth_client.user.id)
    session.add(lesson_tutor)
    session.commit()

    # Update lesson
    update_data = {
        'subject': 'Physics',
        'topic': 'Mechanics',
        'notes': 'Updated lesson',
    }
    r = auth_client.put(auth_client.app.url_path_for('update_lesson', lesson_id=lesson.id), json=update_data)
    assert r.status_code == 200, r.json()
    data = r.json()
    assert data['id'] == lesson.id
    assert data['subject'] == 'Physics'
    assert data['topic'] == 'Mechanics'
    assert data['notes'] == 'Updated lesson'
    assert len(data['students']) == 1
    assert data['students'][0]['id'] == student.id


def test_update_lesson_with_new_students(auth_client: AuthenticatedTestClient, session: Session):
    """Test updating a lesson with new students"""
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

    # Create two students
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

    # Create a test lesson
    lesson = Lesson(
        start_dt=datetime(2024, 1, 15, 14, 0, tzinfo=timezone.utc),
        end_dt=datetime(2024, 1, 15, 15, 0, tzinfo=timezone.utc),
        subject='Mathematics',
        topic='Algebra',
        notes='Math lesson',
    )
    session.add(lesson)
    session.commit()
    session.refresh(lesson)

    # Associate first student with lesson
    lesson_student = LessonStudent(lesson_id=lesson.id, student_id=students[0].id)
    session.add(lesson_student)
    session.commit()

    # Associate tutor with lesson
    lesson_tutor = LessonTutor(lesson_id=lesson.id, tutor_id=auth_client.user.id)
    session.add(lesson_tutor)
    session.commit()

    # Update lesson with both students
    update_data = {
        'student_ids': [students[0].id, students[1].id],
    }
    r = auth_client.put(auth_client.app.url_path_for('update_lesson', lesson_id=lesson.id), json=update_data)
    assert r.status_code == 200, r.json()
    data = r.json()
    assert data['id'] == lesson.id
    assert len(data['students']) == 2
    student_ids = [s['id'] for s in data['students']]
    assert students[0].id in student_ids
    assert students[1].id in student_ids


def test_update_nonexistent_lesson(auth_client: AuthenticatedTestClient):
    """Test updating a non-existent lesson"""
    update_data = {
        'subject': 'Mathematics',
        'topic': 'Algebra',
        'notes': 'Math lesson',
    }
    r = auth_client.put(auth_client.app.url_path_for('update_lesson', lesson_id=999), json=update_data)
    assert r.status_code == 404, r.json()


def test_delete_lesson(auth_client: AuthenticatedTestClient, session: Session):
    """Test deleting a lesson"""
    # First create a client and student
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

    # Create a test lesson
    lesson = Lesson(
        start_dt=datetime(2024, 1, 15, 14, 0, tzinfo=timezone.utc),
        end_dt=datetime(2024, 1, 15, 15, 0, tzinfo=timezone.utc),
        subject='Mathematics',
        topic='Algebra',
        notes='Math lesson',
    )
    session.add(lesson)
    session.commit()
    session.refresh(lesson)

    # Associate student with lesson
    lesson_student = LessonStudent(lesson_id=lesson.id, student_id=student.id)
    session.add(lesson_student)
    session.commit()

    # Associate tutor with lesson
    lesson_tutor = LessonTutor(lesson_id=lesson.id, tutor_id=auth_client.user.id)
    session.add(lesson_tutor)
    session.commit()

    # Delete lesson
    r = auth_client.delete(auth_client.app.url_path_for('delete_lesson', lesson_id=lesson.id))
    assert r.status_code == 200, r.json()
    assert r.json()['message'] == 'Lesson deleted successfully'

    # Verify lesson is gone
    r = auth_client.get(auth_client.app.url_path_for('get_lesson', lesson_id=lesson.id))
    assert r.status_code == 404, r.json()


def test_delete_nonexistent_lesson(auth_client: AuthenticatedTestClient):
    """Test deleting a non-existent lesson"""
    r = auth_client.delete(auth_client.app.url_path_for('delete_lesson', lesson_id=999))
    assert r.status_code == 404, r.json()


def test_unauthorized_access(client: TestClient):
    """Test accessing endpoints without authentication"""
    # Test create lesson
    r = client.post(client.app.url_path_for('create_lesson'), json={})
    assert r.status_code == 401

    # Test get lessons
    r = client.get(client.app.url_path_for('get_lessons'))
    assert r.status_code == 401

    # Test get lesson by id
    r = client.get(client.app.url_path_for('get_lesson', lesson_id=1))
    assert r.status_code == 401

    # Test update lesson
    r = client.put(client.app.url_path_for('update_lesson', lesson_id=1), json={})
    assert r.status_code == 401

    # Test delete lesson
    r = client.delete(client.app.url_path_for('delete_lesson', lesson_id=1))
    assert r.status_code == 401


def test_get_lessons_tutor_with_no_lessons(auth_client: AuthenticatedTestClient, session: Session):
    """Test that a tutor with no lessons sees no lessons"""
    # Ensure the user is a tutor
    if not auth_client.user.is_tutor:
        auth_client.user.is_tutor = True
        auth_client.user.is_admin = False
        session.add(auth_client.user)
        session.commit()

    # Create a lesson that the tutor is not associated with
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

    lesson = Lesson(
        start_dt=datetime(2024, 1, 15, 14, 0, tzinfo=timezone.utc),
        end_dt=datetime(2024, 1, 15, 15, 0, tzinfo=timezone.utc),
        subject='Mathematics',
        topic='Algebra',
        notes='Math lesson',
    )
    session.add(lesson)
    session.commit()
    session.refresh(lesson)

    # Add student to lesson
    lesson_student = LessonStudent(lesson_id=lesson.id, student_id=student.id)
    session.add(lesson_student)
    session.commit()

    # Get lessons - should return empty list since tutor has no lessons
    r = auth_client.get(auth_client.app.url_path_for('get_lessons'))
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 0
