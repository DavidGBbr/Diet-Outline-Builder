# Interaction Diagrams - Current Brownfield Baseline

## Current Form-Based Flow

```text
Browser form
  -> POST /api/diet
  -> build_diet_outline(payload)
  -> calculation LangGraph
  -> JSON response
  -> Browser renders result
```

## Current CLI Flow

```text
CLI prompts
  -> payload dict
  -> build_diet_outline(payload)
  -> calculation LangGraph
  -> printed JSON
```

## Target Refactor Flow

```text
Next.js chat UI
  -> WebSocket message
  -> FastAPI WebSocket handler
  -> conversational LangGraph
  -> conditional validation edge
       data incomplete -> ask remaining data
       data complete -> calculate diet -> final response
  -> WebSocket response
  -> Next.js renders assistant message/result
```
