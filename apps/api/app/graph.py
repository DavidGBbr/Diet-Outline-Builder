from __future__ import annotations

from typing import Any, TypedDict

from langgraph.graph import END, START, StateGraph

from app.domain import build_diet_outline as build_domain_diet_outline


class DietState(TypedDict, total=False):
    input: dict[str, Any]
    response: dict[str, Any]


def build_diet_outline_node(state: DietState) -> DietState:
    response = build_domain_diet_outline(state["input"])
    return {"response": response.model_dump()}


def _compile_graph():
    graph = StateGraph(DietState)
    graph.add_node("buildDietOutline", build_diet_outline_node)
    graph.add_edge(START, "buildDietOutline")
    graph.add_edge("buildDietOutline", END)
    return graph.compile()


diet_graph = _compile_graph()


def build_diet_outline(payload: dict[str, Any]) -> dict[str, Any]:
    state = diet_graph.invoke({"input": payload})
    return state["response"]
