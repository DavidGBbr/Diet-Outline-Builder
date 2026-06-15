# Unit Of Work Dependency - Monorepo Conversational Agent Refactor

## Dependency Matrix

| Unit | Depends On | Blocks | Parallelization Notes |
|---|---|---|---|
| Unit 1 - Monorepo Foundation | Approved application design | Units 2, 3, 4, 5, 6 | Must run first because paths, package config, and test locations change. |
| Unit 2 - Backend Diet Domain Preservation | Unit 1 | Unit 3, Unit 4 tests, Unit 6 verification | Can start once backend code is moved. Must finish before agent calculation branch. |
| Unit 3 - Conversational LangGraph Agent | Unit 1, Unit 2 | Unit 4, Unit 5 integration, Unit 6 verification | Backend-only work. Requires domain functions and Ollama config. |
| Unit 4 - FastAPI WebSocket API | Unit 1, Unit 2, Unit 3 | Unit 5 integration, Unit 6 verification | Requires message schemas and graph service. |
| Unit 5 - Next.js Conversational UI | Unit 1, Unit 4 | Unit 6 verification | Can build static shell earlier, but approved sequencing integrates after backend WebSocket exists. |
| Unit 6 - Documentation And Verification | Units 1-5 | Completion | Runs last after implementation units. |

## Required Sequence

1. Unit 1 - Monorepo Foundation
2. Unit 2 - Backend Diet Domain Preservation
3. Unit 3 - Conversational LangGraph Agent
4. Unit 4 - FastAPI WebSocket API
5. Unit 5 - Next.js Conversational UI
6. Unit 6 - Documentation And Verification

## Why This Order

- Unit 1 prevents duplicate path migrations later.
- Unit 2 preserves deterministic regression coverage before introducing LLM behavior.
- Unit 3 builds the required conditional LangGraph behavior before transport integration.
- Unit 4 exposes the graph through a validated WebSocket protocol.
- Unit 5 integrates against the completed backend protocol.
- Unit 6 verifies the full local workflow after all moving parts exist.

## Critical Dependency Constraints

- Frontend must not calculate diet formulas; it depends on backend result messages.
- Agent graph must not trust Ollama output directly; it depends on Unit 2 validators.
- WebSocket API must validate frontend-supplied state every turn.
- Documentation must not claim cloud/deployment support in this phase.

## Security Dependency Notes

- Lock files begin in Unit 1 and are verified in Unit 6.
- Validation responsibility begins in Unit 2 and extends through Unit 4.
- CORS and security headers are implemented in Unit 4 and Unit 5.
- Safe user-facing error behavior starts in Unit 3 and is exposed through Unit 4/5.

## PBT Dependency Notes

- Unit 2 introduces Hypothesis and PBT tests.
- Unit 3 and Unit 4 rely on Unit 2 domain tests for deterministic calculation confidence.
- Unit 6 verifies PBT tests run as part of the backend test command.
