# NFR Design Patterns - Unit 1 Monorepo Foundation

## Pattern 1 - Fail-Fast Tooling Preconditions

### Requirement

Unit 1 must fail clearly if required tools are unavailable.

### Design

- Code-generation and verification commands must check for `uv` before Python dependency or test steps.
- Code-generation and verification commands must check for `pnpm` before frontend dependency or workspace steps.
- No fallback to `pip` or `npm` is allowed for Unit 1.

### Rationale

Fail-fast behavior prevents creating partial lock files or mixed package-manager state, supporting SECURITY-10 supply-chain reproducibility.

## Pattern 2 - Lock-File Reproducibility

### Requirement

Dependencies must be reproducible and use official registries.

### Design

- `apps/api` owns `pyproject.toml` and `uv.lock`.
- Root/frontend workspace owns `pnpm-lock.yaml`.
- Root scripts delegate to package-specific commands instead of hiding package-manager behavior.
- Generated docs and scripts should not instruct users to install dependencies with alternative package managers.

### Rationale

This satisfies SECURITY-10 for lock files and trusted registry dependency flow.

## Pattern 3 - Minimal Scaffold Surface

### Requirement

Initial scaffolding must not expose unnecessary debug/demo functionality.

### Design

- `apps/web` contains a minimal placeholder page only.
- The old form UI is removed from backend migration.
- No public `/api/diet` route is created in Unit 1.
- No chat/WebSocket route is introduced until Unit 4.

### Rationale

This supports SECURITY-09 by avoiding obsolete or accidental user-facing surfaces.

## Pattern 4 - Security Headers At The Frontend Boundary

### Requirement

Unit 1 should add initial security headers for the Next.js app.

### Design

`apps/web/next.config.ts` should define headers for all routes:

- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `Referrer-Policy: strict-origin-when-cross-origin`
- A basic local-compatible `Content-Security-Policy`

### Rationale

This partially addresses SECURITY-04 early. Backend-specific HTTP security middleware is deferred to Unit 4 because Unit 1 does not yet expose the final API surface.

## Pattern 5 - Structure-First Migration

### Requirement

Unit 1 must create the target structure and preserve testability without implementing later features.

### Design

- Move backend code into `apps/api/app`.
- Move backend tests into `apps/api/tests`.
- Remove root `src/` and root `tests/` after migration.
- Create directories for later modules only where useful; avoid placeholder business logic.

### Rationale

This reduces duplicate code paths and keeps later units focused on their specific responsibilities.

## Pattern 6 - Verification Gate

### Requirement

Unit 1 must prove the foundation is usable before downstream units begin.

### Design

Required checks after code generation:

- `pnpm install`
- `pnpm test:api`
- `pnpm typecheck:web`
- `pnpm build:web`
- Verify `apps/api/uv.lock` exists.
- Verify root `pnpm-lock.yaml` exists.

### Rationale

These checks confirm backend migration, frontend scaffold validity, and supply-chain lock-file expectations.

## Security Compliance

- SECURITY-04: Partially addressed through Next.js headers.
- SECURITY-09: Addressed by minimal scaffold surface and old UI removal.
- SECURITY-10: Addressed by `uv.lock`, `pnpm-lock.yaml`, and no fallback package managers.

## PBT Compliance

- PBT is N/A for Unit 1 implementation.
- The backend test layout supports future Unit 2 Hypothesis tests.
