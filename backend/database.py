from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from config import settings


def _build_engine():
    url = settings.DATABASE_URL

    connect_args = {}

    if url.startswith("sqlite"):
        connect_args["check_same_thread"] = False

    if url.startswith("postgresql") and "sslmode" not in url:
        separator = "&" if "?" in url else "?"
        url = f"{url}{separator}sslmode=require"

    kwargs = dict(
        connect_args=connect_args,
        pool_pre_ping=True,
    )

    if url.startswith("postgresql"):
        kwargs.update(
            pool_recycle=300,
            pool_size=5,
            max_overflow=10,
        )

    engine = create_engine(url, **kwargs)

    if url.startswith("sqlite"):
        from sqlalchemy import event, text

        @event.listens_for(engine, "connect")
        def set_sqlite_pragmas(dbapi_conn, _):
            cursor = dbapi_conn.cursor()
            cursor.execute("PRAGMA journal_mode=WAL")
            cursor.execute("PRAGMA busy_timeout=30000")
            cursor.close()

    return engine


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
    _migrate_missing_columns()


def _migrate_missing_columns():
    from sqlalchemy import inspect, text

    inspector = inspect(engine)
    with engine.begin() as conn:
        for table_name, table in Base.metadata.tables.items():
            if not inspector.has_table(table_name):
                continue

            existing_cols = {c["name"] for c in inspector.get_columns(table_name)}

            for col in table.columns:
                if col.name in existing_cols:
                    continue

                col_type = col.type.compile(dialect=engine.dialect)
                nullable = "NULL" if col.nullable else "NOT NULL"
                default = ""
                if col.default is not None and col.default.arg is not None:
                    val = col.default.arg
                    if callable(val):
                        default = ""  
                    elif isinstance(val, str):
                        default = f"DEFAULT '{val}'"
                    elif isinstance(val, bool):
                        default = f"DEFAULT {'TRUE' if val else 'FALSE'}"
                    elif isinstance(val, (int, float)):
                        default = f"DEFAULT {val}"

                sql = (
                    f'ALTER TABLE "{table_name}" '
                    f'ADD COLUMN "{col.name}" {col_type} {nullable} {default}'
                )
                print(f"[Migration] {sql.strip()}")
                conn.execute(text(sql))
