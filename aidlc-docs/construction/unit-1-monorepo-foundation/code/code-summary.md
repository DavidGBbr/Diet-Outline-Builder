# Code Summary - Unit 1 Monorepo Foundation

## Created

- `pnpm-workspace.yaml`
- `package.json`
- `.env.example`
- `apps/api/pyproject.toml`
- `apps/api/uv.lock`
- `apps/api/app/__init__.py`
- `apps/api/app/graph.py`
- `apps/api/tests/test_diet_graph.py`
- `apps/web/package.json`
- `apps/web/app/layout.tsx`
- `apps/web/app/page.tsx`
- `apps/web/app/globals.css`
- `apps/web/next.config.ts`
- `apps/web/tsconfig.json`
- `apps/web/next-env.d.ts`
- `pnpm-lock.yaml`

## Moved / Adapted

- `src/diet_outline_builder/graph.py` -> `apps/api/app/graph.py`
- `src/diet_outline_builder/__init__.py` -> `apps/api/app/__init__.py`
- `tests/test_diet_graph.py` -> `apps/api/tests/test_diet_graph.py`
- Backend test imports changed from `diet_outline_builder` to `app`.

## Removed

- Root `pyproject.toml`
- Root `src/` Python package
- Root `tests/` test package
- Old FastAPI inline form UI (`src/diet_outline_builder/web.py`)
- Old CLI entrypoints (`src/diet_outline_builder/cli.py`, `src/diet_outline_builder/__main__.py`)
- Old form-route tests (`tests/test_web_app.py`)

## Modified

- `.gitignore` now ignores Node/Next.js generated artifacts.
- `apps/api/pyproject.toml` includes `pythonpath = ["."]` so `uv run pytest` imports `app` reliably.

## Verification

- `uv --version`: passed.
- `pnpm --version`: passed.
- `uv lock`: passed and generated `apps/api/uv.lock`.
- `pnpm install`: passed and generated `pnpm-lock.yaml`.
- `pnpm test:api`: passed, 4 tests.
- `pnpm typecheck:web`: passed.
- `pnpm build:web`: passed.

## Security Compliance

- SECURITY-09: Old form UI removed and no replacement public diet route was introduced.
- SECURITY-10: Python and frontend lock files generated.
- SECURITY-04: Initial Next.js security headers added in `apps/web/next.config.ts`.

## PBT Compliance

- PBT is N/A for Unit 1.
- Backend test layout is ready for Unit 2 Hypothesis tests.
