from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel, EmailStr
from sqlalchemy import JSON, Column
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from backend.app.models.client import Client
    from backend.app.models.lesson import Lesson


class StudentBase(SQLModel):
    client_id: int = Field(foreign_key='client.id')
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    grade: str
    strengths: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    weaknesses: List[str] = Field(default_factory=list, sa_column=Column(JSON))


class Student(StudentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    lessons: List['Lesson'] = Relationship(back_populates='student')
    client: Optional['Client'] = Relationship(back_populates='students')

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
    # Note: strengths and weaknesses are intentionally excluded from updates


class StudentRead(StudentBase):
    id: int
    lessons_completed: int
