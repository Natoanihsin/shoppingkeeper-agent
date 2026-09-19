from collections import defaultdict
from typing import Any

from app.repositories.meta_repository import (
    get_all_columns,
    get_all_tables,
)
from app.repositories.qdrant.metadata_vector_repository import (
    search_columns,
    search_metrics,
)


def retrieve_vector_schema_context(
    keywords: list[str],
) -> tuple[list[str], str]:
    query_text = " ".join(keywords).strip()

    if not query_text:
        raise ValueError("Keywords cannot be empty")

    column_results = search_columns(query_text, limit=8)
    metric_results = search_metrics(query_text, limit=3)

    table_scores: dict[str, float] = {}

    for result in column_results:
        table_name = result["table_name"]
        score = result["score"]
        table_scores[table_name] = max(
            score,
            table_scores.get(table_name, 0.0),
        )

    ranked_dimension_tables = [
        table_name
        for table_name, _ in sorted(
            table_scores.items(),
            key=lambda item: item[1],
            reverse=True,
        )
        if table_name != "fact_order"
    ][:2]

    selected_table_names = [
        "fact_order",
        *ranked_dimension_tables,
    ]

    tables = get_all_tables()
    columns = get_all_columns()

    table_by_name = {
        table["name"]: table
        for table in tables
    }

    columns_by_table: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for column in columns:
        columns_by_table[column["table_id"]].append(column)

    lines: list[str] = []

    for table_name in selected_table_names:
        table = table_by_name.get(table_name)

        if table is None:
            continue

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

    for metric in metric_results:
        lines.append(
            f"- {metric['name']}: "
            f"{metric['description']}"
        )

    return selected_table_names, "\n".join(lines)