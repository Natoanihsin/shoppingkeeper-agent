from elasticsearch import Elasticsearch

from app.core.config import get_settings

settings = get_settings()

elasticsearch_client = Elasticsearch(
    settings.elasticsearch_url,
)