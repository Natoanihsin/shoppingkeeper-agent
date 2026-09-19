from typing import Any

from app.db.meta_connection import run_meta_sql


def get_all_tables() -> list[dict[str, Any]]:
    sql = """
        SELECT
            id,
            name,
            role,
            description
        FROM table_info
        ORDER BY name
    """
    return run_meta_sql(sql)


def get_all_columns() -> list[dict[str, Any]]:
    sql = """
        SELECT
            c.id,
            c.name,
            c.type,
            c.role,
            c.examples,
            c.description,
            c.alias,
            c.table_id,
            t.name AS table_name
        FROM column_info AS c
        JOIN table_info AS t ON c.table_id = t.id
        ORDER BY t.name, c.name
    """
    return run_meta_sql(sql)


def get_all_metrics() -> list[dict[str, Any]]:
    sql = """
        SELECT
            id,
            name,
            description,
            relevant_columns,
            alias
        FROM metric_info
        ORDER BY name
    """
    return run_meta_sql(sql)