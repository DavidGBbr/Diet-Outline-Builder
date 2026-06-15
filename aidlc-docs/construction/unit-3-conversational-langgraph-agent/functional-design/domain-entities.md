# Domain Entities - Unit 3 Conversational LangGraph Agent

## ConversationTurnInput

Represents one backend agent turn.

Fields:

- `message: str`
- `collected_data: dict[str, Any]`

## AgentState

LangGraph state for one turn.

Fields:

- `message: str`
- `collected_data: dict[str, Any]`
- `candidate_data: dict[str, Any]`
- `accepted_data: dict[str, Any]`
- `missing_fields: list[str]`
- `invalid_fields: list[FieldValidationError]`
- `data_valid: bool`
- `diet_result: DietResponse | None`
- `assistant_message: str`
- `error: AgentError | None`

## AgentTurnResult

Returned by the agent service/graph wrapper.

Fields:

- `assistant_message: str`
- `collected_data: dict[str, Any]`
- `missing_fields: list[str]`
- `invalid_fields: list[FieldValidationError]`
- `diet_result: DietResponse | None`
- `error: AgentError | None`

## ExtractionCandidate

Structured candidate output parsed from Ollama.

Fields are optional:

- `sex`
- `age`
- `heightCM`
- `weightKG`
- `activityLevel`
- `goal`

## AgentError

Safe user-facing error model.

Fields:

- `code: str`
- `message: str`

Expected initial codes:

- `ollama_unavailable`
- `ollama_bad_response`

## OllamaExtractionClient

Interface for extracting candidate data.

Method:

- `extract_fields(message: str) -> dict[str, Any]`

Implementation details:

- Reads `OLLAMA_BASE_URL` and `OLLAMA_MODEL` from environment.
- Uses Ollama local HTTP API.
- Returns parsed candidate field dictionary.
- Raises a safe agent/provider exception on connectivity failures.

## Conversation Graph Public API

Functions:

- `run_conversation_turn(input: ConversationTurnInput, client: OllamaExtractionClient | None = None) -> AgentTurnResult`
- `route_after_validation(state: AgentState) -> Literal["data_ok", "data_incomplete"]`

The optional client allows tests to inject deterministic fake extraction without requiring Ollama.
