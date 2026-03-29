# File content structure overview
_Exported on 3/26/2026 at 17:09:50 GMT+5:30 from Cursor (2.6.21)_

---

**User**

Read these files and return their full contents (first 80 lines of each is enough to understand structure and gaps):
1. d:\code\ayan\contact\docs\9. Contact360 Ecosystem integrations and Platform productization\appointment360-ecosystem-productization-task-pack.md
2. d:\code\ayan\contact\docs\9. Contact360 Ecosystem integrations and Platform productization\connectors-commercial.md
3. d:\code\ayan\contact\docs\9. Contact360 Ecosystem integrations and Platform productization\connectra-ecosystem-productization-task-pack.md
4. d:\code\ayan\contact\docs\9. Contact360 Ecosystem integrations and Platform productization\contact-ai-ecosystem-productization-task-pack.md
5. d:\code\ayan\contact\docs\9. Contact360 Ecosystem integrations and Platform productization\emailapis-ecosystem-productization-task-pack.md
6. d:\code\ayan\contact\docs\9. Contact360 Ecosystem integrations and Platform productization\emailcampaign-ecosystem-productization-task-pack.md
7. d:\code\ayan\contact\docs\9. Contact360 Ecosystem integrations and Platform productization\integration-era-rc.md
8. d:\code\ayan\contact\docs\9. Contact360 Ecosystem integrations and Platform productization\integration-partner-governance.md

Return the first 80 lines of each file showing their structure (headings, task items, placeholder/boilerplate markers).

---

**Cursor**


Reading the first 80 lines of each file.




Below are the **first 80 lines** of each file (each file is shorter than 80 lines except `appointment360`, which is **77 lines** total — everything is included). Paths are absolute as requested.

---

### 1. `d:\code\ayan\contact\docs\9. Contact360 Ecosystem integrations and Platform productization\appointment360-ecosystem-productization-task-pack.md`

**Structure:** Title tied to Era 9.x; tracks **Contract / Service / Surface / Data / Ops** as Markdown tables with **Task | Priority**; ends with **Email app surface contributions (era sync)** bullets.

**Gaps / notes:** Concrete API/type names and file paths; no `[ ]` checkboxes; no Owner column; brief closing section (2 bullets).

```1:77:d:\code\ayan\contact\docs\9. Contact360 Ecosystem integrations and Platform productization\appointment360-ecosystem-productization-task-pack.md
# Appointment360 (contact360.io/api) — Era 9.x Ecosystem Integrations & Productization Task Pack

## Contract track

| Task | Priority |
| --- | --- |
| Define `NotificationQuery { notifications() }` | P0 |
| Define `NotificationMutation { markNotificationRead(id), markAllRead }` | P0 |
| Define `AnalyticsQuery { analytics(dateRange, granularity, metrics) }` | P0 |
| Define `AnalyticsMutation { trackEvent(type, metadata) }` | P0 |
| Define `AdminQuery { adminStats(), paymentSubmissions(), users() }` (SuperAdmin-only) | P0 |
| Define `AdminMutation { creditUser, adjustCredits, approvePayment, declinePayment }` (SuperAdmin-only) | P0 |
| Define `FeatureOverviewQuery { featureOverview() }` returning era/feature matrix | P1 |
| Define tenant model: `Workspace` / `Organization` type with multi-tenant guards | P1 |
| Document tenant entitlement enforcement contract in `docs/governance.md` | P1 |

---

## Service track

| Task | Priority |
| --- | --- |
| Implement notifications service: create, list, mark-read in `app/services/notification.py` | P0 |
| Implement analytics service: aggregate event counts from `events` table | P1 |
| Implement `trackEvent` mutation: write to `events` table with `user_uuid`, `type`, `metadata` | P0 |
| Implement `adminStats()`: aggregated counts (users, contacts, jobs, revenue) for SuperAdmin | P0 |
| Implement `featureOverview()`: return feature flags / credits matrix per plan | P1 |
| Wire notifications polling in background task: dispatch on billing events, job completions | P1 |
| Add `require_super_admin()` guard for all admin mutations | P0 |
| Add plan-based entitlement guard: `require_plan_feature(info, feature)` | P1 |
| Webhook support: outbound webhook on job completion / campaign send | P1 |

---

## Surface track

| Task | Priority |
| --- | --- |
| Notification bell icon → `query notifications()` polling every 30s | P0 |
| Notification drop-down → `mutation markNotificationRead` on click | P0 |
| Analytics dashboard page → `query analytics(...)` with date range picker | P1 |
| Admin panel → `query adminStats()` + `mutation creditUser` | P0 |
| Feature overview page (pricing/plan) → `query featureOverview()` | P1 |
| Plan upgrade modal → triggered by `require_plan_feature` guard response | P1 |
| `useNotifications` hook: polling, badge count, mark-read | P0 |
| `useAdminPanel` hook: manage user credit adjustments, approve payments | P0 |

---

## Data track

| Task | Priority |
| --- | --- |
| Create `notifications` table: uuid, user_uuid, type, message, is_read, created_at | P0 |
| Create `events` table: uuid, user_uuid, type, metadata JSON, created_at | P0 |
| Create `feature_flags` table: feature, plan_id, enabled, credit_cost | P1 |
| Create `workspaces` table for multi-tenant model: uuid, name, owner_uuid, plan_id | P1 |
| Run Alembic migration for all 9.x tables | P0 |

---

## Ops track

| Task | Priority |
| --- | --- |
| Configure webhook secret `WEBHOOK_SECRET` for outbound events | P1 |
| Write test: `trackEvent → query analytics` round-trip | P1 |
| Write test: `notifications()` → `markAllRead` → `notifications() = []` | P1 |
| Load test admin panel with 10,000 user dataset | P1 |
| Document multi-tenant entitlement enforcement in ops runbook | P1 |

---

## Email app surface contributions (era sync)

- Defined ecosystem-level integration backlog for mailbox export and downstream integrations.
- Prepared route and table selection surfaces for integration-driven workflows.
```

