# Era-mapping and execution queue analysis
_Exported on 3/25/2026 at 01:52:46 GMT+5:30 from Cursor (2.6.21)_

---

**User**

Read these files and return their era-mapping and immediate execution queue sections (lines 60+ typically):
1. d:\code\ayan\contact\docs\codebases\emailapis-codebase-analysis.md
2. d:\code\ayan\contact\docs\codebases\mailvetter-codebase-analysis.md
3. d:\code\ayan\contact\docs\codebases\email-codebase-analysis.md

Focus on: "2.x" era rows in any era-mapping tables, gaps/risks relevant to the email system, immediate execution queue items.
Return the relevant sections.

---

**Cursor**


Reading the three analysis files and extracting era-mapping (including 2.x rows), gaps/risks, and immediate execution queue sections.




Here are the sections you asked for, with notes where a file uses a different structure than an “era table + immediate execution queue.”

---

## 1. `d:\code\ayan\contact\docs\codebases\emailapis-codebase-analysis.md`

This doc has **no** separate “Era mapping” table or “Immediate execution queue” heading. The closest material is **cross-service risks** and the **2.x** block inside **Era-by-era task packs**.

### Key findings and cross-service risks (email-relevant)

```62:68:d:\code\ayan\contact\docs\codebases\emailapis-codebase-analysis.md
## Key findings and cross-service risks

1. Provider drift risk: Python/docs often reference `truelist`; Go runtime prioritizes `mailvetter`.
2. Status semantic drift risk: `valid`/`invalid`/`catchall`/`unknown` interpretation can differ across app, api, and runtime mapping.
3. Observability gap: correlation across app -> api -> jobs -> lambda is not consistently documented with one trace contract.
4. Contract drift risk: endpoint and payload assumptions in docs may lag runtime changes.
5. Bulk correctness risk: partial-batch error mapping and retry semantics require explicit cross-layer contract tests.
```

### 2.x era row (from era-by-era task packs)

```86:91:d:\code\ayan\contact\docs\codebases\emailapis-codebase-analysis.md
### 2.x Email system
- Contract: unify provider naming and status semantics for finder/verifier.
- Service: harden bulk fanout, verification race, and fallback behavior.
- Surface: lock Finder/Verifier tabs, mapping modals, progress UX contract.
- Data: enforce cache/pattern lineage quality and mutation evidence.
- Ops: baseline bulk latency/failure dashboards and RC criteria.
```

---

## 2. `d:\code\ayan\contact\docs\codebases\mailvetter-codebase-analysis.md`

### Gaps and risks

```133:143:d:\code\ayan\contact\docs\codebases\mailvetter-codebase-analysis.md
## Gaps and risks

| Risk | Severity | Notes |
| --- | --- | --- |
| V1 + legacy dual API surface | High | Contract drift risk and duplicated behavior |
| In-memory rate limiter | High | Not distributed-safe across replicas |
| Runtime migrations in app startup | Medium | Operational risk in production rollouts |
| Shared secret fallback for webhook signing | Medium | `WEBHOOK_SECRET_KEY` falls back to `API_SECRET_KEY` |
| Old docs naming drift (`Mailvaiter` vs `Mailvetter`) | Medium | Branding/contract confusion across docs |
| Legacy static UI tied to old endpoints | Medium | `/upload` and `/status` legacy route dependence |
| No explicit multi-tenant keys model | Medium | Plan/owner key currently coarse-grained |
```

### Era mapping (`0.x`–`10.x`) — including **2.x**

```147:161:d:\code\ayan\contact\docs\codebases\mailvetter-codebase-analysis.md
## Era mapping (`0.x`-`10.x`)

| Era | Mailvetter concern |
| --- | --- |
| `0.x` | Service bootstrap, API/worker split, Redis+Postgres plumbing |
| `1.x` | API key ownership, plan/rate controls, usage and credit linkage |
| `2.x` | Core verifier contract and bulk job lifecycle (primary era) |
| `3.x` | Contact/company-linked verification lineage |
| `4.x` | Extension/SalesNav ingestion provenance and anti-abuse controls |
| `5.x` | AI-consumable explainability payloads |
| `6.x` | Reliability hardening: idempotency, distributed limiter, SLOs |
| `7.x` | Deployment hardening, migration discipline, runbooks |
| `8.x` | Public/private API formalization, scoped keys, OpenAPI |
| `9.x` | Webhook ecosystem contracts and partner-grade observability |
| `10.x` | Campaign preflight and recipient-level verification orchestration |
```

