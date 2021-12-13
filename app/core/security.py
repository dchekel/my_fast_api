from passlib.context import CryptContext


PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    print('def verify_password')
    print('plain_password=', plain_password)
    print('hashed_password=', hashed_password)
    return PWD_CONTEXT.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    print('def get_password_hash')
    print('password=', password)
    hash_pass = PWD_CONTEXT.hash(password)
    print('hash_pass= ', hash_pass, '; len= ', len(hash_pass))
    # $2b$12$yK.4Aqsxiz8TZmjfYJvA6OnlD/L2OYa/WHj/5UjcVotTngE9tjeea ; len=  60
    return hash_pass
