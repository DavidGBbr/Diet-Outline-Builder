# Business Logic Model - Unit 3 Conversational LangGraph Agent

## Unit Goal

Unit 3 builds the backend conversational agent layer under `apps/api/app/agent/`. The agent processes one user turn at a time, extracts possible diet fields using local Ollama, accepts only fields that pass deterministic Unit 2 validation, and routes to either a missing-data prompt or final diet calculation.

## Target Agent Modules

```text
apps/api/app/agent/
  __init__.py
  graph.py
  models.py
  ollama.py
  prompts.py
```

## Turn Flow

```text
ConversationTurnInput
  -> extractData
  -> mergeValidFields
  -> validateData
  -> conditional edge
       data_ok -> calculateDiet -> generateResponse -> END
       data_incomplete -> askRemainingData -> END
```

## Node Responsibilities

### extractData

- Sends the current user message to Ollama with a structured extraction prompt.
- Requests only supported candidate fields: `sex`, `age`, `heightCM`, `weightKG`, `activityLevel`, `goal`.
- Stores parsed candidate data on graph state.
- Does not mutate validated conversation data directly.
- Converts Ollama connectivity/model failures into safe agent errors.

### mergeValidFields

- Reads candidate fields from `extractData`.
- Validates each present field through Unit 2 partial validation.
- Merges accepted fields into `collected_data`.
- Stores invalid field errors for response generation.
- Never trusts candidate values only because the LLM returned them.

### validateData

- Runs Unit 2 partial validation over current `collected_data`.
- Sets `data_valid` true when all required fields are present and valid.
- Stores missing fields and invalid field errors.

### conditional edge

- Returns `data_ok` when `data_valid` is true.
- Returns `data_incomplete` when `data_valid` is false.

### askRemainingData

- Builds a concise assistant message asking only for missing or invalid fields.
- Ends the current turn after setting the assistant message.
- Does not calculate the diet result.

### calculateDiet

- Runs Unit 2 complete validation and deterministic calculation.
- Stores the `DietResponse` on graph state.

### generateResponse

- Produces the final assistant message that introduces the diet result.
- Leaves the structured `DietResponse` available for Unit 4 WebSocket response mapping.

## Error Flow

```text
Ollama unavailable or invalid transport response
  -> safe AgentRuntimeError
  -> graph state error
  -> assistant message instructing user to start/check Ollama
  -> END
```

## Data Authority

- Ollama is only an extraction helper.
- Unit 2 validation is the source of truth for accepted fields.
- Unit 2 calculator is the source of truth for final diet output.
- Frontend/localStorage state is not trusted until validated by backend graph nodes.

## Story Traceability

- Story 2: extraction and valid field merge.
- Story 3: conditional routing with missing-data branch.
- Story 4: final deterministic diet result once data is complete.
- Story 7: safe Ollama unavailable error.
