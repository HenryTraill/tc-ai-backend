from datetime import UTC, datetime
from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel, EmailStr
from sqlalchemy import JSON, Column
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from backend.app.models.client import Client
    from backend.app.models.company import Company
    from backend.app.models.lesson import Lesson
    from backend.app.models.lesson_student import LessonStudent
    from backend.app.models.tutor_student import TutorStudent


class StudentBase(SQLModel):
    client_id: int = Field(foreign_key='client.id')
    first_name: str
    last_name: str
    email: EmailStr = Field(unique=True)
    phone: str
    grade: str
    company_id: Optional[int] = Field(default=None, foreign_key='company.id')
    tc_path: Optional[str] = None
    strengths: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    weaknesses: List[str] = Field(default_factory=list, sa_column=Column(JSON))


class Student(StudentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: Optional[datetime] = None

    # Relationships
    lesson_students: List['LessonStudent'] = Relationship(back_populates='student')
    client: Optional['Client'] = Relationship(back_populates='students')
    student_tutors: List['TutorStudent'] = Relationship(back_populates='student')
    company: Optional['Company'] = Relationship(back_populates='students')

    @property
    def lessons(self) -> List['Lesson']:
        """Get all lessons for this student"""
        return [ls.lesson for ls in self.lesson_students if ls.lesson]

    @property
    def lessons_completed(self) -> int:
        return len(self.lessons)


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    client_id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    grade: Optional[str] = None
    company_id: Optional[int] = None
    # Note: strengths and weaknesses are intentionally excluded from updates


class StudentRead(StudentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    lessons_completed: int = 0
    company_name: Optional[str] = None
    tutorcruncher_url: Optional[str] = None
