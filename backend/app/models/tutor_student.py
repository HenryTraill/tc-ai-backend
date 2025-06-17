from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from backend.app.models.student import Student
    from backend.app.models.user import User


class TutorStudentBase(SQLModel):
    tutor_id: int = Field(foreign_key='user.id')
    student_id: int = Field(foreign_key='student.id')


class TutorStudent(TutorStudentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    tutor: Optional['User'] = Relationship(back_populates='tutor_students')
    student: Optional['Student'] = Relationship(back_populates='student_tutors')


class TutorStudentCreate(TutorStudentBase):
    pass


class TutorStudentRead(TutorStudentBase):
    id: int
    created_at: datetime
