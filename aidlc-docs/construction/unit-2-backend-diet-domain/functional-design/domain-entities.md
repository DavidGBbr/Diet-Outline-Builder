# Domain Entities - Unit 2 Backend Diet Domain Preservation

## ValidatedDietInput

Purpose: Canonical complete input accepted by deterministic diet calculation.

Fields:

- `sex: Literal["male", "female"]`
- `age: int`
- `heightCM: float`
- `weightKG: float`
- `activityLevel: Literal["low", "moderate", "high"]`
- `goal: Literal["lose_weight", "maintain_weight", "gain_muscle"]`

Implementation decision: Pydantic model.

## PartialDietInput

Purpose: Accepted normalized subset of user-provided fields during conversation.

Fields:

- Same field names as `ValidatedDietInput`, all optional.

Implementation decision: Pydantic model or typed dict suitable for serialization in Unit 3.

## FieldValidationError

Purpose: Structured invalid-field report for conversation prompts and API errors.

Fields:

- `field: str`
- `message: str`

Implementation decision: Pydantic model.

## PartialValidationResult

Purpose: Result of validating incomplete conversation state without raising for missing fields.

Fields:

- `accepted_data: PartialDietInput`
- `missing_fields: list[str]`
- `invalid_fields: list[FieldValidationError]`

Implementation decision: Pydantic model.

## Macros

Purpose: Macronutrient output.

Fields:

- `protein: int`
- `fat: int`
- `carb: int`

Implementation decision: Pydantic model.

## DietResponse

Purpose: Final deterministic result consumed by graph/API/UI layers.

Fields:

- `imc: float`
- `imcClassification: str`
- `totalSpend: int`
- `targetSpend: int`
- `goal: Goal`
- `macros: Macros`
- `explanation: str`
- `safetyDisclaimer: str`

Implementation decision: Pydantic model with serialization to dict for existing graph compatibility.

## DietValidationError

Purpose: Exception raised by complete validation when data is missing or invalid.

Fields:

- `errors: list[FieldValidationError]`

Behavior:

- Exception string may be human readable.
- Unit 3 should use structured `errors`, not parse exception text.
