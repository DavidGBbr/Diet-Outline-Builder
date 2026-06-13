# Components

## Diet Graph Component

- Purpose: Own deterministic diet calculations through the existing LangGraph workflow.
- Responsibilities: Validate input, calculate BMI, energy expenditure, goal target, macros, explanation, and disclaimer.
- Interface: `build_diet_outline(payload: dict) -> DietResponse`.

## Local Web App Component

- Purpose: Provide a localhost browser experience for running the diet builder.
- Responsibilities: Serve the HTML form and expose the local JSON API endpoint.
- Interface: HTTP `GET /` for the form and `POST /api/diet` for calculations.

## Browser Form Component

- Purpose: Capture user inputs without requiring command-line JSON.
- Responsibilities: Collect fields, call `/api/diet`, and render the result or validation errors.
- Interface: HTML form with JavaScript `fetch`.
