# Business Logic Model - Unit 5 Next.js Conversational UI

## Unit Goal

Build a browser chat interface that sends natural-language user messages plus current state to `/ws/chat`, renders assistant messages, displays final diet results, and persists progress across refreshes.

## Client Flow

```text
page load
  -> restore localStorage state
  -> user sends message
  -> append user message
  -> open WebSocket
  -> send user_message + collectedData
  -> render assistant_message/error/diet_result
  -> update state_snapshot
  -> persist localStorage
```
