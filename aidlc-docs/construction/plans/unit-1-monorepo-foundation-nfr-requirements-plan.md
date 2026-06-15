# Unit 1 NFR Requirements Plan - Monorepo Foundation

## Purpose

Define non-functional requirements and tech-stack decisions for Unit 1 before code generation. Unit 1 is a local development foundation unit, so the key NFRs are reproducibility, maintainability, security-baseline compliance, and low-friction local setup.

## Unit Context

- Unit: Unit 1 - Monorepo Foundation
- Functional Design: `aidlc-docs/construction/unit-1-monorepo-foundation/functional-design/`
- Security Baseline: enabled
- PBT: partial, no implementation required in Unit 1

## Planned NFR Steps

- [x] Confirm NFR and tech-stack choices from the questions below.
- [x] Generate `aidlc-docs/construction/unit-1-monorepo-foundation/nfr-requirements/nfr-requirements.md`.
- [x] Generate `aidlc-docs/construction/unit-1-monorepo-foundation/nfr-requirements/tech-stack-decisions.md`.
- [x] Update AI-DLC state and audit log.

## NFR Questions

Please answer all questions by filling the `[Answer]:` line, then tell me to continue.

### Question 1

Which runtime versions should Unit 1 target/document?

A) Python 3.11+ and Node.js 20+ (recommended)
B) Current local Python/Node versions only
C) Python 3.12+ and Node.js 22+
X) Other (please describe after [Answer]: tag below)

[Answer]: option A

### Question 2

How strict should Unit 1 be if `uv` is not installed locally during implementation?

A) Fail and document that `uv` must be installed before proceeding (recommended for lock-file security)
B) Fall back to `pip` and create `uv.lock` later
C) Use `pip-tools` instead
X) Other (please describe after [Answer]: tag below)

[Answer]: option A

### Question 3

How strict should Unit 1 be if `pnpm` is not installed locally during implementation?

A) Fail and document that `pnpm` must be installed before proceeding (recommended for monorepo consistency)
B) Fall back to `npm` and convert later
C) Create package files without installing dependencies or generating lockfile
X) Other (please describe after [Answer]: tag below)

[Answer]: option A

### Question 4

Which default local ports should be documented in `.env.example` and scripts?

A) API `8000`, Web `3000`, Ollama `11434` (recommended)
B) API `8080`, Web `3000`, Ollama `11434`
C) Do not document ports until Unit 4/5
X) Other (please describe after [Answer]: tag below)

[Answer]: option A

### Question 5

How should Unit 1 handle Next.js security headers?

A) Add a basic `next.config.ts` with planned security headers now (recommended)
B) Add an empty `next.config.ts`; implement headers in Unit 5
C) Skip `next.config.ts` until Unit 5
X) Other (please describe after [Answer]: tag below)

[Answer]: option A

### Question 6

What is the minimum verification required after Unit 1 code generation?

A) Backend tests pass, frontend typecheck/build succeeds, lock files generated (recommended)
B) Backend tests pass only
C) File structure exists only; full verification waits for Unit 6
X) Other (please describe after [Answer]: tag below)

[Answer]: option A

## Security Baseline Applicability

- SECURITY-09 applies to avoiding unsafe demo/debug exposure in scaffolding.
- SECURITY-10 applies to dependency lock files and official registries.
- SECURITY-04 partially applies if Unit 1 creates initial Next.js/FastAPI header config.
- SECURITY-05 is prepared through package structure but detailed API validation belongs to later units.

## PBT Applicability

- PBT implementation is not required in Unit 1.
- Unit 1 must create a test layout that supports Unit 2 Hypothesis tests.
