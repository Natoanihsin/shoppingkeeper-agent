from typing import Any

from pydantic import BaseModel, Field


class QueryState(BaseModel):
    question: str
    keywords: list[str] = Field(default_factory=list)
    value_candidates: list[str] = Field(default_factory=list)
    retrieved_values: list[dict[str, Any]] = Field(default_factory=list)
    retrieved_tables: list[str] = Field(default_factory=list)
    schema_context: str = ""
    retrieval_mode: str = "none"
    intent: str = "unknown"
    parameters: dict[str, Any] = Field(default_factory=dict)
    sql: str | None = None
    data: list[dict[str, Any]] = Field(default_factory=list)
    answer: str | None = None
    validation_attempts: int = 0
    error: str | None = None
