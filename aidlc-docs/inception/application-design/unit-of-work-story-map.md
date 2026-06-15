# Unit Of Work Story Map - Monorepo Conversational Agent Refactor

## Story-To-Unit Matrix

| Story | Unit 1 | Unit 2 | Unit 3 | Unit 4 | Unit 5 | Unit 6 |
|---|---|---|---|---|---|---|
| Story 1 - Start A Guided Chat | Supports |  |  | Supports | Primary | Verify |
| Story 2 - Extract And Store Provided User Data | Supports | Supports | Primary | Supports | Supports | Verify |
| Story 3 - Route With Conditional LangGraph Validation |  | Supports | Primary | Supports |  | Verify |
| Story 4 - Receive The Final Diet Result |  | Primary | Primary | Supports | Primary | Verify |
| Story 5 - Preserve Conversation After Refresh |  |  |  | Supports | Primary | Verify |
| Story 6 - Run The Monorepo Locally With Ollama | Primary | Supports | Supports | Supports | Supports | Primary |
| Story 7 - Handle Local Runtime And Security Failures Safely | Supports | Supports | Supports | Primary | Supports | Verify |

## Unit Story Responsibilities

### Unit 1 - Monorepo Foundation

Primary stories:

- Story 6: Establish monorepo setup required to run backend/frontend locally.

Supporting stories:

- Story 1: Provides frontend app shell path.
- Story 2: Provides backend module structure for extraction.
- Story 7: Establishes lock files and dependency foundations.

### Unit 2 - Backend Diet Domain Preservation

Primary stories:

- Story 4: Provides deterministic final diet calculation logic.

Supporting stories:

- Story 2: Provides strict validators used to accept/reject extracted fields.
- Story 3: Provides missing-field and input validation helpers.
- Story 6: Preserves backend tests during monorepo migration.
- Story 7: Validates untrusted numeric/enum inputs.

### Unit 3 - Conversational LangGraph Agent

Primary stories:

- Story 2: Extract and store provided user data.
- Story 3: Conditional validation routing.

Supporting stories:

- Story 4: Calls deterministic calculation and generates final response.
- Story 6: Uses Ollama model/config.
- Story 7: Handles Ollama unavailable and safe graph errors.

### Unit 4 - FastAPI WebSocket API

Primary stories:

- Story 7: Safe local runtime and security failure handling.

Supporting stories:

- Story 1: Enables chat transport.
- Story 2: Validates chat messages and state payloads.
- Story 3: Exposes graph branch behavior through WebSocket responses.
- Story 4: Emits result messages.
- Story 5: Returns state snapshots for frontend persistence.
- Story 6: Provides local API runtime.

### Unit 5 - Next.js Conversational UI

Primary stories:

- Story 1: Guided chat UI.
- Story 4: Render final result.
- Story 5: Persist conversation after refresh.

Supporting stories:

- Story 2: Sends messages/state and renders collected-data summary.
- Story 6: Provides local web app runtime.
- Story 7: Displays safe errors.

### Unit 6 - Documentation And Verification

Primary stories:

- Story 6: Complete local setup and test documentation.

Verification stories:

- Story 1 through Story 7: Verify delivered behavior through tests/manual commands documented in build/test artifacts.

## Coverage Validation

- All 7 stories are assigned to at least one primary unit.
- All stories have supporting verification in Unit 6.
- Security acceptance criteria are covered by Units 1, 2, 4, 5, and 6.
- PBT acceptance criteria are covered by Unit 2 and verified by Unit 6.
