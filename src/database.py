from __future__ import annotations

from typing import Generator, Optional
from pathlib import Path

from platformdirs import user_data_dir
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

APP_NAME = "cliphist"


def default_db_path() -> Path:
    base = Path(user_data_dir(APP_NAME, APP_NAME))
    base.mkdir(parents=True, exist_ok=True)
    return base / "cliphist.sqlite3"


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


engine = make_engine()
SessionLocal = make_session_local(engine)


def db() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
