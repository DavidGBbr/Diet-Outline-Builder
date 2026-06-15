# Component Methods - Monorepo Conversational Agent Refactor

## Web App Component

- `connectChatSocket(): WebSocket`
  - Purpose: Open the chat WebSocket connection to the API.
  - Input: none; reads configured API URL.
  - Output: browser `WebSocket` instance.

- `sendUserMessage(text: string, state: ConversationState): void`
  - Purpose: Send a typed `user_message` event with current conversation state.
  - Input: user text and frontend-owned state.
  - Output: none; response arrives through WebSocket events.

- `persistConversation(state: ConversationState, messages: ChatMessage[]): void`
  - Purpose: Store non-secret conversation data in `localStorage`.
  - Input: conversation state and message list.
  - Output: none.

- `restoreConversation(): StoredConversation | null`
  - Purpose: Restore local chat state after refresh.
  - Input: none.
  - Output: stored conversation or null.

## API App Component

- `create_app() -> FastAPI`
  - Purpose: Construct the FastAPI app with middleware, routes, and WebSocket endpoint.
  - Input: runtime settings.
  - Output: FastAPI application.

- `chat_websocket(websocket: WebSocket) -> None`
  - Purpose: Accept WebSocket messages, validate them, call conversation service, and send responses.
  - Input: WebSocket connection.
  - Output: typed WebSocket events.

- `health() -> dict`
  - Purpose: Confirm backend process is running.
  - Input: none.
  - Output: health JSON.

## Conversation Service Component

- `handle_turn(request: ChatTurnRequest) -> ChatTurnResponse`
  - Purpose: Process one user message with the current frontend-supplied state.
  - Input: typed user message and current conversation state.
  - Output: assistant messages, optional diet result, and updated state snapshot.

- `to_error_response(error: Exception) -> ErrorMessage`
  - Purpose: Convert internal errors into safe user-facing messages.
  - Input: exception.
  - Output: typed `error` message without internal paths or stack traces.

## Conversational Agent Graph Component

- `extract_data_node(state: ConversationGraphState) -> ConversationGraphState`
  - Purpose: Use Ollama to extract candidate required fields from the latest user message.
  - Input: conversation graph state.
  - Output: graph state with field candidates.

- `merge_valid_fields_node(state: ConversationGraphState) -> ConversationGraphState`
  - Purpose: Strictly validate extracted candidates and merge only accepted fields.
  - Input: extracted candidates and current diet data.
  - Output: updated diet data plus validation notes.

- `validate_data_node(state: ConversationGraphState) -> ConversationGraphState`
  - Purpose: Determine whether all required data exists and list missing fields.
  - Input: current diet data.
  - Output: `data_valid` boolean and `missing_fields` list.

- `route_after_validation(state: ConversationGraphState) -> Literal["data_ok", "data_incomplete"]`
  - Purpose: Conditional edge router after validation.
  - Input: graph state with `data_valid`.
  - Output: `data_ok` or `data_incomplete`.

- `calculate_diet_node(state: ConversationGraphState) -> ConversationGraphState`
  - Purpose: Call deterministic domain calculation once data is complete.
  - Input: validated diet input.
  - Output: graph state with diet result.

- `ask_remaining_data_node(state: ConversationGraphState) -> ConversationGraphState`
  - Purpose: Generate an assistant prompt for only missing or invalid required fields.
  - Input: missing fields and validation notes.
  - Output: assistant message and updated state snapshot.

- `generate_response_node(state: ConversationGraphState) -> ConversationGraphState`
  - Purpose: Generate the final assistant message with result summary and disclaimer.
  - Input: diet result.
  - Output: final assistant message and result payload.

## Diet Domain Component

- `validate_diet_input(payload: dict) -> ValidatedDietInput`
  - Purpose: Strictly validate required diet fields, enums, and numeric bounds.
  - Input: untrusted payload.
  - Output: normalized validated input or validation error.

- `build_diet_outline(input: ValidatedDietInput) -> DietResponse`
  - Purpose: Calculate BMI, energy, macros, explanation, and disclaimer.
  - Input: validated diet input.
  - Output: final diet response.

- `missing_required_fields(partial: PartialDietInput) -> list[str]`
  - Purpose: List required fields not yet collected.
  - Input: partial diet data.
  - Output: field-name list.

## Ollama Client Component

- `extract_fields(message: str) -> ExtractedFieldCandidates`
  - Purpose: Ask Ollama for structured field candidates.
  - Input: user message.
  - Output: candidate field values before deterministic validation.

- `check_available() -> None`
  - Purpose: Verify Ollama is reachable enough to produce a useful local error.
  - Input: none.
  - Output: none or typed Ollama unavailable error.
