from app.agent.state import QueryState
from app.services.meta_knowledge_service import build_schema_context
from app.services.meta_retrieval_service import retrieve_schema_context
from app.services.vector_retrieval_service import (
    retrieve_vector_schema_context,
)


def retrieve_metadata(state: QueryState) -> QueryState:
    if state.intent != "data_query":
        return state

    if not state.keywords:
        state.schema_context = build_schema_context()
        state.retrieval_mode = "full_metadata"
        return state

    try:
        retrieved_tables, schema_context = (
            retrieve_vector_schema_context(state.keywords)
        )
        state.retrieval_mode = "vector"
    except Exception:
        retrieved_tables, schema_context = retrieve_schema_context(
            state.keywords
        )
        state.retrieval_mode = "lexical_fallback"

    def add_value_context(
            schema_context: str,
            state: QueryState,
    ) -> str:
        if not state.retrieved_values:
            return schema_context

        lines = ["Known field values:"]

        for item in state.retrieved_values:
            lines.append(
                f"- {item['table_name']}.{item['column_name']} "
                f"= {item['value']}"
            )

        return f"{schema_context}\n\n" + "\n".join(lines)

    state.retrieved_tables = retrieved_tables
    state.schema_context = add_value_context(
        schema_context,
        state,
    )

    return state