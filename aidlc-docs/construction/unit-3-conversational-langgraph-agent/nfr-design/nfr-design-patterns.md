# NFR Design Patterns - Unit 3 Conversational LangGraph Agent

## Pattern 1 - Candidate-Only LLM Extraction

### Requirement

Ollama must not be trusted as authoritative state.

### Design

- `extractData` writes to `candidate_data` only.
- `mergeValidFields` applies Unit 2 partial validation before state mutation.
- Unsupported or invalid candidates are captured as structured errors.

## Pattern 2 - Deterministic Conditional Routing

### Requirement

Routing must follow the approved labels and branches.

### Design

- `validateData` writes `data_valid`.
- `route_after_validation` returns only `data_ok` or `data_incomplete`.
- Graph edges are named to match the approved contract.

## Pattern 3 - Injectable Extraction Client

### Requirement

Tests must not require live Ollama.

### Design

- Define a protocol-like client interface with `extract_fields(message)`.
- `run_conversation_turn` accepts an optional client.
- Production default uses `OllamaExtractionClient`.
- Tests inject fake clients.

## Pattern 4 - Safe Provider Failure Boundary

### Requirement

Ollama failures must be user-safe.

### Design

- Transport layer raises `OllamaUnavailableError` or returns empty extraction for malformed JSON.
- Graph converts provider failure to `AgentError(code="ollama_unavailable", message=...)`.
- Error messages do not include stack traces, internal paths, or raw provider bodies.

## Pattern 5 - No Personal Body Data Logging

### Requirement

Avoid unnecessary logging of personal data.

### Design

- Agent implementation does not call logging with raw messages or state.
- Tests inspect returned state directly rather than relying on logs.

## Pattern 6 - Minimal Dependency Transport

### Requirement

Keep Unit 3 dependency surface small.

### Design

- Use `urllib.request` with JSON body and finite timeout for Ollama.
- Do not add a new HTTP dependency in Unit 3.

## Pattern 7 - Unit 4 Ready Result Contract

### Requirement

Agent output must map cleanly to WebSocket messages later.

### Design

- Return `AgentTurnResult` containing assistant message, collected data, missing fields, invalid fields, diet result, and error.
- Keep transport-specific WebSocket schemas out of Unit 3.

## Security Compliance

- SECURITY-03: No raw personal data logs.
- SECURITY-09: Safe structured agent/provider errors.
- SECURITY-11: Finite current-turn prompt and HTTP timeout; full WebSocket size validation deferred to Unit 4.
