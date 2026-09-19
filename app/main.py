from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.orders import router as orders_router
from app.api.query import router as query_router
from app.core.config import get_settings
from app.core.context import request_id_context
from app.core.log import logger

settings = get_settings()

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID"],
)

app.include_router(orders_router)
app.include_router(query_router)

@app.middleware("http")
async def add_request_id(
    request: Request,
    call_next,
):
    request_id = request.headers.get(
        "X-Request-ID",
        str(uuid4()),
    )

    token = request_id_context.set(request_id)
    started_at = perf_counter()

    try:
        logger.info(
            "Request started: %s %s",
            request.method,
            request.url.path,
        )

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id

        duration_ms = (perf_counter() - started_at) * 1000

        logger.info(
            "Request completed: %s %s status=%s duration_ms=%.2f",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )

        return response
    except Exception:
        logger.exception(
            "Request failed: %s %s",
            request.method,
            request.url.path,
        )
        raise
    finally:
        request_id_context.reset(token)

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}