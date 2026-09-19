from collections.abc import Generator
from typing import Any

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings

settings = get_settings()

engine: Engine = create_engine(
    settings.mysql_url,
    pool_pre_ping=True,
    pool_recycle=3600,
    connect_args={
        "connect_timeout": settings.query_timeout_seconds,
        "read_timeout": settings.query_timeout_seconds,
        "write_timeout": settings.query_timeout_seconds,
    },
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


def get_db_session() -> Generator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def run_sql(
    sql: str,
    parameters: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    with engine.connect() as connection:
        result = connection.execute(
            text(sql),
            parameters or {},
        )
        return [dict(row._mapping) for row in result]

def explain_sql(
    sql: str,
    parameters: dict[str, Any] | None = None,
) -> None:
    explain_statement = f"EXPLAIN {sql}"

    with engine.connect() as connection:
        connection.execute(
            text(explain_statement),
            parameters or {},
        )