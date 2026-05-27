import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

if os.getenv("DATABASE_URL"):
    POSTGRES_DATABASE_URL = os.getenv("DATABASE_URL")
else:
    raise ValueError("DATABASE_URL not set")

engine = create_engine(POSTGRES_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
