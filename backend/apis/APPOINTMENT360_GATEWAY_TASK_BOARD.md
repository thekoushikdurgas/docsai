# Appointment360 gateway task board (`contact360.io/api`)

Granular tasks for the GraphQL gateway aligned with Contact360 eras `0.x.x`–`10.x.x`. Use this file together with [appointment360-codebase-analysis.md](../../codebases/appointment360-codebase-analysis.md) (narrative + risks) and [APPOINTMENT360_ERA_TASK_PACKS.md](APPOINTMENT360_ERA_TASK_PACKS.md) (index to per-era docs under `docs/0…10/`).

**Verification note (schema):** Root `Query` / `Mutation` in `contact360.io/api/app/graphql/schema.py` currently expose the namespaces listed in the era sections below. **`campaigns`, `sequences`, and `campaignTemplates` are not mounted on the root schema**; module docs `22_*`, `24_*`, `25_*` describe the intended contract ahead of implementation. There is **no** `CampaignServiceClient` (or `CAMPAIGN_*` settings) under `app/clients/` / `app/core/config.py` yet.

## Task status legend

| Symbol | Meaning |
| --- | --- |
| ✅ | Completed (behavior present in runtime and aligned with docs at last review) |
| 🟡 | In progress (partially done or needs continuous upkeep) |
| 📌 | Planned (scoped but not started, or waiting on dependencies) |
| ⬜ | Incomplete (known gap or blocking follow-up) |

## Era summary

| Era | Theme | Gateway posture (high level) |
| --- | --- | --- |
| `0.x.x` | Foundation | Core app, middleware, context, schema composition ✅; secure defaults and doc drift 🟡/⬜ |
| `1.x.x` | User, billing, credits | Auth, users, billing, usage, activities wired ✅; production idempotency/audit ⬜/🟡 |
| `2.x.x` | Email | Email + jobs integration ✅; provider semantics and test depth 🟡/⬜ |
| `3.x.x` | Contacts & companies | Connectra + VQL + S3/upload paths ✅; filter parity and lineage 🟡/⬜ |
| `4.x.x` | Extension & Sales Navigator | LinkedIn + SN mutations ✅; extension diagnostics ⬜ |
| `5.x.x` | AI | `aiChats` + `resume` ✅; `LambdaAIClient` → Contact AI REST 🟡/⬜ for policy/lineage |
| `6.x.x` | Reliability & scaling | Complexity, timeout, guards, metrics ✅; shared store for guards ⬜ |
| `7.x.x` | Deployment | EC2/Lambda/Docker ✅; strict secret policy and runbooks 🟡/⬜ |
| `8.x.x` | Public & private APIs | Broad internal GraphQL surface 🟡; versioning & partner contracts 📌/⬜ |
| `9.x.x` | Ecosystem | Notifications, saved searches, profile, 2FA, pages, feature overview ✅/🟡; integrations/webhooks as docs-only until schema mounts 📌 |
| `10.x.x` | Email campaign | REST service exists separately; **gateway GraphQL + HTTP client ⬜** |

---

## `0.x.x` — Foundation and pre-product stabilization

- [x] ✅ FastAPI app, Strawberry schema, `/graphql` and health routes (`app/main.py`).
- [x] ✅ Per-request DB session + `DatabaseCommitMiddleware` commit discipline.
- [x] ✅ JWT context and `get_context` (`app/graphql/context.py`).
- [x] ✅ GraphQL extensions: complexity + timeout (`app/graphql/extensions.py`).
- [x] ✅ Custom middleware: body size, idempotency, abuse guard, rate limit, request/trace IDs, timing, RED metrics (`app/core/middleware.py`, `main.py`).
- [ ] 🟡 Keep [appointment360-codebase-analysis.md](../../codebases/appointment360-codebase-analysis.md) middleware order table identical to `main.py` registration order on every stack change.
- [ ] ⬜ Remove or gate insecure **default** API URLs/keys in `app/core/config.py` (secret-only or fail-fast in production).
- [ ] ⬜ Eliminate residual debug patterns (e.g. forbidden `open(...)` writes in resolvers/clients); enforce via CI grep or review checklist.
- [ ] 📌 Add/extend contract tests: boot app, `GET /health`, minimal `POST /graphql` smoke per environment profile.

