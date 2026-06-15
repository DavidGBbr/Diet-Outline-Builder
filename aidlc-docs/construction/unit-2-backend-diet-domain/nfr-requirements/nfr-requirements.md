# NFR Requirements - Unit 2 Backend Diet Domain Preservation

## Scope

Unit 2 turns the deterministic diet logic into a pure, validated domain layer. The main NFRs are validation safety, deterministic behavior, testability, dependency reproducibility, and property-based test coverage for documented domain invariants.

## Runtime Dependency Requirements

- Add `pydantic>=2.7,<3` as a runtime dependency for domain models and validation.
- Keep `langgraph` available because `app.graph` remains as a compatibility wrapper during Unit 2.
- Update `uv.lock` after dependency changes.

## Development Dependency Requirements

- Add `hypothesis>=6,<7` as a dev dependency.
- Preserve Hypothesis default shrinking and reproducibility behavior.
- Do not cap generated examples artificially low in Unit 2.

## Validation Requirements

- Complete validation must return Pydantic `ValidatedDietInput` when all fields are valid.
- Complete validation must raise `DietValidationError` with `errors: list[FieldValidationError]` when fields are missing or invalid.
- Complete validation errors must be safe, human-readable, and not expose stack traces or implementation details.
- Partial validation must return accepted data, missing field names, and structured invalid-field errors without raising for missing fields.
- Domain validation must reject misspelled aliases `heighCM` and `weighKG`; canonical fields are `heightCM` and `weightKG`.

## Determinism Requirements

- Domain calculation functions must be pure and deterministic.
- Domain calculation must not depend on FastAPI, WebSocket state, Ollama, frontend state, or environment variables.
- Existing final output behavior must be preserved except for canonical input field requirements.

## PBT Requirements

- PBT macro calorie tolerance: absolute tolerance of 5 kcal.
- Valid generated inputs must produce positive `totalSpend` and `targetSpend`.
- Valid generated inputs must produce positive protein and fat grams.
- Valid generated inputs must produce non-negative carbs.
- BMI classification must match calculated BMI ranges.
- Macro calories must stay close to target calories within 5 kcal.
- PBT generators must be domain-specific and produce valid canonical diet inputs.

## Security Requirements

- SECURITY-05: Validate all untrusted diet fields for type, required status, enum values, numeric ranges, and canonical names before calculation.
- SECURITY-09: Domain validation errors must be safe to surface through future API/UI layers.
- SECURITY-10: Dependency changes must update `uv.lock`.

## Maintainability Requirements

- Split domain code into `models.py`, `validation.py`, `calculator.py`, and `__init__.py`.
- Keep `app.graph` as a compatibility wrapper around the new domain layer until Unit 3 replaces graph flow.
- Keep tests organized so example-based tests and PBT tests are easy to distinguish.

## Verification Requirements

- Existing example-based tests must pass after being updated to canonical `heightCM` and `weightKG`.
- New partial validation tests must cover missing and invalid field behavior.
- New tests must prove misspelled aliases are no longer accepted.
- Hypothesis PBT tests must run as part of `pnpm test:api`.

## Compliance Summary

- SECURITY-05: Applicable and required through Pydantic/domain validation.
- SECURITY-09: Applicable and required through safe structured errors.
- SECURITY-10: Applicable and required through `uv.lock` update.
- PBT-03: Applicable to domain invariants.
- PBT-07: Applicable to valid diet input generators.
- PBT-08: Applicable through Hypothesis defaults.
- PBT-09: Applicable through Hypothesis selection.
