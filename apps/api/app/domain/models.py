from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


Sex = Literal["male", "female"]
ActivityLevel = Literal["low", "moderate", "high"]
Goal = Literal["lose_weight", "maintain_weight", "gain_muscle"]


class FieldValidationError(BaseModel):
    field: str
    message: str


class DietValidationError(ValueError):
    def __init__(self, errors: list[FieldValidationError]) -> None:
        self.errors = errors
        message = "; ".join(f"{error.field}: {error.message}" for error in errors)
        super().__init__(message)


class ValidatedDietInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sex: Sex
    age: int = Field(ge=13, le=120)
    heightCM: float = Field(ge=100, le=250)
    weightKG: float = Field(ge=30, le=300)
    activityLevel: ActivityLevel
    goal: Goal

    @field_validator("sex", "activityLevel", "goal", mode="before")
    @classmethod
    def normalize_lowercase(cls, value: Any) -> Any:
        if isinstance(value, str):
            return value.lower()
        return value

    @field_validator("goal", mode="before")
    @classmethod
    def normalize_goal_aliases(cls, value: Any) -> Any:
        if not isinstance(value, str):
            return value

        aliases: dict[str, Goal] = {
            "lose_fat": "lose_weight",
            "lose_weight": "lose_weight",
            "maintain": "maintain_weight",
            "maintain_weight": "maintain_weight",
            "gain_muscle": "gain_muscle",
        }
        return aliases.get(value.lower(), value.lower())


class Macros(BaseModel):
    protein: int
    fat: int
    carb: int


class DietResponse(BaseModel):
    imc: float
    imcClassification: str
    totalSpend: int
    targetSpend: int
    goal: Goal
    macros: Macros
    explanation: str
    safetyDisclaimer: str


class PartialValidationResult(BaseModel):
    accepted_data: dict[str, Any]
    missing_fields: list[str]
    invalid_fields: list[FieldValidationError]
