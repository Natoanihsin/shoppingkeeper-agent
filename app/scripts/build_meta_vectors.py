from uuid import NAMESPACE_URL, uuid5

from qdrant_client.models import PointStruct

from app.clients.embedding_client import embedding_client
from app.clients.qdrant_client import qdrant_client
from app.core.config import get_settings
from app.repositories.meta_repository import (
    get_all_columns,
    get_all_metrics,
)

settings = get_settings()


def build_column_text(column: dict) -> str:
    return (
        f"Table: {column['table_name']}. "
        f"Column: {column['name']}. "
        f"Type: {column['type']}. "
        f"Role: {column['role']}. "
        f"Description: {column['description']}. "
        f"Aliases: {column['alias']}."
    )


def build_metric_text(metric: dict) -> str:
    return (
        f"Metric: {metric['name']}. "
        f"Description: {metric['description']}. "
        f"Aliases: {metric['alias']}. "
        f"Relevant columns: {metric['relevant_columns']}."
    )


def index_columns() -> int:
    columns = get_all_columns()
    texts = [build_column_text(column) for column in columns]
    vectors = embedding_client.embed_documents(texts)

    points = [
        PointStruct(
            id=str(uuid5(NAMESPACE_URL, f"column:{column['id']}")),
            vector=vector,
            payload={
                "metadata_id": column["id"],
                "name": column["name"],
                "table_id": column["table_id"],
                "table_name": column["table_name"],
                "type": column["type"],
                "role": column["role"],
                "description": column["description"],
                "alias": column["alias"],
                "text": text,
            },
        )
        for column, text, vector in zip(columns, texts, vectors)
    ]

    qdrant_client.upsert(
        collection_name=settings.qdrant_column_collection,
        points=points,
        wait=True,
    )

    return len(points)


def index_metrics() -> int:
    metrics = get_all_metrics()
    texts = [build_metric_text(metric) for metric in metrics]
    vectors = embedding_client.embed_documents(texts)

    points = [
        PointStruct(
            id=str(uuid5(NAMESPACE_URL, f"metric:{metric['id']}")),
            vector=vector,
            payload={
                "metadata_id": metric["id"],
                "name": metric["name"],
                "description": metric["description"],
                "relevant_columns": metric["relevant_columns"],
                "alias": metric["alias"],
                "text": text,
            },
        )
        for metric, text, vector in zip(metrics, texts, vectors)
    ]

    qdrant_client.upsert(
        collection_name=settings.qdrant_metric_collection,
        points=points,
        wait=True,
    )

    return len(points)


def main() -> None:
    column_count = index_columns()
    metric_count = index_metrics()

    print(f"Indexed columns: {column_count}")
    print(f"Indexed metrics: {metric_count}")


if __name__ == "__main__":
    main()