# Unit 2 NFR Requirements Plan - Backend Diet Domain Preservation

## Purpose

Define non-functional requirements and tech-stack decisions for Unit 2 before implementation. Unit 2 introduces Pydantic domain models, structured validation, strict canonical field handling, and Hypothesis property-based tests.

## Unit Context

- Unit: Unit 2 - Backend Diet Domain Preservation
- Functional Design: `aidlc-docs/construction/unit-2-backend-diet-domain/functional-design/`
- Security Baseline: enabled
- PBT: partial, directly applicable in Unit 2

## Planned NFR Steps

- [x] Confirm NFR and tech-stack choices from the questions below.
- [x] Generate `aidlc-docs/construction/unit-2-backend-diet-domain/nfr-requirements/nfr-requirements.md`.
- [x] Generate `aidlc-docs/construction/unit-2-backend-diet-domain/nfr-requirements/tech-stack-decisions.md`.
- [x] Update AI-DLC state and audit log.

## NFR Questions

Please answer all questions by filling the `[Answer]:` line, then tell me to continue.

### Question 1

How should Pydantic be added for domain models?

A) Add `pydantic>=2.7,<3` as a runtime dependency (recommended)
B) Add unbounded `pydantic>=2`
C) Avoid adding Pydantic and use current transitive dependency from LangGraph
X) Other (please describe after [Answer]: tag below)

[Answer]: option A

### Question 2

How should Hypothesis be configured for PBT?

A) Add `hypothesis>=6,<7` to dev dependencies with default shrinking/reproducibility behavior (recommended)
B) Add Hypothesis but cap generated examples very low for speed
C) Defer Hypothesis until Unit 6
X) Other (please describe after [Answer]: tag below)

[Answer]: option A

### Question 3

What tolerance should PBT use for macro calories vs target calories?

A) Absolute tolerance of 5 kcal, matching current example-based test (recommended)
B) Absolute tolerance of 10 kcal
C) Exact equality only
X) Other (please describe after [Answer]: tag below)

[Answer]: option A

### Question 4

How should structured validation errors be exposed in complete validation failures?

A) Raise `DietValidationError` with `errors: list[FieldValidationError]` and a safe human-readable message (recommended)
B) Raise Pydantic raw `ValidationError` directly
C) Return result objects only, never raise
X) Other (please describe after [Answer]: tag below)

[Answer]: option A

### Question 5

Should Unit 2 keep the existing calculation LangGraph wrapper?

A) Yes, keep `app.graph` as a compatibility wrapper around the new domain functions until Unit 3 replaces graph flow (recommended)
B) Remove `app.graph` and expose only domain functions
C) Move LangGraph into `domain/` alongside pure functions
X) Other (please describe after [Answer]: tag below)

[Answer]: option A

## Security Baseline Applicability

- SECURITY-05 applies directly: all untrusted diet fields must receive type, enum, range, and required-field validation before calculation.
- SECURITY-09 applies to safe error messages: complete validation should not expose stack traces or internal details.
- SECURITY-10 applies to dependency lock updates through `uv.lock`.

## PBT Applicability

- PBT-03 applies to BMI classification, positive energy/macros, and macro calorie proximity invariants.
- PBT-07 applies to domain-specific valid diet input generators.
- PBT-08 applies through Hypothesis default shrinking/reproducibility.
- PBT-09 applies through Hypothesis framework selection.
