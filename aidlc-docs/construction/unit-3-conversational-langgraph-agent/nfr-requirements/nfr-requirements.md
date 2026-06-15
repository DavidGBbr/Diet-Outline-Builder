# NFR Requirements - Unit 3 Conversational LangGraph Agent

## Scope

Unit 3 adds the backend LangGraph conversation agent. The main NFRs are safe local LLM failure handling, deterministic validation authority, personal-data logging restraint, testability without a live Ollama process, and preserving the exact required conditional graph behavior.

## Reliability Requirements

- Ollama connectivity failures must return a safe `ollama_unavailable` error.
- Ollama malformed JSON responses must not crash the graph.
- Provider failures must not mutate existing collected data.
- The graph must be testable with injected fake extraction clients.

## Determinism Requirements

- Extracted LLM fields are candidates only.
- Unit 2 validation decides which fields are accepted.
- Unit 2 calculation decides the final diet result.
- Conditional routing must be deterministic from validated graph state.

## Security Requirements

- SECURITY-03: Do not log personal body data from messages or collected state.
- SECURITY-09: Return safe user-facing Ollama and agent errors without stack traces, internal paths, or raw provider dumps.
- SECURITY-11: Keep prompt and response handling bounded for the current turn. Full WebSocket size validation is deferred to Unit 4.

## Performance Requirements

- Ollama HTTP calls must have a finite timeout.
- Agent processing should complete in one backend turn without background jobs.
- Tests must not require a running Ollama service.

## Maintainability Requirements

- Put conversation code under `apps/api/app/agent/`.
- Separate graph orchestration, models, Ollama transport, and prompts.
- Keep transport/API concerns out of Unit 3; WebSocket mapping belongs to Unit 4.
- Keep final domain calculation delegated to `apps/api/app/domain`.

## Compatibility Requirements

- Unit 3 must not remove Unit 2 `app.graph` compatibility exports.
- Unit 3 agent state/result models must be ready for Unit 4 WebSocket schema mapping.

## Verification Requirements

- Tests must cover `data_incomplete` route.
- Tests must cover `data_ok` route.
- Tests must cover multi-field extraction and merge.
- Tests must cover invalid candidate data not overwriting valid existing data.
- Tests must cover Ollama unavailable safe error path.
- `pnpm test:api` must pass.
