# Technology Stack - Current Brownfield Baseline

## Current Stack

- Language: Python 3.11+
- Backend framework: FastAPI
- Local server: Uvicorn
- Graph framework: LangGraph
- Testing: pytest
- Packaging: pyproject with Hatchling

## Planned Stack From Approved Requirements

- Monorepo package manager: pnpm workspaces
- Frontend: Next.js, React, TypeScript
- Backend: Python FastAPI in `apps/api`
- Agent orchestration: LangGraph
- Local LLM provider: Ollama
- Default model: `llama3.1:8b`
- LLM base URL: `http://localhost:11434`
- Frontend persistence: browser localStorage
- Frontend/backend communication: WebSocket
- Python PBT framework: Hypothesis for partial property-based testing
