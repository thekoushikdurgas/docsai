# Era 8 — Reliability

**Goal:** Chunking + retries.

**Checklist**

- [x] Client chunk size **1000** profiles per GraphQL `saveSalesNavigatorProfiles` request (matches `SaveProfilesInput` max)
- [x] `fetchWithRetry` with backoff + jitter on 5xx/429
- [x] Empty profile list short-circuits (no POST)
- [x] GraphQL errors surfaced as thrown `Error` with server message

### Rewrite checklist (v2.0)

- [ ] `GatewayError` typing + user-visible strings in side panel
- [ ] `src/background/offlineQueue.ts` (IndexedDB) for failed batches + drain on `online` (stub acceptable)
- [ ] Preserve chunk size **1000** and `fetchWithRetry` semantics in `gatewayClient.ts`
