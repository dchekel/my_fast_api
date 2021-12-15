from passlib.context import CryptContext


# PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# функция для проверки совпадения полученного пароля с сохраненным хешем.
def verify_password(plain_password: str, hashed_password: str) -> bool:
    print('from def verify_password', 'plain_password=', plain_password)
    print('from def verify_password', 'hashed_password=', hashed_password)
    # return PWD_CONTEXT.verify(plain_password, hashed_password)
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    print('from def get_password_hash', 'password=', password)
    hash_pass = pwd_context.hash(password)
    print('from def get_password_hash', 'hash_pass= ', hash_pass, '; len= ', len(hash_pass))
    # $2b$12$yK.4Aqsxiz8TZmjfYJvA6OnlD/L2OYa/WHj/5UjcVotTngE9tjeea ; len=  60
    return hash_pass
