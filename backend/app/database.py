from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os
from typing import Generator

# PostgreSQL database URL
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://mvp_user:mvp_password@localhost:5432/mvp_db"
)

# Create engine with PostgreSQL optimizations
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before using
    pool_size=10,  # Connection pool size
    max_overflow=20,  # Max overflow connections
    echo=False  # Set to True for SQL query logging
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
