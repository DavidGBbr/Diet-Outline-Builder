# Logical Components - Unit 1 Monorepo Foundation

## Root Workspace Component

### Responsibilities

- Define pnpm workspace package discovery.
- Provide root command aliases.
- Own `pnpm-lock.yaml`.
- Own root `.env.example`.

### Files

- `pnpm-workspace.yaml`
- `package.json`
- `pnpm-lock.yaml`
- `.env.example`

## API Project Component

### Responsibilities

- Host the migrated Python backend package.
- Own Python dependency metadata and lock file.
- Run migrated backend tests.
- Prepare future `agent/`, `domain/`, `schemas/`, and `services/` structure.

### Files And Directories

- `apps/api/pyproject.toml`
- `apps/api/uv.lock`
- `apps/api/app/`
- `apps/api/tests/`

## Web Project Component

### Responsibilities

- Host minimal Next.js TypeScript shell.
- Own frontend package metadata.
- Provide initial security headers.
- Run typecheck and build.

### Files And Directories

- `apps/web/package.json`
- `apps/web/app/layout.tsx`
- `apps/web/app/page.tsx`
- `apps/web/app/globals.css`
- `apps/web/next.config.ts`
- `apps/web/tsconfig.json`

## Environment Template Component

### Responsibilities

- Document local runtime defaults without secrets.
- Provide common values for later units.

### Required Variables

- `OLLAMA_BASE_URL=http://localhost:11434`
- `OLLAMA_MODEL=llama3.1:8b`
- `API_HOST=127.0.0.1`
- `API_PORT=8000`
- `WEB_PORT=3000`
- `NEXT_PUBLIC_API_WS_URL=ws://127.0.0.1:8000/ws/chat`

## Verification Component

### Responsibilities

- Execute foundation checks after code generation.
- Confirm lock files and build/test commands.

### Commands

- `pnpm install`
- `pnpm test:api`
- `pnpm typecheck:web`
- `pnpm build:web`

## Removed Legacy Components

### Root Python Package

- Current root `src/` is removed after migration.
- Current root `tests/` is removed after migration.

### Old Form UI

- Current FastAPI inline form UI is removed.
- No replacement form route is introduced.

## Component Interaction

```text
Root Workspace
  -> apps/api through dev/test scripts
  -> apps/web through dev/typecheck/build scripts
  -> .env.example for shared local defaults

apps/api
  -> uv.lock for Python reproducibility
  -> tests for backend regression coverage

apps/web
  -> pnpm-lock.yaml for frontend reproducibility
  -> next.config.ts for initial security headers
```
