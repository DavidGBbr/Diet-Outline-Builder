from __future__ import annotations

from typing import Any, Literal, TypedDict

from langgraph.graph import END, START, StateGraph


Sex = Literal["male", "female"]
ActivityLevel = Literal["low", "moderate", "high"]
Goal = Literal["lose_weight", "maintain_weight", "gain_muscle"]

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

GOAL_ALIASES: dict[str, Goal] = {
    "lose_fat": "lose_weight",
    "lose_weight": "lose_weight",
    "maintain": "maintain_weight",
    "maintain_weight": "maintain_weight",
    "gain_muscle": "gain_muscle",
}


class DietInput(TypedDict):
    sex: Sex
    age: int
    heightCM: float
    weightKG: float
    activityLevel: ActivityLevel
    goal: Goal


class ValidationResult(TypedDict):
    isValid: bool
    normalizedInput: DietInput


class Anthropometrics(TypedDict):
    imc: float
    imcClassification: str
    bmr: float


class Energy(TypedDict):
    totalSpend: int
    targetSpend: int
    adjustmentPercent: int


class Macros(TypedDict):
    protein: int
    fat: int
    carb: int


class DietResponse(TypedDict):
    imc: float
    imcClassification: str
    totalSpend: int
    targetSpend: int
    goal: Goal
    macros: Macros
    explanation: str
    safetyDisclaimer: str


class DietState(TypedDict, total=False):
    input: dict[str, Any]
    validation: ValidationResult
    anthropometrics: Anthropometrics
    energy: Energy
    macros: Macros
    response: DietResponse


def _pick(payload: dict[str, Any], *names: str) -> Any:
    for name in names:
        if name in payload:
            return payload[name]
    raise ValueError(f"Missing required field: {names[0]}")


def _normalize_input(payload: dict[str, Any]) -> DietInput:
    sex = str(_pick(payload, "sex")).lower()
    activity_level = str(_pick(payload, "activityLevel")).lower()
    raw_goal = str(_pick(payload, "goal")).lower()
    goal = GOAL_ALIASES.get(raw_goal)

    if sex not in {"male", "female"}:
        raise ValueError("sex must be either 'male' or 'female'")
    if activity_level not in ACTIVITY_FACTORS:
        raise ValueError("activityLevel must be one of: low, moderate, high")
    if goal is None:
        raise ValueError("goal must be one of: lose_fat, lose_weight, maintain, gain_muscle")

    age = int(_pick(payload, "age"))
    height_cm = float(_pick(payload, "heightCM", "heighCM"))
    weight_kg = float(_pick(payload, "weightKG", "weighKG"))

    if not 13 <= age <= 120:
        raise ValueError("age must be between 13 and 120")
    if not 100 <= height_cm <= 250:
        raise ValueError("heightCM must be between 100 and 250")
    if not 30 <= weight_kg <= 300:
        raise ValueError("weightKG must be between 30 and 300")

    return {
        "sex": sex,  # type: ignore[typeddict-item]
        "age": age,
        "heightCM": height_cm,
        "weightKG": weight_kg,
        "activityLevel": activity_level,  # type: ignore[typeddict-item]
        "goal": goal,
    }


def validate_input_node(state: DietState) -> DietState:
    normalized = _normalize_input(state["input"])
    return {"validation": {"isValid": True, "normalizedInput": normalized}}


def calculate_anthropometrics_node(state: DietState) -> DietState:
    payload = state["validation"]["normalizedInput"]
    height_m = payload["heightCM"] / 100
    imc = round(payload["weightKG"] / (height_m**2), 1)

    if imc < 18.5:
        classification = "underweight"
    elif imc < 25:
        classification = "normal_weight"
    elif imc < 30:
        classification = "overweight"
    else:
        classification = "obesity"

    sex_offset = 5 if payload["sex"] == "male" else -161
    bmr = 10 * payload["weightKG"] + 6.25 * payload["heightCM"] - 5 * payload["age"] + sex_offset

    return {
        "anthropometrics": {
            "imc": imc,
            "imcClassification": classification,
            "bmr": bmr,
        }
    }


