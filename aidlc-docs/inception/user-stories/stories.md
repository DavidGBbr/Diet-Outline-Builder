# User Stories - Monorepo Conversational Agent Refactor

## Story 1 - Start A Guided Chat

As a Local Diet Builder User, I want to start a clean chat-based diet builder, so that I can provide my information conversationally instead of using a rigid form.

### Acceptance Criteria

- Given the frontend is running, when I open the local web app, then I see a clean minimal chat interface instead of the old form UI.
- Given I type a message, when I send it, then the message is displayed in the conversation.
- Given the backend is reachable, when I send a message, then the frontend sends it through the WebSocket chat session.
- Given user text is rendered in the chat, then it is safely escaped and cannot inject HTML/script content.

### INVEST Check

- Independent: Can be validated against the frontend shell and WebSocket send behavior.
- Negotiable: Visual polish can evolve while preserving clean minimal chat UX.
- Valuable: Replaces the core form workflow with the desired conversation experience.
- Estimable: Bounded to chat shell and basic message exchange.
- Small: Does not include extraction or final diet calculation.
- Testable: Verified through UI/manual check and WebSocket/backend tests.

## Story 2 - Extract And Store Provided User Data

As a Local Diet Builder User, I want the agent to understand diet details I provide in natural language, so that I do not need to answer one fixed question at a time.

### Acceptance Criteria

- Given I say `I am male, 22, 178cm, 87.4kg`, when the agent processes the message, then it stores all valid fields found in that message.
- Given I provide multiple required fields in one message, when those fields are valid, then the agent does not ask me to repeat them.
- Given I provide unsupported or invalid values, when the agent validates state, then it asks only for the invalid or missing fields.
- Given the backend receives a chat message, then the message has schema validation and explicit length bounds before processing.
- Given the extraction uses Ollama, when Ollama returns structured field candidates, then deterministic validation decides whether those fields are accepted.

### INVEST Check

- Independent: Focuses on extraction and state update only.
- Negotiable: Extraction prompt/schema can change while preserving accepted fields and validation behavior.
- Valuable: Makes the conversation flexible rather than fixed.
- Estimable: Bounded to required-field extraction and state update.
- Small: Does not include final calculation UI rendering.
- Testable: Verified with backend unit/API tests for multi-field and invalid-field messages.

## Story 3 - Route With Conditional LangGraph Validation

As a Local Diet Builder User, I want the agent to ask only for missing data until it has enough information, so that the final result is calculated only when the required data is complete.

### Acceptance Criteria

- Given conversation state is missing one or more required fields, when `validateData` runs, then it returns `data_valid = false` and a list of missing fields.
- Given `data_valid = false`, when the conditional edge runs, then the graph routes to `askRemainingData` and ends the current turn after asking for missing fields.
- Given all required fields are valid, when `validateData` runs, then it returns `data_valid = true` and no missing fields.
- Given `data_valid = true`, when the conditional edge runs, then the graph routes to `calculateDiet`, then `generateResponse`, then ends.
- Given the graph is tested, then tests cover both conditional branches.

### INVEST Check

- Independent: Captures the core graph control flow requirement.
- Negotiable: Node names can map to Python naming conventions while preserving behavior.
- Valuable: Prevents incomplete or premature diet calculations.
- Estimable: Bounded to graph state validation and conditional routing.
- Small: Does not require frontend implementation.
- Testable: Verified with LangGraph/backend tests.

## Story 4 - Receive The Final Diet Result

As a Local Diet Builder User, I want the agent to return my diet outline immediately once all required data is valid, so that I can see BMI, calories, macros, and the explanation without extra confirmation steps.

### Acceptance Criteria

- Given all required fields are valid, when the graph routes to calculation, then the deterministic diet calculation logic is used.
- Given the final result is generated, then it includes `imc`, `imcClassification`, `totalSpend`, `targetSpend`, `goal`, `macros`, `explanation`, and `safetyDisclaimer`.
- Given the output is shown in the chat, then the explanation includes macro/calorie assumptions and the safety disclaimer.
- Given deterministic calculation functions are tested, then property-based tests cover applicable validation/calculation invariants in partial PBT mode.

