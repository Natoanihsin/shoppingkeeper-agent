from collections.abc import Iterator

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field, field_validator

from app.agent.state import QueryState
from app.api.sse import encode_sse
from app.core.context import get_request_id
from app.core.log import logger
from app.services.query_cancellation_service import (
    query_cancellation_service,
)
from app.services.query_service import (
    answer_question,
    stream_answer,
)

router = APIRouter(prefix="/query", tags=["query"])


class QueryRequest(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=500,
        examples=["Which brand has the highest sales amount?"],
    )

    @field_validator("question")
    @classmethod
    def validate_question(cls, value: str) -> str:
        normalized_value = value.strip()

        if not normalized_value:
            raise ValueError("Question cannot be blank")

        return normalized_value


class QueryCancellationResponse(BaseModel):
    request_id: str
    cancelled: bool


@router.post("")
def query(request: QueryRequest) -> QueryState:
    return answer_question(request.question)


@router.post(
    "/cancel/{request_id}",
    response_model=QueryCancellationResponse,
)
def cancel_query(
    request_id: str,
) -> QueryCancellationResponse:
    cancelled = query_cancellation_service.cancel(
        request_id,
    )

    logger.info(
        "Query cancellation requested "
        "target_request_id=%s cancelled=%s",
        request_id,
        cancelled,
    )

    return QueryCancellationResponse(
        request_id=request_id,
        cancelled=cancelled,
    )


@router.post("/stream")
def query_stream(
    request: QueryRequest,
) -> StreamingResponse:
    request_id = get_request_id()

    query_cancellation_service.start(request_id)

    def event_generator() -> Iterator[str]:
        try:
            for item in stream_answer(
                request.question,
                request_id,
            ):
                event_type = str(item["type"])
                payload = {
                    key: value
                    for key, value in item.items()
                    if key != "type"
                }
                payload["request_id"] = request_id

                yield encode_sse(
                    event_type,
                    payload,
                )
        except Exception:
            logger.exception(
                "Streaming query failed request_id=%s",
                request_id,
            )

            yield encode_sse(
                "error",
                {
                    "message": "查询执行失败，请稍后重试。",
                    "request_id": request_id,
                },
            )
        finally:
            query_cancellation_service.finish(
                request_id,
            )

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )