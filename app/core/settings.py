import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

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