---

### 2. `d:\code\ayan\contact\docs\9. Contact360 Ecosystem integrations and Platform productization\connectors-commercial.md`

**Structure:** Era **8** (Stages 8.6–8.8); **Connector framework** (artifact table), **Integration observability** (bullets + doc refs), **Commercial controls** (bullets).

**Gaps / notes:** Not a 9.x “task pack”; no prioritized task tables; cross-links to governance and reliability docs.

```1:27:d:\code\ayan\contact\docs\9. Contact360 Ecosystem integrations and Platform productization\connectors-commercial.md
# Connector framework + integration observability + commercial controls (Era 8 — Stages 8.6–8.8)

## Connector framework (baseline)

Treat each **external system** as a connector with:

| Artifact | Description |
| -------- | ----------- |
| **Client module** | `contact360.io/api/app/clients/<name>_client.py` (or service-specific Lambda) |
| **Config** | `Settings` fields + env vars; no secrets in code |
| **Contract** | Request/response shapes documented; version pinned when upstream changes |
| **Health** | Callable health check or smoke test in `scripts/test_external_services.py` where applicable |

New connectors must follow `docs/integration-partner-governance.md` for identity and tenant safety.

## Integration observability

- **Correlation:** `X-Trace-Id` end-to-end — `docs/6. Contact360 Reliability and Scaling/queue-observability.md`.
- **SLO:** Gateway `/health/slo`; downstream SLOs owned per service — `docs/6. Contact360 Reliability and Scaling/slo-idempotency.md`.
- **Structured logs:** Include connector name, operation, latency, and error class (transient vs permanent).

## Commercial controls (integrations)

- **Metering:** Billable usage tied to successful user-visible outcomes (e.g. verified email, export row) — align with `usage` / credits modules.
- **Entitlements:** Feature flags per plan tier before calling expensive connectors — roadmap to Era 9.
- **Rate limits:** Per-tenant or per-partner caps in addition to gateway abuse guards — `docs/6. Contact360 Reliability and Scaling/performance-storage-abuse.md`.
```

---

### 3. `d:\code\ayan\contact\docs\9. Contact360 Ecosystem integrations and Platform productization\connectra-ecosystem-productization-task-pack.md`

**Structure:** Short title; **Scope**; **Small tasks** as bullets grouped Contract/Service/Database/Flow/Release gate.

**Gaps / notes:** Much thinner than Appointment360/Email Campaign packs — no tables, no P0/P1, no file paths; “9.x” only in title.

```1:14:d:\code\ayan\contact\docs\9. Contact360 Ecosystem integrations and Platform productization\connectra-ecosystem-productization-task-pack.md
# Connectra ecosystem-productization task pack (`9.x`)

## Scope

Enable Connectra as a tenant-safe, entitlement-aware platform primitive.

## Small tasks

- **Contract:** Define entitlement-aware filter/query policy by tenant plan.
- **Service:** Apply per-tenant quota/throttle controls for search/export heavy paths.
- **Database:** Store tenant usage aggregates for billing, quota, and SLA reporting.
- **Flow:** Validate connector SDK interactions against Connectra contract boundaries.
- **Release gate evidence:** Tenant isolation report, quota enforcement tests, and SLA evidence.
```