**Small tasks (checklist)**

1. [ ] ⬜ Audit `deploy/env.example` vs `Settings` for any credential-looking defaults; document “must override” in module docs.
2. [ ] ⬜ Document actual middleware order once in [08_HEALTH_MODULE.md](08_HEALTH_MODULE.md) or codebase analysis only (single source of truth).
3. [ ] 🟡 Run `scripts/validate_env.py` / pre-deploy checks in CI for `production`.

---

## `1.x.x` — User, billing, and credit system

- [x] ✅ `auth`, `users`, `billing`, `usage`, `activities` namespaces in schema.
- [x] ✅ Credit and usage services integrated from domain modules (see [14_BILLING_MODULE.md](14_BILLING_MODULE.md), [09_USAGE_MODULE.md](09_USAGE_MODULE.md)).
- [ ] 🟡 `IDEMPOTENCY_ENFORCE_GRAPHQL_MUTATIONS` / `IDEMPOTENCY_REQUIRED_MUTATIONS`: confirm production env enforces billing-related mutations.
- [ ] ⬜ Immutable audit trail for `billing.*` and `admin.*` credit/payment mutations (evidence for disputes).
- [ ] ⬜ Parity tests for billing mutation payloads vs Stripe/payment submission flows documented in [14_BILLING_MODULE.md](14_BILLING_MODULE.md).

**Small tasks**

1. [ ] ⬜ List billing mutations that must require `X-Idempotency-Key`; align `settings` and Postman examples.
2. [ ] 🟡 Trace `admin.creditUser` / `billing.subscribe` through repositories and log redaction rules.
3. [ ] 📌 Define retention policy for payment proof artifacts (S3 vs DB) and document in data lineage.

---

## `2.x.x` — Email system

- [x] ✅ `email` queries/mutations and `jobs` orchestration for exports/imports ([15_EMAIL_MODULE.md](15_EMAIL_MODULE.md), [16_JOBS_MODULE.md](16_JOBS_MODULE.md)).
- [x] ✅ `LambdaEmailClient` wired via `LAMBDA_EMAIL_API_*`.
- [ ] 🟡 Align status vocabulary and error mapping with `lambda/emailapis` and mailvetter docs ([MAILVETTER_ERA_TASK_PACKS.md](MAILVETTER_ERA_TASK_PACKS.md)).
- [ ] ⬜ Integration tests for job failure/retry paths (tkdjob + email worker semantics).
- [ ] ⬜ Document rate limits and bulk caps in [15_EMAIL_MODULE.md](15_EMAIL_MODULE.md) when downstream changes.

**Small tasks**

1. [ ] 🟡 One end-to-end trace: `createEmailFinderExport` → tkdjob → processor (document job types in [16_JOBS_MODULE.md](16_JOBS_MODULE.md)).
2. [ ] ⬜ Verify `addEmailPatternBulk` idempotency expectations for UI/extension callers.

---

## `3.x.x` — Contact and company data

- [x] ✅ `contacts`, `companies`, `s3`, `upload`, `savedSearches` in schema.
- [x] ✅ `ConnectraClient` + `vql_converter` / mappers.
- [ ] 🟡 Filter taxonomy parity: GraphQL `filters` / `filterData` vs Connectra VQL ([connectra_endpoint_era_matrix.json](../endpoints/connectra_endpoint_era_matrix.json)).
- [ ] ⬜ DataLoader coverage audit for new list fields (avoid N+1 in large exports).
- [ ] 🟡 Enrichment / denormalized column rules (`company_config.populate`) documented and tested.

**Small tasks**

1. [ ] ⬜ Add one golden test: complex `VQLQueryInput` → Connectra JSON (snapshot).
2. [ ] 🟡 Cross-check [03_CONTACTS_MODULE.md](03_CONTACTS_MODULE.md) / [04_COMPANIES_MODULE.md](04_COMPANIES_MODULE.md) operation tables against `queries.py` / `mutations.py`.

---

## `4.x.x` — Extension and Sales Navigator maturity

