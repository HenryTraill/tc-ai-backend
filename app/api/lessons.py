from datetime import datetime, timezone
from typing import List, Optional

import httpx
from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Query
from sqlmodel import Session, select

from ..core.auth import get_current_active_user
from ..core.config import settings
from ..core.database import get_session
from ..models import Company, Lesson, LessonCreate, LessonRead, LessonStudent, LessonTutor, LessonUpdate, Student, User

router = APIRouter(prefix='/lessons', tags=['lessons'])


def _get_lessons_for_user(session: Session, current_user: User, base_query=None):
    """
    Get all lessons viewable by the current user. If the user is a tutor, return all lessons that have a linked
    LessonTutor with that Tutor. If the user is an admin, return all lessons that have a linked Company_id and
    where the company_id is in the user's company_ids.

    Args:
        session: The database session
        current_user: The current user
        base_query: Optional base query to apply the filtering to. If not provided, starts with select(Lesson)

    Returns:
        A query with the appropriate filtering applied
    """
    if base_query is None:
        base_query = select(Lesson)

    if current_user.is_tutor:
        # For tutors, return only lessons linked to them
        return base_query.join(LessonTutor).where(LessonTutor.tutor_id == current_user.id)
    else:
        assert current_user.is_admin
        # For admins, if they have no company_ids, return all lessons
        # Otherwise, return only lessons linked to their companies
        if not current_user.company_ids:
            return base_query
        return base_query.where(Lesson.company_id.in_(current_user.company_ids))


def build_lesson_read(lesson: Lesson) -> LessonRead:
    """Helper function to build LessonRead with computed fields"""
    tutorcruncher_url = None
    if lesson.company and lesson.tc_path and lesson.company.tutorcruncher_domain:
        tutorcruncher_url = f'{lesson.company.tutorcruncher_domain.rstrip("/")}/{lesson.tc_path.lstrip("/")}'

    # Build the lesson read with students
    lesson_data = lesson.model_dump(exclude={'company'})
    lesson_data['students'] = lesson.students  # Use the property to get students
    return LessonRead(**lesson_data, tutorcruncher_url=tutorcruncher_url)


@router.get('/', response_model=List[LessonRead], name='get_lessons')
def get_lessons(
    student_id: Optional[int] = Query(None, description='Filter by student ID'),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
):
    """Get all lessons, optionally filtered by student"""
    if student_id:
        # Filter by student using junction table
        base_query = (
            select(Lesson)
            .join(LessonStudent, Lesson.id == LessonStudent.lesson_id)
            .where(LessonStudent.student_id == student_id)
        )
    else:
        base_query = select(Lesson)

    # Apply user-based filtering
    query = _get_lessons_for_user(session, current_user, base_query)
    results = session.exec(query).all()
    return [build_lesson_read(lesson) for lesson in results]


@router.get('/{lesson_id}', response_model=LessonRead, name='get_lesson')
def get_lesson(
    lesson_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_active_user)
):
    """Get a specific lesson by ID"""
    base_query = select(Lesson).where(Lesson.id == lesson_id)
    query = _get_lessons_for_user(session, current_user, base_query)
    lesson = session.exec(query).first()

    if not lesson:
        raise HTTPException(status_code=404, detail='Lesson not found')

    return build_lesson_read(lesson)


@router.post('/', response_model=LessonRead, name='create_lesson')
def create_lesson(
    lesson_data: LessonCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
):
    """Create a new lesson"""
    # Validate student existence
    for student_id in lesson_data.student_ids:
        student = session.get(Student, student_id)
        if not student:
            raise HTTPException(status_code=404, detail='Student not found')

    # Validate company if provided
    if lesson_data.company_id:
        company = session.get(Company, lesson_data.company_id)
        if not company:
            raise HTTPException(status_code=404, detail='Company not found')
        # For admins, verify they have access to this company
        if not current_user.is_tutor and company.id not in current_user.company_ids:
            raise HTTPException(status_code=403, detail='Not authorized to create lessons for this company')

    # Validate dates
    if lesson_data.end_dt <= lesson_data.start_dt:
        raise HTTPException(status_code=400, detail='End date must be after start date.')

    # Create lesson without student_ids (they are not part of the base model)
    lesson_dict = lesson_data.model_dump(exclude={'student_ids'})
    lesson = Lesson(**lesson_dict)
    session.add(lesson)
    session.commit()
    session.refresh(lesson)

    # Create junction table entries for each student
    for student_id in lesson_data.student_ids:
        student = session.get(Student, student_id)
        if student:
            lesson_student = LessonStudent(lesson_id=lesson.id, student_id=student.id)
            session.add(lesson_student)

    # Create tutor association
    lesson_tutor = LessonTutor(lesson_id=lesson.id, tutor_id=current_user.id)
    session.add(lesson_tutor)

    session.commit()
    session.refresh(lesson)  # Refresh to load relationships

    return build_lesson_read(lesson)


