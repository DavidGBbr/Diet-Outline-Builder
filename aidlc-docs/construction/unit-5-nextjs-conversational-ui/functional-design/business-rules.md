# Business Rules - Unit 5 Next.js Conversational UI

- Do not render or restore the old form UI.
- Do not calculate diet formulas in the frontend.
- Send `user_message` events with current `collectedData`.
- Render backend `assistant_message`, `error`, `diet_result`, and `state_snapshot` messages.
- Persist messages and conversation state in `localStorage`.
- Do not store secrets or API keys in `localStorage`.
- Safely render user text through React text rendering.
