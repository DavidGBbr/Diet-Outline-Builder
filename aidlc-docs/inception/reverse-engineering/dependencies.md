# Dependencies - Current Brownfield Baseline

## Python Dependencies

- `fastapi>=0.115.0`
- `langgraph>=0.2.60`
- `uvicorn>=0.30.0`
- `pytest>=8.0` for development tests

## Current Missing Locking

No Python lock file is currently committed. Security Baseline is enabled for the refactor, so the monorepo plan must introduce dependency lock files.

## Planned Additional Dependencies

- Next.js/React/TypeScript dependencies in `apps/web` managed by `pnpm-lock.yaml`.
- Ollama client dependency or HTTP client in `apps/api`.
- Hypothesis for partial PBT in backend tests.
