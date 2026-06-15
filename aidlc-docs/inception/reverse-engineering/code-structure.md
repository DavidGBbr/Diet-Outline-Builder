# Code Structure - Current Brownfield Baseline

## Root Files

- `pyproject.toml`: Python package metadata, dependencies, console scripts, pytest config.
- `README.md`: install, CLI, local browser app, and test instructions.
- `.gitignore`: Python-oriented ignore rules.

## Python Package

- `src/diet_outline_builder/__init__.py`: exports `build_diet_outline` and `diet_graph`.
- `src/diet_outline_builder/__main__.py`: runs CLI entrypoint.
- `src/diet_outline_builder/cli.py`: prompts for required fields in the terminal and prints JSON.
- `src/diet_outline_builder/graph.py`: owns diet calculation types, constants, validation, calculation nodes, graph compilation, and public build function.
- `src/diet_outline_builder/web.py`: owns FastAPI app, inline HTML UI, `GET /`, `POST /api/diet`, and local Uvicorn startup.

## Tests

- `tests/test_diet_graph.py`: verifies calculation values, validation errors, macro calorie consistency, and BMI-based macro ranges.
- `tests/test_web_app.py`: verifies local HTML route and `/api/diet` behavior.

## Planning Docs

- `aidlc-docs/`: AI-DLC state, audit, requirements, design, and build/test artifacts.
- `aws-aidlc-rule-details/`: AI-DLC workflow rule details and extensions.
