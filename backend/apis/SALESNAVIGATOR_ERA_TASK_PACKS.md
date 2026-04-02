# Sales Navigator — Era Task Pack Index

**Service:** `backend(dev)/salesnavigator`
**GraphQL module:** `docs/backend/apis/23_SALES_NAVIGATOR_MODULE.md`
**Codebase analysis:** `docs/codebases/salesnavigator-codebase-analysis.md`

---

## Purpose

This index maps the Sales Navigator ingestion service across all 11 Contact360 project eras, linking to per-era task pack files that detail the 5-track task breakdown (Contract, Service, Surface, Data, Ops) for each era.

---

## Era Map

| Era | Folder | Task pack file | Primary status |
| --- | --- | --- | --- |
| `0.x` | `docs/0. Foundation...` | `salesnavigator-foundation-task-pack.md` | Scaffold |
| `1.x` | `docs/1. Contact360 user...` | patches `1.N.P — *.md` (**Service task slices**; former `salesnavigator-user-billing-task-pack.md` merged) | Auth/actor stub |
| `2.x` | `docs/2. Contact360 email...` | patches `2.N.P — *.md` (**Service task slices**; former `salesnavigator-email-system-task-pack.md` merged) | Email field validation |
| `3.x` | `docs/3. Contact360 contact...` | patches `3.N.P — *.md` (**Service task slices**; former `salesnavigator-contact-company-task-pack.md` merged) | Full field mapping |
| `4.x` | `docs/4. Contact360 Extension...` | patches `4.N.P — *.md` (**Service task slices**; former `salesnavigator-extension-sn-task-pack.md` merged) | **Primary delivery era** |
| `5.x` | `docs/5. Contact360 AI workflows` | patches `5.N.P — *.md` (**Service task slices**; former `salesnavigator-ai-workflows-task-pack.md` merged) | AI field enrichment |
| `6.x` | `docs/6. Contact360 Reliability and Scaling/` | patches `6.N.P — *.md` (**Service task slices**; ex–`salesnavigator-reliability-scaling-task-pack.md`) | Hardening |
| `7.x` | `docs/7. Contact360 deployment/` | patches `7.N.P — *.md` (**Service task slices**; ex–`salesnavigator-deployment-task-pack.md`) | Governance |
| `8.x` | `docs/8. Contact360 public and private apis and endpoints/` | patches `8.N.P — *.md` (**Micro-gate** + **Service task slices**; former `salesnavigator-public-private-apis-task-pack.md` merged) | Rate limits + keys |
| `9.x` | `docs/9. Contact360 Ecosystem integrations and Platform productization/` | patches `9.N.P — *.md` (**Micro-gate** + **Service task slices**; former `salesnavigator-ecosystem-productization-task-pack.md` merged) | Connectors |
| `10.x` | `docs/10. Contact360 email campaign/` | patches `10.N.P — *.md` (**Micro-gate** + **Service task slices**; former `salesnavigator-email-campaign-task-pack.md` merged) | Audience provenance |

---

## Endpoint-era matrix

`docs/backend/endpoints/salesnavigator_endpoint_era_matrix.json`

---

## Cross-service context

| Service | Relationship |
| --- | --- |
| `appointment360` GraphQL | Calls `saveSalesNavigatorProfiles` → forwards to SN service |
| `contact360.extension` | FastAPI ingest (`/v1/scrape`, `/v1/save-profiles`); JS transport (`lambdaClient.js`, `graphqlSession.js`, `profileMerger.js`). Browser shell (MV3) remains **4.5+** scope. |
| `Connectra` | Downstream persistence target (`/contacts/bulk`, `/companies/bulk`) |
| `contact.ai` | AI enrichment of SN-sourced contacts via `parse-filters`, `company/summary` |
| `contact360.io/jobs` | Potential long-running job wrapper for large SN ingestion batches |

---

## Key design decisions per era

### 0.x
- SAM Lambda baseline, `X-API-Key` auth, deterministic UUID5 contract defined.

### 1.x
- `actor_id` / `org_id` headers required for audit traceability.
- Billing event stub — SN save may consume credits.

### 2.x
- Email/phone field quality gates; enrichment queue handoff stub.

### 3.x
- Connectra contact/company field schema locked; provenance tags (`source`, `lead_id`, `search_id`).

### 4.x
- HTML extraction hardened; full extension UX: save button, progress bar, error drawer.
- Docs drift (`scrape-html-with-fetch`) resolved.

### 5.x
- `seniority`, `departments`, `about` quality gated; `data_quality_score` available for AI context.

### 6.x
- Rate limiter, chunk idempotency, request-ID; CORS locked; load tests for 1000-profile batches.

### 7.x
- Per-tenant API key; immutable audit event per save; GDPR cascade.

### 8.x
- Rate-limit headers; `X-Request-ID`; usage counter in `api_usage`; versioned `/api/v1/` path prefix.

### 9.x
- Connector adapter layer; webhook delivery; tenant-isolated lineage.

### 10.x
- Campaign audience provenance: `lead_id`/`search_id` → campaign records.

---

## Immediate action queue (P0/P1 before 4.x delivery)

| ID | Task |
| --- | --- |
| SN-P0-1 | Remove `POST /v1/scrape-html-with-fetch` from `docs/api.md` (not implemented) |
| SN-P0-2 | Clarify `POST /v1/scrape` active status in `README.md` |
| SN-P1-1 | Add `X-Request-ID` correlation header to all responses |
| SN-P1-2 | Implement rate limiting middleware |
| SN-P1-3 | Lock CORS to known service origins |
| SN-P1-4 | Add chunk idempotency token to prevent replay duplication on Lambda retry |

---

## Delivery snapshot (through `4.2`)

- `4.0` service ingestion baseline: **completed**.
- `4.1` auth/session utility layer for extension transport (`graphqlSession.js`, token storage): **completed**.
- `4.2` backend save/scrape ingestion path (`/v1/save-profiles`, `/v1/scrape`) on `contact360.extension` FastAPI: **completed**.
- Remaining `4.x` scope is the Chrome extension shell/UI (`manifest`, `background`/`service worker`, `content`, `popup`) and CSP/permissions hardening — tracked as **4.5+**; does not block backend ingest completion status.

## Data lineage

- Provenance and Connectra field mapping: [`docs/backend/database/salesnavigator_data_lineage.md`](../database/salesnavigator_data_lineage.md)
