# Unit 2 Functional Design Plan - Backend Diet Domain Preservation

## Purpose

Define the domain model, validation rules, pure calculation functions, missing-field behavior, and property-based testing targets before refactoring `apps/api/app/graph.py` into `apps/api/app/domain/`.

## Unit Context

- Unit: Unit 2 - Backend Diet Domain Preservation
- Primary Story: Story 4 - Receive The Final Diet Result
- Supporting Stories: Story 2, Story 3, Story 6, Story 7
- Depends On: Unit 1 - Monorepo Foundation
- Blocks: Unit 3 - Conversational LangGraph Agent

## Current Baseline

- Existing deterministic calculation lives in `apps/api/app/graph.py`.
- Existing tests live in `apps/api/tests/test_diet_graph.py`.
- Current validation accepts complete payloads and raises `ValueError` for invalid values.
- Current code does not expose a partial-input validator or `missing_required_fields` helper.
- Hypothesis is not yet installed.

## Planned Functional Design Steps

- [x] Confirm Unit 2 domain choices from the questions below.
- [x] Generate `aidlc-docs/construction/unit-2-backend-diet-domain/functional-design/business-logic-model.md`.
- [x] Generate `aidlc-docs/construction/unit-2-backend-diet-domain/functional-design/business-rules.md`.
- [x] Generate `aidlc-docs/construction/unit-2-backend-diet-domain/functional-design/domain-entities.md`.
- [x] Update AI-DLC state and audit log.

## Functional Design Questions

Please answer all questions by filling the `[Answer]:` line, then tell me to continue.

### Question 1

How should the domain code be split under `apps/api/app/domain/`?

A) `models.py`, `validation.py`, `calculator.py`, and `__init__.py` (recommended)
B) Single `diet.py` file with all domain logic
C) Keep logic in `graph.py` and only add helper functions
X) Other (please describe after [Answer]: tag below)

[Answer]: option A

### Question 2

What should strict validation return for complete inputs?

A) Pydantic models for typed validated inputs/results (recommended)
B) TypedDict dictionaries, preserving current style
C) Dataclasses without Pydantic
X) Other (please describe after [Answer]: tag below)

[Answer]: option A

### Question 3

How should partial input validation behave for missing fields?

A) Return accepted normalized fields, invalid field errors, and missing field names without raising for missing fields (recommended)
B) Raise on the first missing or invalid field
C) Only list missing fields; defer value validation until complete input exists
X) Other (please describe after [Answer]: tag below)

[Answer]: option A

### Question 4

Should legacy misspelled aliases remain supported in Unit 2?

A) Yes, keep `heighCM` and `weighKG` as input aliases for backward compatibility with existing sample/tests (recommended)
B) No, remove aliases and require only `heightCM` and `weightKG`
C) Keep aliases only in tests, not in production validation
X) Other (please describe after [Answer]: tag below)

[Answer]: option B

### Question 5

How should validation errors be represented for later conversation use?

A) Structured error objects with `field` and `message` (recommended)
B) Plain strings only
C) Raise raw exceptions and let Unit 3 parse exception text
X) Other (please describe after [Answer]: tag below)

[Answer]: option A

### Question 6

Which PBT properties should Unit 2 enforce first?

A) Valid generated inputs always produce positive calories/macros, BMI classification matches BMI ranges, and macro calories stay close to target (recommended)
B) Only macro calories stay close to target
C) Add broad randomized tests without explicit domain properties
X) Other (please describe after [Answer]: tag below)

[Answer]: option A

## Security Notes

- SECURITY-05 applies directly: strict type, enum, numeric range, and structured validation are required for diet inputs.
- Domain validation must not trust frontend or future Ollama-provided values.

## PBT Notes

- PBT-03 applies to documented invariants.
- PBT-07 requires domain-specific generated diet inputs.
- PBT-08 requires Hypothesis shrinking/reproducibility defaults to remain enabled.
- PBT-09 selects Hypothesis for Python.
