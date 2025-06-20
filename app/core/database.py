from typing import Generator

from sqlmodel import Session, SQLModel, create_engine

from .config import settings

settings.database_url = settings.database_url.replace('postgres://', 'postgresql://', 1)

engine = create_engine(settings.database_url, echo=settings.debug)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
