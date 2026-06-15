from typing import Any

from app.agent import OllamaUnavailableError, route_after_validation, run_conversation_turn


class FakeExtractionClient:
    def __init__(self, fields: dict[str, Any]) -> None:
        self.fields = fields

    def extract_fields(self, message: str) -> dict[str, Any]:
        return self.fields


class FailingExtractionClient:
    def extract_fields(self, message: str) -> dict[str, Any]:
        raise OllamaUnavailableError("offline")


def test_route_after_validation_uses_required_labels() -> None:
    assert route_after_validation({"data_valid": True}) == "data_ok"
    assert route_after_validation({"data_valid": False}) == "data_incomplete"


def test_incomplete_turn_asks_for_missing_fields() -> None:
    result = run_conversation_turn(
        {"message": "I am male and 22 years old."},
        client=FakeExtractionClient({"sex": "male", "age": 22}),
    )

    assert result.diet_result is None
    assert result.collected_data == {"sex": "male", "age": 22}
    assert "heightCM" in result.missing_fields
    assert "weightKG" in result.missing_fields
    assert "heightCM" in result.assistant_message


def test_complete_turn_calculates_diet_result() -> None:
    result = run_conversation_turn(
        {"message": "Male, 22, 178cm, 87.4kg, moderate, lose fat."},
        client=FakeExtractionClient(
            {
                "sex": "male",
                "age": 22,
                "heightCM": 178,
                "weightKG": 87.4,
                "activityLevel": "moderate",
                "goal": "lose_fat",
            }
        ),
    )

    assert result.missing_fields == []
    assert result.invalid_fields == []
    assert result.diet_result is not None
    assert result.diet_result.imcClassification == "overweight"
    assert result.diet_result.goal == "lose_weight"
    assert "everything I need" in result.assistant_message


def test_multi_field_extraction_merges_with_existing_state() -> None:
    result = run_conversation_turn(
        {
            "message": "I am 178cm, 87.4kg, moderate activity, and want to lose fat.",
            "collected_data": {"sex": "male", "age": 22},
        },
        client=FakeExtractionClient(
            {
                "heightCM": 178,
                "weightKG": 87.4,
                "activityLevel": "moderate",
                "goal": "lose_fat",
            }
        ),
    )

    assert result.diet_result is not None
    assert result.collected_data["sex"] == "male"
    assert result.collected_data["age"] == 22
    assert result.collected_data["goal"] == "lose_weight"


def test_invalid_candidate_does_not_overwrite_existing_valid_data() -> None:
    result = run_conversation_turn(
        {
            "message": "Actually my weight is 10kg.",
            "collected_data": {
                "sex": "male",
                "age": 22,
                "heightCM": 178,
                "weightKG": 87.4,
                "activityLevel": "moderate",
                "goal": "lose_weight",
            },
        },
        client=FakeExtractionClient({"weightKG": 10}),
    )

    assert result.diet_result is None
    assert result.collected_data["weightKG"] == 87.4
    assert [error.field for error in result.invalid_fields] == ["weightKG"]
    assert "weightKG" in result.assistant_message


def test_ollama_unavailable_returns_safe_error() -> None:
    result = run_conversation_turn(
        {"message": "I am male and 22."},
        client=FailingExtractionClient(),
    )

    assert result.error is not None
    assert result.error.code == "ollama_unavailable"
    assert "Start Ollama" in result.error.message
    assert result.diet_result is None
    assert result.collected_data == {}
