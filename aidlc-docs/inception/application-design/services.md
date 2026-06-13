# Services

## Local Diet Service

- Orchestrates requests from the browser/API into the existing `build_diet_outline` function.
- Does not persist data.
- Does not call external APIs.
- Keeps calculation logic in the graph instead of duplicating formulas in the web layer.
