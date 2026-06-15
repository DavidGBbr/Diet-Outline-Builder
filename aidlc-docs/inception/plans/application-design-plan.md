# Application Design Plan - Monorepo Conversational Agent Refactor

## Purpose

Define high-level components, interfaces, service responsibilities, and dependency relationships for the approved monorepo conversational diet builder.

## Context Summary

- Requirements approved for a pnpm monorepo with `apps/web` and `apps/api`.
- User stories approved for guided chat, extraction, conditional LangGraph validation, final result, local persistence, local setup, and safe error handling.
- Security Baseline is enabled.
- Property-Based Testing is enabled in partial mode.

## Planned Application Design Steps

- [x] Confirm design decisions from the questions below.
- [x] Generate `aidlc-docs/inception/application-design/components.md`.
- [x] Generate `aidlc-docs/inception/application-design/component-methods.md`.
- [x] Generate `aidlc-docs/inception/application-design/services.md`.
- [x] Generate `aidlc-docs/inception/application-design/component-dependency.md`.
- [x] Generate consolidated `aidlc-docs/inception/application-design/application-design.md`.
- [x] Validate security baseline applicability for the high-level design.
- [x] Validate PBT partial-mode implications for design.
- [x] Update AI-DLC state and audit log.

## Proposed Component Groups

- `apps/web`: Next.js chat UI, WebSocket client, localStorage persistence, result rendering.
- `apps/api`: FastAPI app, WebSocket endpoint, conversation service, LangGraph agent graph, diet calculation domain, Ollama client, validation/schemas, security middleware/config.
- Root workspace: pnpm workspace config, root scripts, `.env.example`, docs.

## Design Questions

Please answer all questions by filling the `[Answer]:` line, then tell me to continue.

### Question 1

How should the backend organize the LangGraph logic inside `apps/api`?

A) Separate `agent/` for conversational graph and `domain/` for deterministic diet calculation (recommended)
B) Single `graph/` package containing both conversational and calculation graphs
C) Keep the current `diet_outline_builder` package name inside `apps/api/src`
X) Other (please describe after [Answer]: tag below)

[Answer]: option A

### Question 2

What WebSocket message protocol should the first version use?

A) Simple typed JSON messages: `user_message`, `assistant_message`, `diet_result`, `error`, `state_snapshot` (recommended)
B) Minimal protocol with only `{ message: string }` in and `{ reply: string }` out
C) Event-sourced protocol with message IDs, timestamps, and explicit acknowledgements
X) Other (please describe after [Answer]: tag below)

[Answer]: option A

### Question 3

Where should conversation state live during a WebSocket session?

A) Frontend sends full state each turn; backend returns updated state (recommended for no backend persistence)
B) Backend keeps in-memory state per WebSocket connection only
C) Backend keeps process-wide session state by generated session ID
X) Other (please describe after [Answer]: tag below)

[Answer]: option A

### Question 4

How strict should the deterministic validator be when Ollama extracts ambiguous fields?

A) Strict: accept only values that exactly match allowed enums/ranges, ask again otherwise (recommended)
B) Lenient: normalize likely synonyms and infer values when possible
C) Mixed: exact validation for numeric fields, lenient normalization for goal/activity terms
X) Other (please describe after [Answer]: tag below)

[Answer]: option A

### Question 5

Should the frontend show collected data before the final result?

A) Yes, show a small “collected so far” summary beside/under chat (recommended)
B) No, keep only chat messages until final result
C) Show collected data only in a collapsible debug panel
X) Other (please describe after [Answer]: tag below)

[Answer]: option A

### Question 6

How should the old direct `/api/diet` calculation endpoint be handled?

A) Keep it internally/test-only in the backend but do not expose it in the frontend (recommended)
B) Remove it completely and only calculate through the conversation graph
C) Keep it public as a documented backend endpoint
X) Other (please describe after [Answer]: tag below)

[Answer]: option B

### Question 7

How should local security headers be applied?

A) FastAPI middleware for API docs/health endpoints plus Next.js config for frontend headers (recommended)
B) Only Next.js config because the browser primarily hits the frontend
C) Skip strict headers for local development and document the exception
X) Other (please describe after [Answer]: tag below)

[Answer]: option A

### Question 8

Should the application design preserve the CLI?

A) No, drop CLI from the target monorepo unless needed later (recommended)
B) Yes, preserve CLI in `apps/api` for direct calculation only
C) Yes, add a CLI chat mode too
X) Other (please describe after [Answer]: tag below)

[Answer]: option A

## Security Baseline Design Notes

- SECURITY-03: Design must avoid logging personal body data from chat payloads.
- SECURITY-04: Design must assign responsibility for HTTP security headers.
- SECURITY-05: Design must assign schema validation to all WebSocket messages and backend API payloads.
- SECURITY-08: Local public endpoints must be documented as unauthenticated by design; CORS must be explicit.
- SECURITY-09: Design must include safe user-facing error boundaries.
- SECURITY-10: Design must preserve lock files for pnpm and Python dependencies.
- SECURITY-11: Design must include message size limits and abuse constraints for local WebSocket usage.

## PBT Partial Design Notes

- PBT-03: Diet calculation invariants and validation invariants should be designed as pure functions.
- PBT-07: Domain generators should exist for valid diet input payloads.
- PBT-08: Use the selected PBT framework defaults without disabling shrinking.
- PBT-09: Hypothesis is selected for Python property-based tests.
