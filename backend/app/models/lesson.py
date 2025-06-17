from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel
from sqlalchemy import JSON, Column
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from backend.app.models.company import Company
    from backend.app.models.lesson_student import LessonStudent
    from backend.app.models.lesson_tutor import LessonTutor
    from backend.app.models.student import Student


class LessonStatus(str, Enum):
    """Status of a lesson"""

    PLANNED = 'planned'
    COMPLETE = 'complete'
    PENDING = 'pending'
    CANCELLED = 'cancelled'
    CANCELLED_BUT_CHARGEABLE = 'cancelled-but-chargeable'


class LessonBase(SQLModel):
    company_id: Optional[int] = Field(default=None, foreign_key='company.id')
    tc_path: Optional[str] = None
    start_dt: datetime
    end_dt: datetime
    subject: str
    topic: str
    notes: str
    status: LessonStatus = Field(default=LessonStatus.PLANNED)
    skills_practiced: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    main_subjects_covered: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    student_strengths_observed: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    student_weaknesses_observed: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    tutor_tips: List[str] = Field(default_factory=list, sa_column=Column(JSON))


class Lesson(LessonBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None

    # Relationships
    lesson_students: List['LessonStudent'] = Relationship(back_populates='lesson')
    lesson_tutors: List['LessonTutor'] = Relationship(back_populates='lesson')
    company: Optional['Company'] = Relationship(back_populates='lessons')

    @property
    def students(self) -> List['Student']:
        """Get all students for this lesson"""
        return [ls.student for ls in self.lesson_students if ls.student]


class LessonCreate(LessonBase):
    student_ids: List[int] = Field(default_factory=list)  # List of student IDs to associate with the lesson


class LessonUpdate(BaseModel):
    company_id: Optional[int] = None
    tc_path: Optional[str] = None
    start_dt: Optional[datetime] = None
    end_dt: Optional[datetime] = None
    subject: Optional[str] = None
    topic: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[LessonStatus] = None
    student_ids: Optional[List[int]] = None  # Allow updating associated students
    # Note: skills_practiced, main_subjects_covered, student_strengths_observed,
    # student_weaknesses_observed, and tutor_tips are intentionally excluded from updates


class LessonRead(LessonBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    students: List['Student'] = Field(default_factory=list)  # Include students in read response
