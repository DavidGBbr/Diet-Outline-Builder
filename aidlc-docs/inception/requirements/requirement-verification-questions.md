# Requirement Verification Questions - Monorepo Conversational Agent Refactor

Please answer all questions by filling the `[Answer]:` line. After you finish, tell me to continue and I will validate the answers before moving to Workflow Planning.

## Question 1

Which frontend module should the monorepo use?

A) Next.js with React and TypeScript
B) Vite with React and TypeScript
C) Plain HTML/CSS/JavaScript inside a frontend package
X) Other (please describe after [Answer]: tag below)

[Answer]: option A

## Question 2

Which monorepo/package manager setup should we use?

A) pnpm workspace with `apps/web` and `apps/api`
B) npm workspaces with `apps/web` and `apps/api`
C) Keep Python packaging at root and add `apps/web` only
X) Other (please describe after [Answer]: tag below)

[Answer]: option A

## Question 3

Where should the Python LangGraph backend live after the refactor?

A) `apps/api` as a FastAPI Python service
B) `packages/diet-agent` as a Python package plus a thin API app
C) Keep it under `src/diet_outline_builder` and only add frontend module
X) Other (please describe after [Answer]: tag below)

[Answer]: option A

## Question 4

Should the conversational agent use a real LLM provider or remain deterministic/rule-based for now?

A) Deterministic LangGraph conversation only, no LLM/API key
B) OpenAI-compatible provider through OpenRouter
C) OpenAI directly
D) Anthropic directly
X) Other (please describe after [Answer]: tag below)

[Answer]: Let's use ollama to run it locally

## Question 5

If using an LLM provider, where should the model name and key be configured?

A) `.env` in the API app with `.env.example` committed
B) Root `.env` with `.env.example` committed
C) Do not configure now; leave provider integration as a future phase
X) Other (please describe after [Answer]: tag below)

[Answer]: option B

## Question 6

How should the agent collect the required diet fields from the user?

A) Ask one question at a time in chat until all fields are collected
B) Allow freeform messages and extract multiple fields when mentioned
C) Hybrid: ask one question at a time but accept extra fields from freeform replies
X) Other (please describe after [Answer]: tag below)

[Answer]: option C) needs to be a guided conversation but not fixed, if the user send to us good part of the necessary information we don't need to repeat the question

## Question 7

What exact fields must be collected before the final result?

A) Current fields only: sex, age, heightCM, weightKG, activityLevel, goal
B) Current fields plus dietary restrictions/allergies
C) Current fields plus meals per day and food preferences
D) Current fields plus restrictions, preferences, and meals per day
X) Other (please describe after [Answer]: tag below)

[Answer]: option A

## Question 8

When should the agent produce the final diet result?

A) Immediately after all required fields are valid
B) Ask the user to confirm collected data before final calculation
C) Show a draft and ask whether to adjust goal/activity before final calculation
X) Other (please describe after [Answer]: tag below)

[Answer]: option A

## Question 9

Should conversation state persist after page refresh?

A) No, keep it in browser memory only
B) Use browser localStorage only
C) Store sessions in the backend process memory
D) Store sessions in a database
X) Other (please describe after [Answer]: tag below)

[Answer]: option B

## Question 10

How should the frontend communicate with the agent backend?

A) Simple HTTP POST per message, return full updated conversation state
B) Server-Sent Events for streaming assistant responses
C) WebSocket chat session
X) Other (please describe after [Answer]: tag below)

[Answer]: option C

## Question 11

What should the UI prioritize visually?

A) Clean minimal chat interface focused on usability
B) Premium polished product UI with stronger visual design
C) Developer/debug interface showing state transitions and graph nodes
X) Other (please describe after [Answer]: tag below)

[Answer]: option A

## Question 12

Should the old form-based local UI remain available?

A) No, replace it completely with the conversational UI
B) Yes, keep it as a debug/manual calculator route
C) Keep only the `/api/diet` endpoint, remove the form page
X) Other (please describe after [Answer]: tag below)

[Answer]: option A

## Question 13

What tests should be required for this refactor?

A) Backend unit tests and API tests only
B) Backend tests plus frontend component tests
C) Backend tests plus Playwright end-to-end browser tests
D) Backend tests, frontend component tests, and Playwright e2e tests
X) Other (please describe after [Answer]: tag below)

[Answer]: option A

## Question 14

Should security extension rules be enforced for this refactor?

A) Yes, enforce security baseline rules as blocking constraints
B) No, keep security baseline disabled for this local prototype
X) Other (please describe after [Answer]: tag below)

[Answer]: option A

## Question 15

Should property-based testing rules be enforced for the conversation/data extraction logic?

A) Yes, enforce PBT rules for the state machine and validation logic
B) Partial, only for pure validation/calculation functions
C) No, keep normal unit/integration tests only
X) Other (please describe after [Answer]: tag below)

[Answer]: option B
