# 1.x.x era documentation extraction
_Exported on 3/25/2026 at 01:55:39 GMT+5:30 from Cursor (2.6.21)_

---

**User**

Read the following files and return content relevant to 1.x.x era (billing, user, credit system):
1. d:\code\ayan\contact\docs\versions.md - search for "1.0", "1.1", "1.2", "1.3", "1.4" entries and the general 1.x plan
2. d:\code\ayan\contact\docs\roadmap.md - search for "1.x" era sections (user, billing, credits)
3. d:\code\ayan\contact\docs\governance.md - search for "1.x" code maps

Return just the relevant sections for 1.x era including: status, scope, dependencies, KPIs, stage summaries.

---

**Cursor**


Searching the three docs for 1.x-era content on billing, users, and credits.




Here is a consolidated extract for the **1.x era** (user, billing, credits) from the three files. Paths are absolute.

---

## `d:\code\ayan\contact\docs\versions.md`

**Planning / horizon**

- Near-term execution is **`1.x`–`6.x`**; foundation `0.x` exits before `1.x` pressure (`0.10` is the foundation exit gate).

**Release index (1.x-related)**

| Version | Status | Summary |
|--------|--------|---------|
| `1.0.0` | released | Contact360 MVP — auth, credits, email core |
| `1.1.0` | in_progress | Bulk + billing maturity |
| `1.2.0` | planned | Analytics, notifications, admin, security baseline |

**Unreleased next cut**

- **Target:** `1.1.0` — **in_progress**  
- **Summary:** Bulk validation hardening + billing flow operationalization  
- **Planned stage mapping:** `1.3` (billing), `2.4` (bulk)  
- **Owner:** Product + Platform Engineering  

**`1.0.0`**

- **Status:** released  
- **Scope:** Authentication, credits core behavior, email finder/verifier/results  
- **Roadmap mapping:** `1.1`, `1.2`, `2.1`, `2.2`, `2.3`  
- **Reference:** roadmap Stage 1.1  

**`1.1.0`**

- **Status:** in_progress  
- **Scope:** CSV bulk hardening; payment/credit-pack processing improvements  
- **Roadmap mapping:** `1.3`, `2.4`  
- **Reference:** roadmap Stage 1.3  

**`1.2.0`**

- **Status:** planned (post-`1.1.0`)  
- **Scope:** User analytics view, notifications, admin control panel, baseline security  
- **Roadmap mapping:** `1.4`, `1.5`, `1.6`, `1.7`  
- **Reference:** roadmap Stage 1.4  

**`1.x` task-pack pattern (user, billing, credit)**

- **Contract:** user/credit/billing GraphQL schema changes  
- **Service:** auth/session, credit deduction, billing mutation, analytics query updates  
- **Surface:** dashboard auth, credit display, billing UX, notifications  
- **Data/Ops:** credit ledger consistency, billing observability, fraud/abuse  

**Cross-service `1.x` hooks (selected)**

- **s3storage:** user artifact policy (avatar/photo/proof/resume) + validation; task pack → `docs\1. Contact360 user and billing and credit system\s3storage-user-billing-task-pack.md`  
- **logs.api:** auth/billing/credit event schema and lineage  
- **connectra:** credit-aware volume guards, billing event linkage (depends on billing/credit system)  
- **emailapis:** credit-aware finder/verifier contract alignment  
- **jobs:** billing/credit-aware creation and retry audit  
- **contact.ai:** `user_id` FK integrity; user-deletion cascade; IAM hardening  
- **email campaign:** JWT validation; credit pre-check on `/campaign`; `user_id`/`org_id` on campaigns  
- **salesnavigator:** actor context, billing stub  
- **Appointment360 (`contact360.io/api`):** auth mutations; billing/usage module; credit deduction; idempotency on billing  
- **mailvetter:** API key ownership + plan/rate governance aligned with billing/credits  
- **Email app (`contact360.io/email`):** auth + profile/account surface live  

---

## `d:\code\ayan\contact\docs\roadmap.md`

**Current focus**

- Centered on **Stage 1.3 (billing/payments)** and **Stage 2.4 (bulk)**.  
- Near-term horizon: **`1.x`–`6.x`**.

### VERSION 1.x — User, Billing and Credit System

