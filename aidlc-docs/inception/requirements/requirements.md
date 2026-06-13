# Requirements

## Intent Analysis

- User Request: Build a diet outline builder using Python and LangGraph.
- Request Type: New project.
- Scope Estimate: Single service/library with CLI and tests.
- Complexity Estimate: Simple to moderate due to nutrition calculation correctness.

## Functional Requirements

- Accept user fields: `sex`, `age`, `heightCM`, `weightKG`, `activityLevel`, and `goal`.
- Accept the prompt aliases `heighCM` and `weighKG` for the misspelled sample fields.
- Validate supported values for sex, activity level, goal, and reasonable numeric ranges.
- Build a LangGraph with nodes for input validation, anthropometrics, energy, macros, explanation, and safety disclaimer.
- Return BMI as `imc` rounded to one decimal and a BMI classification.
- Estimate daily caloric expenditure with Mifflin-St Jeor BMR and activity factors.
- Apply goal adjustments: 20% deficit for fat loss, no change for maintenance, 10% surplus for muscle gain.
- Calculate protein in the 1.6 to 2.0 g/kg range based on BMI classification, using lower g/kg targets for higher BMI classifications.
- Calculate fat in the 0.6 to 1.0 g/kg range based on BMI classification.
- Calculate carbohydrates from the remaining calories after protein and fat.
- Provide an educational safety disclaimer.
- Provide a local browser UI so the user can run the application locally without writing Python one-liners.
- Expose a local JSON endpoint that accepts the same diet input contract and returns the same diet outline response.
- Keep the existing CLI and library API working.

## Non-Functional Requirements

- Calculations should be deterministic and unit-testable.
- The package should run without an LLM provider or API key.
- The graph should be reusable as a Python library and available through a CLI.
- The local UI should run on localhost and require no external services.
