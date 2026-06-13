# NFR Requirements

## Usability

- The user can run one local command and open a browser page.
- The form should be readable on desktop and mobile widths.

## Maintainability

- Keep the UI layer thin.
- Keep formulas centralized in `graph.py`.

## Security

- Local development server only.
- No authentication, cookies, persistence, or external network calls are required.

## Performance

- Calculation should complete immediately for single-user local usage.
