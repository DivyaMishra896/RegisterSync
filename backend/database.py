from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from config import settings


def _build_engine():
    url = settings.DATABASE_URL

    connect_args = {}

    # SQLite threading
    if url.startswith("sqlite"):
        connect_args["check_same_thread"] = False

    # Neon SSL
    if url.startswith("postgresql") and "sslmode" not in url:
        separator = "&" if "?" in url else "?"
        url = f"{url}{separator}sslmode=require"

    return create_engine(
        url,
        connect_args=connect_args,
        pool_pre_ping=True,  # Reconnect
    )


engine = _build_engine()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)
