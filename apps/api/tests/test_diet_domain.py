import pytest

from app.domain import (
    DietValidationError,
    validate_diet_input,
    validate_partial_diet_input,
)


VALID_INPUT = {
    "sex": "female",
    "age": 34,
    "heightCM": 165,
    "weightKG": 68,
    "activityLevel": "low",
    "goal": "maintain",
}


def test_validate_diet_input_normalizes_goal_alias() -> None:
    validated = validate_diet_input(VALID_INPUT)

    assert validated.goal == "maintain_weight"


def test_validate_diet_input_returns_structured_errors() -> None:
    payload = VALID_INPUT | {"age": 10, "activityLevel": "extreme"}

    with pytest.raises(DietValidationError) as exc_info:
        validate_diet_input(payload)

    errors = {error.field: error.message for error in exc_info.value.errors}
    assert "age" in errors
    assert "activityLevel" in errors


def test_validate_partial_diet_input_reports_missing_fields_without_raising() -> None:
    result = validate_partial_diet_input({"sex": "male", "age": 45})

    assert result.accepted_data == {"sex": "male", "age": 45}
    assert result.missing_fields == [
        "heightCM",
        "weightKG",
        "activityLevel",
        "goal",
    ]
    assert result.invalid_fields == []


def test_validate_partial_diet_input_reports_invalid_present_fields() -> None:
    result = validate_partial_diet_input(
        {"sex": "unknown", "age": 45, "heighCM": 170}
    )

    assert result.accepted_data == {"age": 45}
    errors = {error.field: error.message for error in result.invalid_fields}
    assert "sex" in errors
    assert errors["heighCM"] == "Field is not supported."
    assert "sex" in result.missing_fields
    assert "heightCM" in result.missing_fields
