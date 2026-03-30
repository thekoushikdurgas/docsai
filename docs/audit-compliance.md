# Audit, Compliance, and Governance (All Eras: 0.x–10.x)

> **Scope:** This document covers the full era range. Each service section details per-era compliance requirements from `0.x` (foundation) through `10.x` (email campaign). For full RBAC policy and role-enforcement patterns, see **`docs/7. Contact360 deployment/rbac-authz.md`**. For release and governance process, see **`docs/governance.md`**.

## RBAC matrix

| Capability | FreeUser | ProUser | Admin | SuperAdmin |
|---|---|---|---|---|
| Manage webhooks | no | yes | yes | yes |
| Manage integrations | no | yes | yes | yes |
| Create/schedule campaigns | no | yes | yes | yes |
| Approve billing submissions | no | no | yes | yes |

## Audit event schema

- event_id, event_time, actor_user_id, actor_role
- tenant_id, service, action, status
- target_type, target_id, request_id, metadata

## Tenant isolation

- Tenant scoped access required for all mutable resources
- Cross-tenant references return not-found semantics

## Service implementation language (governance note)

Audit and security reviews must distinguish **(a)** the **Python GraphQL gateway** (`contact360.io/api`), which is the primary customer API surface, from **(b)** **Go/Gin** and other satellite services. Language choice does not change tenant isolation or audit field requirements; it affects **build pipelines, dependency scanning, and SCA** per runtime. Canonical policy: **`docs/docs/backend-language-strategy.md`**.

## EC2 Go satellites (compliance scope)

When reviewing **`EC2/s3storage.server`**, **`EC2/log.server`**, **`EC2/ai.server`**, and **`EC2/extension.server`**:

- **Data residency / PII:** Treat S3 object keys and CSV payloads as **sensitive**; ensure bucket policies, encryption, and retention match tenant policy (see `s3storage` / `logs.api` era tables elsewhere in this doc).
- **AI (`ai.server`):** Log only redacted prompts where required; HF API keys must be injected via secrets manager / env — never committed.
- **Extension (`extension.server`):** `POST /v1/save-profiles` must enforce API key / mTLS as deployed; **HTML scrape** remains client-side (`501` on server scrape route).
- **Jobs (`EC2/job.server`):** `job_events` table and metrics endpoints support audit trails for async work; ensure DB migrations applied in regulated environments.

## Era-specific RBAC and evidence mapping

- `7.x` is the RBAC baseline era and defines role enforcement patterns.
- `8.x` extends controls to partner/public API access and webhook identities.
- `9.x` extends controls to tenant/workspace/admin self-serve governance.
- `10.x` applies compliance controls to campaign consent, suppression, and opt-out audit trails.

## P0 security findings (must close before era promotion)

- `2.x` blocker: `contact360.io/email/src/context/imap-context.tsx` stores mailbox credentials in plaintext local storage.
- `2.x` blocker: `contact360.io/email/src/app/email/[mailId]/page.tsx` and `contact360.io/email/src/app/account/[userId]/page.tsx` rely on direct `X-Email` / `X-Password` transport.
- `0.x`/`7.x` blocker: admin `.env` examples include insecure default secret key patterns and must be rotated/replaced with placeholder values.
- `4.x` blocker: `extension/contact360/.example.env` uses real-looking key values and must be sanitized to placeholder-only examples.
- `4.x` release requirement: extension `manifest.json` CSP must explicitly allow the Lambda API domain before store submission.

## `s3storage` compliance controls by era

- `1.x`: enforce file type and size policy for user/billing artifacts.
- `2.x`: require multipart completion traceability (`uploadId`, part registration, completion evidence).
- `6.x`: require idempotent storage lifecycle operations and reconciliation evidence.
- `7.x`: enforce service-to-service authz for storage endpoints and retention policy controls.
- `8.x`: enforce versioned storage API behavior with compatibility tests.
- `10.x`: enforce immutable campaign compliance artifacts and retention/audit verifiability.

