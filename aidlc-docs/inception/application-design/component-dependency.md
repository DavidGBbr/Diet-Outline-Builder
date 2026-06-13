# Component Dependency

## Dependencies

- Browser Form depends on Local Web App HTTP routes.
- Local Web App depends on Diet Graph Component.
- Diet Graph Component depends on LangGraph only.

## Data Flow

1. User opens `GET /` in the browser.
2. Browser submits form data to `POST /api/diet`.
3. Local Web App calls `build_diet_outline`.
4. Diet Graph returns the calculated response.
5. Browser renders calories, BMI, macros, explanation, disclaimer, and raw JSON.
