# Architecture - Current Brownfield Baseline

## System Overview

The current project is a single Python package named `diet_outline_builder`. It exposes deterministic diet calculations through:

- A reusable Python function: `build_diet_outline(payload)`.
- A compiled LangGraph workflow in `src/diet_outline_builder/graph.py`.
- A FastAPI local web app in `src/diet_outline_builder/web.py`.
- A CLI in `src/diet_outline_builder/cli.py`.

## Runtime Architecture

```text
CLI or FastAPI endpoint
  -> build_diet_outline(payload)
  -> LangGraph calculation graph
  -> final diet response JSON
```

## Current UI Architecture

The current browser UI is an inline HTML/CSS/JavaScript string inside the Python FastAPI module. It renders a form, submits to `POST /api/diet`, and displays the returned JSON.

## Current LangGraph Flow

```text
START
  -> validateInput
  -> calculateAnthropometrics
  -> calculateEnergy
  -> calculateMacros
  -> generateExplanation
  -> addSafetyDisclaimer
  -> END
```

## Refactor Implication

The current graph is calculation-oriented, not conversation-oriented. The refactor must preserve deterministic calculation behavior while adding a separate conversational LangGraph flow with conditional routing for missing data.