def calculate_energy_node(state: DietState) -> DietState:
    payload = state["validation"]["normalizedInput"]
    bmr = state["anthropometrics"]["bmr"]
    total_spend = round(bmr * ACTIVITY_FACTORS[payload["activityLevel"]])

    if payload["goal"] == "lose_weight":
        adjustment_percent = -20
    elif payload["goal"] == "gain_muscle":
        adjustment_percent = 10
    else:
        adjustment_percent = 0

    target_spend = round(total_spend * (1 + adjustment_percent / 100))

    return {
        "energy": {
            "totalSpend": total_spend,
            "targetSpend": target_spend,
            "adjustmentPercent": adjustment_percent,
        }
    }


def calculate_macros_node(state: DietState) -> DietState:
    payload = state["validation"]["normalizedInput"]
    target_spend = state["energy"]["targetSpend"]
    imc_classification = state["anthropometrics"]["imcClassification"]
    protein_per_kg, fat_per_kg = MACRO_FACTORS[imc_classification]

    protein = round(payload["weightKG"] * protein_per_kg)
    fat = round(payload["weightKG"] * fat_per_kg)
    protein_calories = protein * 4
    fat_calories = fat * 9
    carb = max(0, round((target_spend - protein_calories - fat_calories) / 4))

    return {"macros": {"protein": protein, "fat": fat, "carb": carb}}


def generate_explanation_node(state: DietState) -> DietState:
    payload = state["validation"]["normalizedInput"]
    energy = state["energy"]
    macros = state["macros"]

    if payload["goal"] == "lose_weight":
        goal_sentence = (
            "For fat loss, a 20% deficit was applied. Protein intake was kept higher "
            "to help preserve muscle mass during the deficit."
        )
    elif payload["goal"] == "gain_muscle":
        goal_sentence = "For muscle gain, a 10% surplus was applied to support training adaptation."
    else:
        goal_sentence = "For maintenance, no calorie adjustment was applied."

    explanation = (
        f"Your estimated caloric expenditure is approximately {energy['totalSpend']} kcal per day. "
        f"Your target is approximately {energy['targetSpend']} kcal per day. "
        f"The macro split is {macros['protein']} g protein, {macros['fat']} g fat, "
        f"and {macros['carb']} g carbohydrates. Protein and fat were selected from "
        f"BMI-based grams-per-kg ranges, and carbohydrates fill the remaining calories. {goal_sentence}"
    )

    return {
        "response": {
            "imc": state["anthropometrics"]["imc"],
            "imcClassification": state["anthropometrics"]["imcClassification"],
            "totalSpend": energy["totalSpend"],
            "targetSpend": energy["targetSpend"],
            "goal": payload["goal"],
            "macros": macros,
            "explanation": explanation,
            "safetyDisclaimer": "",
        }
    }


def add_safety_disclaimer_node(state: DietState) -> DietState:
    response = state["response"].copy()
    response["safetyDisclaimer"] = (
        "This is an educational estimate, not medical advice. Consult a qualified health "
        "professional before changing your diet, especially if you have medical conditions."
    )
    return {"response": response}


def _compile_graph():
    graph = StateGraph(DietState)
    graph.add_node("validateInput", validate_input_node)
    graph.add_node("calculateAnthropometrics", calculate_anthropometrics_node)
    graph.add_node("calculateEnergy", calculate_energy_node)
    graph.add_node("calculateMacros", calculate_macros_node)
    graph.add_node("generateExplanation", generate_explanation_node)
    graph.add_node("addSafetyDisclaimer", add_safety_disclaimer_node)

    graph.add_edge(START, "validateInput")
    graph.add_edge("validateInput", "calculateAnthropometrics")
    graph.add_edge("calculateAnthropometrics", "calculateEnergy")
    graph.add_edge("calculateEnergy", "calculateMacros")
    graph.add_edge("calculateMacros", "generateExplanation")
    graph.add_edge("generateExplanation", "addSafetyDisclaimer")
    graph.add_edge("addSafetyDisclaimer", END)
    return graph.compile()


diet_graph = _compile_graph()


def build_diet_outline(payload: dict[str, Any]) -> DietResponse:
    state = diet_graph.invoke({"input": payload})
    return state["response"]
