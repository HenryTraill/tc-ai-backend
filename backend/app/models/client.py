from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel, EmailStr
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from backend.app.models.student import Student


class ClientBase(SQLModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    address: Optional[str] = None
    notes: Optional[str] = None
    company_id: Optional[int] = Field(default=None, foreign_key='company.id')
    tc_id: Optional[str] = None
    tc_path: Optional[str] = None


class Client(ClientBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None
    email: EmailStr = Field(unique=True)

    students: List['Student'] = Relationship(back_populates='client')


class ClientCreate(ClientBase):
    pass


class ClientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    notes: Optional[str] = None
    tc_id: Optional[str] = None
    tc_path: Optional[str] = None
    # Note: company_id is intentionally excluded from updates


class ClientRead(ClientBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
