# Tech Stack Decisions - Unit 2 Backend Diet Domain Preservation

## Runtime Validation Framework

Decision: Add `pydantic>=2.7,<3` as a runtime dependency.

Rationale:

- Matches approved functional design for Pydantic domain models.
- Provides typed validation, field constraints, serialization helpers, and structured validation behavior.
- Avoids relying on LangGraph's transitive Pydantic dependency.
- Upper bound avoids accidental Pydantic 3 breaking changes.

## Property-Based Testing Framework

Decision: Add `hypothesis>=6,<7` as a dev dependency.

Rationale:

- Satisfies PBT-09 for Python.
- Provides custom strategies for domain-specific generators.
- Supports shrinking and reproducibility by default, satisfying PBT-08.
- Upper bound avoids accidental Hypothesis 7 breaking changes.

## Macro Calorie Tolerance

Decision: Use absolute tolerance of 5 kcal for macro calories vs target calories.

Rationale:

- Matches the existing example-based test.
- Accounts for gram rounding in protein, fat, and carbohydrate calculations.
- Keeps the property strict enough to catch formula regressions.

## Validation Error Strategy

Decision: Raise `DietValidationError` for complete validation failures with structured `FieldValidationError` entries.

Rationale:

- Keeps complete validation strict for calculation safety.
- Provides structured field-level errors for Unit 3 conversation prompts.
- Avoids parsing raw exception text later.
- Avoids exposing raw Pydantic internals through future API/UI layers.

## Graph Compatibility Strategy

Decision: Keep `app.graph` as a compatibility wrapper around the new domain functions during Unit 2.

Rationale:

- Preserves current public backend test path.
- Reduces risk while refactoring the domain.
- Allows Unit 3 to replace/add conversational graph behavior without coupling domain code to LangGraph.

## Canonical Field Strategy

Decision: Remove `heighCM` and `weighKG` alias support.

Rationale:

- Matches user decision in Unit 2 Functional Design.
- Reduces ambiguity for future LLM extraction and WebSocket state schemas.
- Forces canonical field names before conversation flow is implemented.

## Dependency Lock Strategy

Decision: Update `apps/api/uv.lock` after adding Pydantic and Hypothesis.

Rationale:

- Maintains SECURITY-10 lock-file reproducibility.
- Keeps Unit 2 dependency changes auditable.
