# Documentation retrieval for user billing and credit systems
_Exported on 3/25/2026 at 01:55:27 GMT+5:30 from Cursor (2.6.21)_

---

**User**

Read the following files and return their content (full or first 60 lines each):
1. d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\connectra-user-billing-task-pack.md
2. d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\jobs-user-billing-task-pack.md
3. d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\logsapi-user-billing-credit-task-pack.md
4. d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\s3storage-user-billing-task-pack.md
5. d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\emailapis-user-billing-credit-task-pack.md
6. d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\mailvetter-user-billing-task-pack.md

Also get sections from docs\codebases\appointment360-codebase-analysis.md that reference "1.x" era mapping and billing/credit/user features (search for those terms).

Return raw content.

---

**Cursor**


Reading the six task-pack files and searching the codebase analysis for relevant sections.




Below is the raw content you asked for, plus the matching parts of `appointment360-codebase-analysis.md`.

---

## 1. `d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\connectra-user-billing-task-pack.md` (full)

```markdown
# Connectra user-billing task pack (`1.x`)

## Scope

Align Connectra search/export volume with credit and billing contracts.

## Small tasks

- **Contract:** Define credit-aware search/export usage policy and reject semantics when limits are exhausted.
- **Service:** Add gateway-side guardrails before Connectra-heavy queries and export job creation.
- **Database:** Track usage evidence in usage/ledger tables tied to Connectra query and export actions.
- **Flow:** Trace `/contacts` and `/companies` query events through billing and activity logging paths.
- **Release gate evidence:** Quota tests, over-limit behavior snapshots, and audit trail proof for billing reconciliation.

## Root/Admin surface contributions (era sync)

- **`contact360.io/root`**: user/billing CTAs, pricing and auth-form hooks/services (`usePricing`, `useAuthForm`, billing/auth GraphQL services).
- **`contact360.io/admin`**: payment submission review and admin billing controls (approve/decline flows), user-role governance surfaces.

---

## Extension surface contributions (era sync)

### Era 1.x — User/Billing/Credit

**`extension/contact360` auth layer:**
- `auth/graphqlSession.js` — `getValidAccessToken()` and `refreshAccessToken()` fully implemented
- Token lifecycle: `accessToken` + `refreshToken` stored in `chrome.storage.local` only
- `auth.refreshToken` GraphQL mutation on Appointment360 established as the extension auth contract
- `isTokenExpired()` with 300-second buffer prevents mid-scrape token expiry

**Tasks:**
- 🔴 Incompleted: Confirm Appointment360 `auth.refreshToken` mutation returns `{ accessToken, refreshToken, expiresIn }`
- 🔴 Incompleted: Verify `chrome.storage.local` token keys (`accessToken`, `refreshToken`) are consistent with any future auth refactor
- 🔴 Incompleted: Document token security policy (no logging, no sync storage, no third-party transmission) in governance
```

---

## 2. `d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\jobs-user-billing-task-pack.md` (full)

```markdown
# jobs task pack — era 1.x

This pack decomposes `contact360.io/jobs` work into Contract, Service, Surface, Data, and Ops tracks.

## Contract tasks
- Define credit-aware job creation payload expectations.
- Define billing/audit semantics for retry and cancellation events.

## Service tasks
- Attach billing context to job metadata when applicable.
- Validate access checks between owner/admin and retry controls.

## Surface tasks
- Add billing-aware retry UX states and credit warning patterns.
- Document job ownership and role-gated action visibility.

## Data tasks
- Ensure `job_events` carries credit/billing trace context.
- Document correlation between job IDs and usage/billing records.

## Ops tasks
- Add billing-impact alerts for job failure spikes.
- Add release checklist for billing-flow regression checks.
```

---

## 3. `d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\logsapi-user-billing-credit-task-pack.md` (full)

```markdown
# logs.api task pack — era 1.x

This pack decomposes `lambda/logs.api` work into Contract, Service, Surface, Data, and Ops tracks.

## Contract tasks
- Define and freeze era `1.x` logging schema additions and compatibility notes.
- Update endpoint/reference matrix in `docs/backend/endpoints/logsapi_endpoint_era_matrix.json`.

## Service tasks
- Implement/validate service behavior for era `1.x` event sources and query expectations.
- Verify auth, error envelope, and health behavior for consuming services.

## Surface tasks
- Document impacted pages/tabs/buttons/inputs/components for era `1.x`.
- Document relevant hooks/services/contexts and UX states (loading/error/progress/check/radio).

## Data tasks
- Document S3 CSV storage and lineage impact for era `1.x`.
- Record retention, trace IDs, and query-window expectations.

## Ops tasks
- Add observability checks and release validation evidence for era `1.x`.
- Capture rollback and incident-runbook notes for logging-impacting releases.
```

---

## 4. `d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\s3storage-user-billing-task-pack.md` (full)

```markdown
# `s3storage` Task Pack - Era `1.x.x`

## Scope
- User artifacts and billing-proof related storage paths
- Validation policy for object classes

## Small tasks
- Contract:
  - define object-class policy contract (`avatar`, `photo`, `resume`, `upload`)
  - define max size/content-type rules per object class
- Service:
  - enforce path-specific validation at upload endpoints
  - add retry-safe semantics for overwrite/delete flows
- Database/Data lineage:
  - store actor/source metadata for compliance and audit trails
- Flow/Graph:
  - billing proof flow: upload proof -> approval workflow linkage
  - profile avatar flow: upload/replace/read URL
- Release gate evidence:
  - validation matrix pass (allowed vs blocked types)
  - audit field presence checks
```

---

## 5. `d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\emailapis-user-billing-credit-task-pack.md` (full)

