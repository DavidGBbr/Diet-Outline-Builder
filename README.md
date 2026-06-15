# Diet Outline Builder

Local-first conversational diet outline builder powered by Next.js, FastAPI, LangGraph, and Ollama.

The app collects diet inputs through chat, validates them deterministically on the backend, and returns BMI, calorie target, macros, an explanation, and a safety disclaimer.

## Requirements

- Node.js with `pnpm`
- Python 3.11+
- `uv`
- Ollama running locally

## Install

```bash
pnpm install
```

```bash
cd apps/api && uv sync
```

## Ollama Setup

Start Ollama, then pull the local model:

```bash
ollama pull llama3.1:8b
```

Defaults are documented in `.env.example`:

```text
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
NEXT_PUBLIC_API_WS_URL=ws://127.0.0.1:8000/ws/chat
```

## Run Locally

Start the API:

```bash
pnpm dev:api
```

Start the web app in another terminal:

```bash
pnpm dev:web
```

Open:

```text
http://127.0.0.1:3000
```

## API

- `GET /health`: local health check.
- `WS /ws/chat`: conversational diet-builder WebSocket.

There is no public `/api/diet` endpoint. Diet calculation is internal to the backend agent/domain layer.

## Tests And Checks

```bash
pnpm test:api
```

```bash
pnpm typecheck:web
```

```bash
pnpm build:web
```

Backend tests include example-based tests, Hypothesis property-based tests, LangGraph routing tests, and WebSocket API tests.

## Notes

- Conversation state is stored locally in browser `localStorage`.
- The frontend does not calculate diet formulas.
- Ollama extraction is treated as candidate data only; deterministic Pydantic validation decides what is accepted.
- If Ollama is not running, the API/UI returns a clear local setup error.
