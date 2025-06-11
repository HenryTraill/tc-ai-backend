from datetime import datetime
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from backend.app.models.student import Student


class LessonBase(SQLModel):
    student_id: int = Field(foreign_key='student.id')
    date: str
    start_time: str
    subject: str
    topic: str
    duration: int  # in minutes
    notes: str
    skills_practiced: list[str] = Field(default_factory=list, sa_column_kwargs={'type_': 'JSON'})
    main_subjects_covered: list[str] = Field(default_factory=list, sa_column_kwargs={'type_': 'JSON'})
    student_strengths_observed: list[str] = Field(default_factory=list, sa_column_kwargs={'type_': 'JSON'})
    student_weaknesses_observed: list[str] = Field(default_factory=list, sa_column_kwargs={'type_': 'JSON'})
    tutor_tips: list[str] = Field(default_factory=list, sa_column_kwargs={'type_': 'JSON'})


class Lesson(LessonBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    student: Optional['Student'] = Relationship(back_populates='lessons')


class LessonCreate(LessonBase):
    pass


class LessonUpdate(BaseModel):
    student_id: Optional[int] = None
    date: Optional[str] = None
    start_time: Optional[str] = None
    subject: Optional[str] = None
    topic: Optional[str] = None
    duration: Optional[int] = None
    notes: Optional[str] = None
    skills_practiced: Optional[list[str]] = None
    main_subjects_covered: Optional[list[str]] = None
    student_strengths_observed: Optional[list[str]] = None
    student_weaknesses_observed: Optional[list[str]] = None
    tutor_tips: Optional[list[str]] = None


class LessonRead(LessonBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
