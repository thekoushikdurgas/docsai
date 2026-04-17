# Era 3 — Design system

**Goal:** Tokens + components split; kit mapping and **subset alignment** with the Dashboard UI kit (reference) and `contact360.io/app` token names—without shipping Bootstrap/jQuery in the extension.

**Checklist**

- [x] `ui/tokens.css`, `ui/components.css`
- [x] `sidepanel.css` imports shared layers; side panel uses `c360-panel__*` + `c360-card` (no legacy popup block names)
- [x] `docs/frontend/extension/design-tokens.md`
- [x] `docs/frontend/docs/index.json` — `fe.extension.tokens`
- [x] Optional small ES modules under `sidepanel/` (`tabs.js`, `preview.js`) for readability—plain functions only