### INVEST Check

- Independent: Focuses on final result generation and rendering contract.
- Negotiable: Result presentation can evolve while preserving response fields.
- Valuable: Delivers the user-facing outcome of the app.
- Estimable: Bounded to final calculation and chat response.
- Small: Does not include local setup or Ollama errors.
- Testable: Verified through backend tests and manual UI result check.

## Story 5 - Preserve Conversation After Refresh

As a Local Diet Builder User, I want the conversation to remain after refreshing the page, so that I do not lose progress while entering my data.

### Acceptance Criteria

- Given I have chat messages in the browser, when I refresh the page, then the frontend restores the conversation from `localStorage`.
- Given stored conversation data exists, when the frontend loads, then it restores only client-side state and does not require a backend database.
- Given stored messages are rendered, then user-provided text is safely escaped.
- Given the app stores local state, then no secrets or API keys are stored in `localStorage`.

### INVEST Check

- Independent: Frontend persistence can be implemented separately from backend storage.
- Negotiable: Exact stored shape can change.
- Valuable: Improves local usability.
- Estimable: Bounded to browser storage and restore behavior.
- Small: Does not introduce database persistence.
- Testable: Verified manually or through lightweight frontend checks.

## Story 6 - Run The Monorepo Locally With Ollama

As a Developer/Operator, I want clear local setup and run commands, so that I can start Ollama, the backend, and the frontend without guessing.

### Acceptance Criteria

- Given a fresh checkout, when I follow README setup instructions, then I can install dependencies for the pnpm workspace and Python API.
- Given Ollama is installed, when I run the documented command, then `llama3.1:8b` is pulled or confirmed available.
- Given local environment configuration is needed, then root `.env.example` documents `OLLAMA_BASE_URL=http://localhost:11434` and the default model.
- Given dependencies are installed, then lock files are committed for package-manager reproducibility.
- Given tests are documented, then the README includes commands for backend tests and relevant frontend checks.

### INVEST Check

- Independent: Setup can be validated without completing all conversation features.
- Negotiable: Script names can change if documented.
- Valuable: Makes the local-first app usable by the developer/operator.
- Estimable: Bounded to project structure, config, and docs.
- Small: Does not include cloud deployment.
- Testable: Verified by running install/start/test commands.

## Story 7 - Handle Local Runtime And Security Failures Safely

As a Developer/Operator, I want local runtime failures and unsafe inputs handled clearly, so that the app fails safely without leaking internals or confusing the user.

### Acceptance Criteria

- Given Ollama is not running, when the user sends a chat message requiring LLM extraction, then the API/UI returns a clear instruction to start Ollama.
- Given an API or WebSocket error occurs, then the user-facing response does not expose stack traces, internal paths, or framework internals.
- Given frontend origin restrictions are configured, then CORS allows the local frontend origin and does not use wildcard origins for the app API.
- Given HTTP content is served, then applicable security headers are set or documented with local-development justification.
- Given personal body data is processed, then logs avoid unnecessary sensitive personal data.

### INVEST Check

- Independent: Error/security behavior can be tested separately from full happy path.
- Negotiable: Exact wording can change while remaining clear and safe.
- Valuable: Reduces local runtime confusion and supports security baseline compliance.
- Estimable: Bounded to local error paths, logging, CORS, and headers.
- Small: Does not include authentication or cloud hardening.
- Testable: Verified with backend tests and configuration review.

## Story Coverage Summary

- Journey coverage: Stories 1, 2, 3, 4, 5.
- Feature/setup coverage: Stories 6, 7.
- Security acceptance criteria embedded: Stories 1, 2, 5, 6, 7.
- PBT acceptance criteria embedded: Story 4.
- Personas covered: Local End User, Developer/Operator, Nutrition Professional Reviewer.
