import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table, String, INTEGER, Column, Text, DateTime, Boolean
from datetime import datetime
from sqlalchemy import select
# from sqlalchemy.orm import declarative_base, sessionmaker

# DATABASE_URI = DBE + dbUser + ':' + dbPassword + '@' + dbServer + '/'+ dbName
# engine=create_engine('postgresql://<username>:<password>@localhost/<db_name>'
DATABASE_URI = 'postgresql+psycopg2://postgres_admin:pos12345@localhost:5432/postgres_db'
# engine = create_engine(DATABASE_URI, echo=True)

try:
    engine = create_engine(DATABASE_URI)
    connection = engine.connect()

except sqlalchemy.exc.OperationalError:
    print("Database doesn't exists or username/password incorrect")
    # input("Press Enter to continue...")
else:
    print('OK')
    print('connection to the database is established')
input("Press Enter to continue...")

from sqlalchemy import MetaData, Table, String, Integer, Column, Text, DateTime, Boolean
from datetime import datetime

metadata = MetaData()
'''username varchar(100) not null,
password varchar(60) not null,
first_name varchar(100),
last_name varchar(100),
email varchar(100) not null,
address varchar(100) not null,
primary key(id),
unique(username),
unique(email)
'''
user = Table('user', metadata,
             Column('id', Integer(), primary_key=True),
             Column('username', String(100), nullable=False),
             Column('password', String(60),  nullable=False),
             Column('first_name', String(100)),
             Column('last_name', String(100)),
             Column('email', String(100), nullable=False),
             Column('address', String(100), nullable=False)
             )

# , DateTime(), default=datetime.now, onupdate=datetime.now)
'''
ins = user.insert().values(
    username='dchekel',
    password='1234567890',
    first_name='Dmitry',
    last_name='Chekel',
    email='dchekel@mail.com',
    address='Grodno, Boldina 400, appt. 400'
    )
r = connection.execute(ins)
'''
s = select([user])
r = connection.execute(s)
print(s)
print(r.fetchall())

# Base = declarative_base()
# Session = sessionmaker()
