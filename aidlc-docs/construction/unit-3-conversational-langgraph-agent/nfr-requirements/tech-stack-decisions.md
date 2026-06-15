# Tech Stack Decisions - Unit 3 Conversational LangGraph Agent

## Graph Framework

Decision: Continue using `langgraph`.

Rationale:

- Already present from Units 1 and 2.
- Required by the approved architecture.
- Supports explicit node names and conditional routing tests.

## Ollama Transport

Decision: Use Python standard library `urllib.request` for the Unit 3 Ollama client.

Rationale:

- Avoids adding a runtime HTTP dependency before FastAPI/WebSocket work.
- The required Ollama call is a single local JSON POST.
- Keeps Unit 3 dependency surface small.

## Test Strategy

Decision: Use injected fake extraction clients for graph tests.

Rationale:

- Tests must be deterministic and not require a local Ollama daemon.
- Allows direct coverage of happy path, incomplete path, invalid candidate merge, and provider failure.

## Error Model

Decision: Use structured `AgentError` with safe `code` and `message` fields.

Rationale:

- Supports Unit 4 WebSocket error mapping.
- Keeps user-facing errors safe and concise.
- Avoids leaking raw exceptions or provider responses.

## Dependency Strategy

Decision: No new Unit 3 dependencies unless implementation proves standard library transport insufficient.

Rationale:

- Pydantic and LangGraph are already available.
- Lower supply-chain surface supports SECURITY-10.
