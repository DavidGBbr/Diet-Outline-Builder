# Domain Entities - Unit 4 FastAPI WebSocket API

## IncomingChatMessage

- `type: Literal["user_message"]`
- `text: str`
- `state: ClientConversationState`

## ClientConversationState

- `collectedData: dict[str, Any]`

## AssistantMessage

- `type: Literal["assistant_message"]`
- `text: str`

## DietResultMessage

- `type: Literal["diet_result"]`
- `result: DietResponse`

## ErrorMessage

- `type: Literal["error"]`
- `code: str`
- `message: str`

## StateSnapshotMessage

- `type: Literal["state_snapshot"]`
- `state: ServerConversationState`

## ServerConversationState

- `collectedData: dict[str, Any]`
- `missingFields: list[str]`
- `invalidFields: list[FieldValidationError]`
