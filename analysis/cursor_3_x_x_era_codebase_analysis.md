# 3.x.x era codebase analysis
_Exported on 3/25/2026 at 14:32:36 GMT+5:30 from Cursor (2.6.21)_

---

**User**

Read these files and return sections relevant to the 3.x.x era (contact/company data, enrichment, export, search UX, dedup):
1. d:\code\ayan\contact\docs\codebases\jobs-codebase-analysis.md - era mapping table, 3.x row, immediate execution queue, gaps
2. d:\code\ayan\contact\docs\codebases\app-codebase-analysis.md - era mapping, 3.x row, search UX gap items
3. d:\code\ayan\contact\docs\codebases\appointment360-codebase-analysis.md - era mapping, 3.x row

Return only the relevant sections.

---

**Cursor**


Reading the three analysis files and extracting sections relevant to the 3.x.x era.




Here are the parts of those docs that match what you asked for. **Note:** `jobs-codebase-analysis.md` has no “immediate execution queue” section (that heading exists in `appointment360-codebase-analysis.md`). **`app-codebase-analysis.md` has no separate “search UX gap items” list**—only general “Key findings and risks.”

---

### 1. `d:\code\ayan\contact\docs\codebases\jobs-codebase-analysis.md`

**Era mapping (era-by-era breakdown) — 3.x row**

```116:121:d:\code\ayan\contact\docs\codebases\jobs-codebase-analysis.md
### 3.x Contact/company data
- Contract: import/export + VQL validation contracts.
- Service: `contact360_import_prepare` and `contact360_export_stream`.
- Surface: import/export table states and detail dialogs.
- Data: PG+OpenSearch lineage and replay safety.
- Ops: partial-failure handling and replay runbooks.
```

**Related processors / API (contact import/export, VQL)**

```51:59:d:\code\ayan\contact\docs\codebases\jobs-codebase-analysis.md
| Job type | Processor | Main creation endpoint |
| --- | --- | --- |
| `email_finder_export_stream` | `email_finder_export_stream` | `POST /api/v1/jobs/email-export` |
| `email_verify_export_stream` | `email_verify_export_stream` | `POST /api/v1/jobs/email-verify` |
| `email_pattern_import_stream` | `email_pattern_import_stream` | `POST /api/v1/jobs/email-pattern-import` |
| `contact360_import_prepare` | `contact360_import_prepare` | `POST /api/v1/jobs/contact360-import` |
| `contact360_export_stream` | `contact360_export_stream` | `POST /api/v1/jobs/contact360-export` |
| `export_csv_file` | validation stub | DAG/manual only |
| `insert_csv_file` | validation stub | DAG/manual only |
```

```67:72:d:\code\ayan\contact\docs\codebases\jobs-codebase-analysis.md
- `POST /api/v1/jobs/contact360-import`
- `POST /api/v1/jobs/contact360-export`
...
- `POST /api/v1/jobs/validate/vql`
```

**Gaps (document-wide, not 3.x-only)**

```85:91:d:\code\ayan\contact\docs\codebases\jobs-codebase-analysis.md
## Known gaps and risks

1. Stale `processing` recovery depends on active scheduler recovery loop.
2. DAG degree-decrement failure can block downstream nodes.
3. Single shared `X-API-Key` model (no per-user/role authz in service itself).
4. Retry trigger is explicit `retry` status semantics; docs must not model retry directly from `failed`.
5. Some legacy multi-node Contact360 DAG patterns are no longer active in registry.
```

**Immediate execution queue:** not present in this file.

---

### 2. `d:\code\ayan\contact\docs\codebases\app-codebase-analysis.md`

**Era alignment — 3.x row**

```63:75:d:\code\ayan\contact\docs\codebases\app-codebase-analysis.md
## Era alignment (`0.x`-`10.x`)

- `0.x`: shell, auth gate, foundational contexts, shared UI primitives
- `1.x`: user, billing, credits, usage and role/plan surfaces
- `2.x`: email finder/verifier workflows and bulk file/job progress UX
- `3.x`: contacts/companies search, tables, filters, saved-search workflows
- `4.x`: extension/Sales Navigator and LinkedIn-integrated surfaces
- `5.x`: AI chat/assistant and AI-assisted workflow surfaces
- `6.x`: reliability patterns (guards, retries, health feedback)
- `7.x`: admin/deployment/governance role-aware dashboard controls
- `8.x`: API/platform analytics and private/public endpoint-aligned product pages
- `9.x`: integrations and ecosystem productization UX
- `10.x`: campaign-oriented product surfaces and supporting controls
```

