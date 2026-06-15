# Components - Monorepo Conversational Agent Refactor

## Root Workspace

Purpose: Own monorepo configuration and local orchestration.

Responsibilities:

- Define pnpm workspace packages.
- Provide root scripts for running frontend/backend checks.
- Provide root `.env.example` for shared local config.
- Keep package-manager lock files committed.

Interfaces:

- `pnpm` workspace commands.
- Root `.env` consumed by local services.

## Web App Component

Location: `apps/web`

Purpose: Provide the clean minimal conversational UI.

Responsibilities:

- Render chat messages.
- Send typed WebSocket messages to the API.
- Maintain local conversation state and persist it to `localStorage`.
- Show a small collected-data summary before final result.
- Render final diet results and safe runtime errors.
- Escape user-supplied text in rendered chat content.
- Apply frontend HTTP security headers through Next.js config.

Interfaces:

- WebSocket client to `apps/api` chat endpoint.
- Browser `localStorage`.

## API App Component

Location: `apps/api`

Purpose: Host the FastAPI backend and WebSocket interface.

Responsibilities:

- Accept WebSocket chat connections.
- Validate incoming typed JSON messages.
- Enforce message length and payload size limits.
- Orchestrate conversation turns through the conversation service.
- Return typed JSON messages to the frontend.
- Apply CORS restrictions for local frontend origins.
- Apply FastAPI security headers for HTTP responses.
- Return safe errors without stack traces or internal paths.

Interfaces:

- WebSocket endpoint, proposed as `/ws/chat`.
- Health endpoint, proposed as `/health`.

## Conversation Service Component

Location: `apps/api/app/services/conversation_service.py`

Purpose: Coordinate each chat turn between incoming state, extraction, validation, graph execution, and outgoing messages.

Responsibilities:

- Receive frontend-supplied conversation state each turn.
- Call the LangGraph conversational graph.
- Return updated state and assistant/diet-result/error messages.
- Avoid logging personal body data.

Interfaces:

- Input: typed user message plus current frontend state.
- Output: typed response messages and updated state snapshot.

## Conversational Agent Graph Component

Location: `apps/api/app/agent/`

Purpose: Manage the conversation workflow with LangGraph.

Responsibilities:

- Extract candidate fields from user messages using Ollama.
- Merge validated fields into conversation state.
- Run `validateData` before calculation.
- Route through a conditional edge:
  - `data_ok` to `calculateDiet`.
  - `data_incomplete` to `askRemainingData`.
- Generate final assistant response for diet results.
- Generate missing-field prompts when data is incomplete.

Interfaces:

- `run_conversation_turn(state) -> ConversationTurnResult`.

## Diet Domain Component

Location: `apps/api/app/domain/`

Purpose: Preserve deterministic diet calculations and validation as pure domain logic.

Responsibilities:

- Validate and normalize required diet fields.
- Calculate BMI, energy, macro targets, explanation, and disclaimer.
- Expose pure functions suitable for unit and property-based tests.
- Avoid LLM dependencies.

Interfaces:

- `build_diet_outline(input) -> DietResponse`.
- `validate_diet_input(input) -> ValidatedDietInput`.

## Ollama Client Component

Location: `apps/api/app/agent/ollama_client.py`

Purpose: Encapsulate local Ollama calls.

Responsibilities:

- Use `OLLAMA_BASE_URL`, default `http://localhost:11434`.
- Use `OLLAMA_MODEL`, default `llama3.1:8b`.
- Request structured field extraction.
- Convert connection/model failures into explicit application errors.

Interfaces:

- `extract_fields(message) -> ExtractedFieldCandidates`.

## Validation And Schema Component

Location: `apps/api/app/schemas/`

Purpose: Define message, state, and response contracts.

Responsibilities:

- Define WebSocket message models.
- Enforce type, enum, numeric range, and length bounds.
- Keep schema contracts shared by tests and service code.

Interfaces:

- Pydantic models for inbound/outbound message types and conversation state.
