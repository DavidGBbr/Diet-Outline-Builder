# Workflow Planning - Monorepo Conversational Agent Refactor

## Context Loaded

- Requirements: `aidlc-docs/inception/requirements/requirements.md`
- Requirements questions: `aidlc-docs/inception/requirements/requirement-verification-questions.md`
- Follow-up questions: `aidlc-docs/inception/requirements/requirement-follow-up-questions.md`
- Reverse engineering baseline: `aidlc-docs/inception/reverse-engineering/`
- Security Baseline extension: enabled
- Property-Based Testing extension: partial mode

## Scope And Impact Analysis

This is a system-wide brownfield refactor.

## Impact Areas

- Repository structure: root package becomes pnpm monorepo with `apps/web` and `apps/api`.
- Backend packaging: existing `src/diet_outline_builder` package migrates into `apps/api`.
- Frontend architecture: inline FastAPI-served form UI is replaced by Next.js chat UI.
- API interface: form POST flow is replaced by WebSocket chat flow.
- LangGraph architecture: calculation graph remains reusable, and a new conversation graph manages extraction, missing-field validation, conditional routing, and final calculation.
- Local runtime: root scripts and docs must run Ollama, backend, and frontend.
- Tests: existing calculation tests must move/adapt; WebSocket/backend tests must be added; partial PBT must cover pure validation/calculation properties.

## Risk Assessment

- Risk level: Medium-high.
- Main risks:
  - Monorepo migration can break imports, scripts, and tests.
  - Ollama availability can make local testing flaky if not handled clearly.
  - LLM extraction can be inconsistent without schema validation and deterministic fallbacks.
  - Security Baseline adds constraints around input bounds, CORS, security headers, and dependency locking.

## Selected AI-DLC Stages

- Reverse Engineering: Completed because this is now a brownfield refactor.
- Requirements Analysis: Completed with question file and follow-up questions.
- User Stories: Execute, because this changes user interaction from form to conversational UI and needs acceptance criteria.
- Application Design: Execute, because new backend/frontend components and WebSocket contracts are required.
- Units Generation: Execute, because work spans multiple modules and must be sequenced.
- Functional Design: Execute per unit, because conversation state, extraction, validation, and conditional graph routing require detailed design.
- NFR Requirements: Execute per unit where relevant, because Security Baseline and local LLM reliability matter.
- NFR Design: Execute where security headers, CORS, input validation, and dependency locking need design.
- Infrastructure Design: Skip for cloud infrastructure; include local runtime design inside NFR/build docs.
- Code Generation: Execute per unit after approval gates.
- Build and Test: Execute after implementation.

## Proposed Units Of Work

### Unit 1 - Monorepo Foundation

- Create pnpm workspace root.
- Move Python backend into `apps/api`.
- Create Next.js app in `apps/web`.
- Add root `.env.example` and local run scripts.
- Preserve backend test execution.

### Unit 2 - Backend Diet Domain Preservation

- Preserve deterministic calculation graph behavior.
- Keep or adapt `build_diet_outline` API inside `apps/api`.
- Add PBT for pure validation/calculation invariants where applicable.
- Maintain existing sample output expectations.

### Unit 3 - Conversational LangGraph Agent

- Add conversation state model.
- Add Ollama-backed field extraction.
- Add `validateData` node.
- Add conditional edge:
  - `data_ok` -> `calculateDiet`
  - `data_incomplete` -> `askRemainingData`
- Add final response generation.
- Add clear Ollama unavailable error handling.

### Unit 4 - FastAPI WebSocket API

- Add WebSocket chat endpoint.
- Validate message schemas, length bounds, and session payloads.
- Restrict CORS to local frontend origins.
- Add security headers for HTTP responses where applicable.
- Add backend WebSocket tests.

### Unit 5 - Next.js Conversational UI

- Replace old form UI with clean minimal chat interface.
- Connect to WebSocket backend.
- Persist conversation state with localStorage.
- Render final diet result in chat.
- Render Ollama/backend errors clearly.

### Unit 6 - Documentation And Verification

- Update README with monorepo setup.
- Document Ollama install/start/pull model steps.
- Document root scripts.
- Run backend tests and any required frontend checks.
- Update AI-DLC build/test artifacts.

## Execution Sequence

1. User Stories
2. Application Design
3. Units Generation
4. Per-unit Functional/NFR Design
5. Code Generation per unit in dependency order
6. Build and Test

## Dependency Order

- Unit 1 must run before all other units.
- Unit 2 must run before Unit 3.
- Unit 3 must run before Unit 4 can be fully tested.
- Unit 4 must run before Unit 5 can integrate.
- Unit 6 runs after all implementation units.

## Testing Strategy

- Backend example-based tests for calculations and validation.
- Backend WebSocket tests for incomplete data, complete data, and Ollama unavailable error.
- Partial PBT with Hypothesis for pure validation/calculation invariants.
- Frontend component/e2e tests are out of scope for this phase per requirements, but frontend build/typecheck should pass if Next.js tooling is installed.

## Security Baseline Planning

- SECURITY-01: N/A, no backend persistence store.
- SECURITY-02: N/A, no deployed network intermediary in this local phase.
- SECURITY-03: Applicable in design/code generation: avoid logging personal body data.
- SECURITY-04: Applicable for HTTP endpoints serving web content.
- SECURITY-05: Applicable for WebSocket and API message validation.
- SECURITY-06: N/A, no IAM policies.
- SECURITY-07: N/A for local-only runtime; no cloud network config.
- SECURITY-08: Local public endpoints are intentionally unauthenticated and must be documented. CORS must still be restricted.
- SECURITY-09: Applicable: no stack traces/internal paths in user-facing errors.
- SECURITY-10: Applicable: lock files and official registries required.
- SECURITY-11: Applicable: rate limiting/abuse handling should be considered for local API; at minimum message length limits are required.
- SECURITY-12: N/A, no authentication in scope.

## PBT Planning

Partial mode enforces PBT-02, PBT-03, PBT-07, PBT-08, and PBT-09 where applicable.

- PBT-02: Round-trip properties apply if structured extraction parse/serialize helpers are added.
- PBT-03: Invariant properties apply to BMI ranges, macro calorie non-negativity, and validation constraints.
- PBT-07: Domain-specific generators are required for diet inputs.
- PBT-08: Hypothesis shrinking/reproducibility must remain enabled.
- PBT-09: Hypothesis is selected for Python PBT.

## Approval Gate

This workflow plan requires explicit user approval before User Stories/Application Design begin.
