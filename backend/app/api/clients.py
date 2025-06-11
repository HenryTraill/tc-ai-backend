from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..core.database import get_session
from ..models.client import Client, ClientCreate, ClientRead, ClientUpdate

router = APIRouter(prefix='/clients', tags=['clients'])


@router.get('/', response_model=list[ClientRead])
def get_clients(session: Session = Depends(get_session)):
    """Get all clients"""
    clients = session.exec(select(Client)).all()
    return clients


@router.get('/{client_id}', response_model=ClientRead)
def get_client(client_id: int, session: Session = Depends(get_session)):
    """Get a specific client by ID"""
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail='Client not found')
    return client


@router.post('/', response_model=ClientRead)
def create_client(client_data: ClientCreate, session: Session = Depends(get_session)):
    """Create a new client"""
    client = Client(**client_data.model_dump())
    session.add(client)
    session.commit()
    session.refresh(client)
    return client


@router.put('/{client_id}', response_model=ClientRead)
def update_client(client_id: int, client_data: ClientUpdate, session: Session = Depends(get_session)):
    """Update a client"""
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail='Client not found')

    client_data_dict = client_data.model_dump(exclude_unset=True)
    for key, value in client_data_dict.items():
        setattr(client, key, value)

    client.updated_at = datetime.utcnow()
    session.add(client)
    session.commit()
    session.refresh(client)
    return client


@router.delete('/{client_id}')
def delete_client(client_id: int, session: Session = Depends(get_session)):
    """Delete a client"""
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail='Client not found')

    session.delete(client)
    session.commit()
    return {'message': 'Client deleted successfully'}
