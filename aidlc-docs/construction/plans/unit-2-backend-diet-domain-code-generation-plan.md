# Unit 2 Code Generation Plan - Backend Diet Domain Preservation

## Purpose

Implement the approved Unit 2 design by extracting deterministic diet validation and calculation into `apps/api/app/domain/`, preserving `app.graph` as a compatibility wrapper, adding Pydantic/Hypothesis dependencies, and expanding example plus property-based tests.

## Unit Context

- Unit: Unit 2 - Backend Diet Domain Preservation
- Depends On: Approved Unit 2 Functional Design, NFR Requirements, and NFR Design.
- Primary Story: Story 2 - Conversational Backend Collects Required Diet Data.
- Supporting Stories: Story 3 and Story 7.
- Security: SECURITY-05, SECURITY-09, and SECURITY-10 directly apply.
- PBT: PBT-03, PBT-07, PBT-08, and PBT-09 directly apply.

## Existing Files To Modify

- `apps/api/pyproject.toml`
- `apps/api/uv.lock`
- `apps/api/app/__init__.py`
- `apps/api/app/graph.py`
- `apps/api/tests/test_diet_graph.py`
- `aidlc-docs/aidlc-state.md`
- `aidlc-docs/audit.md`

## New Files To Create

- `apps/api/app/domain/__init__.py`
- `apps/api/app/domain/models.py`
- `apps/api/app/domain/validation.py`
- `apps/api/app/domain/calculator.py`
- `apps/api/tests/test_diet_domain.py`
- `apps/api/tests/test_diet_domain_properties.py`
- `aidlc-docs/construction/unit-2-backend-diet-domain/code/code-summary.md`

## Step-by-Step Generation Plan

### Step 1 - Add Dependencies

- [x] Add `pydantic>=2.7,<3` to runtime dependencies.
- [x] Add `hypothesis>=6,<7` to dev dependencies.
- [x] Run `uv lock` from `apps/api`.

### Step 2 - Create Domain Models

- [x] Create Pydantic model types for validated input, field errors, partial validation result, macros, and final response.
- [x] Create `DietValidationError` carrying structured field errors.
- [x] Enforce canonical fields and forbid unknown fields for complete validation.

### Step 3 - Create Domain Validation

- [x] Implement complete validation returning `ValidatedDietInput` or raising `DietValidationError`.
- [x] Implement partial validation returning accepted data, missing fields, and invalid fields.
- [x] Normalize supported goal aliases without accepting legacy height/weight aliases.

### Step 4 - Create Domain Calculator

- [x] Move deterministic BMI, BMR, energy, macro, explanation, and disclaimer logic into pure functions.
- [x] Preserve sample output behavior for canonical input.
- [x] Ensure macro calories stay within 5 kcal of target for valid generated inputs.

### Step 5 - Update Graph Compatibility Wrapper

- [x] Replace graph-owned diet math with delegation to the domain layer.
- [x] Preserve public `diet_graph` and `build_diet_outline` exports.
- [x] Keep `build_diet_outline` returning dict-compatible output for existing callers.

### Step 6 - Update Example-Based Tests

- [x] Update sample tests to canonical `heightCM` and `weightKG`.
- [x] Update invalid validation test to expect `DietValidationError`.
- [x] Add tests for legacy alias rejection.
- [x] Add tests for partial validation missing and invalid field behavior.

### Step 7 - Add Property-Based Tests

- [x] Add Hypothesis strategies for valid canonical diet inputs.
- [x] Assert positive calorie and macro invariants.
- [x] Assert BMI classification range invariants.
- [x] Assert macro calories stay within 5 kcal of target.

### Step 8 - Verification

- [x] Run `pnpm test:api`.
- [ ] Run `pnpm typecheck:web` if frontend files are touched. Not required for this backend-only unit.
- [ ] Run `pnpm build:web` if frontend files are touched. Not required for this backend-only unit.

### Step 9 - AI-DLC Code Summary Artifacts

- [x] Create Unit 2 code summary.
- [x] Update this code-generation plan checkboxes.
- [x] Update AI-DLC state and audit log.

## Security Compliance Plan

- SECURITY-05: Validate all complete and partial domain payloads through Pydantic-backed domain validation.
- SECURITY-09: Surface only structured field/message validation errors.
- SECURITY-10: Update `uv.lock` after dependency changes.

## PBT Compliance Plan

- PBT-03: Test diet calculation invariants across generated valid inputs.
- PBT-07: Use reusable domain-specific input strategies.
- PBT-08: Keep Hypothesis default shrinking and reproducibility.
- PBT-09: Use Hypothesis as the Python PBT framework.

## Approval Gate

The user instructed to continue if there are next steps. This plan has no unresolved choices and is treated as approved for Unit 2 implementation.
