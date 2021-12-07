from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.auth import oauth2_scheme
from app.core.settings import settings

from app.core.models.models import User
from app.core.settings import SessionLocal  # session_scope


class TokenData(BaseModel):
    username: Optional[str] = None


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


async def get_current_user(
    # Здесь входящий токен JWT декодируется (снова с использованием python-jose)
    # с комбинацией JWT_SECRET значения, установленного в API, app/core/config.py а также
    # настроенного там алгоритма кодирования (HS256). Если это декодирование прошло успешно,
    # мы «доверяем» токену и извлекаем пользователя из базы данных.
    db: Session = Depends(get_db),  # session_scope
    token: str = Depends(oauth2_scheme)
) -> User:
    # token = ''
    # print('db=', db)  # <sqlalchemy.orm.session.Session object at 0x10a0e8a30>
    print('token=', token)
    # token= eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
    # eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNjM5MzAxMjYxLCJpYXQiOjE2Mzg2MTAwNjEsInN1YiI6IjIifQ.
    # 0YzpPKRwcMkkuJZa0X45Oy_kq1xR8ZDSCddqHLrhcgA
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,  # .HTTP_401_UNAUTHORIZED
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )
        username: str = payload.get("sub")
        print('settings.JWT_SECRET=', settings.JWT_SECRET)  # вывод: settings.JWT_SECRET= TEST_SECRET_DO_NOT_USE_IN_PROD
        print('username=', username)  # username= 2
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
        print('token_data=', token_data)  # username='2'
    except JWTError:  #
        raise credentials_exception
    user = db.query(User).filter(User.id == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user
# NOT WORKING !!
# with session_scope() as session:


async def get_first_user(db: Session = Depends(get_db),
                         token: str = Depends(oauth2_scheme)
                         ) -> User:
    # user = session.query(User).first()
    print(token)
    user = db.query(User).first()
    return user
#
# def get_db() -> Generator:
#     db = SessionLocal()
#     db.current_user_id = None
#     try:
#         yield db
#     finally:
#         db.close()
