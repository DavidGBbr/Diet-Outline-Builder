# Application Design - Monorepo Conversational Agent Refactor

## Design Decisions

- Backend organization: separate `agent/` for conversational LangGraph logic and `domain/` for deterministic diet calculation.
- WebSocket protocol: simple typed JSON messages.
- Conversation state: frontend sends full state each turn; backend returns updated state snapshots.
- Validation: strict deterministic validator accepts only allowed enums and numeric ranges.
- Frontend UX: show a small collected-data summary before final result.
- Direct calculation endpoint: remove public `/api/diet`; keep calculation internally callable by graph/tests.
- Security headers: FastAPI middleware for backend HTTP responses and Next.js config for frontend headers.
- CLI: drop from target monorepo unless needed in a later phase.

## Target Repository Layout

```text
apps/
  api/
    app/
      agent/
      domain/
      schemas/
      services/
      main.py
    tests/
    pyproject.toml
  web/
    app/
    components/
    lib/
    next.config.ts
    package.json
pnpm-workspace.yaml
package.json
.env.example
README.md
```

## Backend Design

The backend is a FastAPI service that exposes a local WebSocket chat endpoint. It validates every incoming message, delegates a conversation turn to the Conversation Service, and returns typed protocol messages.

The backend separates concerns:

- `agent/`: LangGraph conversation orchestration, Ollama extraction, conditional routing.
- `domain/`: deterministic diet validation and calculation.
- `schemas/`: Pydantic message and state contracts.
- `services/`: WebSocket and conversation orchestration.

## Frontend Design

The frontend is a Next.js app focused on a minimal chat experience. It owns local durable conversation state using `localStorage`, sends that state with every user message, and updates local storage from backend `state_snapshot` events.

The frontend does not calculate diet formulas and does not call Ollama directly.

## LangGraph Design

The conversational graph handles a full turn:

```text
START
  -> extractData
  -> mergeValidFields
  -> validateData
  -> conditional edge
       data_ok -> calculateDiet -> generateResponse -> END
       data_incomplete -> askRemainingData -> END
```

The graph trusts only deterministic validation. Ollama outputs are treated as candidate fields, not authoritative state.

## Security Design Summary

- SECURITY-03: No unnecessary logging of personal body data.
- SECURITY-04: FastAPI and Next.js both own security headers for their served content.
- SECURITY-05: Pydantic schemas validate WebSocket messages and conversation state.
- SECURITY-08: Endpoints are local public endpoints by design; CORS is restricted to explicit local web origins.
- SECURITY-09: Errors shown to users are safe and do not expose stack traces/internal paths.
- SECURITY-10: pnpm lock file and Python lock strategy are required during implementation.
- SECURITY-11: WebSocket messages have length/size limits.

## PBT Design Summary

Partial PBT applies to pure backend functions:

- Diet input validation invariants.
- BMI classification range invariants.
- Macro calories are non-negative and stay close to target calories.
- Domain-specific generators produce valid diet input payloads.
- Hypothesis is selected for Python PBT.

## Design Completeness Check

- Components defined: yes.
- Component methods defined: yes.
- Services and orchestration defined: yes.
- Dependencies and data flow defined: yes.
- Security baseline responsibilities assigned: yes.
- PBT partial responsibilities assigned: yes.
- Remaining detail moves to Units Generation and per-unit Functional/NFR Design.
