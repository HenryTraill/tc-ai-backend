from datetime import UTC, datetime
from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from backend.app.models.lesson import Lesson
    from backend.app.models.student import Student


class CompanyBase(SQLModel):
    name: str
    tc_id: Optional[str] = None
    tutorcruncher_domain: Optional[str] = None


class Company(CompanyBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: Optional[datetime] = None

    # Relationships
    students: List['Student'] = Relationship(back_populates='company')
    lessons: List['Lesson'] = Relationship(back_populates='company')


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    tc_id: Optional[str] = None
    tutorcruncher_domain: Optional[str] = None


class CompanyRead(CompanyBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
