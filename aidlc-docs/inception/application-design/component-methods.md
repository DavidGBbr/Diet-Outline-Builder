# Component Methods

## Diet Graph Component

- `build_diet_outline(payload: dict) -> DietResponse`: Runs the compiled LangGraph and returns the final response.

## Local Web App Component

- `create_app() -> FastAPI`: Creates the local FastAPI application.
- `index() -> HTMLResponse`: Serves the local browser UI.
- `calculate_diet(payload: dict) -> dict`: Validates request payload through the graph and returns the diet outline.

## Browser Form Component

- `submit` handler: Serializes form values, calls `/api/diet`, and renders JSON plus user-friendly macro cards.
