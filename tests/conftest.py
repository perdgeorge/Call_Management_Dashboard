from typing import Generator
import os
import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.engine import Engine
from main import app as fastapi_app
from src.core.database import get_db, Base
from src.models.call import Call
from tests.factories import make_call_payload

load_dotenv()


@pytest.fixture(scope="session")
def engine():
    database_url = os.getenv("DATABASE_URL")
    engine = create_engine(database_url, pool_pre_ping=True)
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture(scope="session")
def session_factory(engine: Engine):
    return sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        class_=Session,
    )


@pytest.fixture
def db_session(session_factory):
    """Create a new database session for each test"""
    session = session_factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


@pytest.fixture
def client(db_session: Session) -> Generator[TestClient, None, None]:

    def override_get_db():
        yield db_session

    fastapi_app.dependency_overrides[get_db] = override_get_db
    with TestClient(fastapi_app) as test_client:
        yield test_client
    fastapi_app.dependency_overrides.clear()


@pytest.fixture()
def call(db_session: Session):
    payload = make_call_payload()
    row = Call(
        direction=payload.direction,
        from_number=payload.from_number,
        to_number=payload.to_number,
        call_type=payload.call_type,
        duration=payload.duration,
        is_archived=payload.is_archived,
    )

    db_session.add(row)
    db_session.commit()
    db_session.refresh(row)
    return row


@pytest.fixture()
def call_factory(db_session: Session):

    def _create(**overrides):
        payload = make_call_payload()
        row = Call(
            direction=payload.direction,
            from_number=payload.from_number,
            to_number=payload.to_number,
            call_type=payload.call_type,
            duration=payload.duration,
            is_archived=payload.is_archived,
        )
        db_session.add(row)
        db_session.commit()
        db_session.refresh(row)
        return row

    return _create
