from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models.client import Client


def test_create_client(client: TestClient):
    """Test creating a new client"""
    client_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'phone': '+1234567890',
    }
    response = client.post(client.app.url_path_for('create_client'), json=client_data)
    assert response.status_code == 200
    data = response.json()
    assert data['first_name'] == client_data['first_name']
    assert data['last_name'] == client_data['last_name']
    assert data['email'] == client_data['email']
    assert data['phone'] == client_data['phone']
    assert 'id' in data
    assert 'created_at' in data
    assert 'updated_at' in data


def test_create_client_invalid_email(client: TestClient):
    """Test creating a client with invalid email"""
    client_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'invalid-email',
        'phone': '+1234567890',
    }
    response = client.post(client.app.url_path_for('create_client'), json=client_data)
    assert response.status_code == 422  # Validation error


def test_create_client_duplicate_email(client: TestClient, session: Session):
    """Test creating a client with duplicate email"""
    # Create first client
    client_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'phone': '+1234567890',
    }
    response = client.post(client.app.url_path_for('create_client'), json=client_data)
    assert response.status_code == 200

    # Try to create another client with the same email
    client_data2 = {
        'first_name': 'Jane',
        'last_name': 'Smith',
        'email': 'john.doe@example.com',  # Same email
        'phone': '+0987654321',
    }
    response = client.post(client.app.url_path_for('create_client'), json=client_data2)
    # Should allow duplicate emails currently (no unique constraint)
    assert response.status_code == 200


def test_get_clients(client: TestClient, session: Session):
    """Test getting all clients"""
    # Create a test client
    test_client = Client(first_name='John', last_name='Doe', email='john.doe@example.com', phone='+1234567890')
    session.add(test_client)
    session.commit()

    response = client.get(client.app.url_path_for('get_clients'))
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    # Find our test client in the response
    client_found = False
    for client_item in data:
        if client_item['email'] == 'john.doe@example.com':
            client_found = True
            break
    assert client_found


def test_get_client_by_id(client: TestClient, session: Session):
    """Test getting a specific client by ID"""
    # Create a test client
    test_client = Client(first_name='John', last_name='Doe', email='john.doe@example.com', phone='+1234567890')
    session.add(test_client)
    session.commit()
    session.refresh(test_client)

    response = client.get(client.app.url_path_for('get_client', client_id=test_client.id))
    assert response.status_code == 200
    data = response.json()
    assert data['first_name'] == 'John'
    assert data['last_name'] == 'Doe'
    assert data['email'] == 'john.doe@example.com'
    assert data['id'] == test_client.id


def test_get_client_not_found(client: TestClient):
    """Test getting a non-existent client"""
    response = client.get(client.app.url_path_for('get_client', client_id=999))
    assert response.status_code == 404
    assert 'Client not found' in response.json()['detail']


def test_update_client(client: TestClient, session: Session):
    """Test updating a client"""
    # Create a test client
    test_client = Client(first_name='John', last_name='Doe', email='john.doe@example.com', phone='+1234567890')
    session.add(test_client)
    session.commit()
    session.refresh(test_client)

    # Update client
    update_data = {'first_name': 'Jane', 'email': 'jane.doe@example.com'}
    response = client.put(client.app.url_path_for('update_client', client_id=test_client.id), json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data['first_name'] == 'Jane'
    assert data['email'] == 'jane.doe@example.com'
    assert data['last_name'] == 'Doe'  # Should remain unchanged


def test_update_client_not_found(client: TestClient):
    """Test updating a non-existent client"""
    update_data = {'first_name': 'Jane'}
    response = client.put(client.app.url_path_for('update_client', client_id=999), json=update_data)
    assert response.status_code == 404
    assert 'Client not found' in response.json()['detail']


def test_delete_client(client: TestClient, session: Session):
    """Test deleting a client"""
    # Create a test client
    test_client = Client(first_name='John', last_name='Doe', email='john.doe@example.com', phone='+1234567890')
    session.add(test_client)
    session.commit()
    session.refresh(test_client)

    response = client.delete(client.app.url_path_for('delete_client', client_id=test_client.id))
    assert response.status_code == 200
    assert response.json()['message'] == 'Client deleted successfully'

    # Verify the client was deleted
    response = client.get(client.app.url_path_for('get_client', client_id=test_client.id))
    assert response.status_code == 404


def test_delete_client_not_found(client: TestClient):
    """Test deleting a non-existent client"""
    response = client.delete(client.app.url_path_for('delete_client', client_id=999))
    assert response.status_code == 404
    assert 'Client not found' in response.json()['detail']
