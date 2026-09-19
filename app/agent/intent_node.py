from app.agent.llm import llm
from app.agent.state import QueryState
from app.prompt.prompt_loader import load_prompt

ALLOWED_INTENTS = {
    "total_sales",
    "order_count",
    "data_query",
    "unknown",
}

ANALYSIS_KEYWORDS = (
    "哪个",
    "最高",
    "最低",
    "排行",
    "排名",
    "分别",
    "各个",
    "按",
    "商品",
    "产品",
    "品牌",
    "分类",
    "客户",
    "会员",
    "月份",
    "季度",
    "年份",
    "省份",
)


def detect_intent(state: QueryState) -> QueryState:
    question = state.question.strip()
    requires_analysis = any(
        keyword in question
        for keyword in ANALYSIS_KEYWORDS
    )

    if not requires_analysis:
        if "总销售额" in question or "销售额" in question:
            state.intent = "total_sales"
            return state

        if (
            "订单数" in question
            or "订单数量" in question
            or "多少订单" in question
        ):
            state.intent = "order_count"
            return state

    prompt_template = load_prompt("intent_detection.prompt")
    prompt = prompt_template.format(question=question)

    response = llm.invoke(prompt)
    detected_intent = str(response.content).strip().lower()

    if detected_intent in ALLOWED_INTENTS:
        state.intent = detected_intent
    else:
        state.intent = "unknown"

    return state