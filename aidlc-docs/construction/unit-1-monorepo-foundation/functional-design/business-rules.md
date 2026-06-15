# Business Rules - Unit 1 Monorepo Foundation

## Repository Rules

- The repository must use pnpm workspaces with `apps/*` packages.
- `apps/api` is the only Python application module in the target structure.
- `apps/web` is the only frontend application module in the target structure.
- Old root `src/` and root `tests/` must be removed after migration to avoid duplicate sources and ambiguous test discovery.
- The old form-based local UI must be removed during backend migration because the approved target design replaces it with the conversational frontend.

## API Package Rules

- The moved Python package must be named `app`.
- Unit 1 may preserve existing calculation behavior but should not redesign it; Unit 2 owns domain cleanup/hardening.
- Unit 1 must not add a public `/api/diet` endpoint to the target backend.
- Unit 1 must preserve enough backend functionality for existing calculation tests to pass after path/import updates.

## Dependency Rules

- `apps/api` must use `uv` with `pyproject.toml` and `uv.lock` from the start.
- Root frontend dependencies must be managed by pnpm and committed through `pnpm-lock.yaml` when installed.
- Dependencies must come from official package registries.

## Script Rules

- Root scripts should include:
  - `dev:api`
  - `dev:web`
  - `test:api`
  - `lint:web` or equivalent placeholder if not fully available
  - `typecheck:web` or equivalent placeholder if not fully available
- Root scripts should not claim a complete integrated `dev` command until backend/frontend integration exists.

## Environment Rules

- Root `.env.example` must include:
  - `OLLAMA_BASE_URL=http://localhost:11434`
  - `OLLAMA_MODEL=llama3.1:8b`
  - local API/web URL defaults where useful.
- No real secrets must be committed.

## Security Rules

- SECURITY-10 applies: lock files must be introduced or the absence must be documented as a blocker.
- SECURITY-09 applies: generated app shells must avoid unnecessary demo/debug exposure beyond normal local development scaffolding.

## PBT Rules

- Unit 1 has no PBT implementation requirement.
- Unit 1 must leave test structure ready for Unit 2 Hypothesis tests.
