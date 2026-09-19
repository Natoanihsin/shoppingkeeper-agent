from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "shopkeeper-agent-learning"
    app_env: str = "local"

    mysql_host: str = "127.0.0.1"
    mysql_port: int = 3307
    mysql_user: str = "root"
    mysql_password: str = "root"
    mysql_database: str = "shopkeeper_dw"
    mysql_meta_database: str = "shopkeeper_meta"

    llm_model: str = "deepseek-flash"
    llm_api_key: str = ""
    llm_base_url: str = "https://api.deepseek.com"

    qdrant_url: str = "http://127.0.0.1:6335"
    qdrant_column_collection: str = "column_metadata"
    qdrant_metric_collection: str = "metric_metadata"

    embedding_model: str = "BAAI/bge-small-zh-v1.5"
    embedding_dimension: int = 512

    elasticsearch_url: str = "http://127.0.0.1:9200"
    elasticsearch_value_index: str = "field_values"

    max_sql_validation_attempts: int = 3

    query_timeout_seconds: int = 5

    frontend_origin: str = "http://localhost:5173"

    hf_cache_path: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    @property
    def mysql_url(self) -> str:
        return (
            f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"
            f"?charset=utf8mb4"
        )

    @property
    def mysql_meta_url(self) -> str:
        return (
            f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_meta_database}"
            f"?charset=utf8mb4"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()