# Tech Stack Decisions - Unit 1 Monorepo Foundation

## Monorepo Package Manager

Decision: Use `pnpm` workspaces.

Rationale:

- Matches approved requirements.
- Provides deterministic workspace dependency management through `pnpm-lock.yaml`.
- Keeps frontend scripts centralized while preserving package boundaries.

Required files:

- `pnpm-workspace.yaml`
- root `package.json`
- `pnpm-lock.yaml`

## Python Dependency Manager

Decision: Use `uv` for `apps/api`.

Rationale:

- Produces `uv.lock` for reproducibility and Security Baseline supply-chain requirements.
- Works with `pyproject.toml`.
- Fast local install/test workflow.

Required files:

- `apps/api/pyproject.toml`
- `apps/api/uv.lock`

## Python Runtime

Decision: Target Python 3.11+.

Rationale:

- Compatible with existing code requirements.
- Avoids unnecessarily requiring latest local Python versions.
- Broad support for FastAPI, LangGraph, pytest, and Hypothesis in later units.

## Node Runtime

Decision: Target Node.js 20+.

Rationale:

- Stable baseline for modern Next.js and TypeScript.
- Avoids forcing Node.js 22+ for a local prototype.

## Frontend Framework

Decision: Use a minimal hand-written Next.js React TypeScript shell in `apps/web`.

Rationale:

- Avoids interactive scaffolding.
- Keeps Unit 1 focused on structure, not chat UI.
- Prepares the exact target path for Unit 5.

Required initial files:

- `apps/web/package.json`
- `apps/web/app/layout.tsx`
- `apps/web/app/page.tsx`
- `apps/web/app/globals.css`
- `apps/web/tsconfig.json`
- `apps/web/next.config.ts`

## Security Headers

Decision: Add initial frontend security headers through `next.config.ts`.

Rationale:

- Satisfies early SECURITY-04 planning for HTML-serving frontend.
- Keeps detailed backend middleware for later API units.

Initial headers:

- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `Referrer-Policy: strict-origin-when-cross-origin`
- Basic `Content-Security-Policy` compatible with local Next.js development/build.

## Local Environment Defaults

Decision: Root `.env.example` documents shared local defaults.

Required values:

- `OLLAMA_BASE_URL=http://localhost:11434`
- `OLLAMA_MODEL=llama3.1:8b`
- `API_HOST=127.0.0.1`
- `API_PORT=8000`
- `WEB_PORT=3000`
- `NEXT_PUBLIC_API_WS_URL=ws://127.0.0.1:8000/ws/chat`

## Verification Stack

Decision: Unit 1 must verify backend tests and frontend build/typecheck.

Rationale:

- Confirms migration did not break existing backend behavior.
- Confirms the hand-written Next.js shell is valid.
- Confirms lock-file expectations are met before downstream units build on the foundation.

Expected commands after code generation:

- `pnpm install`
- `pnpm test:api`
- `pnpm typecheck:web`
- `pnpm build:web`

## Rejected Alternatives

- `pip` only: rejected because Security Baseline expects lock-file reproducibility.
- Poetry: rejected because `uv` is simpler for this project and was approved.
- `create-next-app`: rejected to avoid interactive generator behavior and keep Unit 1 minimal.
- Integrated root `dev` script now: rejected until backend/frontend integration exists.
