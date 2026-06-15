# Unit 5 Code Generation Plan - Next.js Conversational UI

## Purpose

Replace the placeholder web shell with a minimal conversational UI that sends user messages to the FastAPI WebSocket API, renders typed backend messages, persists conversation state in `localStorage`, and never calculates diet formulas in the frontend.

## Design/NFR Summary

- Use existing Next.js, React, and TypeScript dependencies.
- Use `NEXT_PUBLIC_API_WS_URL` with fallback `ws://127.0.0.1:8000/ws/chat`.
- Persist messages, collected state, and latest diet result in `localStorage`.
- Render user text through React text nodes only.
- Use a per-message WebSocket session and close it after `state_snapshot`.
- Enforce a basic 4000-character client-side message limit matching Unit 4.

## Steps

- [x] Add chat protocol types.
- [x] Add localStorage helpers.
- [x] Add client chat component.
- [x] Replace placeholder page with chat UI.
- [x] Update CSS for desktop/mobile chat layout.
- [x] Run `pnpm typecheck:web`.
- [x] Run `pnpm build:web`.
- [x] Create code summary and update AI-DLC state/audit.

## Approval Gate

The user instructed to continue if there are next steps. This plan has no unresolved choices and is treated as approved for Unit 5 implementation.
