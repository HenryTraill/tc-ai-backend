from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..core.database import get_session
from ..models import Student, StudentCreate, StudentRead, StudentUpdate

router = APIRouter(prefix='/students', tags=['students'])


@router.get('/', response_model=list[StudentRead])
def get_students(session: Session = Depends(get_session)):
    """Get all students"""
    students = session.exec(select(Student)).all()
    return [StudentRead(**student.model_dump(), lessons_completed=student.lessons_completed) for student in students]


@router.get('/{student_id}', response_model=StudentRead)
def get_student(student_id: int, session: Session = Depends(get_session)):
    """Get a specific student by ID"""
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail='Student not found')

    return StudentRead(**student.model_dump(), lessons_completed=student.lessons_completed)


@router.post('/', response_model=StudentRead)
def create_student(student_data: StudentCreate, session: Session = Depends(get_session)):
    """Create a new student"""
    student = Student(**student_data.model_dump())
    session.add(student)
    session.commit()
    session.refresh(student)

    return StudentRead(**student.model_dump(), lessons_completed=student.lessons_completed)


@router.put('/{student_id}', response_model=StudentRead)
def update_student(student_id: int, student_data: StudentUpdate, session: Session = Depends(get_session)):
    """Update a student"""
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail='Student not found')

    student_data_dict = student_data.model_dump(exclude_unset=True)
    for key, value in student_data_dict.items():
        setattr(student, key, value)

    session.add(student)
    session.commit()
    session.refresh(student)

    return StudentRead(**student.model_dump(), lessons_completed=student.lessons_completed)


@router.delete('/{student_id}')
def delete_student(student_id: int, session: Session = Depends(get_session)):
    """Delete a student"""
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail='Student not found')

    session.delete(student)
    session.commit()

    return {'message': 'Student deleted successfully'}
