import math
from typing import Any

from hypothesis import given
from hypothesis import strategies as st

from app.domain import build_diet_outline, classify_bmi


@st.composite
def valid_diet_inputs(draw: st.DrawFn) -> dict[str, Any]:
    return {
        "sex": draw(st.sampled_from(["male", "female"])),
        "age": draw(st.integers(min_value=13, max_value=120)),
        "heightCM": draw(st.floats(min_value=100, max_value=250, allow_nan=False, allow_infinity=False)),
        "weightKG": draw(st.floats(min_value=30, max_value=300, allow_nan=False, allow_infinity=False)),
        "activityLevel": draw(st.sampled_from(["low", "moderate", "high"])),
        "goal": draw(
            st.sampled_from(
                ["lose_fat", "lose_weight", "maintain", "maintain_weight", "gain_muscle"]
            )
        ),
    }


@given(valid_diet_inputs())
def test_valid_inputs_produce_positive_calorie_and_macro_outputs(
    payload: dict[str, Any],
) -> None:
    result = build_diet_outline(payload)

    assert result.totalSpend > 0
    assert result.targetSpend > 0
    assert result.macros.protein > 0
    assert result.macros.fat > 0
    assert result.macros.carb >= 0


@given(valid_diet_inputs())
def test_bmi_classification_matches_bmi_ranges(payload: dict[str, Any]) -> None:
    result = build_diet_outline(payload)

    assert result.imcClassification == classify_bmi(result.imc)


@given(valid_diet_inputs())
def test_macro_calories_stay_close_to_target_calories(payload: dict[str, Any]) -> None:
    result = build_diet_outline(payload)
    macros = result.macros
    macro_calories = macros.protein * 4 + macros.fat * 9 + macros.carb * 4

    assert math.isclose(macro_calories, result.targetSpend, abs_tol=5)
