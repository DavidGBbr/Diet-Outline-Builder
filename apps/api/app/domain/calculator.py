from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from app.domain.models import ActivityLevel, DietResponse, Macros, ValidatedDietInput
from app.domain.validation import validate_diet_input


ACTIVITY_FACTORS: dict[ActivityLevel, float] = {
    "low": 1.2,
    "moderate": 1.55,
    "high": 1.725,
}

MACRO_FACTORS: dict[str, tuple[float, float]] = {
    "underweight": (2.0, 1.0),
    "normal_weight": (1.8, 0.8),
    "overweight": (1.6, 0.6),
    "obesity": (1.6, 0.6),
}


def calculate_bmi(input_data: ValidatedDietInput) -> float:
    height_m = input_data.heightCM / 100
    return round(input_data.weightKG / (height_m**2), 1)


def classify_bmi(imc: float) -> str:
    if imc < 18.5:
        return "underweight"
    if imc < 25:
        return "normal_weight"
    if imc < 30:
        return "overweight"
    return "obesity"


def calculate_bmr(input_data: ValidatedDietInput) -> float:
    sex_offset = 5 if input_data.sex == "male" else -161
    return (
        10 * input_data.weightKG
        + 6.25 * input_data.heightCM
        - 5 * input_data.age
        + sex_offset
    )


def calculate_total_spend(input_data: ValidatedDietInput) -> int:
    return round(calculate_bmr(input_data) * ACTIVITY_FACTORS[input_data.activityLevel])


def calculate_target_spend(total_spend: int, input_data: ValidatedDietInput) -> int:
    if input_data.goal == "lose_weight":
        adjustment_percent = -20
    elif input_data.goal == "gain_muscle":
        adjustment_percent = 10
    else:
        adjustment_percent = 0

    return round(total_spend * (1 + adjustment_percent / 100))


def calculate_macros(
    input_data: ValidatedDietInput, target_spend: int, imc_classification: str
) -> Macros:
    protein_per_kg, fat_per_kg = MACRO_FACTORS[imc_classification]
    protein = round(input_data.weightKG * protein_per_kg)
    fat = round(input_data.weightKG * fat_per_kg)

    protein_calories = protein * 4
    fat_calories = fat * 9
    base_calories = protein_calories + fat_calories

    if base_calories > target_spend:
        scale = target_spend / base_calories
        protein = max(1, round(protein * scale))
        fat = max(1, round(fat * scale))
        protein_calories = protein * 4
        fat_calories = fat * 9

    carb = max(0, round((target_spend - protein_calories - fat_calories) / 4))
    return Macros(protein=protein, fat=fat, carb=carb)


def generate_explanation(
    input_data: ValidatedDietInput,
    total_spend: int,
    target_spend: int,
    macros: Macros,
) -> str:
    if input_data.goal == "lose_weight":
        goal_sentence = (
            "For fat loss, a 20% deficit was applied. Protein intake was kept higher "
            "to help preserve muscle mass during the deficit."
        )
    elif input_data.goal == "gain_muscle":
        goal_sentence = (
            "For muscle gain, a 10% surplus was applied to support training adaptation."
        )
    else:
        goal_sentence = "For maintenance, no calorie adjustment was applied."

    return (
        f"Your estimated caloric expenditure is approximately {total_spend} kcal per day. "
        f"Your target is approximately {target_spend} kcal per day. "
        f"The macro split is {macros.protein} g protein, {macros.fat} g fat, "
        f"and {macros.carb} g carbohydrates. Protein and fat were selected from "
        f"BMI-based grams-per-kg ranges, and carbohydrates fill the remaining calories. "
        f"{goal_sentence}"
    )


def build_diet_outline(payload: ValidatedDietInput | Mapping[str, Any]) -> DietResponse:
    input_data = (
        payload
        if isinstance(payload, ValidatedDietInput)
        else validate_diet_input(payload)
    )
    imc = calculate_bmi(input_data)
    imc_classification = classify_bmi(imc)
    total_spend = calculate_total_spend(input_data)
    target_spend = calculate_target_spend(total_spend, input_data)
    macros = calculate_macros(input_data, target_spend, imc_classification)
    explanation = generate_explanation(input_data, total_spend, target_spend, macros)

    return DietResponse(
        imc=imc,
        imcClassification=imc_classification,
        totalSpend=total_spend,
        targetSpend=target_spend,
        goal=input_data.goal,
        macros=macros,
        explanation=explanation,
        safetyDisclaimer=(
            "This is an educational estimate, not medical advice. Consult a qualified health "
            "professional before changing your diet, especially if you have medical conditions."
        ),
    )