Mandatory evidence pack for storage-impacting releases:

- endpoint contract diff (if changed),
- metadata integrity/reconciliation report,
- access-control validation report,
- retention/deletion policy validation report.

## `logs.api` compliance controls by era

- `1.x`: user and billing event traceability with actor and request identifiers.
- `2.x`: bulk email workflow event retention and queryability.
- `6.x`: reliability evidence from logs-based SLO metrics and incident timelines.
- `7.x`: deployment and RBAC governance audit trails with retention policy checks.
- `8.x`: public/private API access auditing and investigation-grade filtering.
- `10.x`: campaign consent/suppression/send event audit integrity for compliance reviews.

## `jobs` compliance controls by era

- `2.x`: ensure email bulk job events and status transitions are queryable and reproducible.
- `3.x`: ensure Contact360 import/export jobs preserve query and artifact lineage evidence.
- `6.x`: enforce retry/idempotency evidence and stale-recovery auditability.
- `7.x`: treat `job_events` as immutable audit trail for privileged operations and retries.
- `8.x`: include partner callback delivery audit evidence for public/private API jobs.
- `9.x`: include tenant-isolated job visibility and quota/audit controls.
- `10.x`: use timeline evidence (`GET /api/v1/jobs/{uuid}/timeline`) for campaign compliance bundles.

Required evidence for jobs-impacting releases:

- lifecycle/status transition report,
- retry/audit trace report,
- timeline endpoint sample evidence pack,
- retention and access-control validation report.

## DocsAI admin decorator access matrix

| Admin feature/view area | Access decorator expectation | Audit significance |
| --- | --- | --- |
| Main admin dashboard controls | `require_admin_or_super_admin` | operational control trail |
| Payment approval/decline flows | `require_admin_or_super_admin` (super-admin override where configured) | financial decision evidence |
| User management and history | `require_admin_or_super_admin` | identity and entitlement audit |
| System logs and log queries | `require_admin_or_super_admin` | incident and compliance investigation trail |
| Sensitive system settings | `require_super_admin` | high-privilege change governance |
| Architecture/roadmap governance edits | `require_super_admin` or stricter workflow gate | release-governance and policy traceability |

## DocsAI audit surface checklist

The following views/actions must emit or preserve audit-relevant evidence:

- Billing payment submission review (`approve` / `decline` actions)
- User profile/role/package administrative changes
- System log query and export operations
- Billing settings updates (UPI/phone/email/QR and related configuration)
- Deployment/governance state transitions referenced by admin tooling

## `contact.ai` compliance controls by era

**Service:** `backend(dev)/contact.ai` — FastAPI Lambda, `ai_chats` PostgreSQL table, HF Inference / Gemini.

| Era | Compliance control | Evidence artifact |
| --- | --- | --- |
| `0.x` | `ai_chats` DDL migration idempotency | Migration script review; CI smoke test |
| `1.x` | `user_id` FK referential integrity; cascade strategy | FK constraint test; cascade behavior documented |
| `2.x` | Email PII handling in `analyzeEmailRisk` utility | HF data retention policy review; no persistence confirmed |
| `3.x` | Contact PII in `parseContactFilters` output (stateless) | Confirm no PII stored outside `ai_chats.messages` JSONB |
| `4.x` | SN contact provenance in `messages.contacts[]` JSONB | Field-level consent documentation for embedded contact data |
| `5.x` | Model version audit in message metadata | `model_version` field in JSONB; reproducibility evidence |
| `5.x` | User isolation: `X-User-ID` ownership enforcement | Ownership check test evidence; 403 on cross-user access |
| `6.x` | Chat TTL and archival policy | Archival job evidence; max age documented |
| `6.x` | Concurrent write protection (optimistic lock) | `version` column; race condition test evidence |
| `7.x` | GDPR right-to-erasure cascade | `ai_chats` DELETE on user deletion; audit log entry |
| `7.x` | Audit log for chat create/delete/message-send events | `logs.api` event schema; event trail sample |
| `7.x` | Role-based AI feature gating | Plan-level gate test evidence; upgrade prompt on deny |
| `8.x` | Rate limit compliance: `Retry-After`, `X-RateLimit-*` headers | Header presence test; token bucket config documented |
| `8.x` | API key scope isolation | Scoped key validation test; `ai:chat` vs `ai:utilities` |
| `9.x` | Webhook delivery audit trail | Delivery log schema; retry evidence; DLQ handling |
| `10.x` | Campaign AI generation compliance evidence | `campaign_ai_log` table; `generation_id`, model version, prompt hash |
| `10.x` | AI-generated content disclosure | "AI-generated" badge on campaign subject/body; `generation_id` link |

