from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from backend.app.models.lesson import Lesson
    from backend.app.models.user import User


class LessonTutorBase(SQLModel):
    lesson_id: int = Field(foreign_key='lesson.id')
    tutor_id: int = Field(foreign_key='user.id')


class LessonTutor(LessonTutorBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    lesson: Optional['Lesson'] = Relationship(back_populates='lesson_tutors')
    tutor: Optional['User'] = Relationship(back_populates='lesson_tutors')


class LessonTutorCreate(LessonTutorBase):
    pass


class LessonTutorRead(LessonTutorBase):
    id: int
    created_at: datetime
