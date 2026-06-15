# NFR Requirements - Unit 1 Monorepo Foundation

## Scope

Unit 1 establishes the local monorepo foundation. The main non-functional requirements are reproducibility, maintainability, local developer usability, and Security Baseline compliance for dependency management and safe scaffolding.

## Runtime Requirements

- Python target: 3.11+.
- Node.js target: 20+.
- pnpm is required for the workspace.
- uv is required for the Python API project.
- If `uv` is unavailable during implementation or setup, the process must fail with a clear instruction to install `uv`.
- If `pnpm` is unavailable during implementation or setup, the process must fail with a clear instruction to install `pnpm`.

## Local Port Requirements

- API default port: `8000`.
- Web default port: `3000`.
- Ollama default port: `11434`.
- Root `.env.example` must document these defaults.

## Reproducibility Requirements

- `apps/api` must use `uv` with `pyproject.toml` and `uv.lock`.
- Frontend workspace dependencies must be managed with pnpm and `pnpm-lock.yaml`.
- Dependencies must come from official registries.
- The migrated backend tests must run from the new `apps/api` structure.
- Root scripts must delegate to package-specific commands without hiding failures.

## Maintainability Requirements

- The target structure must avoid duplicate source trees.
- Old root `src/` and root `tests/` must be removed after migration.
- The old form UI must be removed during Unit 1 because it conflicts with the approved target design.
- `apps/api/app` must be prepared for later `agent/`, `domain/`, `schemas/`, and `services/` modules.
- `apps/web` must be a minimal Next.js shell, not a full chat implementation.

## Security Requirements

- SECURITY-09: Initial app scaffolding must not add unnecessary exposed demo/debug routes beyond normal local development pages.
- SECURITY-10: Lock files must be generated and committed for Python and frontend dependencies.
- SECURITY-04: Unit 1 should add initial Next.js security headers in `next.config.ts`; detailed backend header middleware may be implemented in Unit 4.
- SECURITY-05: Unit 1 must preserve structure for later schema validation but does not implement WebSocket/API validation yet.
- No real secrets may be committed.

## Verification Requirements

Minimum Unit 1 verification after code generation:

- Backend tests pass from `apps/api`.
- Frontend typecheck succeeds.
- Frontend build succeeds.
- `uv.lock` exists.
- `pnpm-lock.yaml` exists.
- Root `.env.example` exists and documents local defaults.

## Availability And Scalability Requirements

- No production availability or scalability requirements apply in Unit 1.
- Local development commands should fail clearly when required tools are missing.

## Usability Requirements

- Root scripts must make common local commands discoverable.
- README updates may be deferred to Unit 6, but Unit 1 scripts and `.env.example` should be self-explanatory enough for later documentation.

## PBT Requirements

- No property-based tests are required in Unit 1.
- The API test layout must support Unit 2 Hypothesis tests.

## Compliance Summary

- SECURITY-09: Applicable, addressed by minimal app scaffolding.
- SECURITY-10: Applicable, addressed by `uv.lock` and `pnpm-lock.yaml` requirements.
- SECURITY-04: Partially applicable, addressed by initial Next.js headers.
- SECURITY-05: Prepared but detailed implementation deferred to backend API units.
- PBT partial: N/A for Unit 1 implementation, but test layout must support Unit 2.