### Required evidence for contact.ai-impacting releases

- User isolation test report (403 on cross-user chat access).
- PII handling confirmation (no email/contact PII stored in utility calls).
- Model version audit entry in message JSONB for chat sends.
- GDPR erasure test evidence (user deletion → `ai_chats` cascade).
- Rate limit header validation report for all endpoints.


---

## Extension audit and compliance surface

### Extension RBAC / access control

| Capability | Who can use | Control mechanism |
| --- | --- | --- |
| Scrape SN profiles | Authenticated user with valid `accessToken` | `getValidAccessToken()` gating |
| Submit profiles to Lambda | Authenticated user with valid `accessToken` | `Authorization: Bearer` header on every request |
| Token refresh | Any user session with valid `refreshToken` | `auth.refreshToken` GraphQL mutation on Appointment360 |
| Access `chrome.storage.local` | Extension runtime only | Chrome MV3 API boundary — not accessible outside extension |

### Extension audit event contract

| Event | Triggered by | Audit evidence |
| --- | --- | --- |
| Token refresh | `refreshAccessToken()` call | Appointment360 GraphQL auth log (server-side) |
| Profile batch submitted | `saveProfiles()` success | Lambda SN API server-side log |
| Profile batch failed | `saveProfiles()` error | Error object returned to caller; Lambda SN API error log |
| Dedup completed | `deduplicateProfiles()` | No server-side audit — client-side only; dedup ratio can be logged to Logs API if wired |

### Extension token security checklist

- 📌 Planned: `accessToken` never logged to console, error report, or network request other than `Authorization` header
- 📌 Planned: `refreshToken` never logged to console, error report, or network request other than `auth.refreshToken` mutation body
- 📌 Planned: Both tokens stored only in `chrome.storage.local`; never in `localStorage`, `sessionStorage`, or `chrome.storage.sync`
- 📌 Planned: Token expiry buffer (300 s) is documented and tested
- 📌 Planned: Token rotation on refresh: old tokens are immediately replaced in storage after a successful refresh

### Extension data privacy checklist

| Data category | Handling |
| --- | --- |
| LinkedIn profile URLs | Used as dedup key; submitted to Lambda SN API |
| Profile names, titles, companies | Submitted to Lambda SN API → Connectra |
| Email addresses (if present in profile) | Submitted to Lambda SN API → Connectra |
| Phone numbers (if present in profile) | Submitted to Lambda SN API → Connectra |
| `accessToken` / `refreshToken` | Stored in `chrome.storage.local` only; never sent to third parties |

> All scraped data is subject to the Contact360 data privacy policy and must only be captured and processed in the context of a valid authenticated user session.

---

## `salesnavigator` service compliance controls by era

### Scope
Service: `backend(dev)/salesnavigator`
Deployment: AWS Lambda (SAM)
Data flows to: Connectra (PostgreSQL + Elasticsearch)

### Era-specific compliance notes

