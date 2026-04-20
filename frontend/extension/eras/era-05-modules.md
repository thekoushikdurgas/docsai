# Era 5 — Modules

**Goal:** Gateway GraphQL client + store.

**Checklist**

- [x] `services/gatewayClient.js` — `globalThis.C360Gateway` (`saveProfilesToGateway` + `postScrape` via GraphQL; `checkHealth` on API origin `/health`)
- [x] `state/store.js` — side panel ES module
- [x] Telemetry remains centralized in `background.js` (single path)

### Rewrite checklist (v2.0)

- [ ] `src/services/gatewayClient.ts` (typed) + `useCapture` / `useApiHealth` / `useLastCapture`
- [ ] `src/types/messages.ts` (discriminated unions) consumed by service worker message routing
- [ ] Telemetry remains in `src/background/telemetry.ts` only
