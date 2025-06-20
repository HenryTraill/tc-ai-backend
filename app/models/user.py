from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel, EmailStr
from sqlalchemy import JSON, Column
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from backend.app.models.lesson_tutor import LessonTutor
    from backend.app.models.tutor_student import TutorStudent


class UserType(str, Enum):
    """Type of user"""

    TUTOR = 'tutor'
    ADMIN = 'admin'


class UserBase(SQLModel):
    first_name: str
    last_name: str
    email: EmailStr
    user_type: UserType
    tc_id: Optional[str] = None
    company_ids: List[int] = Field(default_factory=list, sa_column=Column(JSON))


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None

    # Relationships for tutors
    tutor_students: List['TutorStudent'] = Relationship(back_populates='tutor')
    lesson_tutors: List['LessonTutor'] = Relationship(back_populates='tutor')

    @property
    def is_tutor(self) -> bool:
        return self.user_type == UserType.TUTOR

    @property
    def is_admin(self) -> bool:
        return self.user_type == UserType.ADMIN


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    user_type: Optional[UserType] = None
    tc_id: Optional[str] = None
    company_ids: Optional[List[int]] = None
    password: Optional[str] = None


class UserRead(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
    type: Optional[str] = None
