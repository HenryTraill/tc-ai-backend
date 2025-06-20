from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from backend.app.models.lesson import Lesson
    from backend.app.models.student import Student


class LessonStudent(SQLModel, table=True):
    """Junction table for many-to-many relationship between lessons and students"""

    lesson_id: Optional[int] = Field(default=None, foreign_key='lesson.id', primary_key=True)
    student_id: Optional[int] = Field(default=None, foreign_key='student.id', primary_key=True)

    # Relationships
    lesson: Optional['Lesson'] = Relationship(back_populates='lesson_students')
    student: Optional['Student'] = Relationship(back_populates='lesson_students')
