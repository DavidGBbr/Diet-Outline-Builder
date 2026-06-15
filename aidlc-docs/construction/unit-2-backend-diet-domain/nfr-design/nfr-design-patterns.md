# NFR Design Patterns - Unit 2 Backend Diet Domain Preservation

## Pattern 1 - Strict Domain Boundary

### Requirement

Diet calculations must be deterministic, pure, and independent from transport/LLM layers.

### Design

- Place all deterministic domain logic in `apps/api/app/domain/`.
- Keep `app.graph` as a wrapper that delegates to domain functions.
- Domain modules must not import FastAPI, WebSocket, Ollama, or frontend-related code.

### Rationale

This keeps future conversational and API layers from duplicating or corrupting core calculation logic.

## Pattern 2 - Pydantic Validation Boundary

### Requirement

All untrusted diet input must be validated before calculation.

### Design

- `models.py` defines Pydantic models for validated inputs, partial inputs, field errors, macros, and final response.
- `validation.py` exposes complete and partial validators.
- Complete validation returns `ValidatedDietInput` or raises `DietValidationError`.
- Partial validation returns `PartialValidationResult` without raising for missing fields.

### Rationale

This satisfies SECURITY-05 and gives Unit 3 structured validation information for conversation prompts.

## Pattern 3 - Canonical Field Enforcement

### Requirement

Unit 2 removes legacy misspelled input aliases.

### Design

- Accept only `heightCM` and `weightKG`.
- Treat `heighCM` and `weighKG` as unknown/missing canonical fields.
- Update tests and samples to canonical field names.

### Rationale

Strict canonical fields simplify future WebSocket state schemas and Ollama extraction validation.

## Pattern 4 - Safe Structured Error Surface

### Requirement

Validation errors must be safe for later API/UI display.

### Design

- `FieldValidationError` contains only `field` and `message`.
- `DietValidationError` contains `errors: list[FieldValidationError]`.
- Exception string is concise and human-readable.
- Unit 3/4 should use structured errors instead of parsing exception text.

### Rationale

This supports SECURITY-09 by avoiding raw Pydantic internals or stack traces in user-facing layers.

## Pattern 5 - Domain-Specific PBT Generators

### Requirement

PBT must use realistic domain inputs.

### Design

- Create reusable Hypothesis strategies in backend tests for valid canonical diet inputs.
- Generate constrained values:
  - `sex`: `male` or `female`
  - `age`: 13 to 120
  - `heightCM`: 100 to 250
  - `weightKG`: 30 to 300
  - `activityLevel`: `low`, `moderate`, `high`
  - `goal`: accepted goal aliases/canonical values
- Avoid raw unconstrained primitive generators for domain payloads.

### Rationale

This satisfies PBT-07 and avoids meaningless randomized tests.

## Pattern 6 - Invariant-Based PBT

### Requirement

Domain invariants must be tested across generated inputs.

### Design

Property-based tests assert:

- Valid generated inputs produce positive `totalSpend` and `targetSpend`.
- Valid generated inputs produce positive protein and fat.
- Valid generated inputs produce non-negative carbs.
- BMI classification matches BMI range boundaries.
- Macro calories are within 5 kcal of `targetSpend`.

### Rationale

This satisfies PBT-03 and catches formula regressions beyond fixed example cases.

## Pattern 7 - Lock-File Dependency Update

### Requirement

Dependency changes must remain reproducible.

### Design

- Add bounded Pydantic and Hypothesis dependencies in `apps/api/pyproject.toml`.
- Run `uv lock` after changes.
- Verify `apps/api/uv.lock` updates.

### Rationale

This satisfies SECURITY-10 for supply-chain reproducibility.

## Security Compliance

- SECURITY-05: Implemented through Pydantic domain validation before calculation.
- SECURITY-09: Implemented through structured, safe domain errors.
- SECURITY-10: Implemented through bounded dependencies and `uv.lock` update.

## PBT Compliance

- PBT-03: Invariant tests for domain calculations.
- PBT-07: Reusable domain-specific strategies.
- PBT-08: Hypothesis defaults preserve shrinking/reproducibility.
- PBT-09: Hypothesis selected as Python PBT framework.
