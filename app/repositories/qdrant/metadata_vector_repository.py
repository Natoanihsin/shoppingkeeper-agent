from typing import Any

from app.clients.embedding_client import embedding_client
from app.clients.qdrant_client import qdrant_client
from app.core.config import get_settings

settings = get_settings()


def format_results(points: list[Any]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []

    for point in points:
        result = dict(point.payload or {})
        result["score"] = float(point.score)
        results.append(result)

    return results


def search_columns(
    query_text: str,
    limit: int = 8,
) -> list[dict[str, Any]]:
    query_vector = embedding_client.embed_query(query_text)

    response = qdrant_client.query_points(
        collection_name=settings.qdrant_column_collection,
        query=query_vector,
        limit=limit,
        with_payload=True,
    )

    return format_results(response.points)


def search_metrics(
    query_text: str,
    limit: int = 4,
) -> list[dict[str, Any]]:
    query_vector = embedding_client.embed_query(query_text)

    response = qdrant_client.query_points(
        collection_name=settings.qdrant_metric_collection,
        query=query_vector,
        limit=limit,
        with_payload=True,
    )

    return format_results(response.points)