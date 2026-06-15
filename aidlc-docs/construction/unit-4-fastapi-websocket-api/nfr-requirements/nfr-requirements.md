# NFR Requirements - Unit 4 FastAPI WebSocket API

## Security Requirements

- SECURITY-04: Add HTTP security headers for backend HTTP responses.
- SECURITY-05: Validate all WebSocket input payloads before calling the agent.
- SECURITY-08: Configure explicit local frontend CORS origins; do not use wildcard origins.
- SECURITY-09: Return safe user-facing errors only.
- SECURITY-11: Enforce current-turn message length bounds.

## Reliability Requirements

- WebSocket malformed payloads must not crash the server.
- Agent exceptions must be converted to safe error messages.
- Tests must not require live Ollama.

## Dependency Requirements

- Add `fastapi>=0.115,<1`.
- Add `uvicorn[standard]>=0.30,<1`.
- Add dev dependency `httpx>=0.27,<1` for FastAPI TestClient support.
- Update `uv.lock`.