| Era | Compliance requirement |
| --- | --- |
| `0.x` | UUID5 deterministic contract documented; no PII ingested yet |
| `1.x` | Actor context (`user_id`, `org_id`) injected into Connectra records for audit traceability |
| `2.x` | Email and phone data handled — confirm processing basis (user consent via B2B data source policy) |
| `3.x` | Provenance tags (`source=sales_navigator`, `lead_id`, `search_id`) enable source-of-record queries |
| `4.x` | PII ingested at scale — privacy policy must cover SN scraping; user notified of saved contacts |
| `5.x` | AI-context exposure of SN data — confirm AI service data retention and PII policy alignment |
| `6.x` | Chunk idempotency tokens prevent duplicate PII submissions; audit trail for partial failures |
| `7.x` | RBAC enforced; per-tenant API keys; immutable audit event per save session; GDPR right-to-erasure via Connectra |
| `8.x` | Rate limit headers; usage tracking per API key; quota model documented for compliance |
| `9.x` | Connector audit trail; webhook delivery log; tenant-isolated lineage |
| `10.x` | Campaign audience provenance: `lead_id`/`search_id` traceable to source SN session; suppression non-overwrite guard |

### GDPR controls (7.x+)

| Control | Implementation |
| --- | --- |
| Right to erasure | Delete contact by UUID via Connectra; UUID deterministic from SN URL + email |
| Data minimization | Only fields from SN lead card are captured; no external enrichment by SN service itself |
| Purpose limitation | SN data is used for Contact360 contact enrichment only; not sold or shared with third parties |
| Subject access request | Contact records traceable via `source=sales_navigator` + `lead_id` filter |
| Consent basis | B2B professional context (LinkedIn Sales Navigator); user must verify compliance with LI ToS |

### RBAC for SN operations (7.x+)

| Capability | FreeUser | ProUser | Admin | SuperAdmin |
| --- | --- | --- | --- | --- |
| Save SN profiles (up to daily limit) | limited | yes | yes | yes |
| Bulk SN ingest (>100 profiles) | no | yes | yes | yes |
| View SN sync history | no | yes | yes | yes |
| Admin: view all org SN sessions | no | no | yes | yes |
| Force re-ingest / override | no | no | no | yes |

### Audit event schema for SN saves

```json
{
  "event": "sn_save",
  "user_id": "<uuid>",
  "org_id": "<uuid>",
  "profiles_submitted": 25,
  "profiles_saved": 23,
  "profiles_failed": 2,
  "session_id": "<uuid>",
  "source_ip": "<ip>",
  "timestamp": "<ISO8601>",
  "data_quality_avg": 72.4
}
```

### Compliance checklists

**PII handling checklist:**
- 📌 Planned: Email addresses from SN profiles are submitted to Connectra with processing basis documented
- 📌 Planned: Phone numbers from SN profiles are submitted to Connectra with processing basis documented
- 📌 Planned: LinkedIn profile URLs treated as personal identifiers — subject to erasure
- 📌 Planned: `data_quality_score` does not expose PII; contains only numeric metadata

**GDPR right-to-erasure checklist (7.x+):**
- 📌 Planned: Contact erasure request → look up UUID via `linkedin_sales_url` or `email` → Connectra delete by UUID
- 📌 Planned: Verify all SN-sourced contacts for a user can be enumerated via `source=sales_navigator` + `user_id` filter
- 📌 Planned: Erasure cascade does not affect contacts from other sources with same UUID (impossible by UUID uniqueness)

**Campaign compliance (10.x):**
- 📌 Planned: Campaign audience from SN contacts traceable to `lead_id` + `search_id` + `session_id`
- 📌 Planned: Unsubscribed SN contacts must not be re-added to campaign audiences on re-ingest
- 📌 Planned: Evidence bundle for campaign recipients: SN session → contact UUID → campaign recipient

## Mailvetter (`backend(dev)/mailvetter`) audit and compliance controls

### Data classes processed

- Email address (direct personal data)
- Verification metadata (`status`, `score`, `score_details`)
- Operational metadata (`job_id`, `owner_key`, callback URL, timestamps)
- Optional signal metadata from SMTP/DNS/OSINT probes

