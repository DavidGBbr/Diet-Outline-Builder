# Tech Stack Decisions - Unit 5 Next.js Conversational UI

## WebSocket Client

Decision: Use the browser native `WebSocket` API.

Rationale: No additional dependency is needed for a local single-endpoint chat flow.

## Persistence

Decision: Use browser `localStorage`.

Rationale: It is explicitly required and sufficient for local-only conversation state.
