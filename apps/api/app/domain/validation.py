from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from pydantic import ValidationError

from app.domain.models import (
    DietValidationError,
    FieldValidationError,
    PartialValidationResult,
    ValidatedDietInput,
)


REQUIRED_FIELDS = ["sex", "age", "heightCM", "weightKG", "activityLevel", "goal"]

DEFAULT_VALID_INPUT: dict[str, Any] = {
    "sex": "male",
    "age": 30,
    "heightCM": 175,
    "weightKG": 75,
    "activityLevel": "moderate",
    "goal": "maintain_weight",
}


def _error_message(error_type: str, raw_message: str) -> str:
    if error_type == "missing":
        return "Field is required."
    if error_type == "extra_forbidden":
        return "Field is not supported."
    return raw_message.rstrip(".") + "."


def _field_name(location: tuple[Any, ...]) -> str:
    if not location:
        return "input"
    return str(location[0])


def _structured_errors(exc: ValidationError) -> list[FieldValidationError]:
    return [
        FieldValidationError(
            field=_field_name(error["loc"]),
            message=_error_message(str(error["type"]), str(error["msg"])),
        )
        for error in exc.errors()
    ]


def validate_diet_input(payload: Mapping[str, Any]) -> ValidatedDietInput:
    try:
        return ValidatedDietInput.model_validate(dict(payload))
    except ValidationError as exc:
        raise DietValidationError(_structured_errors(exc)) from None


def missing_required_fields(payload: Mapping[str, Any]) -> list[str]:
    return [field for field in REQUIRED_FIELDS if field not in payload]


def validate_partial_diet_input(payload: Mapping[str, Any]) -> PartialValidationResult:
    accepted_data: dict[str, Any] = {}
    invalid_fields: list[FieldValidationError] = []

    for field, value in payload.items():
        if field not in REQUIRED_FIELDS:
            invalid_fields.append(
                FieldValidationError(field=field, message="Field is not supported.")
            )
            continue

        candidate = DEFAULT_VALID_INPUT | {field: value}
        try:
            validated = ValidatedDietInput.model_validate(candidate)
        except ValidationError as exc:
            field_errors = [
                error for error in _structured_errors(exc) if error.field == field
            ]
            invalid_fields.extend(
                field_errors
                or [FieldValidationError(field=field, message="Field is invalid.")]
            )
            continue

        accepted_data[field] = getattr(validated, field)

    return PartialValidationResult(
        accepted_data=accepted_data,
        missing_fields=missing_required_fields(accepted_data),
        invalid_fields=invalid_fields,
    )
