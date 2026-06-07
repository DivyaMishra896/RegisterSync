"""
Suraksha — Database Setup
SQLAlchemy engine, session, and base model configuration.
Supports both NeonDB (PostgreSQL) and SQLite.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from config import settings


def _build_engine():
    """Build the SQLAlchemy engine with driver-appropriate settings."""
    url = settings.DATABASE_URL

    connect_args = {}

    # SQLite needs check_same_thread=False
    if url.startswith("sqlite"):
        connect_args["check_same_thread"] = False

    # NeonDB requires SSL; psycopg2 handles it via sslmode in the URL
    # If using psycopg2 and sslmode is not in the URL, add it
    if url.startswith("postgresql") and "sslmode" not in url:
        separator = "&" if "?" in url else "?"
        url = f"{url}{separator}sslmode=require"

    return create_engine(
        url,
        connect_args=connect_args,
        pool_pre_ping=True,  # reconnect stale connections (good for serverless Neon)
    )


engine = _build_engine()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """FastAPI dependency that provides a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all tables. Called on app startup."""
    Base.metadata.create_all(bind=engine)
