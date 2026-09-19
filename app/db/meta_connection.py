from typing import Any

from sqlalchemy import Engine, create_engine, text

from app.core.config import get_settings

settings = get_settings()

meta_engine: Engine = create_engine(
    settings.mysql_meta_url,
    pool_pre_ping=True,
    pool_recycle=3600,
    connect_args={
        "connect_timeout": settings.query_timeout_seconds,
        "read_timeout": settings.query_timeout_seconds,
        "write_timeout": settings.query_timeout_seconds,
    },
)


def run_meta_sql(
    sql: str,
    parameters: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    with meta_engine.connect() as connection:
        result = connection.execute(
            text(sql),
            parameters or {},
        )
        return [dict(row._mapping) for row in result]