@router.put('/{lesson_id}', response_model=LessonRead, name='update_lesson')
def update_lesson(
    lesson_id: int,
    lesson_data: LessonUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
):
    """Update a lesson (only basic fields can be updated)"""
    # First check if user has access to this lesson
    base_query = select(Lesson).where(Lesson.id == lesson_id)
    query = _get_lessons_for_user(session, current_user, base_query)
    lesson = session.exec(query).first()

    if not lesson:
        raise HTTPException(status_code=404, detail='Lesson not found')

    # Check if lesson is linked to a company and prevent updates
    if lesson.company_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Cannot update lesson that is linked to a company. Lessons linked to companies are read-only.',
        )

    # Validate company if being updated
    if lesson_data.company_id:
        company = session.get(Company, lesson_data.company_id)
        if not company:
            raise HTTPException(status_code=404, detail='Company not found')
        # For admins, verify they have access to this company
        if not current_user.is_tutor and company.id not in current_user.company_ids:
            raise HTTPException(status_code=403, detail='Not authorized to update lessons for this company')

    # Handle student association updates
    if lesson_data.student_ids is not None:
        # Verify all students exist
        students = []
        for student_id in lesson_data.student_ids:
            student = session.get(Student, student_id)
            if not student:
                raise HTTPException(status_code=404, detail=f'Student with ID {student_id} not found')
            students.append(student)

        # Remove existing student associations
        existing_associations = session.exec(select(LessonStudent).where(LessonStudent.lesson_id == lesson_id)).all()
        for association in existing_associations:
            session.delete(association)

        # Add new student associations
        for student in students:
            lesson_student = LessonStudent(lesson_id=lesson.id, student_id=student.id)
            session.add(lesson_student)

    # Update basic lesson fields (exclude student_ids as it's handled above)
    lesson_data_dict = lesson_data.model_dump(exclude_unset=True, exclude={'student_ids'})
    for key, value in lesson_data_dict.items():
        setattr(lesson, key, value)

    lesson.updated_at = datetime.now(timezone.utc)
    session.add(lesson)
    session.commit()
    session.refresh(lesson)

    return build_lesson_read(lesson)


@router.delete('/{lesson_id}', name='delete_lesson')
def delete_lesson(
    lesson_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_active_user)
):
    """Delete a lesson"""
    # First check if user has access to this lesson
    base_query = select(Lesson).where(Lesson.id == lesson_id)
    query = _get_lessons_for_user(session, current_user, base_query)
    lesson = session.exec(query).first()

    if not lesson:
        raise HTTPException(status_code=404, detail='Lesson not found')

    # Check if lesson is linked to a company and prevent deletion
    if lesson.company_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Cannot delete lesson that is linked to a company. Lessons linked to companies are read-only.',
        )

    # Delete associated LessonStudent entries first (cascade delete)
    lesson_students = session.exec(select(LessonStudent).where(LessonStudent.lesson_id == lesson_id)).all()
    for lesson_student in lesson_students:
        session.delete(lesson_student)

    # Delete associated LessonTutor entries
    lesson_tutors = session.exec(select(LessonTutor).where(LessonTutor.lesson_id == lesson_id)).all()
    for lesson_tutor in lesson_tutors:
        session.delete(lesson_tutor)

    session.delete(lesson)
    session.commit()
    return {'message': 'Lesson deleted successfully'}


@router.get('/student/{student_id}', response_model=List[LessonRead], name='get_lessons_for_student')
def get_lessons_for_student(
    student_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_active_user)
):
    """Get all lessons for a specific student"""
    # Check if student exists
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail='Student not found')

    # Query lessons through junction table
    base_query = (
        select(Lesson)
        .join(LessonStudent, Lesson.id == LessonStudent.lesson_id)
        .where(LessonStudent.student_id == student_id)
    )
    # Apply user-based filtering
    query = _get_lessons_for_user(session, current_user, base_query)
    lessons = session.exec(query).all()
    return [build_lesson_read(lesson) for lesson in lessons]


@router.post('/{lesson_id}/eurus-space', name='create_eurus_space')
async def create_eurus_space(
    lesson_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
):
    """Create a Eurus space for a lesson and return the access URL"""
    # Get the lesson
    base_query = select(Lesson).where(Lesson.id == lesson_id)
    query = _get_lessons_for_user(session, current_user, base_query)
    lesson = session.exec(query).first()

    if not lesson:
        raise HTTPException(status_code=404, detail='Lesson not found')

    # Get all students for this lesson
    lesson_students = session.exec(
        select(Student)
        .join(LessonStudent, Student.id == LessonStudent.student_id)
        .where(LessonStudent.lesson_id == lesson_id)
    ).all()

    if not lesson_students:
        raise HTTPException(status_code=404, detail='No students found for this lesson')

    # Prepare the data for Eurus
    space_data = {
        'lesson_id': str(lesson_id),  # Convert to string as API accepts both string and integer
        'tutors': [
            {
                'user_id': str(current_user.id),
                'name': f'{current_user.first_name} {current_user.last_name}',
                'email': current_user.email if hasattr(current_user, 'email') else None,
                'is_leader': True,
            }
        ],
        'students': [
            {
                'user_id': str(student.id),
                'name': f'{student.first_name} {student.last_name}',
                'email': student.email if hasattr(student, 'email') else None,
            }
            for student in lesson_students
        ],
        'not_before': lesson.start_dt.isoformat() if lesson.start_dt else None,
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f'{settings.eurus_api_url}/api/space/', json=space_data, headers={'X-API-Key': settings.eurus_api_key}
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f'Failed to create Eurus space: {str(e)}')
