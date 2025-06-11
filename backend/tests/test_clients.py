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
    response = client.post('/api/clients/', json=client_data)
    assert response.status_code == 200
    data = response.json()
    assert data['first_name'] == client_data['first_name']
    assert data['last_name'] == client_data['last_name']
    assert data['email'] == client_data['email']
    assert data['phone'] == client_data['phone']
    assert 'id' in data
    assert 'created_at' in data


def test_create_client_invalid_email(client: TestClient):
    """Test creating a client with invalid email"""
    client_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'invalid-email',
        'phone': '+1234567890',
    }
    response = client.post('/api/clients/', json=client_data)
    assert response.status_code == 422  # Validation error


def test_get_clients(client: TestClient, session: Session):
    """Test getting all clients"""
    # Create test clients
    client1 = Client(first_name='John', last_name='Doe', email='john.doe@example.com', phone='+1234567890')
    client2 = Client(first_name='Jane', last_name='Smith', email='jane.smith@example.com', phone='+0987654321')
    session.add(client1)
    session.add(client2)
    session.commit()

    response = client.get('/api/clients/')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]['first_name'] == 'John'
    assert data[1]['first_name'] == 'Jane'


def test_get_client_by_id(client: TestClient, session: Session):
    """Test getting a specific client by ID"""
    test_client = Client(first_name='John', last_name='Doe', email='john.doe@example.com', phone='+1234567890')
    session.add(test_client)
    session.commit()
    session.refresh(test_client)

    response = client.get(f'/api/clients/{test_client.id}')
    assert response.status_code == 200
    data = response.json()
    assert data['first_name'] == 'John'
    assert data['id'] == test_client.id


def test_get_nonexistent_client(client: TestClient):
    """Test getting a non-existent client"""
    response = client.get('/api/clients/999')
    assert response.status_code == 404


def test_update_client(client: TestClient, session: Session):
    """Test updating a client"""
    test_client = Client(first_name='John', last_name='Doe', email='john.doe@example.com', phone='+1234567890')
    session.add(test_client)
    session.commit()
    session.refresh(test_client)

    update_data = {'first_name': 'Johnny', 'email': 'johnny.doe@example.com'}
    response = client.put(f'/api/clients/{test_client.id}', json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data['first_name'] == 'Johnny'
    assert data['last_name'] == 'Doe'  # Should remain unchanged
    assert data['email'] == 'johnny.doe@example.com'
    assert 'updated_at' in data


def test_update_nonexistent_client(client: TestClient):
    """Test updating a non-existent client"""
    update_data = {'first_name': 'Johnny'}
    response = client.put('/api/clients/999', json=update_data)
    assert response.status_code == 404


def test_delete_client(client: TestClient, session: Session):
    """Test deleting a client"""
    test_client = Client(first_name='John', last_name='Doe', email='john.doe@example.com', phone='+1234567890')
    session.add(test_client)
    session.commit()
    session.refresh(test_client)

    response = client.delete(f'/api/clients/{test_client.id}')
    assert response.status_code == 200
    data = response.json()
    assert data['message'] == 'Client deleted successfully'

    # Verify client is deleted
    response = client.get(f'/api/clients/{test_client.id}')
    assert response.status_code == 404


def test_delete_nonexistent_client(client: TestClient):
    """Test deleting a non-existent client"""
    response = client.delete('/api/clients/999')
    assert response.status_code == 404
