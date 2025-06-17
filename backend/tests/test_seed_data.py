from datetime import datetime

from sqlmodel import Session, select

from app.models import Client, Lesson, LessonStudent, Student
from scripts.seed_data import clients_data, generate_lessons_for_student, students_data


def test_seed_clients(session: Session):
    """Test creating clients from seed data"""
    # Create clients from seed data
    clients = []
    for client_data in clients_data:
        client = Client(**client_data)
        session.add(client)
        clients.append(client)

    session.commit()

    # Verify clients were created
    db_clients = session.exec(select(Client)).all()
    assert len(db_clients) == len(clients_data)

    # Check first client details
    first_client = db_clients[0]
    assert first_client.first_name == clients_data[0]['first_name']
    assert first_client.last_name == clients_data[0]['last_name']
    assert first_client.email == clients_data[0]['email']


def test_seed_students(session: Session):
    """Test creating students from seed data"""
    # First create clients
    clients = []
    for client_data in clients_data:
        client = Client(**client_data)
        session.add(client)
        clients.append(client)

    session.commit()

    # Refresh to get IDs
    for client in clients:
        session.refresh(client)

    # Create students linked to clients
    students = []
    for i, student_data in enumerate(students_data):
        student_data_with_client = student_data.copy()
        student_data_with_client['client_id'] = clients[i].id

        student = Student(**student_data_with_client)
        session.add(student)
        students.append(student)

    session.commit()

    # Verify students were created
    db_students = session.exec(select(Student)).all()
    assert len(db_students) == len(students_data)

    # Check first student details
    first_student = db_students[0]
    assert first_student.first_name == students_data[0]['first_name']
    assert first_student.last_name == students_data[0]['last_name']
    assert first_student.grade == students_data[0]['grade']
    assert first_student.client_id == clients[0].id


def test_generate_lessons_for_student():
    """Test lesson generation functionality"""
    student_id = 1
    student_name = 'Test Student'
    grade = '8th Grade'
    num_lessons = 5

    lessons = generate_lessons_for_student(student_id, student_name, grade, num_lessons)

    assert len(lessons) == num_lessons

    # Check lesson structure
    for lesson in lessons:
        assert lesson['_student_id'] == student_id  # Now stored as _student_id
        assert 'start_dt' in lesson
        assert 'end_dt' in lesson
        assert 'subject' in lesson
        assert 'topic' in lesson
        assert 'notes' in lesson
        assert 'skills_practiced' in lesson
        assert 'main_subjects_covered' in lesson
        assert 'student_strengths_observed' in lesson
        assert 'student_weaknesses_observed' in lesson
        assert 'tutor_tips' in lesson

        # Check data types
        assert isinstance(lesson['start_dt'], datetime)
        assert isinstance(lesson['end_dt'], datetime)
        assert isinstance(lesson['skills_practiced'], list)
        assert isinstance(lesson['main_subjects_covered'], list)
        assert isinstance(lesson['student_strengths_observed'], list)
        assert isinstance(lesson['student_weaknesses_observed'], list)
        assert isinstance(lesson['tutor_tips'], list)

        # Check that end_dt is after start_dt
        assert lesson['end_dt'] > lesson['start_dt']


def test_seed_lessons(session: Session):
    """Test creating lessons from generated data"""
    # Create clients and students first
    clients = []
    for client_data in clients_data:
        client = Client(**client_data)
        session.add(client)
        clients.append(client)

    session.commit()

    for client in clients:
        session.refresh(client)

    students = []
    for i, student_data in enumerate(students_data):
        student_data_with_client = student_data.copy()
        student_data_with_client['client_id'] = clients[i].id

        student = Student(**student_data_with_client)
        session.add(student)
        students.append(student)

    session.commit()

    for student in students:
        session.refresh(student)

    # Generate and create lessons
    all_lessons = []
    for student in students:
        student_name = f'{student.first_name} {student.last_name}'
        student_lessons = generate_lessons_for_student(
            student_id=student.id,
            student_name=student_name,
            grade=student.grade,
            num_lessons=3,  # Smaller number for testing
        )
        all_lessons.extend(student_lessons)

    # Create lesson objects and junction table entries
    lesson_student_pairs = []
    for lesson_data in all_lessons:
        # Extract student_id before creating lesson
        student_id = lesson_data.pop('_student_id')
        lesson = Lesson(**lesson_data)
        session.add(lesson)
        lesson_student_pairs.append((lesson, student_id))

    session.commit()

    # Refresh all lessons to get their IDs
    for lesson, _ in lesson_student_pairs:
        session.refresh(lesson)

    # Now create junction table entries
    for lesson, student_id in lesson_student_pairs:
        lesson_student = LessonStudent(lesson_id=lesson.id, student_id=student_id)
        session.add(lesson_student)

    session.commit()

    # Verify lessons were created
    db_lessons = session.exec(select(Lesson)).all()
    assert len(db_lessons) == len(all_lessons)

    # Check that lessons are properly linked to students through junction table
    for lesson in db_lessons:
        lesson_students = session.exec(select(LessonStudent).where(LessonStudent.lesson_id == lesson.id)).all()
        assert len(lesson_students) > 0  # Each lesson should have at least one student association
        for ls in lesson_students:
            assert ls.student_id in [s.id for s in students]


