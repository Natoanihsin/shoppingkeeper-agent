from threading import Lock


class QueryCancellationService:
    def __init__(self) -> None:
        self._active_request_ids: set[str] = set()
        self._cancelled_request_ids: set[str] = set()
        self._lock = Lock()

    def start(self, request_id: str) -> None:
        with self._lock:
            self._active_request_ids.add(request_id)
            self._cancelled_request_ids.discard(request_id)

    def cancel(self, request_id: str) -> bool:
        with self._lock:
            if request_id not in self._active_request_ids:
                return False

            self._cancelled_request_ids.add(request_id)
            return True

    def is_cancelled(self, request_id: str) -> bool:
        with self._lock:
            return request_id in self._cancelled_request_ids

    def finish(self, request_id: str) -> None:
        with self._lock:
            self._active_request_ids.discard(request_id)
            self._cancelled_request_ids.discard(request_id)


query_cancellation_service = QueryCancellationService()