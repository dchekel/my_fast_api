# https://fastapi.tiangolo.com/tutorial/bigger-applications/
from typing import Any
from fastapi import APIRouter, status
from fastapi import HTTPException, Depends  # , FastAPI
# from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import app.core.schemas.schemas as schemas
from app.core.models import models
# from app.core.models.models import User
from app.v1.crud import user as crud_user
from app.v1.api import Token, get_current_user, get_db, get_current_active_user
from app.core.security import get_password_hash
from app.core.auth import (
    authenticate,
    create_access_token,
)
# from app.v1.endpoints.auth.JWTBearer import JWTBearer  # Дениса вариант
router = APIRouter(prefix="/v1/users")

# https://stackoverflow.com/questions/14799189/avoiding-boilerplate-session-handling-code-in-sqlalchemy-functions
# with session_scope() as session:


@router.get("/", status_code=202, tags=["Get Methods"])  # когда ВСЕ , ТО response_model=..., НЕ НУЖЕН
async def read_users(
        db: Session = Depends(get_db)
) -> Any:
        print('@router.get("/",')
        users = db.query(models.User).all()  # session.query(User).all()
        return users  # jsonable_encoder(users) # результат вывода одинаковый


# Вариант Дениса
# @router.get("/secured", status_code=202, dependencies=[Depends(JWTBearer())])
# def secured_url() -> dict:
#     return {"data": "success"}


# NOT WORKING ! 	Error: Unauthorized Response body "detail": "Not authenticated"
@router.get("/me", response_model=schemas.User, tags=["Get Methods"])  #
def read_user_me(
        db: Session = Depends(get_db),
        current_user: schemas.User =Depends(get_current_active_user)  # =Depends(get_current_user)
) -> Any:
    """
    Получение данных о текущем вошедшем в систему пользователе.
    """
    print('@router.get("/me",', db)
    print('from read_user_me \ncurrent_user.email=', current_user.email, '\npassw=', current_user.password)
    return current_user


