import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy_utils import database_exists, create_database

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
print(SQLALCHEMY_DATABASE_URL)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"options": "-c timezone=utc"},
    pool_size=100, max_overflow=10
)

if not database_exists(engine.url):
    create_database(engine.url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def create_all_models():
    Base.metadata.create_all(bind=engine)
