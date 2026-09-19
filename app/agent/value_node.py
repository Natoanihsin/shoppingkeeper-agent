from app.agent.llm import llm
from app.agent.state import QueryState
from app.prompt.prompt_loader import load_prompt
from app.repositories.elasticsearch.value_repository import (
    search_values,
)


def parse_value_candidates(content: str) -> list[str]:
    normalized_content = content.replace("\n", ",").strip()

    if normalized_content.upper() == "NONE":
        return []

    return [
        value.strip()
        for value in normalized_content.split(",")
        if value.strip()
    ][:8]


def recall_values(state: QueryState) -> QueryState:
    if state.intent == "unknown":
        return state

    prompt_template = load_prompt("extract_values.prompt")
    prompt = prompt_template.format(question=state.question)

    response = llm.invoke(prompt)
    state.value_candidates = parse_value_candidates(
        str(response.content)
    )

    retrieved_values: list[dict] = []
    seen_values: set[tuple[str, str, str]] = set()

    for candidate in state.value_candidates:
        results = search_values(candidate, limit=3)

        exact_results = [
            result
            for result in results
            if str(result["value"]).lower() == candidate.lower()
        ]

        selected_results = exact_results or results[:1]

        for result in selected_results:
            result_key = (
                result["table_name"],
                result["column_name"],
                str(result["value"]),
            )

            if result_key in seen_values:
                continue

            seen_values.add(result_key)
            retrieved_values.append(result)

    state.retrieved_values = retrieved_values


    if (
        state.retrieved_values
        and state.intent in {"total_sales", "order_count"}
    ):
        state.intent = "data_query"
    return state