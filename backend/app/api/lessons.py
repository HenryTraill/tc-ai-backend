from datetime import datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Query
from sqlmodel import Session, select

from ..core.database import get_session
from ..models import Company, Lesson, LessonCreate, LessonRead, LessonUpdate, Student

router = APIRouter(prefix='/lessons', tags=['lessons'])


def build_lesson_read(lesson: Lesson, company: Company = None) -> LessonRead:
    """Helper function to build LessonRead with computed fields"""
    company_name = company.name if company else None
    tutorcruncher_url = None

    if company and lesson.tc_path and company.tutorcruncher_domain:
        tutorcruncher_url = f'{company.tutorcruncher_domain.rstrip("/")}/{lesson.tc_path.lstrip("/")}'

    return LessonRead(**lesson.model_dump(), company_name=company_name, tutorcruncher_url=tutorcruncher_url)


@router.get('/', response_model=List[LessonRead], name='get_lessons')
def get_lessons(
    student_id: Optional[int] = Query(None, description='Filter by student ID'), session: Session = Depends(get_session)
):
    """Get all lessons, optionally filtered by student"""
    query = select(Lesson, Company).outerjoin(Company, Lesson.company_id == Company.id)
    if student_id:
        query = query.where(Lesson.student_id == student_id)

    results = session.exec(query).all()
    return [build_lesson_read(lesson, company) for lesson, company in results]


@router.get('/{lesson_id}', response_model=LessonRead, name='get_lesson')
def get_lesson(lesson_id: int, session: Session = Depends(get_session)):
    """Get a specific lesson by ID"""
    query = select(Lesson, Company).outerjoin(Company, Lesson.company_id == Company.id).where(Lesson.id == lesson_id)
    result = session.exec(query).first()

    if not result:
        raise HTTPException(status_code=404, detail='Lesson not found')

    lesson, company = result
    return build_lesson_read(lesson, company)


@router.post('/', response_model=LessonRead, name='create_lesson')
def create_lesson(lesson_data: LessonCreate, session: Session = Depends(get_session)):
    """Create a new lesson"""
    # Check if student exists
    student = session.get(Student, lesson_data.student_id)
    if not student:
        raise HTTPException(status_code=404, detail='Student not found')

    lesson = Lesson(**lesson_data.model_dump())
    session.add(lesson)
    session.commit()
    session.refresh(lesson)

    # Get company if exists
    company = None
    if lesson.company_id:
        company = session.get(Company, lesson.company_id)

    return build_lesson_read(lesson, company)


@router.put('/{lesson_id}', response_model=LessonRead, name='update_lesson')
def update_lesson(lesson_id: int, lesson_data: LessonUpdate, session: Session = Depends(get_session)):
    """Update a lesson (only basic fields can be updated)"""
    lesson = session.get(Lesson, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail='Lesson not found')

    # Check if lesson is linked to a company and prevent updates
    if lesson.company_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Cannot update lesson that is linked to a company. Lessons linked to companies are read-only.',
        )

    # If updating student_id, verify the student exists
    if lesson_data.student_id is not None:
        student = session.get(Student, lesson_data.student_id)
        if not student:
            raise HTTPException(status_code=404, detail='Student not found')

    lesson_data_dict = lesson_data.model_dump(exclude_unset=True)
    for key, value in lesson_data_dict.items():
        setattr(lesson, key, value)

    lesson.updated_at = datetime.now(timezone.utc)
    session.add(lesson)
    session.commit()
    session.refresh(lesson)

    # Get company if exists
    company = None
    if lesson.company_id:
        company = session.get(Company, lesson.company_id)

    return build_lesson_read(lesson, company)


@router.delete('/{lesson_id}', name='delete_lesson')
def delete_lesson(lesson_id: int, session: Session = Depends(get_session)):
    """Delete a lesson"""
    lesson = session.get(Lesson, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail='Lesson not found')

    # Check if lesson is linked to a company and prevent deletion
    if lesson.company_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Cannot delete lesson that is linked to a company. Lessons linked to companies are read-only.',
        )

    session.delete(lesson)
    session.commit()
    return {'message': 'Lesson deleted successfully'}


@router.get('/student/{student_id}', response_model=List[LessonRead], name='get_lessons_for_student')
def get_lessons_for_student(student_id: int, session: Session = Depends(get_session)):
    """Get all lessons for a specific student"""
    # Check if student exists
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail='Student not found')

    query = (
        select(Lesson, Company)
        .outerjoin(Company, Lesson.company_id == Company.id)
        .where(Lesson.student_id == student_id)
    )
    results = session.exec(query).all()
    return [build_lesson_read(lesson, company) for lesson, company in results]
