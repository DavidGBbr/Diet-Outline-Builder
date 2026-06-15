# Logical Components - Unit 4 FastAPI WebSocket API

## Schema Component

Location: `apps/api/app/schemas/chat.py`

Responsibilities: define incoming and outgoing WebSocket protocol models.

## Conversation Service Component

Location: `apps/api/app/services/conversation.py`

Responsibilities: wrap Unit 3 `run_conversation_turn` for API use and app-level injection.

## FastAPI App Component

Location: `apps/api/app/main.py`

Responsibilities: create FastAPI app, configure CORS/security headers, expose `/health` and `/ws/chat`.

## Test Component

Location: `apps/api/tests/test_websocket_api.py`

Responsibilities: verify health, headers, schema errors, and successful WebSocket agent mapping.