---

### 4. `d:\code\ayan\contact\docs\9. Contact360 Ecosystem integrations and Platform productization\contact-ai-ecosystem-productization-task-pack.md`

**Structure:** Metadata block (Service, Era, Status); same five tracks as checklist **`- [ ]`** items; **References** at end.

**Gaps / notes:** No priority/owner; conditional wording (“If `organization_id` added”); points to analysis/lineage docs.

```1:46:d:\code\ayan\contact\docs\9. Contact360 Ecosystem integrations and Platform productization\contact-ai-ecosystem-productization-task-pack.md
# Contact AI — 9.x Ecosystem Integrations / Platform Productization Task Pack

**Service:** `backend(dev)/contact.ai`  
**Era:** `9.x` — Ecosystem integrations and Platform productization  
**Status:** AI-powered connectors, webhook delivery, tenant model

---

## Contract track

- 🔴 Incompleted: Define Contact AI connector spec for external integration platforms (Zapier, Make, HubSpot).
- 🔴 Incompleted: Define webhook contract for async AI results: `{event: "ai_result", chat_id, result, timestamp}`.
- 🔴 Incompleted: Document multi-tenant isolation: each tenant's `ai_chats` data is fully isolated by `user_id`/`organization_id`.
- 🔴 Incompleted: Define connector auth model: connector keys separate from user keys; documented in API key management.

## Service track

- 🔴 Incompleted: Implement webhook delivery: on AI response completion, POST result to registered webhook URL.
- 🔴 Incompleted: Implement connector adapter: standardized input/output format for external platform integrations.
- 🔴 Incompleted: Implement organization-level AI usage aggregation (for tenant billing/quota).
- 🔴 Incompleted: Add `organization_id` to `ai_chats` if multi-tenant isolation requires org-level partitioning.

## Surface track

- 🔴 Incompleted: Integration panel in dashboard: AI-powered connectors configuration (webhook URL, trigger events).
- 🔴 Incompleted: Connector card: shows AI connector status (active/inactive), last delivery, error rate.
- 🔴 Incompleted: Webhook delivery log: show recent deliveries, status codes, retry count per webhook.

## Data track

- 🔴 Incompleted: If `organization_id` added: migration file to add column to `ai_chats`; update `contact_ai_data_lineage.md`.
- 🔴 Incompleted: Webhook delivery log schema: `{webhook_id, chat_id, payload_hash, status_code, retries, timestamp}`.
- 🔴 Incompleted: Connector audit trail: log all connector-initiated AI calls with `source: "connector"` tag.

## Ops track

- 🔴 Incompleted: Webhook delivery retry: exponential backoff, max 3 retries, dead-letter queue on final failure.
- 🔴 Incompleted: Connector health monitoring: track delivery success rate per connector.
- 🔴 Incompleted: Tenant isolation audit: verify no cross-tenant data leakage in AI responses.
- 🔴 Incompleted: Add connector endpoints to API rate limit policy.

---

**References:**  
`docs/codebases/contact-ai-codebase-analysis.md` · `docs/backend/database/contact_ai_data_lineage.md`
```

---

### 5. `d:\code\ayan\contact\docs\9. Contact360 Ecosystem integrations and Platform productization\emailapis-ecosystem-productization-task-pack.md`

**Structure:** Intro; **Contract / Service / Surface / Data / Ops** as short bullet lists.

**Gaps / boilerplate:** **`$(System.Collections.Hashtable.era)`** is repeated — broken template / placeholder, not a real era value. References JSON/matrix docs.

```1:23:d:\code\ayan\contact\docs\9. Contact360 Ecosystem integrations and Platform productization\emailapis-ecosystem-productization-task-pack.md
# emailapis task pack — era 9.x

This pack decomposes lambda/emailapis and lambda/emailapigo work into Contract, Service, Surface, Data, and Ops tracks.

## Contract tasks
- Define and freeze era $(System.Collections.Hashtable.era) email endpoint and payload compatibility notes.
- Update endpoint/reference matrix in docs/backend/endpoints/emailapis_endpoint_era_matrix.json.

## Service tasks
- Implement/validate runtime behavior for era $(System.Collections.Hashtable.era) finder, verifier, pattern, and fallback paths.
- Verify auth, provider routing, error envelope, and health diagnostics behavior.

## Surface tasks
- Document impacted pages/tabs/buttons/inputs/components for era $(System.Collections.Hashtable.era).
- Document relevant hooks/services/contexts and UX states (loading/error/progress/checkbox/radio).

## Data tasks
- Document email_finder_cache and email_patterns lineage impact for era $(System.Collections.Hashtable.era).
- Record provider, status, and traceability expectations for this era.

## Ops tasks
- Add observability checks and release validation evidence for era $(System.Collections.Hashtable.era).
- Capture rollback and incident-runbook notes for email-impacting releases.
```

