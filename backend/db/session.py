from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.config import get_settings

settings = get_settings()

engine_kwargs = {}
if settings.database_url.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(settings.database_url, future=True, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
