from collections import defaultdict
from typing import Any

from app.repositories.meta_repository import (
    get_all_columns,
    get_all_metrics,
    get_all_tables,
)


def build_schema_context() -> str:
    tables = get_all_tables()
    columns = get_all_columns()
    metrics = get_all_metrics()

    columns_by_table: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for column in columns:
        columns_by_table[column["table_id"]].append(column)

    lines: list[str] = []

    for table in tables:
        lines.append(
            f"Table {table['name']} "
            f"({table['role']}): "
            f"{table['description']}"
        )

        for column in columns_by_table[table["id"]]:
            lines.append(
                f"- {column['name']} "
                f"[{column['type']}, {column['role']}]: "
                f"{column['description']}"
            )

        lines.append("")

    lines.append("Business metrics:")

    for metric in metrics:
        lines.append(
            f"- {metric['name']}: "
            f"{metric['description']}"
        )

    return "\n".join(lines)