---

### 6. `d:\code\ayan\contact\docs\9. Contact360 Ecosystem integrations and Platform productization\emailcampaign-ecosystem-productization-task-pack.md`

**Structure:** Title + **Context**; **Track A–E** (Contract–Ops) as **Task | Description | Owner** tables; **Completion gate** checkboxes.

**Gaps / notes:** No P0/P1; sign-off section not here (unlike `integration-era-rc.md`).

```1:57:d:\code\ayan\contact\docs\9. Contact360 Ecosystem integrations and Platform productization\emailcampaign-ecosystem-productization-task-pack.md
# Email Campaign Service — Era 9.x Task Pack
## Contact360 Ecosystem Integrations and Platform Productization

### Context
Era `9.x` productises Contact360 for marketplace and ecosystem exposure. The campaign service must support per-tenant entitlement limits, suppression-list import from third-party providers (HubSpot, Mailchimp), Zapier/webhook triggers, and white-label campaign delivery for reseller partners.

---

## Track A — Contract

| Task | Description | Owner |
| --- | --- | --- |
| A-9.1 | Define tenant entitlement model: max recipients/month, max campaigns/day, template count limits | Product |
| A-9.2 | Define suppression import API: accept CSV or webhook from CRM connectors | Backend |
| A-9.3 | Define partner campaign-delivery API for white-label reseller paths | Backend |

## Track B — Service

| Task | Description | Owner |
| --- | --- | --- |
| B-9.1 | Entitlement enforcement middleware: check org tier limits before accepting campaign | Backend |
| B-9.2 | Suppression import endpoint: `POST /suppression/import` (CSV or JSON payload) | Backend |
| B-9.3 | CRM connector: accept unsubscribe events from HubSpot/Mailchimp webhooks → suppression | Backend |
| B-9.4 | White-label send path: campaigns can specify `sender_domain` from org's verified domain pool | Backend |
| B-9.5 | Zapier trigger: campaign lifecycle event published to Zapier webhook | Backend |

## Track C — Surface

| Task | Description | Owner |
| --- | --- | --- |
| C-9.1 | Integrations settings page: connect HubSpot/Mailchimp for suppression sync | Frontend |
| C-9.2 | Domains management page: verified sender domains list with DKIM/SPF status indicators | Frontend |
| C-9.3 | Billing/plan page: show campaign-specific entitlement usage (campaigns used / limit) | Frontend |

## Track D — Data

| Task | Description | Owner |
| --- | --- | --- |
| D-9.1 | Migration: `sender_domains` table (org_id, domain, verified, dkim_record, spf_record) | Backend |
| D-9.2 | Migration: `entitlements` table (org_id, feature, limit_value, used_value, period) | Backend |
| D-9.3 | Migration: `integration_suppression_sync` table (org_id, provider, last_synced_at) | Backend |

## Track E — Ops

| Task | Description | Owner |
| --- | --- | --- |
| E-9.1 | Periodic suppression sync cron job: pull opted-out contacts from connected CRMs | DevOps |
| E-9.2 | Domain verification DNS checker job: poll DKIM/SPF records and update `verified` flag | DevOps |

---

## Completion gate
- 🔴 Incompleted: Org exceeding campaign send limit receives 429 with descriptive limit error.
- 🔴 Incompleted: Suppression list import accepts CSV with 10k+ emails without timeout.
- 🔴 Incompleted: HubSpot unsubscribe webhook adds contact to Contact360 suppression list.
- 🔴 Incompleted: Sender domain DKIM verification status visible in settings UI.
```

---

### 7. `d:\code\ayan\contact\docs\9. Contact360 Ecosystem integrations and Platform productization\integration-era-rc.md`

**Structure:** Era **8** Stage **8.9** RC gate; **Preconditions** table (Check | Reference); **Regression** bullets; **Sign-off** table with empty **Name | Date**.

**Gaps / boilerplate:** Sign-off cells are blank; mix of Era 8 vs folder “9” naming.

