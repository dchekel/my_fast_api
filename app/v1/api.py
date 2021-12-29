from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.auth import oauth2_scheme
from app.core.settings import settings

from app.core.models.models import User, Cart
# from app.core.schemas.cart import Cart
from app.core.settings import SessionLocal  # session_scope
from app.v1 import crud


class TokenData(BaseModel):
    username: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str


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
    print('from get_current_user db=', db)  # <sqlalchemy.orm.session.Session object at 0x10a0e8a30>
    print('from get_current_user token=', token) # token= eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
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
            options={"verify_aud": False},  # TODO это надо?
        )
        username: str = payload.get("sub")
        print('from api  def get_current_user', 'payload=', payload.values())
        print('from api  def get_current_user', 'settings.JWT_SECRET=', settings.JWT_SECRET)  # вывод: settings.JWT_SECRET= TEST_SECRET_DO_NOT_USE_IN_PROD
        print('from api  def get_current_user', 'username=', username)  # username= 2
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
        print('token_data=', token_data)  # username='2'
    except JWTError:  #
        raise credentials_exception
    print('from api  def get_current_user', '\nUser.id=', User.id, '\ntoken_data.username=', token_data.username)
    user = db.query(User).filter(User.username == token_data.username).first()  # TODO проверить типы данных filter
    if user is None:
        raise credentials_exception
    return user
# NOT WORKING !!
# with session_scope() as session:


def get_current_active_user(current_user: User = Depends(get_current_user)):  # -> User
    print('def get_current_active_user(')
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user


async def get_cart_current_user(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),  # session_scope
        # token: str = Depends(oauth2_scheme)
) -> Cart:
    '''
    id: int
    user_id: int
    product_id: int
    price: float
    quantity: float
    '''
    print('from get_cart_current_user db=', db)  # <sqlalchemy.orm.session.Session object at 0x10a0e8a30>
    #
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,  # .HTTP_401_UNAUTHORIZED
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).all()
    # .with_entities(id, product_id, quantity, 'price')
    print('from api  def get_cart_current_user', type(cart), 'cart=', cart)
    if cart is None:
        raise credentials_exception
    return cart
