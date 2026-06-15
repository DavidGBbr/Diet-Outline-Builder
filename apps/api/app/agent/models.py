from __future__ import annotations

from typing import Any, Protocol, TypedDict

from pydantic import BaseModel, Field

from app.domain import DietResponse, FieldValidationError


class ExtractionClient(Protocol):
    def extract_fields(self, message: str) -> dict[str, Any]: ...


class AgentError(BaseModel):
    code: str
    message: str


class AgentTurnInput(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    collected_data: dict[str, Any] = Field(default_factory=dict)


class AgentTurnResult(BaseModel):
    assistant_message: str
    collected_data: dict[str, Any]
    missing_fields: list[str]
    invalid_fields: list[FieldValidationError]
    diet_result: DietResponse | None = None
    error: AgentError | None = None


class AgentState(TypedDict, total=False):
    message: str
    collected_data: dict[str, Any]
    candidate_data: dict[str, Any]
    accepted_data: dict[str, Any]
    missing_fields: list[str]
    invalid_fields: list[FieldValidationError]
    data_valid: bool
    diet_result: DietResponse
    assistant_message: str
    error: AgentError
    client: ExtractionClient | None
