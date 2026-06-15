# Business Logic Model - Unit 1 Monorepo Foundation

## Unit Goal

Unit 1 establishes the repository structure and local runtime foundation required by later units. It does not introduce new diet business behavior. Its core functional behavior is migration and scaffolding: move the existing backend into `apps/api`, create the frontend shell in `apps/web`, and preserve backend testability.

## Migration Flow

```text
current root Python package
  -> apps/api/app package
  -> apps/api/tests
  -> root pnpm workspace
  -> apps/web Next.js shell
  -> root scripts and .env.example
```

## Functional Operations

### Create Monorepo Root

- Add `pnpm-workspace.yaml` including `apps/*`.
- Add root `package.json` with workspace scripts.
- Keep AI-DLC docs and AWS AI-DLC rule docs at root.

### Create API App

- Create `apps/api` as a Python project managed by `uv`.
- Rename the backend package to `app`, following approved layout.
- Move reusable calculation code from root `src/diet_outline_builder` into `apps/api/app`.
- Remove old local form UI code from the target backend.
- Move/adapt root backend tests into `apps/api/tests`.

### Create Web App Shell

- Create a minimal hand-written Next.js React TypeScript app shell.
- Add only enough UI to prove the app starts; full chat UI is Unit 5.
- Add Next.js config placeholder for future security headers.

### Preserve Testability

- Backend tests must remain runnable from the new `apps/api` context.
- Root script `test:api` must delegate to the API test command.

## Inputs

- Existing root Python source files.
- Existing root tests.
- Approved AI-DLC design and unit artifacts.

## Outputs

- Monorepo structure.
- Migrated API package.
- Minimal web package.
- Updated root scripts and environment template.
- Removed duplicate old root source/test copies after successful migration.

## Non-Goals

- No conversational agent implementation.
- No WebSocket endpoint.
- No Ollama integration beyond environment defaults.
- No final chat UI beyond app shell.
- No PBT implementation yet.
