# Frontend Components - Unit 1 Monorepo Foundation

## Scope

Unit 1 creates only a minimal hand-written Next.js shell. The conversational chat UI is implemented in Unit 5.

## App Shell

Purpose:

- Prove `apps/web` can run as a Next.js TypeScript app inside the pnpm workspace.
- Provide a placeholder page for later chat implementation.

Responsibilities:

- Render a simple local app page.
- Avoid copying the old form UI.
- Avoid client-side diet calculations.
- Keep structure ready for later `components/` and `lib/` additions.

## Proposed Initial Files

```text
apps/web/
  app/
    globals.css
    layout.tsx
    page.tsx
  next.config.ts
  package.json
  tsconfig.json
```

## Placeholder Page Behavior

- Displays project name and local setup intent.
- Does not show the old diet form.
- Does not connect to WebSocket yet.
- Does not persist localStorage yet.

## Future Unit 5 Integration Points

- `components/ChatShell.tsx`
- `components/CollectedDataSummary.tsx`
- `components/DietResultCard.tsx`
- `lib/chatSocket.ts`
- `lib/conversationStorage.ts`
