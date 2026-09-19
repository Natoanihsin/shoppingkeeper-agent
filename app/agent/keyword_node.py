from app.agent.llm import llm
from app.agent.state import QueryState
from app.prompt.prompt_loader import load_prompt


def extract_keywords(state: QueryState) -> QueryState:
    if state.intent == "total_sales":
        state.keywords = [
            "total sales",
            "order amount",
        ]
        return state

    if state.intent == "order_count":
        state.keywords = [
            "order count",
            "order id",
        ]
        return state

    if state.intent != "data_query":
        state.keywords = []
        return state

    prompt_template = load_prompt("extract_keywords.prompt")
    prompt = prompt_template.format(question=state.question)

    response = llm.invoke(prompt)
    raw_content = str(response.content)

    normalized_content = raw_content.replace("\n", ",")

    state.keywords = [
        keyword.strip().lower()
        for keyword in normalized_content.split(",")
        if keyword.strip()
    ][:8]

    return state