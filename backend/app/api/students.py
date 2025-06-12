from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..core.database import get_session
from ..models import Client, Company, Student, StudentCreate, StudentRead, StudentUpdate

router = APIRouter(prefix='/students', tags=['students'])


def build_student_read(student: Student, company: Company = None) -> StudentRead:
    """Helper function to build StudentRead with computed fields"""
    company_name = company.name if company else None
    tutorcruncher_url = None

    if company and student.tc_path and company.tutorcruncher_domain:
        tutorcruncher_url = f'{company.tutorcruncher_domain.rstrip("/")}/{student.tc_path.lstrip("/")}'

    return StudentRead(
        **student.model_dump(),
        lessons_completed=student.lessons_completed,
        company_name=company_name,
        tutorcruncher_url=tutorcruncher_url,
    )


@router.get('/', response_model=list[StudentRead])
def get_students(session: Session = Depends(get_session)):
    """Get all students"""
    query = select(Student, Company).outerjoin(Company, Student.company_id == Company.id)
    results = session.exec(query).all()

    return [build_student_read(student, company) for student, company in results]


@router.get('/{student_id}', response_model=StudentRead, name='get_student')
def get_student(student_id: int, session: Session = Depends(get_session)):
    """Get a specific student by ID"""
    query = (
        select(Student, Company).outerjoin(Company, Student.company_id == Company.id).where(Student.id == student_id)
    )
    result = session.exec(query).first()

    if not result:
        raise HTTPException(status_code=404, detail='Student not found')

    student, company = result
    return build_student_read(student, company)


@router.post('/', response_model=StudentRead, name='create_student')
def create_student(student_data: StudentCreate, session: Session = Depends(get_session)):
    """Create a new student"""
    # Check if client exists
    client = session.get(Client, student_data.client_id)
    if not client:
        raise HTTPException(status_code=404, detail='Client not found')

    student = Student(**student_data.model_dump())
    session.add(student)
    session.commit()
    session.refresh(student)

    # Get company if exists
    company = None
    if student.company_id:
        company = session.get(Company, student.company_id)

    return build_student_read(student, company)


@router.put('/{student_id}', response_model=StudentRead, name='update_student')
def update_student(student_id: int, student_data: StudentUpdate, session: Session = Depends(get_session)):
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

    student_data_dict = student_data.model_dump(exclude_unset=True)
    for key, value in student_data_dict.items():
        setattr(student, key, value)

    session.add(student)
    session.commit()
    session.refresh(student)

    # Get company if exists
    company = None
    if student.company_id:
        company = session.get(Company, student.company_id)

    return build_student_read(student, company)


@router.delete('/{student_id}', name='delete_student')
def delete_student(student_id: int, session: Session = Depends(get_session)):
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
