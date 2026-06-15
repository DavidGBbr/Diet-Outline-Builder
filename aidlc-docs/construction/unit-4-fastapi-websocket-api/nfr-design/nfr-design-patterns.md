# NFR Design Patterns - Unit 4 FastAPI WebSocket API

## Pattern 1 - Schema First WebSocket Boundary

- Parse every incoming WebSocket JSON payload through Pydantic.
- Return safe `error` messages on validation failure.

## Pattern 2 - Dependency-Injectable Conversation Runner

- Store the conversation runner on `app.state`.
- Tests replace it with a fake runner to avoid live Ollama.

## Pattern 3 - Safe Error Translation

- Catch validation and runtime failures at the WebSocket boundary.
- Send `error` messages without stack traces or internal paths.

## Pattern 4 - Local-Only CORS

- Allow only `http://127.0.0.1:3000` and `http://localhost:3000` by default.

## Pattern 5 - Security Headers Middleware

- Add baseline headers on HTTP responses: `X-Content-Type-Options`, `Referrer-Policy`, and `X-Frame-Options`.
