# Unit 3 Code Generation Plan - Conversational LangGraph Agent

## Purpose

Implement the approved Unit 3 conversational LangGraph agent with local Ollama candidate extraction, deterministic Unit 2 validation/merge, required conditional routing, safe provider errors, and backend tests using fake clients.

## Unit Context

- Unit: Unit 3 - Conversational LangGraph Agent
- Depends On: Unit 2 domain validation/calculation.
- Primary Stories: Story 2, Story 3, Story 4.
- Supporting Story: Story 7.
- Security: SECURITY-03, SECURITY-09, SECURITY-11.
- PBT: No new PBT required in Unit 3.

## Existing Files To Modify

- `aidlc-docs/aidlc-state.md`
- `aidlc-docs/audit.md`

## New Files To Create

- `apps/api/app/agent/__init__.py`
- `apps/api/app/agent/models.py`
- `apps/api/app/agent/prompts.py`
- `apps/api/app/agent/ollama.py`
- `apps/api/app/agent/graph.py`
- `apps/api/tests/test_agent_graph.py`
- `aidlc-docs/construction/unit-3-conversational-langgraph-agent/code/code-summary.md`

## Step-by-Step Generation Plan

### Step 1 - Agent Models

- [x] Add safe `AgentError`.
- [x] Add `AgentTurnInput` and `AgentTurnResult`.
- [x] Add `AgentState` graph typing.

### Step 2 - Prompt And Ollama Client

- [x] Add extraction prompt builder.
- [x] Add `OllamaExtractionClient` using environment defaults and standard-library HTTP.
- [x] Add safe `OllamaUnavailableError`.
- [x] Treat malformed model JSON as empty candidate extraction.

### Step 3 - LangGraph Agent

- [x] Add nodes: `extractData`, `mergeValidFields`, `validateData`, `askRemainingData`, `calculateDiet`, `generateResponse`.
- [x] Add required `data_ok` and `data_incomplete` conditional route.
- [x] Add safe early END path for provider errors.
- [x] Expose `run_conversation_turn` with optional injected client.

### Step 4 - Tests

- [x] Test incomplete route.
- [x] Test complete route.
- [x] Test multi-field extraction merge.
- [x] Test invalid candidate does not overwrite valid existing data.
- [x] Test Ollama unavailable safe error.

### Step 5 - Verification And Docs

- [x] Run `pnpm test:api`.
- [x] Create code summary.
- [x] Update AI-DLC state and audit log.

## Approval Gate

The user instructed to continue if there are next steps. This plan has no unresolved choices and is treated as approved for Unit 3 implementation.