@router.get("/{user_id}", response_model=schemas.User, tags=["Get Methods"])
def read_user_by_id(
    user_id: int,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    # user = db.query(models.User).filter(models.User.id == user_id).first()
    user = crud_user.get(db=db, id=user_id)
    print('from @router.get("/{user_id}" def read_user_by_id\n', 'current_user=', current_user, '\nuser=', user, user.roles)
    if user == current_user:
        return user
    if not crud_user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user  # jsonable_encoder(user)


@router.post("/login", status_code=201, tags=["Post Methods"])  # , response_model=Token
def login(
        # декларируем OAuth2PasswordRequestForm зависимость
        db: Session = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Get the JWT for a user with data from OAuth2 request form body.
    """
    print(db)
    print(form_data)
    print('form_data.username=', form_data.username)
    print('form_data.password=', form_data.password)

    # проверяем тело запроса с помощью authenticate функции
    user = authenticate(username=form_data.username, password=form_data.password, db=db)
    print('from @router.post("/login" user=', user)
    # Если аутентификация не удалась, пользователь не возвращается, это вызывает ответ HTTP 400.
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # if not user:
    #     raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(sub=user.username)
    print(access_token)
    return {  # JWT веб-токен JSON создается и возвращается клиенту
        "access_token": access_token,
        "token_type": "bearer",
    }
# Если пользователь проходит проверку аутентификации, /login конечная точка возвращает JWT клиенту.
#  Затем этот JWT можно использовать для доступа к ограниченным функциям.
# Базовый пример этого находится в третьей новой конечной точке:


@router.post("/signup", response_model=schemas.User, status_code=201, tags=["Post Methods"])  # 1
# указываем Pydantic, response_model, который формирует ответ JSON конечной точки.
def create_user_signup(
        *,
        # request: Request,
        db: Session = Depends(get_db),  # определяем базу данных как зависимость конечной точки с помощью
        # возможностей внедрения зависимостей FastAPI
        # но в случае с @contextmanager
        #               def session_scope(): это не работает
        user_in: schemas.UserCreate
        # 3 Тело запроса POST проверяется в соответствии с UserCreate
        # pydantic схемой. в app/core/schemas/schemas.py
        ) -> Any:
    """
    Создание нового пользователя без необходимости входа в систему
    """
    # users = session.query(User).all()
    # print('users', users)  # users [<User: dchekel, Name: Dmitry Chekel>, <User: dc2, Name: d c>, <User: dch3, Name: dd cc>]
    # print('0', session)
    # print('00', request)
    # print('1', db)  # <sqlalchemy.orm.session.Session object at 0x10e509a60>
    # print('2', db.__dict__)  # {'identity_map': <sqlalchemy.orm.identity.WeakInstanceDict object at 0x10e509ac0>, '_new': {}, '_deleted': {}, 'bind': Engine(sqlite:///example.db), '_Session__binds': {}, '_flushing': False, '_warn_on_events': False, '_transaction': None, '_nested_transaction': None, 'future': False, 'hash_key': 1, 'autoflush': False, 'expire_on_commit': True, 'enable_baked_queries': True, 'autocommit': False, 'twophase': False, '_query_cls': <class 'sqlalchemy.orm.query.Query'>, 'current_user_id': None}
    # print('3', Session)  #  <class 'sqlalchemy.orm.session.Session'>
    # print('4', user_in)  # 4 first_name='john' surname='Do' email='user_do@example.com' is_superuser=False password='string'
    user = db.query(models.User).filter(models.User.email == user_in.email).first()  # 4
    # print('user = ', user)  #  <User: dch3, Name: dd cc>
    # используем ORM SQLAlchemy для запроса user таблицы базы данных , применяя фильтр, чтобы проверить,
    # существуют ли уже какие-либо пользователи с запрошенным адресом электронной почты.
    if user:
        # print('user already exists ', user)
        raise HTTPException(  # 5
            # Чтобы гарантировать уникальность электронных писем пользователей, если соответствующий
            # пользователь найден (то есть существующий пользователь с тем же адресом электронной почты),
            # возвращаем HTTP 400
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    # print('create user')
    user = crud_user.create(db=db, obj_in=user_in)  # 6  ,
    # если адрес электронной почты пользователя уникален, мы переходим к использованию crud
    # служебных функций для создания пользователя.
    return user


'''
@router.post("/auth/login", response_model=Token)  # /token ; важно-response_model
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db),
):
    print('from @app.post("/token"', '\nform_data=', form_data.username, form_data.password, form_data.client_id, form_data.client_secret, form_data.grant_type, form_data.scopes)
    user = authenticate(db=db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # срок действия токена
    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # Создайте настоящий токен доступа JWT и верните его.
    # access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    access_token = create_access_token(sub=user.username)
    # В спецификации JWT говорится, что есть ключ sub с предметом токена.
    # Использовать его необязательно, но здесь вы должны поместить идентификацию пользователя,
    # поэтому мы используем его здесь.
    return {"access_token": access_token, "token_type": "bearer"}





@router.get("/", status_code=202)
async def read_users(
        db: Session = Depends(get_db)
) -> Any:
        print('@router.get("/",')
        users = db.query(models.User).all()  # session.query(User).all()
        return users  # jsonable_encoder(users) # результат вывода одинаковый



@router.get("/show_me")  # , response_model=schemas.User
async def read_user_me():  # User=Depends(get_current_user)
    users = session.query(User).all()  #
    # return users  # jsonable_encoder(users) # результат вывода одинаковый
    # user = 'qqqq'
    # print('это вывод информации из read_users_me', user.email, 'hashed_passw=', user.password)  # hashed_password
    return users[0]




from app.core.auth import AuthHandler
from app.core.schemas.schemas import AuthDetails
# auth_handler = AuthHandler()
# users2 = []
# end test auth

    # test auth
    @router.post('/register', status_code=201)
    def register(*,  auth_details: AuthDetails)-> Any:  # db: Session = Depends(session),,user_in: schemas.UserCreate
        print('auth_details', auth_details)
        users = session.query(User).all()
        print('users', users)
        # print('user_in', user_in),
        if any(x['username'] == auth_details.username for x in users2):
            raise HTTPException(status_code=400, detail='Username is taken2')
        hashed_password = auth_handler.get_password_hash(auth_details.password)
        print('hashed_password', hashed_password)
        users2.append({
            'username': auth_details.username,
            'password': hashed_password
        })
        print('users2', users2)
        return users2
    # end test auth

'''
