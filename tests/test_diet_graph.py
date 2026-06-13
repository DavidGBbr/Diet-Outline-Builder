import math

import pytest

from diet_outline_builder import build_diet_outline


SAMPLE_INPUT = {
    "sex": "male",
    "age": 22,
    "heighCM": 178,
    "weighKG": 87.4,
    "activityLevel": "moderate",
    "goal": "lose_fat",
}


def test_build_diet_outline_returns_accurate_sample_values() -> None:
    result = build_diet_outline(SAMPLE_INPUT)

    assert result["imc"] == 27.6
    assert result["imcClassification"] == "overweight"
    assert result["totalSpend"] == 2916
    assert result["targetSpend"] == 2333
    assert result["goal"] == "lose_weight"
    assert result["macros"] == {"protein": 140, "fat": 52, "carb": 326}
    assert "BMI-based grams-per-kg ranges" in result["explanation"]
    assert "20% deficit" in result["explanation"]
    assert "not medical advice" in result["safetyDisclaimer"]


def test_macros_are_close_to_target_calories() -> None:
    result = build_diet_outline(SAMPLE_INPUT)
    macros = result["macros"]
    macro_calories = macros["protein"] * 4 + macros["fat"] * 9 + macros["carb"] * 4

    assert math.isclose(macro_calories, result["targetSpend"], abs_tol=5)


def test_rejects_invalid_activity_level() -> None:
    payload = SAMPLE_INPUT | {"activityLevel": "extreme"}

    with pytest.raises(ValueError, match="activityLevel"):
        build_diet_outline(payload)


def test_macro_ranges_depend_on_imc_classification() -> None:
    underweight = build_diet_outline(SAMPLE_INPUT | {"weighKG": 55})
    normal = build_diet_outline(SAMPLE_INPUT | {"weighKG": 70})
    overweight = build_diet_outline(SAMPLE_INPUT)

    assert underweight["imcClassification"] == "underweight"
    assert underweight["macros"]["protein"] == round(55 * 2.0)
    assert underweight["macros"]["fat"] == round(55 * 1.0)

    assert normal["imcClassification"] == "normal_weight"
    assert normal["macros"]["protein"] == round(70 * 1.8)
    assert normal["macros"]["fat"] == round(70 * 0.8)

    assert overweight["imcClassification"] == "overweight"
    assert overweight["macros"]["protein"] == round(87.4 * 1.6)
    assert overweight["macros"]["fat"] == round(87.4 * 0.6)
