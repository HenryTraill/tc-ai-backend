from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.auth import get_password_hash
from app.models import User, UserType


def test_login_success(client: TestClient, test_tutor: User):
    """Test successful login with valid credentials."""
    response = client.post('/api/auth/login', json={'email': 'test@example.com', 'password': 'password'})
    assert response.status_code == 200
    data = response.json()
    assert 'access_token' in data
    assert data['token_type'] == 'bearer'


def test_login_invalid_credentials(client: TestClient):
    """Test login with invalid credentials."""
    response = client.post('/api/auth/login', json={'email': 'test@example.com', 'password': 'wrongpassword'})
    assert response.status_code == 401
    assert response.json()['detail'] == 'Incorrect email or password'


def test_login_inactive_user(client: TestClient, session: Session):
    """Test login with an inactive user."""
    # Create an inactive user
    inactive_user = User(
        email='inactive@example.com',
        hashed_password=get_password_hash('password'),
        user_type=UserType.TUTOR,
        is_active=False,
        first_name='Inactive',
        last_name='User',
    )
    session.add(inactive_user)
    session.commit()

    response = client.post('/api/auth/login', json={'email': 'inactive@example.com', 'password': 'password'})
    assert response.status_code == 401
    assert response.json()['detail'] == 'Inactive user'


def test_protected_route_with_valid_token(client: TestClient, tutor_token: str, test_tutor: User):
    """Test accessing a protected route with a valid token."""
    response = client.get('/api/auth/me', headers={'Authorization': f'Bearer {tutor_token}'})
    assert response.status_code == 200
    data = response.json()
    assert data['email'] == 'test@example.com'
    assert data['user_type'] == UserType.TUTOR.value


def test_protected_route_without_token(client):
    """Test accessing a protected route without a token."""
    response = client.get('/api/auth/me')
    assert response.status_code == 401


def test_protected_route_with_invalid_token(client: TestClient):
    """Test accessing a protected route with an invalid token."""
    response = client.get('/api/auth/me', headers={'Authorization': 'Bearer invalid_token'})
    assert response.status_code == 401
    assert response.json()['detail'] == 'Could not validate credentials'


def test_protected_route_with_expired_token(client: TestClient):
    """Test accessing a protected route with an expired token."""
    # Create an expired token
    expired_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0QGV4YW1wbGUuY29tIiwiZXhwIjoxNTE2MjM5MDIyLCJ0eXBlIjoiVFVUT1IifQ.2hDgYvYRtr7VZmHl2XGpZqQxJzQxJzQxJzQxJzQxJzQ'

    response = client.get('/api/auth/me', headers={'Authorization': f'Bearer {expired_token}'})
    assert response.status_code == 401
    assert response.json()['detail'] == 'Could not validate credentials'
