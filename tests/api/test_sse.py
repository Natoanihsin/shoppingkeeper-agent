from collections.abc import Iterator
from typing import Any

from fastapi.testclient import TestClient

from app.api.sse import encode_sse
from app.main import app

client = TestClient(app)


def test_encodes_sse_event() -> None:
    encoded = encode_sse(
        "progress",
        {
            "message": "Query completed",
        },
    )

    assert encoded == (
        'event: progress\n'
        'data: {"message": "Query completed"}\n\n'
    )


def test_streams_progress_and_result(
    monkeypatch: Any,
) -> None:
    def fake_stream_answer(
            question: str,
            request_id: str | None = None,
    ) -> Iterator[dict[str, Any]]:
        yield {
            "type": "progress",
            "node": "start",
            "message": "Query received",
        }
        yield {
            "type": "result",
            "state": {
                "question": question,
            },
        }

    monkeypatch.setattr(
        "app.api.query.stream_answer",
        fake_stream_answer,
    )

    response = client.post(
        "/query/stream",
        json={
            "question": "Total sales",
        },
        headers={
            "X-Request-ID": "sse-test-123",
        },
    )

    assert response.status_code == 200
    assert response.headers["content-type"].startswith(
        "text/event-stream"
    )
    assert "event: progress" in response.text
    assert "event: result" in response.text
    assert '"node": "start"' in response.text
    assert '"request_id": "sse-test-123"' in response.text


def test_streams_error_event(
    monkeypatch: Any,
) -> None:
    def failing_stream_answer(
            question: str,
            request_id: str | None = None,
    ) -> Iterator[dict[str, Any]]:
        raise RuntimeError(
            f"Failed to process: {question}"
        )
        yield {}

    monkeypatch.setattr(
        "app.api.query.stream_answer",
        failing_stream_answer,
    )

    response = client.post(
        "/query/stream",
        json={
            "question": "Total sales",
        },
    )

    assert response.status_code == 200
    assert "event: error" in response.text
    assert "查询执行失败，请稍后重试。" in response.text