# Flow 5 — Chrome extension enrichment (canonical)

**Diagram (PNG):** [`flow5_extension.png`](../../prd/flow5_extension.png)  
**Related phases:** `4` (extension), `2` (email/phone), `3` (CRM), `5` (AI), `8` (APIs)  
**Schemas:** `Contact.json`, `contact.updated.v1.json`, `EnrichmentJob.json`

## Summary

On a supported page (e.g. **LinkedIn / Sales Navigator DOM**), user saves or enriches → **MV3 content script** parses **structured** fields → **service worker** calls **`POST /graphql`** with **JWT** (e.g. `saveSalesNavigatorProfiles`, `scrapeSalesNavigatorHtml`, or enrichment mutations). The **gateway** proxies to **extension.server** / **Connectra** / **email.server** / **phone.server** / **ai.server** per operation — **not** a separate monolithic “CRM Service”. **Sidebar UI** receives **live SSE** updates as jobs complete (`DECISIONS.md`). **Sales Navigator save path:** gateway → extension.server → **`POST /companies/batch-upsert`** then **`POST /contacts/batch-upsert`** on Connectra; preview merge uses **`SaveProfilesResponse`** fields and `chrome.storage` (see Phase 4 / flowchart).

## Actors

- Sales user
- **Content script** — DOM extraction, strict allowlist of fields
- **Service worker** — OAuth/JWT, backoff, single-flight requests
- **Gateway** — authZ, org injection, RLS on gateway-owned tables
- **Connectra + satellites** — persistence and async jobs per `DECISIONS.md`
- **Email / Phone / AI** services — specialized enrichment
- **Postgres** — contacts + audit
- **OpenSearch** — searchable phone/profile facets
- **pgvector** — embeddings for ranking / RAG

## Step-by-step

1. User invokes action on profile page; content script builds payload + **sourceUrl** hash.
2. Worker obtains/rotates short-lived JWT (extension client).
3. **`POST /graphql`** with structured input + metadata (mutations per schema).
4. Gateway / Connectra find or create contact; attach provenance (`source=extension`, url hash).
5. Fire async jobs: **email job**, **phone job**, **AI score** (parallel).
6. Each worker writes incremental results; CRM **streams** consolidated state.
7. **SSE channel** pushes updates to sidebar until terminal state.
8. Append **audit log** row (no raw HTML storage; minimized fields).

## Data contracts

| Type | Name / pattern |
| ---- | ---------------- |
| HTTP | **`POST /graphql`** (product API); public REST is separate (`DECISIONS.md`) |
| SSE | `GET /v1/extension/stream?session=...` (example) — server→client updates |
| Postgres | `contacts`, `activities`, `extension_audit_log` (name TBD) |
| OpenSearch | Contact / phone facets index |
| pgvector | `contact_id` embedding rows |
| Redis | `ext:session:{user_id}`, `ratelimit:ext:{org_id}` |

## Error paths

- **401** — re-auth extension; rotate refresh token.
- **429** — LinkedIn / provider throttle; show cooldown in sidebar.
- **Ambiguous match** — return candidate list for user pick (no silent merge).
- **PII minimization failure** — abort and log security event.

## Cross-links

- **Flowchart:** [`docs/flowchart/extension-capture.md`](../../flowchart/extension-capture.md).
- **Pipeline doc:** [`docs/4.Contact360 Extension and Sales Navigator maturity/63-sales-navigator/00-pipeline-gateway-connectra.md`](../../4.Contact360%20Extension%20and%20Sales%20Navigator%20maturity/63-sales-navigator/00-pipeline-gateway-connectra.md).
- Phase 4 PRD: `docs/prd/Read all the above and previous prompts and then t (5).md`.
- `docs/prd/contact360_security.md`, `docs/prd/contact360_extension` topics in PRD bundle.
- Flow 1 (baseline create), Flow 2 (CSV vs single-profile enrichment), Flow 3 (downstream RAG).
