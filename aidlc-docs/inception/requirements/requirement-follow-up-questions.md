# Requirement Follow-Up Questions - Ollama Configuration

Your main answers are complete. These follow-up questions resolve the remaining ambiguity from choosing Ollama as the local LLM provider.

Please fill every `[Answer]:` line, then tell me to continue.

## Question 1

Which Ollama model should the API use by default for the conversational agent?

A) `llama3.1:8b` - general-purpose default, good local baseline
B) `llama3.2:3b` - lighter and faster on weaker machines
C) `mistral:7b` - strong general instruction-following option
D) `qwen2.5:7b` - good structured extraction and reasoning option
X) Other (please describe the exact Ollama model name after [Answer]: tag below)

[Answer]: option A

## Question 2

How should the app handle Ollama not running locally?

A) Return a clear API/UI error telling the user to start Ollama
B) Fall back to deterministic rule-based extraction without LLM
C) Block app startup if Ollama is unavailable
X) Other (please describe after [Answer]: tag below)

[Answer]: option A

## Question 3

Which Ollama base URL should be the default in `.env.example`?

A) `http://localhost:11434`
B) `http://127.0.0.1:11434`
X) Other (please describe the exact URL after [Answer]: tag below)

[Answer]: option A
