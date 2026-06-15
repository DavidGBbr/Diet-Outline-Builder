# Unit 3 Functional Design Plan - Conversational LangGraph Agent

## Purpose

Define the conversational LangGraph agent that extracts diet fields from user messages, merges only valid candidate data, routes through the required conditional graph branch, and returns either a missing-data prompt or final diet result.

## Ambiguity Assessment

No blocking user questions are required for Functional Design. Approved inception and Unit 2 artifacts already define:

- Graph flow: `extractData -> mergeValidFields -> validateData -> conditional edge`.
- Required conditional routes: `data_ok -> calculateDiet -> generateResponse -> END` and `data_incomplete -> askRemainingData -> END`.
- Ollama provider: local `llama3.1:8b` at `http://localhost:11434`.
- Ollama outputs are candidate data only.
- Deterministic Unit 2 validation is authoritative.
- Missing or invalid data must produce a follow-up prompt.
- Ollama unavailable must produce a clear safe error.

## Planned Functional Design Steps

- [x] Generate `business-logic-model.md`.
- [x] Generate `business-rules.md`.
- [x] Generate `domain-entities.md`.
- [x] Update AI-DLC state and audit log.
