from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import settings
from sqlalchemy.engine import URL
#SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'

# not a good way to hardcode this
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}'
# SQLALCHEMY_DATABASE_URL = URL.create(
#     drivername="postgresql+psycopg",
#     username=settings.db_user,
#     password=settings.db_password,
#     host=settings.db_host,
#     port=settings.db_port,
#     database=settings.db_name,
# )
engine = create_engine(SQLALCHEMY_DATABASE_URL) # engine is SQLAlchemy’s connection manager

# talk to sql we have to make use of session. A session is like a temporary conversation with the database: OPEN,EDIT,DELETE
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() # Base is the parent class for SQLAlchemy ORM models.


# Dependancy to get the session - gives a FastAPI endpoint a database session.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# FLOW IS
# Request arrives
#     ↓
# FastAPI creates a database session
#     ↓
# Endpoint uses the session
#     ↓
# Request finishes
#     ↓
# Session closes