from app.agent.state import QueryState
from app.db.connection import run_sql


def execute_sql(state: QueryState) -> QueryState:
    if state.sql is None:
        return state

    if state.error is not None:
        return state

    state.data = run_sql(
        state.sql,
        state.parameters,
    )
    return state