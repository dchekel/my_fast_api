# https://fastapi.tiangolo.com/tutorial/bigger-applications/
from typing import Any
from fastapi import APIRouter
from fastapi import HTTPException, Depends  # , FastAPI
# from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
# from sqlalchemy.orm.session import Session
from app.core.models.models import User
from app.core.settings import SessionLocal  # session_scope
import app.core.schemas.schemas as schemas
from app.v1.crud import user as crud_user
from app.v1.api import get_current_user, get_first_user, get_db
from app.core.auth import (
    authenticate,
    create_access_token,
)
router = APIRouter(prefix="/v1/users")

# https://stackoverflow.com/questions/14799189/avoiding-boilerplate-session-handling-code-in-sqlalchemy-functions
# with session_scope() as session:


@router.get("/", status_code=202)
async def read_users(
        db: Session = Depends(get_db)
) -> Any:
        users = db.query(User).all()  # session.query(User).all()
        return users  # jsonable_encoder(users) # результат вывода одинаковый


@router.get("/{user_id}", response_model=schemas.User)
def read_user_by_id(
    user_id: int,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = db.query(User).filter(User.id == user_id).first()
    # user = crud.user.get(db, id=user_id)
    # if user == current_user:
    #     return user
    # if not crud.user.is_superuser(current_user):
    #     raise HTTPException(
    #         status_code=400, detail="The user doesn't have enough privileges"
    #     )
    return user  # jsonable_encoder(user)


@router.post("/login", status_code=201)
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

    # проверяем тело запроса с помощью новой authenticate функции
    user = authenticate(username=form_data.username, password=form_data.password, db=db)
    # user = authenticate(email=form_data.username, password=form_data.password, db=db)
    print(user)
    # Если аутентификация не удалась, пользователь не возвращается, это вызывает ответ HTTP 400.
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(sub=user.id)
    print(access_token)
    return {  # JWT веб-токен JSON создается и возвращается клиенту
        "access_token": access_token,
        "token_type": "bearer",
    }
# Если пользователь проходит проверку аутентификации, /login конечная точка возвращает JWT клиенту.
#  Затем этот JWT можно использовать для доступа к ограниченным функциям.
# Базовый пример этого находится в третьей новой конечной точке:


@router.post("/signup", response_model=schemas.User, status_code=201)  # 1
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
    user = db.query(User).filter(User.email == user_in.email).first()  # 4
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


# NOT WORKING !
@router.get("/me")  # , response_model=schemas.User
async def read_users_me(current_user: User = Depends(get_current_user)):  # =Depends(get_current_user)
    """ Получение данных о текущем вошедшем в систему пользователе.
    """
    user = current_user
    print('это вывод информации из read_users_me', user.email, 'hashed_passw=', user.password)  # hashed_password
    return user

'''
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