- [x] ✅ `linkedin` mutations, `salesNavigator` queries/mutations ([21_LINKEDIN_MODULE.md](21_LINKEDIN_MODULE.md), [23_SALES_NAVIGATOR_MODULE.md](23_SALES_NAVIGATOR_MODULE.md)).
- [ ] 🟡 Extension-origin error envelopes: consistent `extensions.code` for retry vs fatal.
- [ ] ⬜ Observability: trace IDs propagated to `LambdaSalesNavigatorClient` requests (if not already).
- [ ] 📌 Runbook for “SN save partial failure” (Connectra vs SN lambda).

**Small tasks**

1. [ ] 🟡 Map `saveSalesNavigatorProfiles` field errors to [docs/frontend/salesnavigator-ui-bindings.md](../../frontend/salesnavigator-ui-bindings.md).
2. [ ] ⬜ Load test SN batch saves against abuse guard limits.

---

## `5.x.x` — AI workflows

- [x] ✅ `aiChats` and utility AI operations via `LambdaAIClient` → **Contact AI** REST (`backend(dev)/contact.ai`, `/api/v1/…`) — not a separate “Gemini-only” service; inference stack lives in that service ([17_AI_CHATS_MODULE.md](17_AI_CHATS_MODULE.md)).
- [x] ✅ `resume` module + `ResumeAIClient` ([29_RESUME_AI_REST_SERVICE.md](29_RESUME_AI_REST_SERVICE.md)).
- [ ] 🟡 Keep `ModelSelection` / GraphQL enums in sync with Contact AI and HF model IDs.
- [ ] ⬜ Policy hooks: PII redaction, prompt injection handling, and audit logging conventions across AI mutations.
- [ ] ⬜ Contract tests for `LambdaAIClient` request/response shapes vs Contact AI OpenAPI or Postman collection.

**Small tasks**

1. [ ] 🟡 Verify headers (`X-API-Key`, `X-User-ID`) on every chat route match Contact AI enforcement.
2. [ ] ⬜ Document failure modes when Contact AI returns 503 (retry hints for dashboard).

---

## `6.x.x` — Reliability and scaling

- [x] ✅ Query complexity + timeout extensions.
- [x] ✅ Idempotency cache, mutation abuse guard, optional GraphQL rate limit, RED/SLO endpoints.
- [ ] ⬜ Redis (or other) **shared** store for idempotency + abuse counters across replicas.
- [ ] ⬜ Token blacklist scaling strategy (single DB vs replicated cache) documented in [appointment360_data_lineage.md](../database/appointment360_data_lineage.md).
- [ ] 🟡 Tune `GRAPHQL_*` and `MUTATION_ABUSE_GUARD_RPM` per environment with evidence.

**Small tasks**

1. [ ] ⬜ Measure idempotency collision rate and document TTL rationale (`IDEMPOTENCY_TTL_SECONDS`).
2. [ ] 🟡 Add dashboard or log-based SLI for top 10 mutations (latency + error rate).

---

## `7.x.x` — Deployment

- [x] ✅ Mangum/Lambda path, Docker/EC2 compatibility, production `SECRET_KEY` hard fail.
- [ ] 🟡 Expand startup validation beyond `SECRET_KEY` (critical downstream URLs/keys).
- [ ] ⬜ Runbook: rollback, blue/green, and GraphQL schema rollback policy.
- [ ] 📌 Synthetic probe: `/health/db` + one authenticated GraphQL query in staging.

**Small tasks**

1. [ ] ⬜ Checklist item: “all `LAMBDA_*` and `CONNECTRA_*` unset → fail or warn” per environment matrix.
2. [ ] 🟡 Document `ROOT_PATH` / reverse proxy behavior for `/graphql` in deploy docs.

---

## `8.x.x` — Public and private APIs and endpoints

- [ ] 🟡 Internal consumers (app, extension) use full schema; **no** separate public GraphQL version field yet.
- [ ] ⬜ Explicit deprecation policy (sunset headers or field-level `@deprecated` in Strawberry when adopted).
- [ ] 📌 Partner-facing subset schema or persisted queries (if product requires).
- [ ] 📌 Compatibility suite: breaking change detector for `appointment360_endpoint_era_matrix.json` + module docs.

**Small tasks**