```1:27:d:\code\ayan\contact\docs\9. Contact360 Ecosystem integrations and Platform productization\integration-era-rc.md
# Integration era RC gate (Era 8 — Stage 8.9)

Release candidate checklist before **partner-facing integrations** or **public API** commitments ship.

## Preconditions

| Check | Reference |
| ----- | --------- |
| Contract docs frozen for the release | `docs/integration-partner-governance.md`, `docs/public-api-surface.md` |
| Idempotency on billing / high-risk writes | `docs/6. Contact360 Reliability and Scaling/slo-idempotency.md` |
| Webhook signing + replay story agreed | `docs/8. Contact360 public and private apis and endpoints/webhooks-replay.md` |
| Connector observability | `docs/9. Contact360 Ecosystem integrations and Platform productization/connectors-commercial.md` |
| No cross-tenant leaks in new resolvers | `docs/tenant-security-observability.md` |

## Regression

- **Compatibility:** GraphQL clients used by dashboard + extension pass smoke tests against staging.
- **Partner sandbox:** If applicable, partner completes test matrix (auth, error cases, idempotent retries).

## Sign-off

| Role | Name | Date |
| ---- | ---- | ---- |
| Engineering | | |
| Partnerships / GTM | | |
| Security review | | |
```

---

### 8. `d:\code\ayan\contact\docs\9. Contact360 Ecosystem integrations and Platform productization\integration-partner-governance.md`

**Structure:** Era **8** Stages **8.1–8.2**; **Contract governance** (principles); **Partner identity** (Today vs **Partner / B2B (target)** table); **Tenant-safe access** bullets.

**Gaps / notes:** Policy doc, not a task checklist; “target” state called out explicitly.

```1:33:d:\code\ayan\contact\docs\9. Contact360 Ecosystem integrations and Platform productization\integration-partner-governance.md
# Integration contract governance + partner identity (Era 8 — Stages 8.1–8.2)

## Contract governance

**Principles**

- Every outbound integration (Lambda, Connectra, s3storage, third-party HTTP) is documented with: base URL, auth scheme, timeout, and idempotency expectations — see `contact360.io/api/app/clients/`.
- Breaking changes require a **version bump** in the consumer and a changelog entry; GraphQL schema changes follow deprecation rules in `docs/public-api-surface.md` (when published).
- Error shapes should map to gateway `GraphQL` errors where proxied; avoid leaking upstream stack traces to clients.

## Partner identity

**Today**

- **First-party clients** (dashboard, extension): user identity via **JWT** (`Authorization: Bearer`) — `docs/7. Contact360 deployment/rbac-authz.md`.
- **Service-to-service**: each downstream service uses its own **API key** (e.g. `X-API-Key`, Connectra key) — configured in `app/core/config.py` / env templates.

**Partner / B2B (target)**

| Concern | Approach |
| ------- | -------- |
| Partner id | Issued `client_id` + rotating **client_secret** or mTLS (infrastructure choice) |
| Scopes | Explicit allowlists per integration (read contacts, enqueue jobs, …) |
| Tenant safety | All partner tokens bound to `tenant_id`; resolvers enforce scope + tenant row access |

Until dedicated partner OAuth/m2m is implemented, treat **integration keys as secrets**, rotate on compromise, and never embed them in client-side code.

## Tenant-safe access (integrations)

- Do not accept a raw `user_id` / `tenant_id` from the partner body without cryptographic binding to the authenticated principal.
- Prefer **short-lived delegated tokens** or signed webhooks (see Era 8 webhook doc) for callbacks.
- Log partner id + `X-Trace-Id` on every cross-boundary call for audit — `docs/6. Contact360 Reliability and Scaling/queue-observability.md`.
```

---

## Cross-file structure contrast (quick)

| File | Primary shape | Era label in doc | Obvious boilerplate / gap |
|------|----------------|------------------|----------------------------|
| appointment360 | Tables + P0/P1 | 9.x | Short “email app” coda only |
| connectors-commercial | Narrative + one artifact table | **8.x** | Not a decomposed task pack |
| connectra | 5 bullets | “9.x” in title only | Very high-level vs peers |
| contact-ai | `- [ ]` by track | 9.x | Optional org migration |
| emailapis | Bullet tracks | 9.x header | **`$(System.Collections.Hashtable.era)`** |
| emailcampaign | Tracks A–E + Owner + gate | 9.x | — |
| integration-era-rc | RC + sign-off | **8.x** | Empty sign-off cells |
| integration-partner-governance | Policy / tables | **8.x** | — |

---

**Note:** Workspace rules mention Byterover MCP `byterover-retrieve-knowledge` / `byterover-store-knowledge` at task start/end; this subagent run was read-only search only, so those tools were not invoked.

