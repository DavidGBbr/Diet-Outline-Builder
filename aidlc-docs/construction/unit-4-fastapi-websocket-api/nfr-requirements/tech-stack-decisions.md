# Tech Stack Decisions - Unit 4 FastAPI WebSocket API

## API Framework

Decision: Use FastAPI.

Rationale: It is the approved backend framework and integrates directly with Pydantic schemas and WebSocket endpoints.

## ASGI Server

Decision: Add `uvicorn[standard]>=0.30,<1`.

Rationale: It is the standard local ASGI runner for FastAPI and will support root `dev:api` usage.

## API Test Client

Decision: Add `httpx>=0.27,<1` as a dev dependency.

Rationale: Starlette/FastAPI TestClient relies on HTTPX for HTTP/WebSocket integration tests.
