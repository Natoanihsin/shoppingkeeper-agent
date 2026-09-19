import json

from app.agent.llm import llm
from app.agent.state import QueryState
from app.prompt.prompt_loader import load_prompt


def generate_answer(state: QueryState) -> QueryState:
    if state.error is not None:
        state.answer = (
            "SQL validation failed after "
            f"{state.validation_attempts} attempts: "
            f"{state.error}"
        )
        return state

    if state.intent == "unknown":
        state.answer = "暂时无法理解这个问题。"
        return state

    if not state.data:
        state.answer = "没有查询到符合条件的数据。"
        return state

    region_name = state.parameters.get("region_name")

    if state.intent == "total_sales":
        total_sales = state.data[0]["total_sales"]

        if total_sales is None:
            state.answer = "没有查询到符合条件的销售数据。"
            return state

        total_sales = float(total_sales)

        if region_name:
            state.answer = f"{region_name}地区销售额是 {total_sales:.2f} 元。"
        else:
            state.answer = f"总销售额是 {total_sales:.2f} 元。"

        return state

    if state.intent == "order_count":
        order_count = state.data[0]["order_count"]

        if region_name:
            state.answer = f"{region_name}地区订单数量是 {order_count} 单。"
        else:
            state.answer = f"订单数量是 {order_count} 单。"

        return state

    if state.intent == "data_query":
        prompt_template = load_prompt("generate_answer.prompt")

        data_text = json.dumps(
            state.data,
            ensure_ascii=False,
            default=str,
            indent=2,
        )

        prompt = prompt_template.format(
            question=state.question,
            data=data_text,
        )

        response = llm.invoke(prompt)
        state.answer = str(response.content).strip()
        return state

    state.answer = "查询已经完成，但暂时无法生成回答。"
    return state