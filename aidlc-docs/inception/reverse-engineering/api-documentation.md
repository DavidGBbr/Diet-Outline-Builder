# API Documentation - Current Brownfield Baseline

## Python API

### `build_diet_outline(payload: dict) -> DietResponse`

Runs the compiled LangGraph calculation workflow.

Required fields:

- `sex`: `male` or `female`
- `age`: integer from 13 to 120
- `heightCM`: number from 100 to 250
- `weightKG`: number from 30 to 300
- `activityLevel`: `low`, `moderate`, or `high`
- `goal`: `lose_fat`, `lose_weight`, `maintain`, `maintain_weight`, or `gain_muscle`

Accepted legacy aliases:

- `heighCM` for `heightCM`
- `weighKG` for `weightKG`

Response fields:

- `imc`
- `imcClassification`
- `totalSpend`
- `targetSpend`
- `goal`
- `macros`
- `explanation`
- `safetyDisclaimer`

## HTTP API

### `GET /`

Returns the current local form-based HTML UI.

### `POST /api/diet`

Accepts the diet input payload as JSON and returns the diet outline response.

Validation errors return HTTP 400 with a `detail` message.

## API Refactor Implication

The refactor must add a WebSocket chat endpoint for conversational messages. The old form route should be removed/replaced, while the calculation function can remain internally reusable.
