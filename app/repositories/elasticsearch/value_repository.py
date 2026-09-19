from typing import Any

from app.clients.elasticsearch_client import elasticsearch_client
from app.core.config import get_settings

settings = get_settings()


def search_values(
    query_text: str,
    limit: int = 5,
) -> list[dict[str, Any]]:
    response = elasticsearch_client.search(
        index=settings.elasticsearch_value_index,
        size=limit,
        query={
            "bool": {
                "should": [
                    {
                        "term": {
                            "value.keyword": {
                                "value": query_text,
                                "boost": 5.0,
                            }
                        }
                    },
                    {
                        "match": {
                            "value": {
                                "query": query_text,
                                "boost": 2.0,
                            }
                        }
                    },
                    {
                        "wildcard": {
                            "value.keyword": {
                                "value": f"*{query_text}*",
                                "boost": 1.0,
                            }
                        }
                    },
                ],
                "minimum_should_match": 1,
            }
        },
    )

    results: list[dict[str, Any]] = []

    for hit in response["hits"]["hits"]:
        result = dict(hit["_source"])
        result["score"] = float(hit["_score"])
        results.append(result)

    return results