from collections import defaultdict
from typing import Any

from app.repositories.meta_repository import (
    get_all_columns,
    get_all_metrics,
    get_all_tables,
)


def normalize_text(value: Any) -> str:
    return str(value).lower().replace("_", " ")


def calculate_score(
    searchable_text: str,
    keywords: list[str],
) -> int:
    normalized_text = normalize_text(searchable_text)

    return sum(
        1
        for keyword in keywords
        if normalize_text(keyword) in normalized_text
    )


def retrieve_schema_context(
    keywords: list[str],
) -> tuple[list[str], str]:
    tables = get_all_tables()
    columns = get_all_columns()
    metrics = get_all_metrics()

    columns_by_table: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for column in columns:
        columns_by_table[column["table_id"]].append(column)

    selected_tables: list[dict[str, Any]] = []

    for table in tables:
        table_columns = columns_by_table[table["id"]]

        searchable_parts = [
            table["name"],
            table["role"],
            table["description"],
        ]

        for column in table_columns:
            searchable_parts.extend(
                [
                    column["name"],
                    column["role"],
                    column["description"],
                    column["alias"],
                ]
            )

        score = calculate_score(
            " ".join(str(part) for part in searchable_parts),
            keywords,
        )

        if score > 0:
            selected_tables.append(table)

    fact_table = next(
        table
        for table in tables
        if table["name"] == "fact_order"
    )

    if fact_table not in selected_tables:
        selected_tables.insert(0, fact_table)

    if len(selected_tables) == 1 and not keywords:
        selected_tables = tables

    selected_table_names = [
        table["name"]
        for table in selected_tables
    ]

    lines: list[str] = []

    for table in selected_tables:
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

    return selected_table_names, "\n".join(lines)