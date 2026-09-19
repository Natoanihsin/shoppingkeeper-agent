from app.clients.elasticsearch_client import elasticsearch_client
from app.core.config import get_settings

settings = get_settings()


def create_value_index() -> None:
    index_name = settings.elasticsearch_value_index

    if elasticsearch_client.indices.exists(index=index_name):
        print(f"Index already exists: {index_name}")
        return

    elasticsearch_client.indices.create(
        index=index_name,
        mappings={
            "properties": {
                "value": {
                    "type": "text",
                    "analyzer": "standard",
                    "fields": {
                        "keyword": {
                            "type": "keyword"
                        }
                    },
                },
                "table_name": {
                    "type": "keyword"
                },
                "column_name": {
                    "type": "keyword"
                },
                "metadata_id": {
                    "type": "keyword"
                },
            }
        },
    )

    print(f"Index created: {index_name}")


if __name__ == "__main__":
    create_value_index()