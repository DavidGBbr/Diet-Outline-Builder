# Business Rules

- The UI must not reimplement diet formulas.
- The API endpoint must delegate calculations to `build_diet_outline`.
- Invalid input must return a client error instead of a server crash.
- The app must remain local-first and require no external account, database, or LLM key.
