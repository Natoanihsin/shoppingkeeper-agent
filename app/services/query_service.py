from collections.abc import Iterator
from typing import Any

from app.agent.state import QueryState
from app.agent.workflow import run_agent, stream_agent
from app.services.query_cancellation_service import (
    query_cancellation_service,
)


def answer_question(question: str) -> QueryState:
    return run_agent(question)


def stream_answer(
    question: str,
    request_id: str | None = None,
) -> Iterator[dict[str, Any]]:
    if request_id is None:
        return stream_agent(question)

    return stream_agent(
        question,
        is_cancelled=lambda: (
            query_cancellation_service.is_cancelled(
                request_id,
            )
        ),
    )