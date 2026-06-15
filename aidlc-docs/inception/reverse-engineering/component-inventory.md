# Component Inventory - Current Brownfield Baseline

## Diet Calculation Graph

- Location: `src/diet_outline_builder/graph.py`
- Purpose: Deterministic validation and diet calculation.
- Key nodes: `validateInput`, `calculateAnthropometrics`, `calculateEnergy`, `calculateMacros`, `generateExplanation`, `addSafetyDisclaimer`.
- Refactor impact: Preserve, possibly move to `apps/api`, and reuse from conversational graph.

## Local Web App

- Location: `src/diet_outline_builder/web.py`
- Purpose: FastAPI app serving inline form UI and JSON calculation endpoint.
- Refactor impact: Replace inline UI with Next.js frontend. Backend moves to `apps/api` and gains WebSocket chat.

## CLI

- Location: `src/diet_outline_builder/cli.py`
- Purpose: Terminal-based prompt flow.
- Refactor impact: Optional to preserve if low cost; not a primary requirement for the monorepo refactor.

## Tests

- Location: `tests/`
- Purpose: Backend calculation and FastAPI route verification.
- Refactor impact: Move or adapt to `apps/api/tests` and add WebSocket tests.
