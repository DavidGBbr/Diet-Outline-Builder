# Component Dependency - Monorepo Conversational Agent Refactor

## Dependency Matrix

| Component | Depends On | Must Not Depend On |
|---|---|---|
| Root Workspace | pnpm, Python tooling | Application runtime logic |
| Web App | Browser APIs, API WebSocket protocol | Diet calculation formulas, Ollama direct calls |
| API App | Conversation Service, Security Middleware, Config | Next.js internals |
| Conversation Service | Conversational Agent Graph, schemas | Frontend localStorage |
| Conversational Agent Graph | Ollama Client, Diet Domain | FastAPI route internals, Next.js UI |
| Ollama Client | Ollama HTTP API, Config | Diet formulas, frontend state |
| Diet Domain | Python standard/domain dependencies | Ollama, FastAPI, WebSocket, frontend |
| Validation/Schemas | Pydantic/domain types | UI rendering |

## Primary Data Flow

```text
User
  -> Next.js Chat UI
  -> WebSocket user_message with current state
  -> FastAPI WebSocket Service
  -> Conversation Service
  -> Conversational LangGraph
       -> Ollama field extraction
       -> deterministic field validation
       -> validateData
       -> conditional edge
            data_incomplete -> askRemainingData -> END
            data_ok -> calculateDiet -> generateResponse -> END
  -> WebSocket assistant/diet_result/error/state_snapshot messages
  -> Next.js UI + localStorage
```

## Conditional LangGraph Flow

```text
START
  -> extractData
  -> mergeValidFields
  -> validateData
  -> routeAfterValidation
       data_ok -> calculateDiet -> generateResponse -> END
       data_incomplete -> askRemainingData -> END
```

## State Ownership

- Frontend owns durable local state through `localStorage`.
- Backend receives current state each turn and returns updated state.
- Backend does not persist sessions in memory beyond a single WebSocket turn.
- Backend validates every frontend-supplied state payload before using it.

## WebSocket Protocol Direction

Incoming messages:

- `user_message`: user text plus current conversation state.

Outgoing messages:

- `assistant_message`: natural-language prompt or explanation.
- `diet_result`: final structured diet response.
- `error`: safe user-facing error.
- `state_snapshot`: updated conversation state for frontend persistence.

## Removed Dependencies From Current Baseline

- The old inline FastAPI HTML form is removed.
- The CLI is not preserved in the target monorepo.
- The public direct `/api/diet` endpoint is removed; deterministic calculation remains callable internally by the conversation graph and tests.
