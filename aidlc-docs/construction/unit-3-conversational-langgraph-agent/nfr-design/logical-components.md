# Logical Components - Unit 3 Conversational LangGraph Agent

## Agent Models Component

### Location

`apps/api/app/agent/models.py`

### Responsibilities

- Define agent turn input/result models.
- Define safe error model.
- Define graph state typing.

### Key Types

- `AgentError`
- `AgentTurnInput`
- `AgentTurnResult`
- `AgentState`

## Prompt Component

### Location

`apps/api/app/agent/prompts.py`

### Responsibilities

- Build the Ollama extraction prompt.
- Define supported field instructions.
- Keep prompt wording centralized.

## Ollama Client Component

### Location

`apps/api/app/agent/ollama.py`

### Responsibilities

- Read `OLLAMA_BASE_URL` and `OLLAMA_MODEL` from environment.
- POST to local Ollama generate API.
- Parse JSON extraction output.
- Raise safe provider exceptions for connectivity failures.

### Key Types/Functions

- `OllamaUnavailableError`
- `OllamaExtractionClient.extract_fields(message: str) -> dict[str, Any]`

## Graph Component

### Location

`apps/api/app/agent/graph.py`

### Responsibilities

- Define LangGraph nodes and required conditional route.
- Expose `run_conversation_turn`.
- Delegate extraction to injected/default client.
- Delegate validation and calculation to Unit 2 domain functions.

### Key Functions

- `extract_data_node`
- `merge_valid_fields_node`
- `validate_data_node`
- `route_after_validation`
- `ask_remaining_data_node`
- `calculate_diet_node`
- `generate_response_node`
- `run_conversation_turn`

## Package Export Component

### Location

`apps/api/app/agent/__init__.py`

### Responsibilities

- Export public agent models and `run_conversation_turn`.

## Test Component

### Location

`apps/api/tests/test_agent_graph.py`

### Responsibilities

- Test incomplete route.
- Test complete route.
- Test multi-field extraction merge.
- Test invalid candidate does not overwrite valid state.
- Test Ollama unavailable safe error.

## Component Interaction

```text
run_conversation_turn
  -> agent graph
  -> injected/default extraction client
  -> Unit 2 validate_partial_diet_input
  -> route_after_validation
      data_incomplete -> askRemainingData -> AgentTurnResult
      data_ok -> Unit 2 build_diet_outline -> generateResponse -> AgentTurnResult
```
