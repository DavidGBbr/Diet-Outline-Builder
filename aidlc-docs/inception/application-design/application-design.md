# Application Design

The local UI adds one thin web layer around the existing LangGraph calculator.

## Component Summary

- Existing calculator remains the source of truth for all business logic.
- FastAPI serves a local-only browser UI and JSON endpoint.
- Browser JavaScript only handles presentation and API submission.

## Endpoint Summary

- `GET /`: Returns the local HTML UI.
- `POST /api/diet`: Accepts the diet input payload and returns the calculated diet outline.

## Design Decision

Use server-rendered HTML as a Python string rather than adding a frontend build system. This keeps the local app easy to install and run.
