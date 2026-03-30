# Contact360 documentation summary
_Exported on 3/24/2026 at 20:13:14 GMT+5:30 from Cursor (2.6.21)_

---

**User**

Read these specific files from d:\code\ayan\contact\docs and summarize their content (first 80 lines each):

1. docs\2. Contact360 email system\cursor_email_system_architecture_explor.md
2. docs\2. Contact360 email system\email_system.md
3. docs\1.  Contact360 user and billing and credit system\dashboard-search-ux.md
4. docs\1.  Contact360 user and billing and credit system\rbac-authz.md
5. docs\3. Contact360 contact and company data system\connectors-commercial.md
6. docs\3. Contact360 contact and company data system\webhooks-replay.md
7. docs\9. Contact360 Ecosystem integrations and Platform productization\analytics-era-rc.md
8. docs\9. Contact360 Ecosystem integrations and Platform productization\performance-storage-abuse.md
9. docs\9. Contact360 Ecosystem integrations and Platform productization\reliability-rc-hardening.md
10. docs\9. Contact360 Ecosystem integrations and Platform productization\queue-observability.md

For each: title, main topics covered (first 80 lines), and whether it seems like an orphan or is well cross-referenced in context of its era folder.

---

**Cursor**


Reading the first 80 lines of each file and scanning their era folders for cross-references.




Checking each era folder for cross-references to these documents.




Here is a concise report based on the first 80 lines of each file (several are shorter than 80 lines, so the summary reflects the full document). Absolute paths use your workspace root `d:\code\ayan\contact`.

---

### 1. `d:\code\ayan\contact\docs\2. Contact360 email system\cursor_email_system_architecture_explor.md`

**Title (implicit):** Email system architecture exploration (Cursor export, 3/24/2026)

**Main topics (first ~80 lines):** Exported chat: user asked to explore `contact360.io\api` for email architecture. Response covers: (1) architecture map — GraphQL `email` module, `LambdaEmailClient`, jobs/`TkdjobClient`, `scheduler_jobs`, auth/credits/activity; (2) key files — `queries.py`, `mutations.py`, `inputs.py`, `types.py`, `lambda_email_client.py`, jobs mutations, `tkdjob_client.py`; (3) E2E flows — real-time find/verify vs bulk export/verify via scheduler; (4) scoring — verification passthrough from Lambda, no in-API scoring; (5) risks — hardcoded secrets, debug file writes, retry on non-idempotent POSTs (line 79+ continues).

**Orphan vs cross-referenced:** **Loosely isolated** in Era 2. It sits among many similar `cursor_email_*` exports; version docs in that folder link to `.cursor/rules/email_system.md`, not this filename. `docs\governance.md` does not cite this export by name.

---

### 2. `d:\code\ayan\contact\docs\2. Contact360 email system\email_system.md`

**Title:** Full distributed email platform map (no H1; opens with “distributed email platform”)

**Main topics:** Unified stack: (1) product/UI `app`; (2) API orchestration `api`; (3) async jobs `jobs`; (4) Lambda `emailapigo` / `emailapis`; (5) verification engine `mailvetter`; (6) sync/index `sync`; (7) admin. E2E flows A–C (sync, async CSV, scoring). **Cross-system risks:** contract drift, status semantics, resume/checkpoint inconsistency, thin e2e tests, observability fragmentation, operational bugs in sync, etc. (continues past line 80).

**Orphan vs cross-referenced:** **Central synthesis doc** for email; era version files point at the **Cursor rule** `email_system.md` under `.cursor/rules/`, not necessarily this `docs\2\...\email_system.md` path. Conceptually foundational; path-level linking is indirect.

---

### 3. `d:\code\ayan\contact\docs\1.  Contact360 user and billing and credit system\dashboard-search-ux.md`

**Title:** Dashboard search UX (roadmap stage 2.4)

**Main topics (full doc ~26 lines):** Intent: contacts/companies discovery, filters, saved searches, company drill-down. Next.js routes table (`contacts`, `companies`, `[id]`). Saved searches UI + GraphQL service + export/jobs hooks. Filter mapping via `vql_converter.py` and `docs/vql-filter-taxonomy.md`. Feature gating via `featureAccess.ts` (`ADVANCED_FILTERS`, `SAVE_SEARCHES`).

**Orphan vs cross-referenced:** **Indexed globally:** `d:\code\ayan\contact\docs\governance.md` lists “Dashboard search UX” → `docs/dashboard-search-ux.md`. **No matches** in other files under Era 1 for these filenames—reliance is on root `governance.md` (flat path).

---

### 4. `d:\code\ayan\contact\docs\1.  Contact360 user and billing and credit system\rbac-authz.md`

**Title:** RBAC and authorization (Era 7 — Stages 6.1–6.2)

**Main topics (full doc ~46 lines):** Roles on `UserProfile` (`SuperAdmin`, `Admin`, `ProUser`, `FreeUser`), `UNLIMITED_CREDITS_ROLES`. GraphQL enforcement: JWT, `require_auth`, `require_admin` / `require_profile_roles`, billing examples, ownership. Content gating `access_control.py`. Downstream service auth (Lambda keys, Connectra, extension). Hardening checklist. Forward reference to partner APIs / Era 8.

**Orphan vs cross-referenced:** **Well linked outside Era 1:** `docs\governance.md` points to `docs/rbac-authz.md`. Cited from `docs\9. Contact360 Ecosystem integrations and Platform productization\analytics-era-rc.md`, `analytics-platform.md`, `integration-partner-governance.md`. **Not** referenced by filename inside the Era 1 folder itself.