### Compliance requirements by era

| Era | Control objective | Required evidence |
| --- | --- | --- |
| `0.x` | Baseline logging and retention for verification jobs | Job creation + completion records and retention policy |
| `1.x` | API key ownership and usage attribution | Key owner mapping and request audit trail |
| `2.x` | Verification decision explainability | Persisted `score_details` and reproducible scoring output |
| `3.x` | Contact/company linkage lineage | Mapping from verification result to contact/company identifiers |
| `4.x` | Source provenance (extension/SN/dashboard) | `source` and `source_session_id` metadata in records |
| `5.x` | AI-safe explainability and PII minimization | Redaction policy and test evidence |
| `6.x` | Reliability and incident auditability | Queue lag, retry, failure, and recovery evidence |
| `7.x` | Deployment/change governance | Migration logs, release approvals, rollback evidence |
| `8.x` | Public/private API key governance | Scoped key policy, rotation logs, endpoint audit |
| `9.x` | Partner webhook and connector governance | Signed delivery logs, retry/dead-letter records |
| `10.x` | Campaign verification compliance | Recipient-level verification snapshot and suppression-safe evidence |

### Mandatory controls

- 📌 Planned: All webhook callbacks are signed with `X-Webhook-Signature` and verified by consumers.
- 📌 Planned: `WEBHOOK_SECRET_KEY` is distinct from API auth secret; rotation documented.
- 📌 Planned: `jobs` and `results` retention policy enforced (default 30 days) with periodic cleanup evidence.
- 📌 Planned: Verification outputs used in campaign decisions are traceable to specific job/result records.
- 📌 Planned: Legacy endpoints are marked deprecated and excluded from new compliance integrations.
---

## Email app compliance surface — `contact360.io/email`

### Access and auth
| Capability | Control |
| --- | --- |
| Login | `POST /auth/login` with server session cookie |
| Logout | `POST /logout` |
| Profile read/update | Authenticated cookie session |
| IMAP account connect | Authenticated account settings operation |

### Data sensitivity notes
- Email bodies are sensitive content and are rendered only after DOMPurify sanitization.
- `mailhub_active_account` localStorage blob currently contains mailbox credentials context; this is a high-risk pattern.
- Custom headers `X-Email` and `X-Password` are currently used for mailbox reads and should be retired in favor of backend mailbox session IDs.

### Audit checklist
- 📌 Planned: Track account switch events (`setActiveAccount`) as audit-relevant action.
- 📌 Planned: Log IMAP connect operations with actor and timestamp.
- 📌 Planned: Ensure logout invalidates backend session.
- 📌 Planned: Ensure credential material is never logged client-side.

## Admin compliance surface — `contact360.io/admin`

### Current gap summary

- High-risk admin mutations (billing approve/decline, log delete/update, job retry) require stronger immutable audit emission coverage.
- Idempotency is not consistently enforced for destructive operational actions.
- Credit change history needs explicit before/after evidence with actor metadata.

### Required controls

- `ADM-0.4`: idempotency keys for destructive and replay-prone admin operations.
- `ADM-1.1`: credit-change audit timeline with actor, reason, and diff evidence.
- Role-policy matrix tests to ensure protected admin routes cannot be accessed outside approved roles.

## `s3storage` compliance surface — `lambda/s3storage`

- Missing universal API auth on non-health endpoints remains a compliance blocker.
- Upload/delete/metadata lifecycle actions require immutable audit event coverage.
- Multipart state durability and reconciliation controls are required for reliable evidence trails.

## `emailapigo`/`emailapis` compliance surface

- Env-only secret management is mandatory (`EGO-0.4`).
- Bulk verification/finder paths require immutable audit trails and replay-safe identifiers.
- Status taxonomy and lineage fields must be consistent for audit and incident reconstruction.

## `email campaign` compliance update

- `EC-0.2` unsubscribe query-path bug is compliance-relevant because suppression evidence may be unreliable until fixed.
