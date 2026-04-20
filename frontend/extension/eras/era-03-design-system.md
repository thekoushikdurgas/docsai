# Era 3 — Design system

**Goal:** Tokens + components split; kit mapping and **subset alignment** with the Dashboard UI kit (reference) and `contact360.io/app` token names—without shipping Bootstrap/jQuery in the extension.

**Checklist**

- [x] `ui/tokens.css`, `ui/components.css`
- [x] `sidepanel.css` imports shared layers; side panel uses `c360-panel__*` + `c360-card` (no legacy popup block names)
- [x] `docs/frontend/extension/design-tokens.md`
- [x] `docs/frontend/docs/index.json` — `fe.extension.tokens`
- [x] Optional small ES modules under `sidepanel/` (`tabs.js`, `preview.js`) for readability—plain functions only

### Rewrite checklist (v2.0)

- [ ] `src/sidebar/styles/{tokens,components,dashboard,sidepanel}.css` — parity with legacy `ui/*.css`
- [ ] React primitives under `src/sidebar/components/ui/*` (`Button`, `Input`, `Checkbox`, `Radio`, `RadioGroup`, `Modal`, `Tabs`, `Progress`, `Steps`, `Card`, `Empty`, `Badge`, `Status`, `Field`)
- [ ] Update `docs/frontend/extension/design-tokens.md` with component file names
