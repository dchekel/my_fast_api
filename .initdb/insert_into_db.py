from psycopg2 import OperationalError
import psycopg2


def create_connection(db_name, db_user, db_password, db_host, db_port):
    conn = None
    try:
        conn = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return conn


connection = create_connection(
    "postgres_db", "postgres_admin", "admin1234", "127.0.0.1", "5432"
)

roles = [
    ("administrator",),
    ("klient",),
    ("visitor",)
]

role_records = ", ".join(["%s"] * len(roles))

insert_query = f'INSERT INTO "role" (name) VALUES {role_records};'

connection.autocommit = True
cursor = connection.cursor()
cursor.execute(insert_query, roles)
"""
cur.execute(
  "INSERT INTO STUDENT (ADMISSION,NAME,AGE,COURSE,DEPARTMENT) VALUES (3423, 'Alice', 18, 'Information Technology', 'ICT')"
)
"""
"""
from sqlalchemy import insert

stmt = (insert(user_table).values(name='username', fullname='Full Username'))
"""

"""
https://proglib.io/p/kak-podruzhit-python-i-bazy-dannyh-sql-podrobnoe-rukovodstvo-2020-02-27
posts = [
    ("Happy", "I am feeling very happy today", 1),
    ("Hot Weather", "The weather is very hot today", 2),
    ("Help", "I need some help with my work", 2),
    ("Great News", "I am getting married", 1),
    ("Interesting Game", "It was a fantastic game of tennis", 5),
    ("Party", "Anyone up for a late-night party today?", 3),
]

post_records = ", ".join(["%s"] * len(posts))

insert_query = (
    f"INSERT INTO posts (title, description, user_id) VALUES {post_records}"
)"""