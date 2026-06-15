from __future__ import annotations

from typing import Literal

from langgraph.graph import END, START, StateGraph

from app.agent.models import AgentError, AgentState, AgentTurnInput, AgentTurnResult
from app.agent.ollama import OllamaExtractionClient, OllamaUnavailableError
from app.domain import DietValidationError, build_diet_outline, validate_partial_diet_input


OLLAMA_UNAVAILABLE_MESSAGE = (
    "I could not reach local Ollama. Start Ollama, make sure the llama3.1:8b model is "
    "available, and try again."
)


def extract_data_node(state: AgentState) -> AgentState:
    client = state.get("client") or OllamaExtractionClient()

    try:
        candidate_data = client.extract_fields(state["message"])
    except OllamaUnavailableError:
        return {
            "candidate_data": {},
            "error": AgentError(
                code="ollama_unavailable",
                message=OLLAMA_UNAVAILABLE_MESSAGE,
            ),
            "assistant_message": OLLAMA_UNAVAILABLE_MESSAGE,
        }

    return {"candidate_data": candidate_data}


def route_after_extraction(state: AgentState) -> Literal["extract_ok", "extract_error"]:
    if state.get("error") is not None:
        return "extract_error"
    return "extract_ok"


def merge_valid_fields_node(state: AgentState) -> AgentState:
    collected_data = dict(state.get("collected_data", {}))
    validation = validate_partial_diet_input(state.get("candidate_data", {}))

    for field, value in validation.accepted_data.items():
        collected_data[field] = value

    return {
        "accepted_data": validation.accepted_data,
        "collected_data": collected_data,
        "invalid_fields": validation.invalid_fields,
    }


def validate_data_node(state: AgentState) -> AgentState:
    validation = validate_partial_diet_input(state.get("collected_data", {}))
    invalid_fields = [*state.get("invalid_fields", []), *validation.invalid_fields]
    data_valid = not validation.missing_fields and not invalid_fields

    return {
        "collected_data": validation.accepted_data,
        "missing_fields": validation.missing_fields,
        "invalid_fields": invalid_fields,
        "data_valid": data_valid,
    }


def route_after_validation(state: AgentState) -> Literal["data_ok", "data_incomplete"]:
    if state.get("data_valid") is True:
        return "data_ok"
    return "data_incomplete"


def ask_remaining_data_node(state: AgentState) -> AgentState:
    invalid_fields = state.get("invalid_fields", [])
    missing_fields = state.get("missing_fields", [])
    invalid_names = [error.field for error in invalid_fields]
    requested_fields = [*invalid_names, *missing_fields]

    if requested_fields:
        field_list = ", ".join(dict.fromkeys(requested_fields))
        message = f"I still need valid values for: {field_list}."
    else:
        message = "Tell me your sex, age, height, weight, activity level, and goal."

    return {"assistant_message": message}


def calculate_diet_node(state: AgentState) -> AgentState:
    try:
        diet_result = build_diet_outline(state.get("collected_data", {}))
    except DietValidationError as exc:
        return {
            "invalid_fields": exc.errors,
            "data_valid": False,
            "assistant_message": "I need a little more valid information before calculating your diet.",
        }

    return {"diet_result": diet_result}


def generate_response_node(state: AgentState) -> AgentState:
    return {"assistant_message": "I have everything I need. Here's your diet outline."}


def _compile_graph():
    graph = StateGraph(AgentState)
    graph.add_node("extractData", extract_data_node)
    graph.add_node("mergeValidFields", merge_valid_fields_node)
    graph.add_node("validateData", validate_data_node)
    graph.add_node("askRemainingData", ask_remaining_data_node)
    graph.add_node("calculateDiet", calculate_diet_node)
    graph.add_node("generateResponse", generate_response_node)

    graph.add_edge(START, "extractData")
    graph.add_conditional_edges(
        "extractData",
        route_after_extraction,
        {"extract_ok": "mergeValidFields", "extract_error": END},
    )
    graph.add_edge("mergeValidFields", "validateData")
    graph.add_conditional_edges(
        "validateData",
        route_after_validation,
        {"data_ok": "calculateDiet", "data_incomplete": "askRemainingData"},
    )
    graph.add_edge("askRemainingData", END)
    graph.add_edge("calculateDiet", "generateResponse")
    graph.add_edge("generateResponse", END)
    return graph.compile()


conversation_graph = _compile_graph()


def run_conversation_turn(
    turn_input: AgentTurnInput | dict[str, object],
    client: object | None = None,
) -> AgentTurnResult:
    parsed_input = (
        turn_input
        if isinstance(turn_input, AgentTurnInput)
        else AgentTurnInput.model_validate(turn_input)
    )
    state = conversation_graph.invoke(
        {
            "message": parsed_input.message,
            "collected_data": parsed_input.collected_data,
            "client": client,
        }
    )

    return AgentTurnResult(
        assistant_message=state.get("assistant_message", ""),
        collected_data=state.get("collected_data", {}),
        missing_fields=state.get("missing_fields", []),
        invalid_fields=state.get("invalid_fields", []),
        diet_result=state.get("diet_result"),
        error=state.get("error"),
    )
