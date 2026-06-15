# Business Logic Model - Unit 2 Backend Diet Domain Preservation

## Unit Goal

Unit 2 extracts deterministic diet logic from `apps/api/app/graph.py` into a pure domain layer under `apps/api/app/domain/`. The domain layer becomes the trusted source for validation, missing-field analysis, calculation, and property-based test invariants.

## Target Domain Modules

```text
apps/api/app/domain/
  __init__.py
  models.py
  validation.py
  calculator.py
```

## Domain Flow - Complete Input

```text
raw payload
  -> validate_diet_input
  -> ValidatedDietInput
  -> build_diet_outline
  -> DietResponse
```

## Domain Flow - Partial Input

```text
partial raw payload
  -> validate_partial_diet_input
  -> PartialValidationResult
       accepted_data
       missing_fields
       invalid_fields
```

## Calculation Flow

```text
ValidatedDietInput
  -> calculate_bmi
  -> classify_bmi
  -> calculate_bmr
  -> calculate_total_spend
  -> calculate_target_spend
  -> calculate_macros
  -> generate_explanation
  -> DietResponse
```

## LangGraph Compatibility

The existing graph remains as an adapter during Unit 2. It should call the new domain functions instead of owning validation and calculation logic directly. Unit 3 will later introduce the conversational graph.

## Input Alias Decision

Legacy misspelled aliases are removed in Unit 2:

- `heighCM` is no longer accepted.
- `weighKG` is no longer accepted.
- Canonical fields are `heightCM` and `weightKG`.

Tests and examples must be updated to canonical field names.

## Error Handling Model

- Complete validation raises a domain validation exception when required fields are missing or invalid.
- Partial validation does not raise for missing fields.
- Partial validation returns structured field errors with `field` and `message` for invalid present values.
- These structured errors are designed for Unit 3 conversation prompts.

## PBT Model

Hypothesis tests target pure domain functions:

- Generated valid inputs always produce positive `totalSpend`, positive `targetSpend`, positive protein/fat, and non-negative carbs.
- BMI classification always matches the calculated BMI range.
- Macro calories remain close to target calories within the accepted rounding tolerance.