```markdown
# emailapis task pack — era 1.x

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

*(File on disk literally contains `$(System.Collections.Hashtable.era)` where era `1.x` was likely intended.)*

---

## 6. `d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\mailvetter-user-billing-task-pack.md` (full)

```markdown
# Mailvetter — 1.x User/Billing/Credit Task Pack

**Service:** `backend(dev)/mailvetter`  
**Era:** `1.x` — User, billing, and credit alignment

## Contract track

- 🔴 Incompleted: Define plan-tier contract (`free`, `pro`, `enterprise`) for rate, bulk, and concurrent jobs.
- 🔴 Incompleted: Define API key ownership contract (`owner_id`, `tenant_id`, `plan`).
- 🔴 Incompleted: Define credit-consumption events for single and bulk validation.

## Service track

- 🔴 Incompleted: Replace env-only single key fallback with DB-backed key management.
- 🔴 Incompleted: Add key scope checks (read-only vs bulk-write permissions).
- 🔴 Incompleted: Attach `owner_id` and `tenant_id` to jobs at creation time.
- 🔴 Incompleted: Emit usage events on each request for billing reconciliation.

## Surface track

- 🔴 Incompleted: Dashboard usage widgets map verifier usage per plan and remaining limits.
- 🔴 Incompleted: Add error messaging for `RATE_LIMIT_EXCEEDED`, `BULK_SIZE_EXCEEDED`, `CONCURRENT_JOB_LIMIT`.

## Data track

- 🔴 Incompleted: Add `api_keys` table (hashed key, owner, plan, active, rotated_at).
- 🔴 Incompleted: Add `usage_logs` table for hourly/daily aggregation.
- 🔴 Incompleted: Add `credit_events` table for billable operations.

## Ops track

- 🔴 Incompleted: Add key rotation runbook and secret separation policy.
- 🔴 Incompleted: Add plan enforcement tests across all three tiers.
- 🔴 Incompleted: Add billing parity checks against appointment360 usage records.
```

---

## 7. `d:\code\ayan\contact\docs\codebases\appointment360-codebase-analysis.md` — sections touching `1.x` mapping and user/billing/credit/usage

**Purpose (gateway + credits/billing/users):**

```markdown
## Purpose and role

`contact360.io/api` (Appointment360) is Contact360's **primary GraphQL gateway and orchestrator**. It is the only entry point through which the dashboard (`contact360.io/app`) and extension reach all backend capability. It translates GraphQL operations into downstream REST calls to Connectra, tkdjob, lambda email, S3 storage, DocsAI, contact.ai, and logs.api. All user authentication, credit deduction, activity logging, usage tracking, and entitlement enforcement pass through this service.
```

**Schema lines including `users`, `usage`, `billing`:**

```markdown
query { auth | users | contacts | companies | email | jobs | usage | billing | analytics | activities | health | pages | s3 | upload | aiChats | notifications | salesNavigator | admin | savedSearches | twoFactor | profile | resume | featureOverview }
mutation { auth | users | contacts | companies | billing | linkedin | jobs | email | usage | upload | s3 | analytics | aiChats | notifications | salesNavigator | admin | savedSearches | twoFactor | profile | resume }
```

**Context (`user`):**

```markdown
### Context (`app/graphql/context.py`)

Per-request `Context` carries:
- `db`: `AsyncSession` (from async generator, committed by `DatabaseCommitMiddleware`)
- `user`: `User | None` extracted from Bearer JWT
- `user_uuid`: `str | None`
- `dataloaders`: `DataLoaders` (per-request N+1 prevention)
```

**Query modules — `usage`, `billing`, `users`, `admin`:**

```markdown
| users | `UserQuery` | `user(uuid)`, `users()`, `userStats()` |
...
| usage | `UsageQuery` | `usage(feature)` |
...
| billing | `BillingQuery` | `billingInfo`, `plans`, `invoices` |
...
| admin | `AdminQuery` | `adminStats()`, `paymentSubmissions()`, `users()` |
```

**Mutation modules — `billing`, `usage`, `admin` (credits):**

```markdown
| billing | `BillingMutation` | `subscribe`, `purchaseAddon`, `submitPaymentProof`, `approvePayment`, `declinePayment` |
...
| usage | `UsageMutation` | `trackUsage`, `resetUsage` |
...
| admin | `AdminMutation` | `creditUser`, `adjustCredits`, `approvePayment`, `declinePayment` |
```

**Middleware — billing/payment idempotency:**

```markdown
| 7 | `GraphQLIdempotencyMiddleware` | Cache and replay `X-Idempotency-Key` mutations (billing/payment guards) |
```

**Era mapping row for `1.x`:**

```markdown
## Era mapping (`0.x`–`10.x`)

| Era | Appointment360 concern |
| --- | --- |
| `0.x` | Service bootstrap, middleware baseline, context/session lifecycle, schema layout |
| `1.x` | Auth mutations (login/register/refresh/logout), credit deduction, billing module, usage tracking |
| `2.x` | Email module (finder/verifier), jobs orchestration module, activity logging |
```

**File map — services layer:**

```markdown
| `app/services/` | Business logic: billing, usage, credit, activity, pages, notification |
| `app/repositories/` | Data access: user, profile, scheduler_job, token_blacklist, saved_search |
```

---

**Note:** The analysis doc also mentions optional Redis / user cache (`TTLCache for user objects`, `ENABLE_USER_CACHE`, `USER_CACHE_TTL`) in the stack and config tables; those lines match “user” in search but are operational, not product “user/billing” features. The blocks above are the ones that directly describe auth, billing, usage, credits, and the `1.x` era row.

