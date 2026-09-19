from app.agent.llm import llm
from app.agent.state import QueryState
from app.prompt.prompt_loader import load_prompt
from app.services.meta_knowledge_service import build_schema_context


def clean_model_sql(content: str) -> str:
    sql = content.strip()

    if sql.startswith("```"):
        lines = sql.splitlines()

        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        sql = "\n".join(lines).strip()

    return sql


def generate_sql(state: QueryState) -> QueryState:
    region_name = state.parameters.get("region_name")

    if state.intent == "total_sales":
        if region_name:
            state.sql = """
                SELECT SUM(f.order_amount) AS total_sales
                FROM fact_order AS f
                JOIN dim_region AS r ON f.region_id = r.region_id
                WHERE r.region_name = :region_name
            """
        else:
            state.sql = """
                SELECT SUM(order_amount) AS total_sales
                FROM fact_order
            """
        return state

    if state.intent == "order_count":
        if region_name:
            state.sql = """
                SELECT COUNT(*) AS order_count
                FROM fact_order AS f
                JOIN dim_region AS r ON f.region_id = r.region_id
                WHERE r.region_name = :region_name
            """
        else:
            state.sql = """
                SELECT COUNT(*) AS order_count
                FROM fact_order
            """
        return state

    if state.intent == "data_query":
        prompt_template = load_prompt("generate_sql.prompt")
        schema_context = (
                state.schema_context
                or build_schema_context()
        )

        prompt = prompt_template.format(
            question=state.question,
            schema_context=schema_context,
        )

        response = llm.invoke(prompt)
        state.sql = clean_model_sql(str(response.content))
        return state

    state.sql = None
    return state