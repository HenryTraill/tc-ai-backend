from datetime import UTC, datetime, timedelta
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from jose import jwt
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.core.auth import get_password_hash
from app.core.config import settings
from app.core.database import get_session
from app.main import app
from app.models import User, UserType


class AuthenticatedTestClient(TestClient):
    """A TestClient that automatically includes authentication headers."""

    def __init__(self, app, token: str, user: User):
        super().__init__(app)
        self.token = token
        self.user = user
        self._auth_header = {'Authorization': f'Bearer {token}'}

    def get(self, *args, **kwargs):
        headers = {**self._auth_header, **kwargs.pop('headers', {})}
        return super().get(*args, headers=headers, **kwargs)

    def post(self, *args, **kwargs):
        headers = {**self._auth_header, **kwargs.pop('headers', {})}
        return super().post(*args, headers=headers, **kwargs)

    def put(self, *args, **kwargs):
        headers = {**self._auth_header, **kwargs.pop('headers', {})}
        return super().put(*args, headers=headers, **kwargs)

    def delete(self, *args, **kwargs):
        headers = {**self._auth_header, **kwargs.pop('headers', {})}
        return super().delete(*args, headers=headers, **kwargs)


@pytest.fixture(name='session')
def session_fixture() -> Generator[Session, None, None]:
    """Create a new database session for a test."""
    engine = create_engine('sqlite://', connect_args={'check_same_thread': False}, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name='client')
def client_fixture(session: Session) -> Generator[TestClient, None, None]:
    """Create a new FastAPI TestClient that uses the `session` fixture to override
    the `get_session` dependency that is injected into routes.
    """

    def _get_session_override():
        return session

    app.dependency_overrides[get_session] = _get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def create_test_token(user_type: UserType = UserType.TUTOR) -> str:
    """Create a test JWT token for a specific user type."""
    expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    expire = datetime.now(UTC) + expires_delta
    to_encode = {
        'exp': expire,
        'email': 'test@example.com',
        'type': user_type.value,
    }
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


@pytest.fixture(name='tutor_token')
def tutor_token_fixture() -> str:
    """Fixture that provides a valid tutor JWT token."""
    return create_test_token(UserType.TUTOR)


@pytest.fixture(name='test_tutor')
def test_tutor_fixture(session: Session) -> User:
    """Fixture that creates a test tutor user in the database."""
    tutor = User(
        email='test@example.com',
        hashed_password=get_password_hash('password'),
        is_active=True,
        is_tutor=True,
        user_type=UserType.TUTOR,
        first_name='Test',
        last_name='Tutor',
        company_ids=[],
    )
    session.add(tutor)
    session.commit()
    session.refresh(tutor)
    return tutor


@pytest.fixture(name='auth_client')
def auth_client_fixture(client: TestClient, tutor_token: str, test_tutor: User) -> AuthenticatedTestClient:
    """Fixture that provides an authenticated test client and ensures the test tutor exists."""
    return AuthenticatedTestClient(client.app, tutor_token, test_tutor)


def create_authenticated_client_for_user(client: TestClient, user: User) -> AuthenticatedTestClient:
    from datetime import datetime, timedelta

    from jose import jwt

    from app.core.config import settings

    expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    expire = datetime.now(UTC) + expires_delta
    to_encode = {
        'exp': expire,
        'email': user.email,
        'type': user.user_type.value,
    }
    token = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return AuthenticatedTestClient(client.app, token, user)
