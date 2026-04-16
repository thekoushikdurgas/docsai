# Flow 5 — Chrome extension enrichment (canonical)

**Diagram (PNG):** [`flow5_extension.png`](../../prd/flow5_extension.png)  
**Related phases:** `4` (extension), `2` (email/phone), `3` (CRM), `5` (AI), `8` (APIs)  
**Schemas:** `Contact.json`, `contact.updated.v1.json`, `EnrichmentJob.json`

## Summary

On a supported page (e.g. **LinkedIn public DOM**), user clicks enrich → **MV3 content script** parses **structured** fields → **service worker** calls **`POST /enrich`** (or namespaced equivalent) with **JWT**. **API Gateway** forwards **create** to **CRM Service**, which orchestrates parallel jobs: **Email Svc** (enrich + verify → **Postgres**), **Phone Svc** (enrich + **DND** → index in **OpenSearch** / contact index), **AI Agent** (score + **embed** → **pgvector**). **Sidebar UI** receives **live SSE** updates as partial results stream (“Truecaller-style” progressive UI in research diagram). **Audit log** stores `{ userId, sourceUrl, timestamp, fields }` for GDPR accountability.

## Actors

- Sales user
- **Content script** — DOM extraction, strict allowlist of fields
- **Service worker** — OAuth/JWT, backoff, single-flight requests
- **API Gateway** — authZ, org injection
- **CRM Service** — orchestration, dedupe, persistence
- **Email / Phone / AI** services — specialized enrichment
- **Postgres** — contacts + audit
- **OpenSearch** — searchable phone/profile facets
- **pgvector** — embeddings for ranking / RAG

## Step-by-step

1. User invokes action on profile page; content script builds payload + **sourceUrl** hash.
2. Worker obtains/rotates short-lived JWT (extension client).
3. `POST /enrich` with structured body + metadata.
4. CRM finds or creates contact; attach provenance (`source=extension`, url hash).
5. Fire async jobs: **email job**, **phone job**, **AI score** (parallel).
6. Each worker writes incremental results; CRM **streams** consolidated state.
7. **SSE channel** pushes updates to sidebar until terminal state.
8. Append **audit log** row (no raw HTML storage; minimized fields).

## Data contracts

| Type | Name / pattern |
| ---- | ---------------- |
| HTTP | `POST /enrich` (document exact path in OpenAPI when published) |
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

- Phase 4 PRD: `docs/prd/Read all the above and previous prompts and then t (5).md`.
- `docs/prd/contact360_security.md`, `docs/prd/contact360_extension` topics in PRD bundle.
- Flow 1 (baseline create), Flow 2 (CSV vs single-profile enrichment), Flow 3 (downstream RAG).
