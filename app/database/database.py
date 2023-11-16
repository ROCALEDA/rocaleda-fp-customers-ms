import os
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = os.getenv(
    "DB_URL", "postgresql://postgres:mock@10.10.10.10:5432/customers"
)
if "mock" not in SQLALCHEMY_DATABASE_URL:
    print("WARNING: Database connection not retrieved, using mock string")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


@contextmanager
def create_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
