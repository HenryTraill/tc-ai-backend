from datetime import UTC, datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.models.tutor_student import TutorStudent

from ..core.auth import get_current_active_user
from ..core.database import get_session
from ..models import Client, Company, Student, StudentCreate, StudentRead, StudentUpdate, User

router = APIRouter(prefix='/students', tags=['students'])


def _get_students_for_user(session: Session, current_user: User):
    """
    Get all students viewable by the current user. If the user is a tutor, return all students that have a linked
    TutorStudent with that Tutor. If the user is an admin, return all students that have a linked company_id and
    where the company_id is in the user's company_ids. If the admin has no company_ids, return no students.
    """
    if current_user.is_tutor:
        # Only students linked to this tutor
        query = (
            select(Student)
            .join(TutorStudent, TutorStudent.student_id == Student.id)
            .where(TutorStudent.tutor_id == current_user.id)
            .order_by(Student.last_name, Student.first_name)
        )
        return session.exec(query).all()
    else:
        assert current_user.is_admin
        # For admins, if they have company_ids, filter by them; else, return no students
        if current_user.company_ids:
            query = select(Student).where(Student.company_id.in_(current_user.company_ids))
            return session.exec(query).all()
        else:
            return []


def build_student_read(student: Student) -> StudentRead:
    """Build a StudentRead model from a Student model."""
    company_name = student.company.name if student.company else None
    tutorcruncher_url = None
    if student.company and student.tc_path and student.company.tutorcruncher_domain:
        tutorcruncher_url = f'{student.company.tutorcruncher_domain.rstrip("/")}/{student.tc_path.lstrip("/")}'

    base_data = student.model_dump(
        exclude={'created_at', 'updated_at', 'lesson_students', 'client', 'student_tutors', 'company'}
    )
    return StudentRead(
        **base_data,
        created_at=student.created_at,
        updated_at=student.updated_at,
        lessons_completed=student.lessons_completed,
        company_name=company_name,
        tutorcruncher_url=tutorcruncher_url,
    )


@router.get('/', response_model=List[StudentRead], name='get_students')
def get_students(
    client_id: Optional[int] = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
):
    """Get all students"""
    students = _get_students_for_user(session, current_user)
    if client_id is not None:
        students = [student for student in students if student.client_id == client_id]
    return [build_student_read(student) for student in students]


@router.get('/{student_id}', response_model=StudentRead, name='get_student')
def get_student(
    student_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_active_user)
):
    """Get a specific student by ID"""
    students = _get_students_for_user(session, current_user)
    student = next((student for student in students if student.id == student_id), None)
    if not student:
        raise HTTPException(status_code=404, detail='Student not found')

    return build_student_read(student)


@router.post('/', response_model=StudentRead, name='create_student')
def create_student(
    student_data: StudentCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
):
    """Create a new student"""
    # Check if client exists
    client = session.get(Client, student_data.client_id)
    if not client:
        raise HTTPException(status_code=404, detail='Client not found')

    # Check if company exists if company_id is provided
    if student_data.company_id:
        company = session.get(Company, student_data.company_id)
        if not company:
            raise HTTPException(status_code=404, detail='Company not found')

    # Check if email already exists
    existing_student = session.exec(select(Student).where(Student.email == student_data.email)).first()
    if existing_student:
        raise HTTPException(status_code=400, detail='Email already registered')

    student = Student(**student_data.model_dump())
    session.add(student)
    try:
        session.commit()
        session.refresh(student)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail='Email already registered')

    return build_student_read(student)


@router.put('/{student_id}', response_model=StudentRead, name='update_student')
def update_student(
    student_id: int,
    student_data: StudentUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
):
    """Update a student"""
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail='Student not found')

    # Check if student is linked to a company and prevent updates
    if student.company_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Cannot update student that is linked to a company. Students linked to companies are read-only.',
        )

    # Check if company exists if company_id is being updated
    if student_data.company_id:
        company = session.get(Company, student_data.company_id)
        if not company:
            raise HTTPException(status_code=404, detail='Company not found')

    # Check if email is being updated and if it already exists
    if student_data.email and student_data.email != student.email:
        existing_student = session.exec(select(Student).where(Student.email == student_data.email)).first()
        if existing_student:
            raise HTTPException(status_code=400, detail='Email already registered')

    student_data_dict = student_data.model_dump(exclude_unset=True)
    for key, value in student_data_dict.items():
        setattr(student, key, value)

    # Update the updated_at timestamp
    student.updated_at = datetime.now(UTC)

    session.add(student)
    try:
        session.commit()
        session.refresh(student)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail='Email already registered')

    return build_student_read(student)


@router.delete('/{student_id}', name='delete_student')
def delete_student(
    student_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_active_user)
):
    """Delete a student"""
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail='Student not found')

    # Check if student is linked to a company and prevent deletion
    if student.company_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Cannot delete student that is linked to a company. Students linked to companies are read-only.',
        )

    session.delete(student)
    session.commit()

    return {'message': 'Student deleted successfully'}
