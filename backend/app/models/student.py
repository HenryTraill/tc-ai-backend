from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from backend.app.models.lesson import Lesson


class StudentBase(SQLModel):
    name: str
    grade: str
    strengths: list[str] = Field(default_factory=list, sa_column_kwargs={'type_': 'JSON'})
    weaknesses: list[str] = Field(default_factory=list, sa_column_kwargs={'type_': 'JSON'})


class Student(StudentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    lessons: list['Lesson'] = Relationship(back_populates='student')

    @property
    def lessons_completed(self) -> int:
        return len(self.lessons)


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    grade: Optional[str] = None
    strengths: Optional[list[str]] = None
    weaknesses: Optional[list[str]] = None


class StudentRead(StudentBase):
    id: int
    lessons_completed: int
