from datetime import datetime, timedelta, timezone
from http import HTTPStatus

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt  
from pwdlib import PasswordHash
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.database import get_session  
from app.db.models import User
from app.core.settings import Settings

settings = Settings()
pwd_context = PasswordHash.recommended()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow().replace(tzinfo=timezone.utc) + timedelta(
        minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({'exp': expire})


    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
) -> User:
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        subject_email = payload.get('sub')
        if not subject_email:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = session.scalar(select(User).where(User.email == subject_email))
    if not user:
        raise credentials_exception

    return user
