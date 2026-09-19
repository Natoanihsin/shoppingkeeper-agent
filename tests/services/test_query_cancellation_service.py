from app.services.query_cancellation_service import (
    QueryCancellationService,
)


def test_rejects_unknown_request_id() -> None:
    service = QueryCancellationService()

    assert service.cancel("unknown-request") is False


def test_marks_active_request_as_cancelled() -> None:
    service = QueryCancellationService()
    request_id = "active-request"

    service.start(request_id)

    assert service.cancel(request_id) is True
    assert service.is_cancelled(request_id) is True


def test_finish_clears_request_state() -> None:
    service = QueryCancellationService()
    request_id = "finished-request"

    service.start(request_id)
    service.cancel(request_id)
    service.finish(request_id)

    assert service.is_cancelled(request_id) is False
    assert service.cancel(request_id) is False