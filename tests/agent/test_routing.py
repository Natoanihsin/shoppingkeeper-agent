from app.agent.routing import route_after_validation
from app.agent.state import QueryState
from app.core.config import get_settings

settings = get_settings()


def test_routes_valid_sql_to_execution() -> None:
    state = QueryState(
        question="test",
        error=None,
        validation_attempts=1,
    )

    assert route_after_validation(state) == "execute_sql"


def test_routes_failed_sql_to_correction() -> None:
    state = QueryState(
        question="test",
        error="invalid sql",
        validation_attempts=1,
    )

    assert route_after_validation(state) == "correct_sql"


def test_routes_exhausted_sql_to_answer() -> None:
    state = QueryState(
        question="test",
        error="invalid sql",
        validation_attempts=settings.max_sql_validation_attempts,
    )

    assert route_after_validation(state) == "generate_answer"
