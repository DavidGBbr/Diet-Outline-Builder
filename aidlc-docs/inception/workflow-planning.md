# Workflow Planning

## Selected Stages

- Workspace Detection: Completed because this is an AI-DLC request.
- Requirements Analysis: Completed at minimal depth because the feature contract was clear.
- Code Generation: Required to create the Python package and LangGraph.
- Build and Test: Required to verify calculation correctness.

## Implementation Units

- Diet Graph: validation, anthropometrics, energy, macros, response, and disclaimer nodes.
- CLI: interactive prompts and JSON output.
- Tests: sample calculation, macro calorie consistency, and validation failure path.
- Local UI: FastAPI localhost server, browser form, `/api/diet` JSON endpoint, and endpoint tests.

## Local UI Stage Selection

- Requirements Analysis: Updated because the user requested local application usage.
- Application Design: Executed because a new local web component and API endpoint are being added.
- Functional Design: Executed at minimal depth because the UI form and API behavior are straightforward.
- NFR Requirements: Captured inline because the local-only app has simple non-functional requirements.
- Code Generation: Required for FastAPI server, HTML page, and tests.
- Build and Test: Required through `pytest` and sample endpoint verification.
