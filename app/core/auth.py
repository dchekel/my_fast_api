from jose import jwt
from fastapi.security import OAuth2PasswordBearer  # HTTPAuthorizationCredentials, HTTPBearer,
from sqlalchemy.orm.session import Session
# from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, MutableMapping, List, Union
from app.core.models.models import User
from app.core.settings import settings
from app.core.security import verify_password

JWTPayloadMapping = MutableMapping[
    str, Union[datetime, bool, str, List[str], List[int]]
]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


def authenticate(
    *,
    username: str,
    password: str,
    db: Session,
) -> Optional[User]:
    # print('db=', db)
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    # используем verify_password функцию, которую мы рассмотрели, в app/core/security.py
    # которой используется библиотека passlib
    if not verify_password(password, user.password):  # hashed_password
        return None
    return user


#  Ключевое слово sub аргумент create_access_token функции будет соответствовать идентификатору пользователя
def create_access_token(*, sub: str) -> str:
    print('def create_access_token')
    return _create_token(
        token_type="access_token",
        # app/core/config.py Обновляются , чтобы включить некоторые AUTH связанных параметров,
        # такие сроки JWT действий до истечения срока действия
        lifetime=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub,
    )


def _create_token(
    token_type: str,
    lifetime: timedelta,
    sub: str,
) -> str:
    print('def _create_token')
    # Строим JWT. В RFC 7519 есть ряд обязательных / необязательных полей (известных как «заявки») .
    payload = {}
    expire = datetime.utcnow() + lifetime
    payload["type"] = token_type

    # https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.3
    # The "exp" (expiration time) claim identifies the expiration time on
    # or after which the JWT MUST NOT be accepted for processing
    # "exp"(время истечения срока действия) определяет время истечения срока действия на или
    # после которого JWT НЕ ДОЛЖЕН приниматься для обработки
    payload["exp"] = expire

    # The "iat" (issued at) claim identifies the time at which the
    # JWT was issued.
    # Заявление «iat» (выдано в) указывает время, когда был выдан JWT.
    payload["iat"] = datetime.utcnow()

    # The "sub" (subject) claim identifies the principal that is the
    # subject of the JWT
    # Утверждение «sub» (субъект) определяет принципала, который является субъектом JWT.
    # В нашем случае это будет идентификатор пользователя.
    payload["sub"] = str(sub)
    print(payload, settings.JWT_SECRET, settings.ALGORITHM)
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)
    print('token=', token)
    return token


'''

class AuthHandler:
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = 'SECRET'

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, password):  # hashed_password
        return self.pwd_context.verify(plain_password, password)  # hashed_password

    def encode_token(self, user_id):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, minutes=5),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Signature has expired')
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail='Invalid token')

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)

'''
