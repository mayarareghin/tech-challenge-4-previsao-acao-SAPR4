from http import HTTPStatus
from typing import Annotated
from fastapi import Query
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.database import get_session  # Agora retorna Session síncrono
from app.db.models import User
from app.api.schemas import (
    FilterPage,
    Message,
    UserList,
    UserPublic,
    UserSchema,
)

from app.api.dependencies.security import (
    get_current_user,
    get_password_hash,
)

users = APIRouter(prefix='/users', tags=['users'])
SessionType = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@users.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: SessionType):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Email already exists',
            )

    hashed_password = get_password_hash(user.password)

    db_user = User(
        email=user.email,
        username=user.username,
        password=hashed_password,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@users.get('/', response_model=UserList)
def read_users(
    session: SessionType,
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
):
    query = session.scalars(
        select(User).offset(offset).limit(limit)
    )
    users_list = query.all()
    return {'users': users_list}


@users.put('/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int,
    user: UserSchema,
    session: SessionType,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Not enough permissions',
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        current_user.username = user.username
        current_user.password = get_password_hash(user.password)
        current_user.email = user.email
        session.commit()
        session.refresh(current_user)

        return current_user

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or Email already exists',
        )


@users.delete('/{user_id}', response_model=Message)
def delete_user(
    user_id: int,
    session: SessionType,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Not enough permissions',
            headers={"WWW-Authenticate": "Bearer"},
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'User deleted'}