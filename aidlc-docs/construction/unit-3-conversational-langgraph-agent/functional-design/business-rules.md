# Business Rules - Unit 3 Conversational LangGraph Agent

## Required Fields

The agent must collect all Unit 2 required fields before calculation:

- `sex`
- `age`
- `heightCM`
- `weightKG`
- `activityLevel`
- `goal`

## Candidate Extraction Rules

- Ollama may return any subset of supported fields.
- Ollama may return no fields.
- Ollama may not create final accepted state directly.
- Unsupported fields from Ollama are ignored or reported as invalid field candidates.
- Legacy misspelled aliases `heighCM` and `weighKG` are not accepted.

## Merge Rules

- Existing valid `collected_data` persists across turns.
- New valid candidate fields overwrite same-field previous values.
- Invalid candidate fields do not overwrite existing valid values.
- Accepted data must use canonical field names.

## Validation Rules

- `validateData` must use Unit 2 validation helpers.
- `data_valid` is true only when no required fields are missing and no invalid fields remain.
- Missing fields must be stable and use canonical names.
- Invalid fields must be represented as safe structured field errors.

## Routing Rules

- If `data_valid` is true, route exactly to `data_ok`.
- If `data_valid` is false, route exactly to `data_incomplete`.
- `data_ok` branch must execute `calculateDiet`, then `generateResponse`, then `END`.
- `data_incomplete` branch must execute `askRemainingData`, then `END`.

## Prompting Rules

- Missing-data prompts must ask only for missing or invalid fields.
- Prompt text must be concise and conversational.
- Prompt text must not expose raw stack traces, internal paths, or raw provider errors.
- Final response must include a short assistant message plus the structured diet result.

## Ollama Failure Rules

- If Ollama is unreachable, return a clear local setup message that instructs the user to start Ollama and confirm the model is available.
- If Ollama returns malformed JSON, treat extraction as no accepted candidate fields and ask for required data unless the current state is already complete.
- Provider failures must not mutate collected data.

## Logging Rules

- Do not log personal body data from user messages or collected state.
- Tests may inspect in-memory state; production logging should stay minimal.