1. [ ] ⬜ Inventory which operations are “dashboard-only” vs “extension-public” vs “future partner”.
2. [ ] 📌 Define auth model for machine clients (API keys via [28_PROFILE_MODULE.md](28_PROFILE_MODULE.md)) vs session JWT.

---

## `9.x.x` — Ecosystem integrations and platform productization

- [x] ✅ `notifications`, `savedSearches`, `twoFactor`, `profile`, `pages`, `featureOverview` in schema.
- [ ] 📌 **`webhooks` / `integrations` root namespaces:** not present in `schema.py` today; [06_WEBHOOKS_MODULE.md](06_WEBHOOKS_MODULE.md) and [20_INTEGRATIONS_MODULE.md](20_INTEGRATIONS_MODULE.md) are forward-looking until mounted.
- [ ] 🟡 DocsAI availability and failure behavior for `pages.*` ([19_PAGES_MODULE.md](19_PAGES_MODULE.md)).
- [ ] ⬜ Tenant isolation review for team/profile APIs ([28_PROFILE_MODULE.md](28_PROFILE_MODULE.md)).
- [ ] 📌 Partner SLA and support tooling (outside gateway code; linked from ecosystem task packs).

**Small tasks**

1. [ ] ⬜ Grep `schema.py` vs module doc list; maintain a “schema-mounted vs doc-only” table in [APPOINTMENT360_ERA_TASK_PACKS.md](APPOINTMENT360_ERA_TASK_PACKS.md).
2. [ ] 🟡 When adding `integrations` to schema, add `NN_MODULE.md` and update [README.md](README.md) module list in same PR.

---

## `10.x.x` — Email campaign

- [ ] ⬜ Add `app/clients/campaign_service_client.py` (name TBD) + `Settings` for email campaign REST base URL and API key.
- [ ] ⬜ Implement GraphQL modules under `app/graphql/modules/campaigns|sequences|campaign_templates` (or equivalent) and **mount** on root `Query` / `Mutation` in `schema.py`.
- [ ] ⬜ Align types with Go service contracts ([emailcampaign.api.md](../services.apis/emailcampaign.api.md), [22_CAMPAIGNS_MODULE.md](22_CAMPAIGNS_MODULE.md), [24_SEQUENCES_MODULE.md](24_SEQUENCES_MODULE.md), [25_CAMPAIGN_TEMPLATES_MODULE.md](25_CAMPAIGN_TEMPLATES_MODULE.md)).
- [ ] ⬜ Status vocabulary parity (`pending`, `sending`, `completed`, …) with worker (see [README.md — Email campaign module maintenance requirements](README.md#email-campaign-module-maintenance-requirements)).
- [ ] 📌 Compliance: unsubscribe/suppression semantics exposed consistently through gateway mutations.
- [ ] 📌 Release gates: deliverability SLO signals before marking era complete.

**Small tasks**

1. [ ] ⬜ Spike: single read-only query `campaigns.campaigns(limit,offset)` proxying REST list endpoint.
2. [ ] ⬜ Add `emailcampaign_endpoint_era_matrix.json` entries for any new gateway-exposed operations.
3. [ ] ⬜ Update [appointment360_data_lineage.md](../database/appointment360_data_lineage.md) if gateway persists campaign metadata locally (likely none; mostly proxy).

---

## Cross-era maintenance (always on)

- [ ] 🟡 After any resolver change, update the matching `NN_*_MODULE.md` and [appointment360-codebase-analysis.md](../../codebases/appointment360-codebase-analysis.md) module tables if the public surface changed.
- [ ] ⬜ Keep Postman / endpoint JSON under `docs/backend/endpoints/` consistent with new operations.
- [ ] 🟡 Run module doc drift review quarterly (compare `schema.py` imports to [README.md](README.md) module file list).

---

## Related links

- Codebase analysis: [appointment360-codebase-analysis.md](../../codebases/appointment360-codebase-analysis.md)
- Era doc index: [APPOINTMENT360_ERA_TASK_PACKS.md](APPOINTMENT360_ERA_TASK_PACKS.md)
- Service mesh / cross-service contracts (if used): [00_SERVICE_MESH_CONTRACTS.md](00_SERVICE_MESH_CONTRACTS.md)
