# Domain Entities - Unit 5 Next.js Conversational UI

## ChatMessage

- `id`
- `role`
- `text`

## StoredConversation

- `messages`
- `state`
- `dietResult`

## ConversationState

- `collectedData`
- `missingFields`
- `invalidFields`

## WebSocket Messages

Mirrors Unit 4 protocol: `user_message`, `assistant_message`, `diet_result`, `error`, and `state_snapshot`.
