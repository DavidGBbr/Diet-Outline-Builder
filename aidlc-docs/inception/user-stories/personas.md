# Personas - Monorepo Conversational Agent Refactor

## Persona 1 - Local End User

- Name: Local Diet Builder User
- Goal: Enter personal body/activity/goal information through a natural chat and receive a diet outline.
- Motivation: Avoid manually filling a rigid form and get the result with minimal friction.
- Technical comfort: Basic. Can open a local web app but should not need to understand API payloads.
- Needs:
  - Guided conversation that asks for missing data only.
  - Clear errors when local services are unavailable.
  - Results that include BMI, calories, macros, explanation, and disclaimer.
  - Conversation state retained after refreshing the browser.

## Persona 2 - Developer/Operator

- Name: Local App Operator
- Goal: Run the monorepo locally, start Ollama, run backend/frontend modules, and verify behavior through tests.
- Motivation: Maintain and evolve the project safely.
- Technical comfort: High. Comfortable with pnpm, Python, FastAPI, Next.js, and local services.
- Needs:
  - Clear setup instructions and root scripts.
  - Explicit Ollama model and URL configuration.
  - Tests for calculations, validation, WebSocket flow, and local error paths.
  - Dependency lock files and security-conscious defaults.

## Persona 3 - Nutrition Professional Reviewer

- Name: Nutrition Reviewer
- Goal: Review the final diet outline format and safety boundaries, without expanding this phase into meal planning or medical advice.
- Motivation: Ensure the app communicates estimates responsibly.
- Technical comfort: Low to medium. Primarily reviews outputs and wording.
- Needs:
  - Clear disclaimer that the output is educational, not medical advice.
  - Visible macro and calorie assumptions.
  - No unsupported claims or hidden calculations in the UI.

## Persona-To-Story Map

- Local Diet Builder User: Stories 1, 2, 3, 4, 5
- Local App Operator: Stories 4, 5, 6, 7
- Nutrition Reviewer: Stories 3, 7
