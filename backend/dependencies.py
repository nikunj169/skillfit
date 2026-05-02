from collections.abc import Generator

from sqlalchemy.orm import Session

from backend.config import get_settings
from backend.db.session import SessionLocal


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_app_settings():
    return get_settings()
