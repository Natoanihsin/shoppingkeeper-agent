from uuid import UUID

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_generates_request_id() -> None:
    response = client.get("/health")

    assert response.status_code == 200

    request_id = response.headers["X-Request-ID"]
    UUID(request_id)


def test_preserves_client_request_id() -> None:
    request_id = "test-request-123"

    response = client.get(
        "/health",
        headers={
            "X-Request-ID": request_id,
        },
    )

    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == request_id