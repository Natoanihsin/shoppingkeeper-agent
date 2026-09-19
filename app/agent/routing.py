from typing import Literal

from app.agent.state import QueryState
from app.core.config import get_settings

settings = get_settings()


def route_after_validation(
    state: QueryState,
) -> Literal["execute_sql", "correct_sql", "generate_answer"]:
    if state.error is None:
        return "execute_sql"

    if (
        state.validation_attempts
        < settings.max_sql_validation_attempts
    ):
        return "correct_sql"

    return "generate_answer"