### Immediate execution queue

```165:173:d:\code\ayan\contact\docs\codebases\mailvetter-codebase-analysis.md
## Immediate execution queue

1. Freeze/deprecate legacy endpoints and keep v1 as canonical API contract.
2. Replace in-memory rate limiter with Redis-backed distributed limiter.
3. Split migrations into explicit migration pipeline (not runtime app startup).
4. Separate webhook secret from API secret (no fallback coupling).
5. Add idempotency keys for bulk job create endpoint.
6. Add status vocabulary hardening (`pending/processing/completed/failed`) and explicit failure paths.
7. Add endpoint parity tests between docs and runtime for all v1 routes.
```

---

## 3. `d:\code\ayan\contact\docs\codebases\email-codebase-analysis.md`

There is **no** section titled “Immediate execution queue”; the parallel content is **Task decomposition** (below). Email-related risk is also called out under **Security and compliance notes**.

### Security / risk (email / IMAP)

```97:100:d:\code\ayan\contact\docs\codebases\email-codebase-analysis.md
## Security and compliance notes

- Email HTML is sanitized with DOMPurify before render in email detail page.
- Current runtime passes IMAP credentials via custom headers (`X-Email`, `X-Password`) and persists account blob in localStorage; this is a high-risk pattern and should move to tokenized backend session abstraction.
```

### Era alignment (0.x – 10.x) — including **2.x**

```102:116:d:\code\ayan\contact\docs\codebases\email-codebase-analysis.md
## Era alignment (0.x – 10.x)

| Era | Email app contribution |
| --- | --- |
| 0.x | App scaffold, route shell, theme/layout primitives |
| 1.x | Login/signup/profile/account flows |
| 2.x | Core mailbox functionality (folders, detail, IMAP connect) |
| 3.x | Limited; preparatory base for contact/company linkage |
| 4.x | Potential extension ingest inbox tie-ins (not active yet) |
| 5.x | AI nav placeholder; no active AI pipeline in this app yet |
| 6.x | Basic resilience (loading/error states), no retry/observability layer yet |
| 7.x | Standard Next build/deploy scripts |
| 8.x | Private REST endpoint consumption contract |
| 9.x | Ecosystem integration hooks are minimal currently |
| 10.x | Campaign handoff opportunity (not implemented in this app yet) |
```

### Immediate execution queue equivalent — **Task decomposition**

```118:135:d:\code\ayan\contact\docs\codebases\email-codebase-analysis.md
## Task decomposition

1. **Security hardening**
   - Remove IMAP password persistence from localStorage.
   - Replace `X-Password` usage with backend-issued mailbox session token.
2. **Service abstraction**
   - Introduce typed API client modules for auth, mailbox, and account.
3. **UX completion**
   - Wire table search input to actual filter state.
   - Implement flagged tab behavior.
   - Implement compose and send flow.
4. **Reliability improvements**
   - Add retry/backoff for mailbox fetches.
   - Add normalized error boundaries/toasts.
5. **Analytics and charts**
   - Reuse `ui/chart.tsx` for mailbox metrics surfaces.
6. **Era linkage docs**
   - Keep this file and era task packs synchronized for 0.x-10.x traceability.
```

---

### Cross-cutting gaps for the **email system** (from these three)

| Source | Theme |
|--------|--------|
| **emailapis** | Provider naming (`truelist` vs `mailvetter`), status semantics drift, tracing across layers, doc/runtime contract drift, bulk partial-batch semantics |
| **mailvetter** | Legacy vs V1 API, non-distributed rate limits, startup migrations, webhook/API secret coupling, multi-tenant keys |
| **email app** | IMAP secrets in headers + `localStorage`; missing retries/observability; several UX flows incomplete (search, flagged tab, compose/send) |

**2.x** in the tables: **emailapis** treats 2.x as the “Email system” task pack; **mailvetter** marks 2.x as core verifier + bulk jobs; **email** marks 2.x as core mailbox (folders, detail, IMAP).

