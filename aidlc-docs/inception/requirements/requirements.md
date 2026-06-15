# Requirements - Monorepo Conversational Agent Refactor

## Intent Analysis

- User Request: Refactor the existing Diet Outline Builder into a monorepo with a dedicated frontend module and a conversational LangGraph agent that collects user data through chat before returning the diet result.
- Request Type: Brownfield refactor plus feature enhancement.
- Scope Estimate: System-wide project restructuring across backend, frontend, packaging, local runtime, and tests.
- Complexity Estimate: Complex, because it changes repository architecture, introduces a real local LLM provider, adds WebSocket conversation flow, and enables security/PBT constraints.

## Existing Behavior To Preserve

- The core diet calculation must continue to produce deterministic results after all required fields are collected.
- BMI must be returned as `imc`, rounded to one decimal.
- BMI classification must remain available as `imcClassification`.
- Energy calculation must continue to estimate total daily expenditure and goal-adjusted target spend.
- Macro rules must remain:
  - Protein: 1.6 to 2.0 g/kg based on BMI classification, with lower g/kg targets for higher BMI classifications.
  - Fat: 0.6 to 1.0 g/kg based on BMI classification.
  - Carbohydrates: remaining calories after protein and fat.
- Safety disclaimer must remain in the final result.
- Existing direct calculation endpoint behavior may remain available internally, but the old form-based UI must be replaced.

## Monorepo Requirements

- The repository must become a monorepo using `pnpm` workspaces.
- The monorepo must include:
  - `apps/web`: Next.js with React and TypeScript.
  - `apps/api`: Python FastAPI service containing the LangGraph backend.
- Root workspace configuration must support installing and running both modules locally.
- Root `.env.example` must document required local configuration.
- The root `.env` must be used for shared local configuration.

## Backend Requirements

- The Python backend must live in `apps/api` as a FastAPI service.
- The backend must expose a WebSocket chat endpoint for the conversational agent.
- The backend must keep diet calculations centralized in reusable Python logic, not duplicated in the frontend.
- The backend must use LangGraph to manage the conversation state and final calculation flow.
- The backend must integrate with Ollama as the local LLM provider.
- Default Ollama model: `llama3.1:8b`.
- Default Ollama base URL: `http://localhost:11434`.
- If Ollama is unavailable, the API/UI must return a clear error instructing the user to start Ollama.
- The backend must not require external cloud LLM APIs or paid API keys.

## Conversational Agent Requirements

- The interface must be conversational instead of form-based.
- The agent must collect these required fields before producing the final answer:
  - `sex`
  - `age`
  - `heightCM`
  - `weightKG`
  - `activityLevel`
  - `goal`
- The conversation must be guided but not rigid.
- If the user provides multiple fields in one message, the agent must extract and store all valid fields and avoid asking repeated questions.
- The agent must ask for only missing or invalid required fields.
- The agent must produce the final diet result immediately after all required fields are valid.
- The final response must include the calculated diet result and a concise explanation.
- The final response must include the safety disclaimer.
- The LangGraph conversation flow must include a validation node before diet calculation.
- The validation node must identify missing required fields and set a boolean state flag indicating whether all required data is available.
- The graph must use a conditional edge after validation:
  - If all required data is present, route to the diet calculation node.
  - If required data is missing, route to a node that asks the user for only the remaining missing data.
- The missing-data branch must end the current turn after asking for the missing fields; the next user message resumes the graph with updated conversation state.
- The diet calculation branch must continue to response generation and then end.

## Required LangGraph Control Flow

The conversational agent graph must follow this routing model:

```text
START
  -> validateData
  -> conditional edge:
       data_ok -> calculateDiet -> generateResponse -> END
       data_incomplete -> askRemainingData -> END
```

The conditional routing function must inspect validation state, not duplicate the diet calculation logic.

## Frontend Requirements

- The frontend must be a Next.js React TypeScript application in `apps/web`.
- The UI must prioritize a clean, minimal chat interface focused on usability.
- The old form-based local UI must be removed/replaced by the conversational UI.
- Conversation state must persist after page refresh using browser `localStorage`.
- The frontend must communicate with the backend through a WebSocket chat session.
- The UI must show a clear error if the backend reports that Ollama is unavailable.
- The UI must be usable on desktop and mobile widths.

## Testing Requirements

- Backend unit tests are required.
- Backend API/WebSocket tests are required.
- Existing diet calculation tests must continue to pass after refactor.
- Frontend component tests and Playwright end-to-end tests are not required in this phase.
- Property-based testing is partially enabled:
  - Enforce PBT for pure validation/calculation functions where applicable.
  - Do not require full stateful PBT for the conversation workflow in this phase.

## Security Requirements

- Security Baseline extension is enabled for this refactor.
- API inputs, including WebSocket messages, must be schema-validated with type and length bounds.
- User-supplied strings must be sanitized or safely escaped before rendering.
- The app must not log sensitive personal health/body data unnecessarily.
- Error responses must not expose stack traces or internal paths.
- HTTP-serving endpoints must include required security headers where applicable.
- CORS must be restricted to explicit local frontend origins, not wildcard origins.
- Dependencies must use lock files and official registries.
- The app remains local-first and does not require authentication in this phase; endpoints must be explicitly documented as local public endpoints.

## Non-Functional Requirements

- The local app must run without paid services.
- The setup instructions must include how to install dependencies, start Ollama, pull the selected model, run the backend, and run the frontend.
- The architecture must keep the LLM extraction/conversation layer separate from deterministic diet calculations.
- The project must remain maintainable with clear module boundaries between web UI, API, LangGraph agent, and diet calculation logic.
- The implementation should avoid unnecessary infrastructure, databases, Docker, or deployment work in this phase.

## Out Of Scope For This Phase

- User authentication.
- Database-backed conversation persistence.
- Cloud deployment.
- Meal plan generation.
- Dietary restrictions, allergies, food preferences, or meals-per-day collection.
- Streaming responses unless needed internally for WebSocket message handling.
- Frontend component tests and Playwright e2e tests.

## Extension Compliance Summary

- Security Baseline: Enabled. Requirements include input validation, safe errors, local-only public endpoint documentation, security headers, restricted CORS, no unnecessary PII logging, and dependency lock files.
- Property-Based Testing: Partial. Requirements enforce PBT for pure validation/calculation functions where applicable, while stateful conversation PBT remains advisory for this phase.
