# Logical Components - Unit 2 Backend Diet Domain Preservation

## Domain Models Component

### Location

`apps/api/app/domain/models.py`

### Responsibilities

- Define Pydantic models and domain literals.
- Provide serializable model types for later graph/API layers.

### Key Types

- `ValidatedDietInput`
- `PartialDietInput`
- `FieldValidationError`
- `PartialValidationResult`
- `Macros`
- `DietResponse`
- `DietValidationError`

## Domain Validation Component

### Location

`apps/api/app/domain/validation.py`

### Responsibilities

- Validate complete payloads.
- Validate partial payloads without raising for missing fields.
- Normalize supported goal aliases.
- Enforce canonical fields and reject legacy misspellings by omission/error.
- Produce structured validation errors.

### Key Functions

- `validate_diet_input(payload: Mapping[str, object]) -> ValidatedDietInput`
- `validate_partial_diet_input(payload: Mapping[str, object]) -> PartialValidationResult`
- `missing_required_fields(payload: Mapping[str, object] | PartialDietInput) -> list[str]`

## Domain Calculator Component

### Location

`apps/api/app/domain/calculator.py`

### Responsibilities

- Own pure calculation functions.
- Build final `DietResponse` from `ValidatedDietInput`.
- Keep nutrition math independent from LangGraph.

### Key Functions

- `calculate_bmi(input: ValidatedDietInput) -> float`
- `classify_bmi(imc: float) -> str`
- `calculate_bmr(input: ValidatedDietInput) -> float`
- `calculate_energy(input: ValidatedDietInput) -> Energy-like values`
- `calculate_macros(input: ValidatedDietInput, target_spend: int, classification: str) -> Macros`
- `build_diet_outline(input: ValidatedDietInput | Mapping[str, object]) -> DietResponse`

## Domain Package Export Component

### Location

`apps/api/app/domain/__init__.py`

### Responsibilities

- Export public domain models and functions.
- Keep imports stable for `app.graph` and later Unit 3 code.

## Graph Compatibility Component

### Location

`apps/api/app/graph.py`

### Responsibilities

- Keep current `diet_graph` and `build_diet_outline` compatibility during Unit 2.
- Delegate validation/calculation to domain functions.
- Avoid owning domain math after Unit 2.

## PBT Test Component

### Location

`apps/api/tests/test_diet_domain_properties.py`

### Responsibilities

- Define reusable domain-specific strategies.
- Test documented invariants with Hypothesis.
- Run as part of `pnpm test:api`.

## Example-Based Test Component

### Location

`apps/api/tests/test_diet_graph.py` and/or `apps/api/tests/test_diet_domain.py`

### Responsibilities

- Preserve known sample expectations using canonical field names.
- Test strict rejection of legacy misspelled aliases.
- Test partial validation behavior for missing/invalid fields.

## Dependency Component

### Files

- `apps/api/pyproject.toml`
- `apps/api/uv.lock`

### Responsibilities

- Add bounded `pydantic` runtime dependency.
- Add bounded `hypothesis` dev dependency.
- Keep dependency lock updated.

## Component Interaction

```text
app.graph compatibility wrapper
  -> app.domain.validate_diet_input
  -> app.domain.build_diet_outline
  -> DietResponse serialized for existing tests

future Unit 3 agent
  -> app.domain.validate_partial_diet_input
  -> missing_required_fields
  -> app.domain.build_diet_outline when complete

tests
  -> app.domain pure functions
  -> app.graph compatibility wrapper
```
