# Era 8 — Reliability

**Goal:** Chunking + retries.

**Checklist**

- [x] Client chunk size 450 profiles per `save-profiles` request
- [x] `fetchWithRetry` with backoff + jitter on 5xx/429
- [x] Empty profile list short-circuits (no POST)
