# Code Summary - Unit 2 Backend Diet Domain Preservation

## Implemented

- Extracted deterministic diet validation and calculation into `apps/api/app/domain/`.
- Added Pydantic domain models and structured validation errors.
- Added complete validation with `DietValidationError`.
- Added partial validation that returns accepted data, missing fields, and invalid field errors.
- Removed support for legacy misspelled `heighCM` and `weighKG` aliases.
- Kept `app.graph` as a LangGraph compatibility wrapper over the domain layer.
- Added Hypothesis property-based tests for diet invariants.
- Updated example-based tests to canonical `heightCM` and `weightKG` fields.

## Files Added

- `apps/api/app/domain/__init__.py`
- `apps/api/app/domain/models.py`
- `apps/api/app/domain/validation.py`
- `apps/api/app/domain/calculator.py`
- `apps/api/tests/test_diet_domain.py`
- `apps/api/tests/test_diet_domain_properties.py`
- `aidlc-docs/construction/unit-2-backend-diet-domain/code/code-summary.md`

## Files Modified

- `apps/api/pyproject.toml`
- `apps/api/uv.lock`
- `apps/api/app/graph.py`
- `apps/api/tests/test_diet_graph.py`
- `aidlc-docs/aidlc-state.md`
- `aidlc-docs/audit.md`
- `aidlc-docs/construction/plans/unit-2-backend-diet-domain-code-generation-plan.md`

## Dependency Changes

- Added runtime dependency: `pydantic>=2.7,<3`.
- Added dev dependency: `hypothesis>=6,<7`.
- Updated `apps/api/uv.lock`.

## Verification

- `pnpm test:api`: passed, 12 tests.

## Notes

- Frontend files were not touched, so web typecheck/build were not required for this backend-only unit.
- Macro calculation preserves existing sample output and scales protein/fat only when fixed BMI-based grams would exceed the calorie target, keeping macro calories within the approved 5 kcal tolerance.
