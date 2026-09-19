from collections.abc import Callable, Iterator
from typing import Any

from app.agent.graph import graph
from app.agent.state import QueryState

NODE_PROGRESS_MESSAGES = {
    "detect_intent": "意图识别完成",
    "recall_values": "字段值召回完成",
    "extract_keywords": "关键词提取完成",
    "retrieve_metadata": "元数据检索完成",
    "extract_parameters": "查询参数提取完成",
    "generate_sql": "SQL 生成完成",
    "validate_sql": "SQL 校验完成",
    "correct_sql": "SQL 修正完成",
    "execute_sql": "数据查询完成",
    "generate_answer": "回答生成完成",
}


def run_agent(question: str) -> QueryState:
    initial_state = QueryState(question=question)

    result = graph.invoke(initial_state)

    return QueryState.model_validate(result)


def stream_agent(
    question: str,
    is_cancelled: Callable[[], bool] | None = None,
) -> Iterator[dict[str, Any]]:
    initial_state = QueryState(question=question)
    latest_state = initial_state

    yield {
        "type": "progress",
        "node": "start",
        "message": "已接收查询问题",
    }

    updates = iter(
        graph.stream(
            initial_state,
            stream_mode="updates",
        )
    )

    try:
        while True:
            if is_cancelled and is_cancelled():
                yield {
                    "type": "cancelled",
                    "message": "查询已取消。",
                }
                return

            try:
                update = next(updates)
            except StopIteration:
                break

            if is_cancelled and is_cancelled():
                yield {
                    "type": "cancelled",
                    "message": "查询已取消。",
                }
                return

            for node_name, state_update in update.items():
                if state_update is None:
                    continue

                latest_state = QueryState.model_validate(
                    state_update,
                )

                yield {
                    "type": "progress",
                    "node": node_name,
                    "message": NODE_PROGRESS_MESSAGES.get(
                        node_name,
                        f"{node_name} 执行完成",
                    ),
                }
    finally:
        close = getattr(updates, "close", None)

        if close:
            close()

    yield {
        "type": "result",
        "state": latest_state.model_dump(mode="json"),
    }