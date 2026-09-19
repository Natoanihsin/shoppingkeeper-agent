from qdrant_client.models import Distance, VectorParams

from app.clients.qdrant_client import qdrant_client
from app.core.config import get_settings

settings = get_settings()


def ensure_collection(collection_name: str) -> None:
    if qdrant_client.collection_exists(collection_name):
        print(f"Collection already exists: {collection_name}")
        return

    qdrant_client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=settings.embedding_dimension,
            distance=Distance.COSINE,
        ),
    )

    print(f"Collection created: {collection_name}")


def main() -> None:
    ensure_collection(settings.qdrant_column_collection)
    ensure_collection(settings.qdrant_metric_collection)


if __name__ == "__main__":
    main()