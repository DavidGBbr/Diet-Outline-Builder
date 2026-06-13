import json

from diet_outline_builder.graph import build_diet_outline


def _ask_choice(label: str, options: set[str]) -> str:
    while True:
        value = input(f"{label} ({', '.join(sorted(options))}): ").strip().lower()
        if value in options:
            return value
        print(f"Please enter one of: {', '.join(sorted(options))}")


def _ask_number(label: str, value_type: type[int] | type[float]) -> int | float:
    while True:
        raw = input(f"{label}: ").strip()
        try:
            return value_type(raw)
        except ValueError:
            print(f"Please enter a valid {value_type.__name__}.")


def main() -> None:
    payload = {
        "sex": _ask_choice("Sex", {"male", "female"}),
        "age": _ask_number("Age", int),
        "heightCM": _ask_number("Height in cm", float),
        "weightKG": _ask_number("Weight in kg", float),
        "activityLevel": _ask_choice("Activity level", {"low", "moderate", "high"}),
        "goal": _ask_choice("Goal", {"lose_fat", "lose_weight", "maintain", "gain_muscle"}),
    }
    print(json.dumps(build_diet_outline(payload), indent=2))
