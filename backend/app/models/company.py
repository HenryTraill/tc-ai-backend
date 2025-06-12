from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class CompanyBase(SQLModel):
    name: str
    tc_id: Optional[str] = None
    tutorcruncher_domain: Optional[str] = None


class Company(CompanyBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None


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