def test_full_seed_data_integration(session: Session):
    """Test the complete seed data process"""
    # Step 1: Create clients
    clients = []
    for client_data in clients_data:
        client = Client(**client_data)
        session.add(client)
        clients.append(client)

    session.commit()

    for client in clients:
        session.refresh(client)

    # Step 2: Create students
    students = []
    for i, student_data in enumerate(students_data):
        student_data_with_client = student_data.copy()
        student_data_with_client['client_id'] = clients[i].id

        student = Student(**student_data_with_client)
        session.add(student)
        students.append(student)

    session.commit()

    for student in students:
        session.refresh(student)

    # Step 3: Generate and create lessons
    all_lessons = []
    for student in students:
        student_name = f'{student.first_name} {student.last_name}'
        student_lessons = generate_lessons_for_student(
            student_id=student.id, student_name=student_name, grade=student.grade, num_lessons=4
        )
        all_lessons.extend(student_lessons)

    # Create lesson objects and junction table entries
    lesson_student_pairs = []
    for lesson_data in all_lessons:
        # Extract student_id before creating lesson
        student_id = lesson_data.pop('_student_id')
        lesson = Lesson(**lesson_data)
        session.add(lesson)
        lesson_student_pairs.append((lesson, student_id))

    session.commit()

    # Refresh all lessons to get their IDs
    for lesson, _ in lesson_student_pairs:
        session.refresh(lesson)

    # Now create junction table entries
    for lesson, student_id in lesson_student_pairs:
        lesson_student = LessonStudent(lesson_id=lesson.id, student_id=student_id)
        session.add(lesson_student)

    session.commit()

    # Verify the complete database state
    db_clients = session.exec(select(Client)).all()
    db_students = session.exec(select(Student)).all()
    db_lessons = session.exec(select(Lesson)).all()

    assert len(db_clients) == len(clients_data)
    assert len(db_students) == len(students_data)
    assert len(db_lessons) == len(students_data) * 4  # 4 lessons per student

    # Verify relationships
    for student in db_students:
        assert student.client_id in [c.id for c in db_clients]
        lesson_students = session.exec(select(LessonStudent).where(LessonStudent.student_id == student.id)).all()
        assert len(lesson_students) > 0  # Each student should have lesson associations


def test_seed_data_script_integration(session: Session):
    """Test that the seed script functions work correctly with fresh database"""
    from unittest.mock import patch

    from scripts.seed_data import seed_database

    # Mock the engine and Session to use our test session
    with (
        patch('scripts.seed_data.Session') as mock_session_class,
        patch('scripts.seed_data.create_db_and_tables') as mock_create,
    ):
        # Set up the mock to return our test session
        mock_session_class.return_value.__enter__.return_value = session
        mock_session_class.return_value.__exit__.return_value = None

        # Make sure database appears empty for seeding
        # (our test database starts fresh each time)

        # Call the actual seed function
        seed_database()

        # Verify that create_db_and_tables was called
        mock_create.assert_called_once()

        # Verify data was created in our test session
        db_clients = session.exec(select(Client)).all()
        db_students = session.exec(select(Student)).all()
        db_lessons = session.exec(select(Lesson)).all()

        assert len(db_clients) == len(clients_data)
        assert len(db_students) == len(students_data)
        assert len(db_lessons) > 0  # Should have generated lessons

        # Verify relationships are correct
        for student in db_students:
            assert student.client_id in [c.id for c in db_clients]
            lesson_students = session.exec(select(LessonStudent).where(LessonStudent.student_id == student.id)).all()
            assert len(lesson_students) > 0  # Each student should have lesson associations
