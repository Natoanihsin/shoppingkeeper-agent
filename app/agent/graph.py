from typing import Any

from langgraph.graph import END, START, StateGraph

from app.agent.answer_node import generate_answer
from app.agent.correction_node import correct_sql
from app.agent.execution_node import execute_sql
from app.agent.intent_node import detect_intent
from app.agent.keyword_node import extract_keywords
from app.agent.parameter_node import extract_parameters
from app.agent.retrieval_node import retrieve_metadata
from app.agent.routing import route_after_validation
from app.agent.sql_node import generate_sql
from app.agent.state import QueryState
from app.agent.validation_node import validate_sql
from app.agent.value_node import recall_values


def intent_step(state: QueryState) -> dict[str, Any]:
    return detect_intent(state).model_dump()


def parameter_step(state: QueryState) -> dict[str, Any]:
    return extract_parameters(state).model_dump()


def sql_step(state: QueryState) -> dict[str, Any]:
    return generate_sql(state).model_dump()


def validation_step(state: QueryState) -> dict[str, Any]:
    return validate_sql(state).model_dump()


def execution_step(state: QueryState) -> dict[str, Any]:
    return execute_sql(state).model_dump()


def answer_step(state: QueryState) -> dict[str, Any]:
    return generate_answer(state).model_dump()

def keyword_step(state: QueryState) -> dict[str, Any]:
    return extract_keywords(state).model_dump()

def retrieval_step(state: QueryState) -> dict[str, Any]:
    return retrieve_metadata(state).model_dump()

def value_step(state: QueryState) -> dict[str, Any]:
    return recall_values(state).model_dump()

def correction_step(state: QueryState) -> dict[str, Any]:
    return correct_sql(state).model_dump()

graph_builder = StateGraph(QueryState)

graph_builder.add_node("detect_intent", intent_step)
graph_builder.add_node("extract_parameters", parameter_step)
graph_builder.add_node("generate_sql", sql_step)
graph_builder.add_node("validate_sql", validation_step)
graph_builder.add_node("execute_sql", execution_step)
graph_builder.add_node("generate_answer", answer_step)
graph_builder.add_node("extract_keywords", keyword_step)
graph_builder.add_node("retrieve_metadata", retrieval_step)
graph_builder.add_node("recall_values", value_step)
graph_builder.add_node("correct_sql", correction_step)

graph_builder.add_edge(START, "detect_intent")
graph_builder.add_edge("detect_intent", "recall_values")
graph_builder.add_edge("recall_values", "extract_keywords")
graph_builder.add_edge("extract_keywords", "retrieve_metadata")
graph_builder.add_edge("retrieve_metadata", "extract_parameters")
graph_builder.add_edge("extract_parameters", "generate_sql")
graph_builder.add_edge("generate_sql", "validate_sql")
graph_builder.add_conditional_edges(
    source="validate_sql",
    path=route_after_validation,
    path_map={
        "execute_sql": "execute_sql",
        "correct_sql": "correct_sql",
        "generate_answer": "generate_answer",
    },
)
graph_builder.add_edge("correct_sql", "validate_sql")
graph_builder.add_edge("execute_sql", "generate_answer")
graph_builder.add_edge("generate_answer", END)

graph = graph_builder.compile()