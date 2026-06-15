from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from app.domain import DietResponse, FieldValidationError


class ClientConversationState(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    collected_data: dict[str, Any] = Field(default_factory=dict, alias="collectedData")


class IncomingChatMessage(BaseModel):
    type: Literal["user_message"]
    text: str = Field(min_length=1, max_length=4000)
    state: ClientConversationState = Field(default_factory=ClientConversationState)


class AssistantMessage(BaseModel):
    type: Literal["assistant_message"] = "assistant_message"
    text: str


class DietResultMessage(BaseModel):
    type: Literal["diet_result"] = "diet_result"
    result: DietResponse


class ErrorMessage(BaseModel):
    type: Literal["error"] = "error"
    code: str
    message: str


class ServerConversationState(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    collected_data: dict[str, Any] = Field(default_factory=dict, alias="collectedData")
    missing_fields: list[str] = Field(default_factory=list, alias="missingFields")
    invalid_fields: list[FieldValidationError] = Field(
        default_factory=list,
        alias="invalidFields",
    )


class StateSnapshotMessage(BaseModel):
    type: Literal["state_snapshot"] = "state_snapshot"
    state: ServerConversationState
