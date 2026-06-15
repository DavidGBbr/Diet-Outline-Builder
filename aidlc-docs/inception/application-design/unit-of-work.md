# Unit Of Work - Monorepo Conversational Agent Refactor

## Decomposition Strategy

Use the approved 6-unit workflow/dependency-based split. Unit 1 creates the monorepo and moves the existing Python backend into `apps/api`. Backend WebSocket work precedes frontend integration. Security responsibilities are spread across relevant units. PBT responsibilities are assigned to Unit 2 because partial PBT applies to pure domain validation/calculation functions. Existing tests move early to preserve regression coverage.

## Unit 1 - Monorepo Foundation

### Purpose

Establish the pnpm monorepo structure and relocate the current Python backend into `apps/api` while preserving existing test coverage.

### Responsibilities

- Create root `pnpm-workspace.yaml`.
- Create root `package.json` with local scripts.
- Create `apps/api` Python service structure.
- Move current `src/diet_outline_builder` code into `apps/api/app` or equivalent target package layout.
- Move/adapt existing backend tests into `apps/api/tests`.
- Create `apps/web` Next.js app shell.
- Add root `.env.example` with Ollama defaults.
- Create dependency lock files.
- Remove root-level Python app entrypoints from the target architecture as appropriate.

### Deliverables

- Monorepo root config.
- `apps/api` package skeleton with migrated current backend code.
- `apps/web` Next.js skeleton.
- Root `.env.example`.
- Updated test commands.

### Security Responsibilities

- SECURITY-10: Introduce lock files and official-registry dependency setup.
- SECURITY-09: Ensure default app scaffolding does not expose debug/demo pages beyond local dev defaults.

### PBT Responsibilities

- None beyond preparing backend test structure.

## Unit 2 - Backend Diet Domain Preservation

### Purpose

Preserve and harden deterministic diet validation/calculation logic as pure backend domain code.

### Responsibilities

- Create/clean `apps/api/app/domain`.
- Preserve `build_diet_outline` behavior.
- Preserve BMI, energy, macro, explanation, and disclaimer outputs.
- Implement strict validation helpers for complete and partial diet inputs.
- Add `missing_required_fields` helper.
- Add property-based tests for pure validation/calculation invariants.
- Keep code independent from FastAPI, WebSockets, Ollama, and frontend concerns.

### Deliverables

- Domain models/functions.
- Migrated example-based tests.
- Hypothesis-based PBT tests for applicable invariants.

### Security Responsibilities

- SECURITY-05: Strict type/range/enum validation for diet inputs.

### PBT Responsibilities

- PBT-03: Invariants for BMI classification, non-negative macros, and macro calories close to target.
- PBT-07: Domain-specific valid diet input generators.
- PBT-08: Preserve Hypothesis shrinking/reproducibility behavior.
- PBT-09: Use Hypothesis as Python PBT framework.

## Unit 3 - Conversational LangGraph Agent

### Purpose

Build the LangGraph conversation state machine that extracts fields, validates completeness, routes through the required conditional edge, and produces missing-data prompts or final diet responses.

### Responsibilities

- Create `apps/api/app/agent`.
- Implement Ollama extraction client using root `.env` settings.
- Treat Ollama output as candidate data only.
- Strictly merge only validated extracted fields.
- Implement `validateData` node.
- Implement conditional router:
  - `data_ok` -> `calculateDiet`
  - `data_incomplete` -> `askRemainingData`
- Implement `askRemainingData` current-turn ending behavior.
- Implement `calculateDiet` and `generateResponse` nodes.
- Add graph tests for both conditional branches and Ollama unavailable error path.

### Deliverables

- Conversational graph module.
- Ollama client module.
- Agent state models or schemas shared with Unit 4.
- Backend tests for graph routing.

### Security Responsibilities

- SECURITY-03: Avoid logging personal body data.
- SECURITY-09: Convert Ollama failures to safe local errors.
- SECURITY-11: Respect message/content size constraints designed with Unit 4 schemas.

### PBT Responsibilities

- No required PBT in this phase because stateful conversation PBT is advisory under partial mode.

## Unit 4 - FastAPI WebSocket API

### Purpose

Expose the conversational agent through a local FastAPI WebSocket API with validation, CORS, headers, and safe errors.

### Responsibilities

- Create FastAPI app entrypoint in `apps/api/app/main.py`.
- Add `/ws/chat` WebSocket endpoint.
- Add `/health` endpoint.
- Define typed JSON message protocol schemas.
- Validate incoming message type, text length, and state payload.
- Call Conversation Service for each message.
- Send `assistant_message`, `diet_result`, `error`, and `state_snapshot` messages.
- Configure CORS with explicit local frontend origin.
- Configure FastAPI security headers for HTTP responses.
- Remove public `/api/diet` from target API.
- Add WebSocket tests.

### Deliverables

- FastAPI app with WebSocket endpoint.
- Message schemas.
- Conversation service wrapper.
- WebSocket/API tests.

### Security Responsibilities

- SECURITY-04: HTTP security headers for backend HTTP responses.
- SECURITY-05: Schema validation for all message payloads.
- SECURITY-08: Explicit local CORS origins and documented unauthenticated local public endpoints.
- SECURITY-09: Safe user-facing error responses.
- SECURITY-11: Message length/size limits.

### PBT Responsibilities

- None required beyond using Unit 2 domain functions.

## Unit 5 - Next.js Conversational UI

### Purpose

Replace the old form-based local UI with a clean minimal Next.js chat interface that connects to the backend WebSocket.

### Responsibilities

- Build chat UI in `apps/web`.
- Connect to backend WebSocket.
- Send `user_message` events with current conversation state.
- Render `assistant_message`, `diet_result`, and `error` events.
- Persist messages and conversation state in `localStorage`.
- Show a collected-data summary before final result.
- Escape/safely render user-supplied text.
- Add Next.js security headers.
- Do not expose old form UI.
- Do not implement diet formulas in the frontend.

### Deliverables

- Next.js chat page/components.
- WebSocket client utility.
- localStorage persistence utility.
- Result rendering component.
- Frontend config for security headers and API URL.

### Security Responsibilities

- SECURITY-04: Frontend HTTP security headers via Next.js config.
- SECURITY-05: Do not trust localStorage blindly before sending state; maintain client-side sanity checks where practical.
- SECURITY-09: Render safe user-facing errors.

### PBT Responsibilities

- None required in this phase.

## Unit 6 - Documentation And Verification

### Purpose

Document the final monorepo setup and verify the integrated local workflow.

### Responsibilities

- Update README for monorepo usage.
- Document Ollama install/start/pull flow for `llama3.1:8b`.
- Document backend and frontend run commands.
- Document test commands.
- Run backend unit/API/WebSocket tests.
- Run frontend install/build/typecheck if available.
- Update AI-DLC build/test artifacts.

### Deliverables

- Updated README.
- Build/test instructions.
- Verification results in AI-DLC docs.

### Security Responsibilities

- SECURITY-10: Document dependency installation from official registries and lock files.
- SECURITY-08: Document local unauthenticated endpoint scope.

### PBT Responsibilities

- Confirm Unit 2 PBT tests are included in backend test command.