---

### 5. `d:\code\ayan\contact\docs\3. Contact360 contact and company data system\connectors-commercial.md`

**Title:** Connector framework + integration observability + commercial controls (Era 8 — Stages 8.6–8.8)

**Main topics (full doc ~27 lines):** Connector pattern (client, config, contract, health). New connectors → `integration-partner-governance.md`. Observability: `X-Trace-Id`, SLO, structured logs with pointers to `queue-observability.md`, `slo-idempotency.md`. Commercial: metering, entitlements, rate limits → `performance-storage-abuse.md`.

**Orphan vs cross-referenced:** **Hub doc** that **out-links** to Era 9 (`queue-observability`, `performance-storage-abuse`) and governance-style docs. **Indexed** in `docs\governance.md` and `docs\9. Contact360 Ecosystem integrations and Platform productization\integration-era-rc.md`. **No inbound references** from other files in Era 3 by filename (grep).

---

### 6. `d:\code\ayan\contact\docs\3. Contact360 contact and company data system\webhooks-replay.md`

**Title:** Webhook delivery + replay / reconciliation (Era 8 — Stages 8.4–8.5)

**Main topics (full doc ~34 lines):** Status: design baseline; implementation in job/queue when productized. Event envelope, HMAC signing, at-least-once delivery, retries, DLQ, replay, reconciliation, observability → `queue-observability.md`.

**Orphan vs cross-referenced:** **Governance + Era 9:** listed in `docs\governance.md`; `integration-era-rc.md` in Era 9 cites webhook signing + replay. **Not** referenced by other Era 3 files by filename.

---

### 7. `d:\code\ayan\contact\docs\9. Contact360 Ecosystem integrations and Platform productization\analytics-era-rc.md`

**Title:** Analytics era RC gate (Era 7 — Stage 6.9)

**Main topics (full doc ~26 lines):** Pre-flight checklist for analytics/reporting RC: stable usage/activity APIs, PII/sampling, RBAC → `rbac-authz.md`, traceability → `queue-observability.md`. Complements `reliability-rc-hardening.md`. Short smoke list and sign-off table.

**Orphan vs cross-referenced:** **Tightly coupled** to `reliability-rc-hardening.md` and cross-doc links; **not** the main index—`governance.md` does not show this filename in the grep sample, but it references related themes. Era 9 file `analytics-platform.md` shares the same observability/RBAC doc pattern.

---

### 8. `d:\code\ayan\contact\docs\9. Contact360 Ecosystem integrations and Platform productization\performance-storage-abuse.md`

**Title:** Era 6.5–6.8: Performance, storage, cost, and abuse guardrails

**Main topics (full doc ~28 lines):** `GET /health/slo`; `GraphQLBodySizeMiddleware` + `GRAPHQL_MAX_BODY_BYTES` (413); `GraphQLMutationAbuseGuardMiddleware`, `MUTATION_ABUSE_GUARD_RPM`, `ABUSE_GUARDED_MUTATIONS`, 429; S3 lifecycle runbook; tuning `429` by tier.

**Orphan vs cross-referenced:** **Governance** indexes it. **Cited from** `connectors-commercial.md` (Era 3), `public-api-surface.md` (Era 8), `tenant-security-observability.md` (Era 7). **Well embedded** in cross-era references.

---

### 9. `d:\code\ayan\contact\docs\9. Contact360 Ecosystem integrations and Platform productization\reliability-rc-hardening.md`

**Title:** Reliability RC hardening (Era 6 — Stage 5.9)

**Main topics (full doc ~45 lines):** RC gate: `/health`, `/health/db`, `/health/logging`, `/health/slo`, abuse env vars, idempotency → `slo-idempotency.md`, traces → `queue-observability.md`. Manual smoke suite (auth, billing, credits, bulk, Connectra/VQL, AI chat). Incident runbook. Sign-off table; build ID must be recorded.

**Orphan vs cross-referenced:** **Central RC doc** — `analytics-era-rc.md` complements it; multiple docs point to `queue-observability.md` alongside it. **Governance**-level theme; strong **inbound** links from analytics RC doc.

---

### 10. `d:\code\ayan\contact\docs\9. Contact360 Ecosystem integrations and Platform productization\queue-observability.md`

**Title:** Era 6.3–6.4: Queue resilience and observability baseline

**Main topics (full doc ~24 lines):** `TraceIdMiddleware`: `X-Trace-Id` / `X-Request-Id` / UUID, echoed on response. Queue runbook: idempotent enqueue, DLQ/replay, trace IDs in payloads. Next step: explicit DLQ/replay endpoints and docs.

**Orphan vs cross-referenced:** **Highly referenced** across the repo: `governance.md`, `connectors-commercial.md`, `webhooks-replay.md`, `analytics-era-rc.md`, `reliability-rc-hardening.md`, `analytics-platform.md`, `integration-partner-governance.md`, `tenant-security-observability.md`. **Not an orphan.**

---

### Cross-reference note (era folders vs `docs\governance.md`)

`d:\code\ayan\contact\docs\governance.md` uses **flat** paths like `docs/dashboard-search-ux.md` and `docs/queue-observability.md`. Your copies live under **numbered era subfolders**, so sibling-era grep may miss links even when **governance** still indexes the same topics. Era **9** files **do** reference each other and several Era **3/7/8** docs by `docs/...` paths. Era **2** exploration exports cluster together but are less tied to **governance** than **`email_system.md`** (via the **Cursor rule**).