| Stage | Status | Depends on | Risk (short) | Definition of done | KPI | Ships in |
|-------|--------|------------|--------------|-------------------|-----|----------|
| **1.1** User & auth | Completed | Foundation | Session regressions | Register, sign in, start with starter credits | Signup→first-action conversion; auth failure rate | `1.0.0` |
| **1.2** Credit management (CORE) | Completed | 1.1 | Wrong deduction/lapse blocks users | Finder deductions + entitlement checks correct | Ledger consistency; zero-balance block correctness | `1.0.0` |
| **1.3** Billing & payments | In progress | 1.1, 1.2 | Payment/credit mismatch or delay | Purchase packs + credits via approved flow | Success-to-crediting time; failed payment rate | `1.1.0` |
| **1.4** User analytics (minimal) | Planned | 1.2, 1.3 | Usage vs billing/credit mismatch | Basic usage + entitlement summary | Analytics adoption; usage ledger consistency | `1.2.0` |
| **1.5** Notifications (minimal) | Planned | 1.3, 1.4 | False/late notifications | Low-credit + payment-success cues reliable | Notification correctness; low-credit conversion | `1.2.0` |
| **1.6** Admin analytics/control | Planned | 1.2, 1.4 | Admin actions without audit clarity | Audit/adjust user credit/package state | Correction turnaround; audit completeness | `1.2.0` |
| **1.7** Security (basic) | Planned | 1.1 + middleware rollout | Abuse/spam volume | Baseline throttling/abuse on core APIs | Rate-limited abuse; API error stability | `1.2.0` |

**Stage content highlights**

- **1.1:** Email signup/login, profile, **50 credits on signup**, sessions. Code: `RoleContext.tsx`, `main.py`.  
- **1.2:** Balance, **finder-only deduction** (verifier 0 credits per current policy), free credits, basic usage logs, block at 0, lapse when pack ends. Code: `09_USAGE_MODULE.md`, `15_EMAIL_MODULE.md`, `featureAccess.ts`.  
- **1.3:** Credit purchase, 2–3 MVP plans, manual payment, credit packs (no subscription). Code: `billingService.ts`, `UpiPaymentModal.tsx`, `14_BILLING_MODULE.md`.  
- **1.4–1.7:** Usage ledger, package/expiry; low-credit UI + payment success (no email automation in v1); admin views + manual credit adjust; basic rate limiting.

**Feature-to-service matrix (1.x rows)**

- 1.1 → `appointment360` / dashboard (+ extension) / PostgreSQL / `1.0.0`  
- 1.2 → same / `1.0.0`  
- 1.3 → same / `1.1.0`  
- 1.4 → `appointment360`, `logs.api` / dashboard / PostgreSQL, S3 (CSV) / `1.2.0`  
- 1.5–1.7 → as in table (1.6 includes DocsAI, `logs.api`)  

**Deep execution: `1.x` → `2.x` (billing-related)**

- **1.3:** Credit pack purchase mutations, payment state machine, payment-proof + admin approval.  
- **1.4–1.7:** Usage + credit ledger UI, low-credit warning, payment success notification, DocsAI admin credit/package management, GraphQL rate-limit middleware.  
- **2.1:** Validate credit deduction per finder call.  

**Cross-era streams (1.x snippets)**

- **s3storage `1.x`:** object policies for avatar/photo/proof/resume; validation; actor/source fields; upload abuse monitoring.  
- **logs.api `1.x`:** user, auth, billing, credit operational event lineage.  
- **jobs `1.x`:** billing/credit-aware job governance and ownership checks.  
- **contact.ai `1.x`:** `user_id` FK, deletion cascade, IAM.  
- **salesnavigator `1.x`:** `X-User-ID` / `X-Org-ID`, billing event stub, secret rotation.  
- **mailvetter `1.x`:** API key ownership + plan limits aligned with billing/credits.  
- **Email app:** `1.x` = auth + profile/account live.  

---

## `d:\code\ayan\contact\docs\governance.md`

**Era row**

- **`1.x.x`:** Contact360 user, billing, and credit system (version era summary table).

**Code map explicitly labeled for 1.x stages**

`governance.md` only defines a **dedicated stage table for 1.4–1.7** (not 1.1–1.3):

| Stage | Intent | Primary locations |
|-------|--------|-------------------|
| **1.4** User analytics | Usage ledger, limits, activity | `contact360.io/app/app/(dashboard)/usage/page.tsx`, `useUsage.ts`, `usageService.ts`, API `usage` GraphQL module |
| **1.5** Notifications | Low-credit UI, payment feedback | `CreditBudgetAlerts.tsx` (via `MainLayout.tsx`), `UpiPaymentModal.tsx` success toast |
| **1.6** Admin | Credits, packages, payment review | `contact360.io/admin/` — `admin_client.py` (`list_payment_submissions`, `approve_payment_submission`), GraphQL `approvePayment` / `declinePayment` |
| **1.7** Security | GraphQL rate limit | `middleware.py` (`GraphQLRateLimitMiddleware`), config when `GRAPHQL_RATE_LIMIT_REQUESTS_PER_MINUTE` > 0 |

**Related (email gateway + credits, under roadmap 2.1–2.3 map)**

- **Gateway + credits (1 per finder):** `contact360.io/api/app/graphql/modules/email/queries.py`, `app/services/credit_service.py`

---

**Note:** There is **no separate `1.3` code map** in `governance.md`; billing code pointers live in **roadmap Stage 1.3** (`billingService.ts`, `UpiPaymentModal.tsx`, `14_BILLING_MODULE.md`). Stages **1.1–1.2** are documented in the roadmap with status/KPIs/dependencies but not in a governance “code map” table.

