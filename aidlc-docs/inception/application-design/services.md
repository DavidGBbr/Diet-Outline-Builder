# Services - Monorepo Conversational Agent Refactor

## Frontend Chat Service

Responsibilities:

- Own the browser WebSocket lifecycle.
- Serialize outgoing typed messages.
- Apply incoming assistant/result/error/state messages to UI state.
- Persist and restore local chat state through `localStorage`.

Interactions:

- Calls API WebSocket endpoint.
- Reads/writes browser `localStorage`.

## Backend WebSocket Service

Responsibilities:

- Accept local WebSocket connections.
- Validate incoming message envelope and payload.
- Enforce message size limits.
- Delegate valid turns to Conversation Service.
- Send typed outbound messages to the client.
- Handle errors safely.

Interactions:

- Receives typed JSON from web app.
- Calls Conversation Service.
- Sends typed JSON to web app.

## Conversation Service

Responsibilities:

- Treat each inbound message as one conversation turn.
- Use frontend-supplied state as the source of session state.
- Call the conversational LangGraph.
- Avoid direct diet math; delegate complete data to Diet Domain.
- Convert graph output into protocol messages.

Interactions:

- Calls Conversational Agent Graph.
- Returns updated state snapshots and response messages.

## Conversational Agent Service

Responsibilities:

- Execute LangGraph nodes for extraction, validation, missing-field prompts, calculation, and final response.
- Maintain graph-level separation between LLM extraction and deterministic validation.
- Ensure the conditional edge is the only route from validation to calculation or missing-field prompt.

Interactions:

- Calls Ollama Client for extraction.
- Calls Diet Domain for validation and final calculation.

## Ollama Extraction Service

Responsibilities:

- Encapsulate all local LLM calls.
- Use structured extraction prompts.
- Return only candidate fields, not trusted final data.
- Raise clear unavailable/model errors for local UI display.

Interactions:

- Calls Ollama HTTP API at configured base URL.
- Returns extracted candidates to Agent Graph.

## Diet Domain Service

Responsibilities:

- Own all deterministic nutrition calculations.
- Own strict validation rules.
- Expose pure functions for unit tests and partial PBT.
- Remain independent from FastAPI, Next.js, WebSockets, and Ollama.

Interactions:

- Called by Conversational Agent Graph.
- Tested directly by backend tests.

## Configuration Service

Responsibilities:

- Load local settings from root `.env`.
- Provide defaults for Ollama URL/model.
- Provide frontend origin allowlist for CORS.

Interactions:

- Used by API App, Ollama Client, and security middleware.

## Security Middleware Service

Responsibilities:

- Apply HTTP security headers for backend HTTP responses.
- Configure CORS with explicit local origins.
- Keep user-facing error responses generic and safe.

Interactions:

- Integrated into FastAPI app construction.
