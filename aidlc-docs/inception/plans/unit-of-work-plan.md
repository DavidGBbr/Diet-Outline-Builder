# Unit Of Work Plan - Monorepo Conversational Agent Refactor

## Purpose

Decompose the approved application design into manageable implementation units with clear responsibilities, dependencies, and story mappings.

## Context Summary

- Requirements approved for a pnpm monorepo with `apps/web` and `apps/api`.
- User stories approved with 7 stories across chat UX, extraction, conditional graph routing, final result, persistence, setup, and safe failures.
- Application Design approved with separate backend `agent/` and `domain/`, typed WebSocket messages, frontend-owned state, strict validation, and no public `/api/diet`.
- Security Baseline is enabled.
- Property-Based Testing is enabled in partial mode.

## Proposed Decomposition Approach

Use workflow/dependency-based units because this is a monorepo refactor with a strict build order:

1. Monorepo foundation
2. Backend domain preservation
3. Conversational agent graph
4. FastAPI WebSocket API
5. Next.js conversational UI
6. Documentation and verification

## Planned Unit Generation Steps

- [x] Confirm decomposition choices from the questions below.
- [x] Generate `aidlc-docs/inception/application-design/unit-of-work.md`.
- [x] Generate `aidlc-docs/inception/application-design/unit-of-work-dependency.md`.
- [x] Generate `aidlc-docs/inception/application-design/unit-of-work-story-map.md`.
- [x] Validate unit boundaries and dependency order.
- [x] Ensure all 7 user stories are assigned to units.
- [x] Include security/PBT responsibilities in relevant units.
- [x] Update AI-DLC state and audit log.

## Questions

Please answer all questions by filling the `[Answer]:` line, then tell me to continue.

### Question 1

Should unit boundaries follow the proposed workflow/dependency-based split?

A) Yes, use the proposed 6 units (recommended)
B) Merge documentation/verification into each implementation unit instead of a separate Unit 6
C) Split backend into more units: domain, agent, WebSocket, security, and config separately
X) Other (please describe after [Answer]: tag below)

[Answer]: option A

### Question 2

Should Unit 1 fully move the current Python package into `apps/api`, or create the monorepo shell first and move code in Unit 2?

A) Unit 1 should create monorepo shell and move existing backend into `apps/api` (recommended)
B) Unit 1 should create only monorepo shell; Unit 2 should move backend code
C) Keep root Python package until all features are rebuilt, then move at the end
X) Other (please describe after [Answer]: tag below)

[Answer]: option A

### Question 3

How should frontend work be sequenced relative to backend WebSocket work?

A) Build backend WebSocket first, then frontend integrates against it (recommended)
B) Build frontend static chat shell first, then backend integrates later
C) Build both in the same unit
X) Other (please describe after [Answer]: tag below)

[Answer]: option A

### Question 4

Where should PBT responsibilities be assigned?

A) Unit 2 only, because PBT applies to pure domain validation/calculation (recommended)
B) Unit 2 and Unit 3, including extraction/validation helper round-trips
C) Separate testing unit at the end only
X) Other (please describe after [Answer]: tag below)

[Answer]: option A

### Question 5

Where should Security Baseline implementation responsibilities be assigned?

A) Spread across relevant units: schema validation in backend units, headers/CORS in WebSocket/API and frontend units, lock files in foundation (recommended)
B) Create one separate security-hardening unit
C) Put all security work in final documentation/verification unit
X) Other (please describe after [Answer]: tag below)

[Answer]: option A

### Question 6

Should the old tests be moved early or rewritten gradually?

A) Move/adapt old backend tests during Unit 1/2 so regression coverage is preserved early (recommended)
B) Leave old tests at root until final verification
C) Rewrite all tests only after all code is migrated
X) Other (please describe after [Answer]: tag below)

[Answer]: option A

## Completion Criteria For Units Generation

- `unit-of-work.md` defines all implementation units and responsibilities.
- `unit-of-work-dependency.md` defines dependency order and parallelization constraints.
- `unit-of-work-story-map.md` maps all 7 stories to one or more units.
- Each unit has security and PBT implications documented where applicable.
- User explicitly approves generated units before moving to Construction phase.