**Hooks / GraphQL domains that back 3.x-style surfaces**

```33:48:d:\code\ayan\contact\docs\codebases\app-codebase-analysis.md
### Hooks (major domains)

- Auth/session: `useLoginForm`, `useRegisterForm`, `useSessionGuard`, `useSessions`
- Billing/usage: `useBilling`, `useFeatureOverview`
- Email: `useEmailFinderSingle`, `useEmailVerifierSingle`, `useEmailVerifierBulk`
- Data/files: `useFiles`, `useCsvUpload`, `useFilePreview`, `useFileStats`
- Product domains: `useContacts*`, `useCompanies*`, `useLinkedIn`, `useAnalytics`, `useAdmin`, `useTeam`
- UI behavior: modal/sidebar/resizable/debounce and page access helpers

### GraphQL services (`src/services/graphql`)

- Auth/users/profile/two-factor
- Contacts/companies/saved searches
- Billing/usage/notifications/exports
```

**Search UX gap items:** this file does not define them. Closest text is general risks:

```77:81:d:\code\ayan\contact\docs\codebases\app-codebase-analysis.md
## Key findings and risks

1. Dashboard docs are strong but should be represented in the same deep-analysis format as root/admin for consistency.
2. API module mapping is broad; contract drift needs continuous sync with docs/backend module docs.
3. Role/page visibility logic is critical and should stay synchronized with governance and roadmap stages.
```

---

### 3. `d:\code\ayan\contact\docs\codebases\appointment360-codebase-analysis.md`

**Era mapping — 3.x row**

```207:222:d:\code\ayan\contact\docs\codebases\appointment360-codebase-analysis.md
## Era mapping (`0.x`–`10.x`)

| Era | Appointment360 concern |
| --- | --- |
| `0.x` | Service bootstrap, middleware baseline, context/session lifecycle, schema layout |
| `1.x` | Auth mutations (login/register/refresh/logout), credit deduction, billing module, usage tracking |
| `2.x` | Email module (finder/verifier), jobs orchestration module, activity logging |
| `3.x` | Contacts/companies modules, VQL conversion, Connectra integration |
| `4.x` | LinkedIn/SalesNavigator modules, extension session and sync mutations |
| `5.x` | AI chats module, resume module, Gemini AI integration |
| `6.x` | Complexity/timeout extensions, idempotency, abuse guard, rate limiting, RED/SLO |
| `7.x` | RBAC (admin/SuperAdmin guards), audit log emissions, deployment security |
| `8.x` | Pages module, saved searches, profile/API keys, public API surface |
| `9.x` | Tenant model, entitlement enforcement, connector governance, notifications |
| `10.x` | Campaigns/sequences/templates modules, campaign wizard orchestration |
```

**Immediate execution queue** (only in this file among your three; not 3.x-specific):

```225:234:d:\code\ayan\contact\docs\codebases\appointment360-codebase-analysis.md
## Immediate execution queue

1. Remove all inline debug file writes (`_debug_log`, `debug.log` writes) from production modules.
2. Add `campaigns`, `sequences`, `campaignTemplates` GraphQL modules in schema.
3. Enable `GRAPHQL_RATE_LIMIT_REQUESTS_PER_MINUTE` in production environment.
4. Restore SQL schema docs or link to shared schema source.
5. Add Redis-backed distributed state for idempotency/abuse guard in multi-replica deployments.
6. Wire `DOCSAI_ENABLED` health check — pages `/health` should surface DocsAI dependency.
7. Write contract parity tests for each module against `docs/backend/apis/*.md`.
```

---

**Coverage vs your themes:** These three docs tie **3.x** to import/export/VQL/jobs (jobs), dashboard search/tables/filters/saved searches (app), and GraphQL contacts/companies + VQL + Connectra (Appointment360). **Enrichment** and **dedup** are not called out explicitly in the extracted 3.x rows; dedup appears in jobs only under **4.x** (“dedupe markers”), not 3.x.

