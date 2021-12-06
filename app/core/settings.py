import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from contextlib import contextmanager
# from part 10
from pydantic import AnyHttpUrl, BaseSettings, EmailStr, validator
from typing import List, Optional, Union

# DATABASE_URI = DBE + dbUser + ':' + dbPassword + '@' + dbServer + '/'+ dbName
# engine=create_engine('postgresql://<username>:<password>@localhost/<db_name>'
DATABASE_URI = 'postgresql+psycopg2://postgres_admin:pos12345@localhost:5432/postgres_db'

try:
    engine = create_engine(DATABASE_URI)  # , echo=True)
    connection = engine.connect()

except sqlalchemy.exc.OperationalError:
    print("Database doesn't exists or username/password incorrect")
    # input("Press Enter to continue...")
else:
    print('OK')
    print('connection to the database is established')
# input("Press Enter to continue...")
Base = declarative_base()

Session = sessionmaker()
# from part 10
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# https://stackoverflow.com/questions/14799189/avoiding-boilerplate-session-handling-code-in-sqlalchemy-functions
@contextmanager
def session_scope():  # рамки сессии
    """Обеспечение транзакционной сферы вокруг серии операций
    Provide a transactional scope around a series of operations."""
    session = Session(bind=engine)  # from part 10 #  SessionLocal()
    # session.current_user_id = None  # from part 10
    try:
        print('from session_scope:', session)
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


# from part 10
class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    JWT_SECRET: str = "TEST_SECRET_DO_NOT_USE_IN_PROD"
    ALGORITHM: str = "HS256"

    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    SQLALCHEMY_DATABASE_URI: Optional[str] = DATABASE_URI  # "sqlite:///example.db"
    FIRST_SUPERUSER: EmailStr = "admin@gmail.com"
    FIRST_SUPERUSER_PW: str = "admin1234"

    class Config:
        case_sensitive = True


settings = Settings()
