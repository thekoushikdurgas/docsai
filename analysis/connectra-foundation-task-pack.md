# Connectra foundation task pack (`0.x`)

| Area | Owner (default) | Priority |
| --- | --- | --- |
| Contract / API | Platform backend | P0 |
| Service (`contact360.io/sync`) | Platform backend | P0 |
| DB + ES | Platform + data | P0 |
| Extension / marketing / admin (listed below) | Frontend + DocsAI | P1 |

## Scope

Bootstrap `contact360.io/sync` service contract and baseline operational readiness.

## Small tasks

- **Contract:** Freeze internal API key contract, health endpoint response envelope, and base route registry. (patch assignment: `0.7.0`–`0.7.2`)
- **Service:** Wire Gin middleware chain (CORS, gzip, rate limit, API key auth) and bootstrap route groups. (patch assignment: `0.7.0`–`0.7.2`)
- **Database:** Create baseline PostgreSQL tables and Elasticsearch index mappings for contacts/companies. (patch assignment: `0.7.0`–`0.7.2`)
- **Flow:** Validate read path skeleton (`VQL -> ES IDs -> PG hydrate`) with smoke fixtures. (patch assignment: `0.7.3`–`0.7.6`)
- **Release gate evidence:** Health checks, seed/load scripts, and contract doc links recorded in `docs/architecture.md` and `docs/versions.md`. (patch assignment: `0.7.7`–`0.7.9`)

## Root/Admin surface contributions (era sync)

- **`contact360.io/root`**: establish marketing shell baseline (`app/layout.tsx`, `app/(marketing)/layout.tsx`), 3D primitives baseline, and public route inventory. (patch assignment: `0.7.3`–`0.7.6`)
- **`contact360.io/admin`**: establish DocsAI base shell (`templates/base.html`), initial sidebar/navigation constants, and foundational admin auth/session views. (patch assignment: `0.7.3`–`0.7.6`)

---

## Extension surface contributions (era sync)

### Era 0.x — Foundation

**`extension/contact360` scaffolding:**
- Extension folder created under canonical path `extension/contact360/` (patch assignment: `0.7.3`–`0.7.6`)
- `auth/graphqlSession.js` module scaffolded with `chrome.storage.local` adapter pattern (MV3 compliant) (patch assignment: `0.7.3`–`0.7.6`)
- `utils/lambdaClient.js` module scaffolded for Lambda REST transport (patch assignment: `0.7.3`–`0.7.6`)
- `utils/profileMerger.js` module scaffolded for profile dedup (patch assignment: `0.7.3`–`0.7.6`)
- No active backend calls in this era; folder structure only (patch assignment: `0.7.3`–`0.7.6`)

**Tasks:**
- [ ] Confirm `extension/contact360/` is in `.gitignore` exclusion list for minimal clones (patch assignment: `0.7.3`–`0.7.6`)
- [ ] Document MV3 `chrome.storage.local` adapter pattern in extension README (patch assignment: `0.7.3`–`0.7.6`)
- [ ] Establish Jest test scaffolding for extension utils (patch assignment: `0.7.3`–`0.7.6`)

---

## Surface track (contacts/companies stubs + VQL builder notes)

This surface track is the foundation-era evidence that Connectra search read path is wired end-to-end enough for UX scaffolding.

| Task | Priority | Patch assignment |
| --- | --- | --- |
| Stub routes for `contacts` and `companies` pages (`/contacts`, `/companies`) | P0 | `0.7.0`–`0.7.2` |
| Scaffold `ContactsFilters` and `VQLQueryBuilder` components (stub acceptable) | P1 | `0.7.3`–`0.7.6` |
| Add `useContactsFilters` hook stub and ensure it feeds “active VQL conditions” | P1 | `0.7.3`–`0.7.6` |
| Render filter chips from API response / VQL conditions model | P1 | `0.7.3`–`0.7.6` |
| Provide empty state + ES timeout/loading skeleton for search UI | P1 | `0.7.3`–`0.7.6` |
| Add a frontend note mapping `VQL -> ES IDs -> PG hydrate` expectations | P1 | `0.7.3`–`0.7.6` |

---

## Foundation hardening (from `docs/codebases/connectra-codebase-analysis.md`)

Use during **`0.7`** (`version_0.7.md`) and early **`0.3`** client contract work — not optional for production-shaped environments.

### Persistent job queue (replaces in-only-memory channel)

| Task | Priority | Notes | Patch assignment |
| --- | --- | --- | --- |
| Design durable queue for `/common/jobs` engine (DB-backed, Redis, or external) with same state machine | P0 | Today: 1000-buffer in-memory channel — lost on restart | `0.7.0`–`0.7.2` |
| Migration path: drain in-flight jobs on deploy | P0 | Document ordering with `first_time` vs `retry` workers | `0.7.0`–`0.7.2` |
| Metrics: queue depth, oldest `OPEN` age | P1 | For ops runbooks (`0.10`) | `0.7.3`–`0.7.6` |

### Elasticsearch ↔ PostgreSQL reconciliation

| Task | Priority | Notes | Patch assignment |
| --- | --- | --- | --- |
| Automated or scheduled **drift report** (ES IDs vs PG rows for contacts/companies) | P0 | Manual playbook until automation lands | `0.7.0`–`0.7.2` |
| **Reconcile** job: repair mode vs report-only | P1 | Tie to `version_0.7` patch ladder | `0.7.3`–`0.7.6` |
| Alerting hooks when drift > threshold | P1 | | `0.7.3`–`0.7.6` |

### Per-tenant rate limits and scoped API keys

| Task | Priority | Notes | Patch assignment |
| --- | --- | --- | --- |
| Replace/adjust `AllowAllOrigins` with env-driven allowlist for non-dev | P0 | Cited gap in analysis | `0.7.0`–`0.7.2` |
| Token-bucket limits: per-key vs per-tenant policy doc | P0 | | `0.7.0`–`0.7.2` |
| Key **scopes** stub: read vs write vs admin internal | P1 | Align with gateway `X-API-Key` story (`0.3`) | `0.7.3`–`0.7.6` |

### VQL and filter contract tests

| Task | Priority | Notes | Patch assignment |
| --- | --- | --- | --- |
| Golden tests for `exact`, `shuffle`, `substring`, `keyword_match`, `range_query` | P0 | Fixtures in repo | `0.7.0`–`0.7.2` |
| Filter `/common/:service/filters` snapshot tests | P1 | UUID5 facet keys | `0.7.3`–`0.7.6` |
| Contract doc cross-link: `docs/backend/apis/` or Connectra pack README | P0 | | `0.7.0`–`0.7.2` |

### Batch-upsert idempotency — release gate

- [ ] Same payload twice → **stable** UUID5 + no duplicate business rows (contacts/companies). (patch assignment: `0.7.7`–`0.7.9`)
- [ ] Parallel upsert stress: **no** deadlocks; deterministic ordering documented or accepted. (patch assignment: `0.7.7`–`0.7.9`)
- [ ] Partial failure semantics **explicit** in API response (per-field or per-record errors). (patch assignment: `0.7.7`–`0.7.9`)
- [ ] Evidence: test output + link from `docs/versions.md` when closing **`0.7.x`** patches. (patch assignment: `0.7.7`–`0.7.9`)

**References:** [`docs/codebases/connectra-codebase-analysis.md`](../codebases/connectra-codebase-analysis.md)