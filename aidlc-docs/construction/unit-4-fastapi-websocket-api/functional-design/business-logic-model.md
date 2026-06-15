# Business Logic Model - Unit 4 FastAPI WebSocket API

## Unit Goal

Expose the Unit 3 conversational agent through a local FastAPI WebSocket endpoint while validating message schemas, returning typed protocol messages, and keeping errors safe.

## API Flow

```text
WebSocket /ws/chat
  -> validate incoming user_message
  -> call Unit 3 run_conversation_turn
  -> send assistant_message
  -> optionally send diet_result
  -> optionally send error
  -> send state_snapshot
```

## Endpoints

- `GET /health`: returns local service health.
- `WS /ws/chat`: accepts chat messages and returns typed JSON messages.

## Message Types

Incoming:

- `user_message`

Outgoing:

- `assistant_message`
- `diet_result`
- `error`
- `state_snapshot`

## Transport Boundary

- Unit 4 does not implement diet formulas.
- Unit 4 does not call Ollama directly.
- Unit 4 delegates conversation turns to Unit 3.
- Unit 4 validates WebSocket payload shape before delegation.
