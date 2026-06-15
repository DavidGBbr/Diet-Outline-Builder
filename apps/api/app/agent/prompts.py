from __future__ import annotations


def build_extraction_prompt(message: str) -> str:
    return f"""
Extract diet-builder fields from the user message.

Return only JSON. Do not include markdown or explanations.

Supported fields:
- sex: "male" or "female"
- age: integer years
- heightCM: height in centimeters
- weightKG: weight in kilograms
- activityLevel: "low", "moderate", or "high"
- goal: "lose_weight", "lose_fat", "maintain_weight", "maintain", or "gain_muscle"

If a field is not present, omit it.
Use canonical heightCM and weightKG keys only.

User message:
{message}
""".strip()
