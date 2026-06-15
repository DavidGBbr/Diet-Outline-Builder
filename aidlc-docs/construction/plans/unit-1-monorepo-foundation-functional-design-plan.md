# Unit 1 Functional Design Plan - Monorepo Foundation

## Purpose

Define the functional behavior and migration rules for Unit 1 before code generation: create the pnpm monorepo, move the existing Python backend into `apps/api`, create a Next.js shell in `apps/web`, preserve existing backend tests, and establish root configuration.

## Unit Context

- Unit: Unit 1 - Monorepo Foundation
- Primary Story: Story 6 - Run The Monorepo Locally With Ollama
- Supporting Stories: Story 1, Story 2, Story 7
- Depends On: Approved Units Generation
- Blocks: Units 2-6

## Planned Functional Design Steps

- [x] Confirm the Unit 1 implementation choices from the questions below.
- [x] Generate `aidlc-docs/construction/unit-1-monorepo-foundation/functional-design/business-logic-model.md`.
- [x] Generate `aidlc-docs/construction/unit-1-monorepo-foundation/functional-design/business-rules.md`.
- [x] Generate `aidlc-docs/construction/unit-1-monorepo-foundation/functional-design/domain-entities.md`.
- [x] Generate `aidlc-docs/construction/unit-1-monorepo-foundation/functional-design/frontend-components.md`.
- [x] Update AI-DLC state and audit log.

## Functional Design Questions

Please answer all questions by filling the `[Answer]:` line, then tell me to continue.

### Question 1

Which Python dependency/lock strategy should `apps/api` use for Unit 1?

A) Keep `pip`/`pyproject.toml` for now and add exact dependency pins later during verification
B) Use `uv` with `pyproject.toml` and `uv.lock` from the start (recommended for lock-file security)
C) Use Poetry with `poetry.lock`
X) Other (please describe after [Answer]: tag below)

[Answer]: option B

### Question 2

How should the existing Python package be renamed when moved into `apps/api`?

A) Rename package to `app` following the approved design layout (recommended)
B) Keep package name `diet_outline_builder` inside `apps/api/src`
C) Use package name `diet_api`
X) Other (please describe after [Answer]: tag below)

[Answer]: option A

### Question 3

How should Unit 1 create the Next.js app shell?

A) Minimal hand-written Next.js app files without using an interactive generator (recommended)
B) Use `create-next-app` if available
C) Create only `apps/web/package.json` now and leave app files for Unit 5
X) Other (please describe after [Answer]: tag below)

[Answer]: option A

### Question 4

Which root scripts should Unit 1 add first?

A) `dev:api`, `dev:web`, `test:api`, `lint:web`/`typecheck:web` placeholders as available (recommended)
B) Only installation scripts; run commands wait until later units
C) Add a single root `dev` script that starts both API and web immediately
X) Other (please describe after [Answer]: tag below)

[Answer]: option A

### Question 5

Should Unit 1 remove the old root `src/` and root `tests/` immediately after moving them?

A) Yes, remove old root copies once moved to avoid duplicate sources/tests (recommended)
B) Keep old root copies temporarily until Unit 6 verification
C) Keep old root source but remove old root tests
X) Other (please describe after [Answer]: tag below)

[Answer]: option A

### Question 6

Should Unit 1 remove the old local form UI code immediately?

A) Yes, remove the form UI while moving backend, because target design removes it (recommended)
B) Keep it temporarily inside `apps/api` until Unit 5 replaces UI
C) Keep it as a debug-only route despite the approved design
X) Other (please describe after [Answer]: tag below)

[Answer]: option A

## Unit 1 Security Notes

- SECURITY-10 requires lock files or an approved lock strategy.
- SECURITY-09 requires avoiding accidental exposed demo/default pages beyond local dev scaffolding.
- No authentication, persistence, cloud infrastructure, IAM, or database security concerns apply in Unit 1.

## Unit 1 PBT Notes

- No PBT implementation is required in Unit 1.
- Unit 1 must preserve test structure so Unit 2 can add Hypothesis PBT cleanly.
