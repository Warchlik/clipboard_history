from __future__ import annotations

from typing import Generator, Optional
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session


def default_db_path() -> Path:
    base = Path().resolve()
    base.mkdir(parents=True, exist_ok=True)
    return base / "database.sqlite3"


def make_sqlite_url(db_path: Optional[Path] = None) -> str:
    path = db_path or default_db_path()
    return f"sqlite:///{path}"


def make_engine(db_path: Optional[Path] = None):
    return create_engine(make_sqlite_url(db_path), future=True)


def make_session_local(engine):
    return sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
        future=True,
    )


class Base(DeclarativeBase):
    pass


engine = make_engine()
SessionLocal = make_session_local(engine)


def init_database():
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
