from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os
from typing import Generator

# PostgreSQL database URL
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://mvp_user:mvp_password@localhost:5432/mvp_db"
)

# Create engine (PostgreSQL pool settings; SQLite for tests)
_engine_kwargs = {
    "pool_pre_ping": True,
    "pool_size": 10,
    "max_overflow": 20,
    "echo": False,
}
_connect_args = {}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    _engine_kwargs = {"echo": False}
    _connect_args = {"check_same_thread": False}

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args=_connect_args,
    **_engine_kwargs,
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency to get database session
def get_db() -> Generator[Session, None, None]:
    """Database session dependency for FastAPI"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
