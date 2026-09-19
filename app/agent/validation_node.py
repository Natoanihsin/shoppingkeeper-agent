from app.agent.state import QueryState
from app.db.connection import explain_sql
from app.security.sql_guard import (
    SQLValidationError,
    validate_read_only_sql,
)


def validate_sql(state: QueryState) -> QueryState:
    if state.sql is None:
        return state

    state.validation_attempts += 1

    try:
        safe_sql = validate_read_only_sql(state.sql)

        explain_sql(
            safe_sql,
            state.parameters,
        )

        state.sql = safe_sql
        state.error = None
    except SQLValidationError as exc:
        state.error = f"SQL safety validation failed: {exc}"
    except Exception as exc:
        state.error = f"Database validation failed: {exc}"

    return state