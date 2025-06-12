from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel
from sqlalchemy import JSON, Column
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from backend.app.models.student import Student


class LessonStatus(str, Enum):
    """Status of a lesson"""

    PLANNED = 'planned'
    COMPLETE = 'complete'
    PENDING = 'pending'
    CANCELLED = 'cancelled'
    CANCELLED_BUT_CHARGEABLE = 'cancelled-but-chargeable'


class LessonBase(SQLModel):
    student_id: int = Field(foreign_key='student.id')
    company_id: Optional[int] = Field(default=None)
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

    student: Optional['Student'] = Relationship(back_populates='lessons')


class LessonCreate(LessonBase):
    pass


class LessonUpdate(BaseModel):
    student_id: Optional[int] = None
    company_id: Optional[int] = None
    tc_path: Optional[str] = None
    start_dt: Optional[datetime] = None
    end_dt: Optional[datetime] = None
    subject: Optional[str] = None
    topic: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[LessonStatus] = None
    # Note: skills_practiced, main_subjects_covered, student_strengths_observed,
    # student_weaknesses_observed, and tutor_tips are intentionally excluded from updates


class LessonRead(LessonBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    company_name: Optional[str] = None
    tutorcruncher_url: Optional[str] = None
