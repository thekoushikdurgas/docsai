# Era 5 — Modules

**Goal:** Gateway GraphQL client + store.

**Checklist**

- [x] `services/gatewayClient.js` — `globalThis.C360Gateway` (`saveProfilesToGateway` + `postScrape` via GraphQL; `checkHealth` on API origin `/health`)
- [x] `state/store.js` — side panel ES module
- [x] Telemetry remains centralized in `background.js` (single path)
