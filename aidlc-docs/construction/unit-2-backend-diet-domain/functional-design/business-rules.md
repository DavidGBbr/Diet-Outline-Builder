# Business Rules - Unit 2 Backend Diet Domain Preservation

## Required Fields

The complete diet input requires exactly these canonical fields:

- `sex`
- `age`
- `heightCM`
- `weightKG`
- `activityLevel`
- `goal`

## Canonical Field Rules

- `heightCM` is required; `heighCM` is not accepted.
- `weightKG` is required; `weighKG` is not accepted.
- Unit 2 updates tests and samples to canonical names.

## Validation Rules

- `sex` must be `male` or `female`.
- `age` must be an integer from 13 to 120.
- `heightCM` must be a number from 100 to 250.
- `weightKG` must be a number from 30 to 300.
- `activityLevel` must be `low`, `moderate`, or `high`.
- `goal` must support accepted user values and normalize to domain goals:
  - `lose_fat` -> `lose_weight`
  - `lose_weight` -> `lose_weight`
  - `maintain` -> `maintain_weight`
  - `maintain_weight` -> `maintain_weight`
  - `gain_muscle` -> `gain_muscle`

## Partial Validation Rules

- Missing fields are returned in `missing_fields`.
- Present valid fields are returned in `accepted_data` after normalization.
- Present invalid fields are returned in `invalid_fields` as structured errors.
- Missing fields do not raise exceptions in partial validation.
- Invalid present values do not block reporting other missing fields.

## Calculation Rules

- BMI (`imc`) is `weightKG / heightM^2`, rounded to one decimal.
- BMI classification:
  - `< 18.5`: `underweight`
  - `>= 18.5` and `< 25`: `normal_weight`
  - `>= 25` and `< 30`: `overweight`
  - `>= 30`: `obesity`
- BMR uses Mifflin-St Jeor:
  - male offset: `+5`
  - female offset: `-161`
- Activity factors:
  - `low`: `1.2`
  - `moderate`: `1.55`
  - `high`: `1.725`
- Goal adjustment:
  - `lose_weight`: `-20%`
  - `maintain_weight`: `0%`
  - `gain_muscle`: `+10%`
- Macro factors by BMI classification:
  - `underweight`: protein `2.0 g/kg`, fat `1.0 g/kg`
  - `normal_weight`: protein `1.8 g/kg`, fat `0.8 g/kg`
  - `overweight`: protein `1.6 g/kg`, fat `0.6 g/kg`
  - `obesity`: protein `1.6 g/kg`, fat `0.6 g/kg`
- Carbs fill remaining calories after protein and fat.
- Carbs cannot be negative.

## Output Rules

The final `DietResponse` includes:

- `imc`
- `imcClassification`
- `totalSpend`
- `targetSpend`
- `goal`
- `macros`
- `explanation`
- `safetyDisclaimer`

## Security Rules

- SECURITY-05 applies: all untrusted input must pass strict field/type/range/enum validation before calculation.
- Domain validation must not trust values from future frontend, WebSocket payloads, or Ollama extraction.

## PBT Rules

- PBT-03 applies to documented calculation invariants.
- PBT-07 requires reusable domain-specific valid input generators.
- PBT-08 requires Hypothesis shrinking/reproducibility defaults.
- PBT-09 uses Hypothesis.
