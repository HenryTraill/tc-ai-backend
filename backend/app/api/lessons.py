from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from ..core.database import get_session
from ..models import Lesson, LessonCreate, LessonRead, LessonUpdate, Student

router = APIRouter(prefix='/lessons', tags=['lessons'])


@router.get('/', response_model=list[LessonRead])
def get_lessons(
    student_id: Optional[int] = Query(None, description='Filter by student ID'), session: Session = Depends(get_session)
):
    """Get all lessons, optionally filtered by student"""
    query = select(Lesson)
    if student_id:
        query = query.where(Lesson.student_id == student_id)

    lessons = session.exec(query).all()
    return lessons


@router.get('/{lesson_id}', response_model=LessonRead)
def get_lesson(lesson_id: int, session: Session = Depends(get_session)):
    """Get a specific lesson by ID"""
    lesson = session.get(Lesson, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail='Lesson not found')
    return lesson


@router.post('/', response_model=LessonRead)
def create_lesson(lesson_data: LessonCreate, session: Session = Depends(get_session)):
    """Create a new lesson"""
    # Verify student exists
    student = session.get(Student, lesson_data.student_id)
    if not student:
        raise HTTPException(status_code=404, detail='Student not found')

    lesson = Lesson(**lesson_data.model_dump())
    session.add(lesson)
    session.commit()
    session.refresh(lesson)
    return lesson


@router.put('/{lesson_id}', response_model=LessonRead)
def update_lesson(lesson_id: int, lesson_data: LessonUpdate, session: Session = Depends(get_session)):
    """Update a lesson"""
    lesson = session.get(Lesson, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail='Lesson not found')

    # If updating student_id, verify the student exists
    if lesson_data.student_id is not None:
        student = session.get(Student, lesson_data.student_id)
        if not student:
            raise HTTPException(status_code=404, detail='Student not found')

    lesson_data_dict = lesson_data.model_dump(exclude_unset=True)
    for key, value in lesson_data_dict.items():
        setattr(lesson, key, value)

    lesson.updated_at = datetime.utcnow()
    session.add(lesson)
    session.commit()
    session.refresh(lesson)
    return lesson


@router.delete('/{lesson_id}')
def delete_lesson(lesson_id: int, session: Session = Depends(get_session)):
    """Delete a lesson"""
    lesson = session.get(Lesson, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail='Lesson not found')

    session.delete(lesson)
    session.commit()
    return {'message': 'Lesson deleted successfully'}


@router.get('/student/{student_id}', response_model=list[LessonRead])
def get_student_lessons(student_id: int, session: Session = Depends(get_session)):
    """Get all lessons for a specific student"""
    # Verify student exists
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail='Student not found')

    lessons = session.exec(select(Lesson).where(Lesson.student_id == student_id)).all()
    return lessons
