from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from ..core.auth import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
    get_password_hash,
)
from ..core.config import settings
from ..core.database import get_session
from ..models import Token, User, UserLogin, UserRead, UserUpdate

router = APIRouter(prefix='/auth', tags=['authentication'])


@router.post('/login', response_model=Token, name='login')
def login(user_credentials: UserLogin, session: Session = Depends(get_session)):
    """Authenticate user and return access token"""
    user = authenticate_user(session, user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Inactive user',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={'email': user.email, 'type': user.user_type.value}, expires_delta=access_token_expires
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.get('/me', response_model=UserRead, name='get_current_user')
def get_me(current_user: User = Depends(get_current_active_user)):
    """Get current user information"""
    return current_user


@router.put('/me', response_model=UserRead, name='update_current_user')
def update_me(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    """Update current user information"""
    user_data_dict = user_data.model_dump(exclude_unset=True)

    # Handle password update separately
    if 'password' in user_data_dict:
        user_data_dict['hashed_password'] = get_password_hash(user_data_dict.pop('password'))

    for key, value in user_data_dict.items():
        setattr(current_user, key, value)

    current_user.updated_at = datetime.now(timezone.utc)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user
