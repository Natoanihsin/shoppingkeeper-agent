from app.agent.llm import llm
from app.agent.sql_node import clean_model_sql
from app.agent.state import QueryState
from app.prompt.prompt_loader import load_prompt


def correct_sql(state: QueryState) -> QueryState:
    if state.sql is None or state.error is None:
        return state

    prompt_template = load_prompt("correct_sql.prompt")

    prompt = prompt_template.format(
        schema_context=state.schema_context,
        question=state.question,
        sql=state.sql,
        error=state.error,
    )

    response = llm.invoke(prompt)

    state.sql = clean_model_sql(
        str(response.content)
    )
    state.error = None

    return state