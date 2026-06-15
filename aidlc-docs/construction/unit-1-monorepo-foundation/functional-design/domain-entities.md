# Domain Entities - Unit 1 Monorepo Foundation

Unit 1 is a repository-structure unit, so its entities are project/module entities rather than nutrition-domain entities.

## Workspace

- Represents the root monorepo.
- Owns pnpm workspace configuration, root scripts, root environment template, and documentation.

Fields:

- `packages`: workspace package globs, initially `apps/*`.
- `scripts`: root command aliases.
- `environmentTemplate`: root `.env.example`.

## ApiApp

- Represents the Python FastAPI backend package in `apps/api`.
- Owns Python dependencies, migrated backend code, and backend tests.

Fields:

- `path`: `apps/api`.
- `packageName`: `app`.
- `dependencyManager`: `uv`.
- `testPath`: `apps/api/tests`.

## WebApp

- Represents the Next.js frontend package in `apps/web`.
- Owns initial Next.js shell and frontend scripts.

Fields:

- `path`: `apps/web`.
- `framework`: `Next.js`.
- `language`: `TypeScript`.
- `packageManager`: `pnpm`.

## Migration

- Represents movement from current root Python package to target monorepo modules.

Fields:

- `sourcePaths`: current root `src/` and `tests/`.
- `targetPaths`: `apps/api/app` and `apps/api/tests`.
- `removeSourceAfterMove`: true.
- `removeOldFormUi`: true.

## EnvironmentVariable

- Represents local runtime configuration documented in `.env.example`.

Fields:

- `name`: variable name.
- `defaultValue`: non-secret local default.
- `consumer`: API or web package.
