# Business Rules - Unit 4 FastAPI WebSocket API

## Incoming Rules

- Accept only JSON objects.
- Accept only `type: "user_message"` for client-to-server chat payloads.
- Require non-empty `text` with maximum length 4000 characters.
- Accept optional state object with `collectedData`.
- Reject malformed payloads with safe `error` messages.

## Outgoing Rules

- Always send an `assistant_message` when the agent returns text.
- Send `diet_result` only when the agent returns a final diet result.
- Send `error` only when the agent returns or the API detects a safe error.
- Send `state_snapshot` after each valid processed turn.

## Endpoint Rules

- `/health` is public local health check.
- `/ws/chat` is the only chat API in Unit 4.
- Do not add or restore public `/api/diet`.
