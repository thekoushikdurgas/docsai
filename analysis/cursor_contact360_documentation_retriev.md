# Contact360 documentation retrieval
_Exported on 3/25/2026 at 01:55:18 GMT+5:30 from Cursor (2.6.21)_

---

**User**

Read the following files and return their content (first 60 lines each or full if short):
1. d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\README.md
2. d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\1.0 — User Genesis.md (first 80 lines)
3. d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\1.1 — Billing Maturity.md (first 80 lines)
4. d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\1.3 — Payment Gateway.md (first 80 lines)
5. d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\1.4 — Usage Ledger.md (first 80 lines)
6. d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\appointment360-user-billing-task-pack.md (first 60 lines)

Also list all files in: d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\

Return the raw content for each.

---

**Cursor**


Reading the requested files and listing the directory.




Here are the **raw contents** and the **directory listing**. `README.md` is shorter than 60 lines, so it is included in full.

---

### 1. `d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\README.md` (full — 23 lines)

```markdown
# 1. Contact360 user and billing and credit system

## Era theme
- See `docs/version-policy.md` and `docs/versions.md` for canonical theme and release mapping for `1.x`.

## Service task-pack files
- `appointment360-user-billing-task-pack.md`
- `connectra-user-billing-task-pack.md`
- `contact-ai-user-billing-task-pack.md`
- `emailapis-user-billing-credit-task-pack.md`
- `emailcampaign-user-billing-task-pack.md`
- `jobs-user-billing-task-pack.md`
- `logsapi-user-billing-credit-task-pack.md`
- `mailvetter-user-billing-task-pack.md`
- `s3storage-user-billing-task-pack.md`
- `salesnavigator-user-billing-task-pack.md`

## Operational and supporting docs
- No additional operational docs in this era folder.

## Version notes
- Version detail files are stored as `version_<major>.<minor>.md` in this folder and indexed from `docs/versions.md`.
```

---

### 2. `d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\1.0 — User Genesis.md` (first 80 lines)

```markdown
# Version 1.0

- **Status:** released
- **Released on:** active MVP baseline
- **Summary:** Core Contact360 user journey from signup to finder/verifier/results. Cross-service execution pack for this minor across contract, service, surface, data, and ops.
- **Scope:** Authentication, credits core behavior, finder/verifier engines, and results experience.
- **Roadmap mapping:** `1.1`, `1.2`, `1.4`, `1.5`, `1.6`
- **Owner:** Product + Core Engineering

## Scope

- Target minor: `1.0.0` aligned to current roadmap mapping in this file.
- In scope: contract, service, surface, data, and ops tasks across core Contact360 services.
- Primary owners: API, App, Jobs, Sync, Admin, and supporting platform services.
- Exclusions: work outside this minor unless required for compatibility or incident risk reduction.
- Output: actionable per-service task breakdown and execution queue for release readiness.

## Flowchart

Delivery work for this minor follows the five-track model (contract, service, surface, data, ops) through a release gate.

```mermaid
flowchart TD
    stageNode["1.0.0 — MVP signup through finder, verifier, and results"]
    contract["Contract"]
    service["Service"]
    surface["Surface"]
    data["Data"]
    ops["Ops"]
    releaseGate["Release gate"]

    stageNode --> contract
    stageNode --> service
    stageNode --> surface
    stageNode --> data
    stageNode --> ops
    contract --> releaseGate
    service --> releaseGate
    surface --> releaseGate
    data --> releaseGate
    ops --> releaseGate
```

### Runtime focus (unique to this minor)

```mermaid
flowchart LR
    intake["v1.0 bulk finder pipeline"]
    orchestrate["Email orchestration"]
    verify["Provider verify + score"]
    persist["Contracts and lineage"]
    releasegate["Minor release gate"]

    intake --> orchestrate --> verify --> persist --> releasegate
    orchestrate --> audittrail["Ops and audit signals"]
    verify --> feedback["P0 bug burn-down feedback loop"]
    persist --> stabilize["status truth table freeze stabilization"]
    audittrail --> stabilize
    feedback --> releasegate
    stabilize --> releasegate
```

See also: [`docs/flowchart.md`](../flowchart.md) for system-wide and master views.


## Task tracks

### Contract
- 🔴 Incompleted: **api**: define v1.0 contract outcomes for bulk finder pipeline; harden request/response schema boundaries in `contact360.io/api` while advancing P0 bug burn-down.
- 🔴 Incompleted: **app**: define v1.0 contract outcomes for bulk finder pipeline; align UI payload contracts with backend enums in `contact360.io/app` while advancing P0 bug burn-down.
- 🔴 Incompleted: **jobs**: define v1.0 contract outcomes for bulk finder pipeline; lock worker message schema and retry metadata in `contact360.io/jobs` while advancing status truth table freeze.
- 🔴 Incompleted: **sync**: define v1.0 contract outcomes for bulk finder pipeline; stabilize sync payload mapping and delta semantics in `contact360.io/sync` while advancing P0 bug burn-down.
- 🔴 Incompleted: **admin**: define v1.0 contract outcomes for bulk finder pipeline; formalize control-plane request contracts and guardrails in `contact360.io/admin` while advancing bulk finder pipeline.
- 🔴 Incompleted: **mailvetter**: define v1.0 contract outcomes for bulk finder pipeline; pin verifier payload expectations and score fields in `backend(dev)/mailvetter` while advancing bulk finder pipeline.
- 🔴 Incompleted: **emailapis**: define v1.0 contract outcomes for bulk finder pipeline; normalize provider adapter contract and fallback keys in `lambda/emailapis` while advancing status truth table freeze.
- 🔴 Incompleted: **emailapigo**: define v1.0 contract outcomes for bulk finder pipeline; enforce Go adapter contract parity with shared models in `lambda/emailapigo` while advancing bulk finder pipeline.

### Service
- 🔴 Incompleted: **api**: deliver v1.0 service outcomes for bulk finder pipeline; implement strict handler guards and deterministic branching in `contact360.io/api` while advancing P0 bug burn-down.
- 🔴 Incompleted: **app**: deliver v1.0 service outcomes for bulk finder pipeline; wire client flows to canonical endpoints and failure states in `contact360.io/app` while advancing P0 bug burn-down.
```

(File continues after line 80.)

---

### 3. `d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\1.1 — Billing Maturity.md` (first 80 lines)

```markdown
# Version 1.1

- **Status:** in_progress
- **Target window:** current delivery cycle
- **Summary:** Bulk processing and billing flow readiness. Cross-service execution pack for this minor across contract, service, surface, data, and ops.
- **Scope:** CSV bulk operations hardening and payment/credit-pack processing improvements.
- **Roadmap mapping:** `1.8`, `1.10`
- **Owner:** Product + Payments/Data Pipeline teams

## Scope

- Target minor: `1.1.0` aligned to current roadmap mapping in this file.
- In scope: contract, service, surface, data, and ops tasks across core Contact360 services.
- Primary owners: API, App, Jobs, Sync, Admin, and supporting platform services.
- Exclusions: work outside this minor unless required for compatibility or incident risk reduction.
- Output: actionable per-service task breakdown and execution queue for release readiness.

## Flowchart

Delivery work for this minor follows the five-track model (contract, service, surface, data, ops) through a release gate.

```mermaid
flowchart TD
    stageNode["1.1.0 — Bulk CSV jobs and billing readiness (stages 1.8, 1.10)"]
    contract["Contract"]
    service["Service"]
    surface["Surface"]
    data["Data"]
    ops["Ops"]
    releaseGate["Release gate"]

    stageNode --> contract
    stageNode --> service
    stageNode --> surface
    stageNode --> data
    stageNode --> ops
    contract --> releaseGate
    service --> releaseGate
    surface --> releaseGate
    data --> releaseGate
    ops --> releaseGate
```

### Runtime focus (unique to this minor)

```mermaid
flowchart LR
    intake["v1.1 P0 bug burn-down"]
    orchestrate["Email orchestration"]
    verify["Provider verify + score"]
    persist["Contracts and lineage"]
    releasegate["Minor release gate"]

    intake --> orchestrate --> verify --> persist --> releasegate
    orchestrate --> audittrail["Ops and audit signals"]
    verify --> feedback["status truth table freeze feedback loop"]
    persist --> stabilize["CSV queue correctness stabilization"]
    audittrail --> stabilize
    feedback --> releasegate
    stabilize --> releasegate
```

See also: [`docs/flowchart.md`](../flowchart.md) for system-wide and master views.


## Task tracks

### Contract
- 🔴 Incompleted: **api**: define v1.1 contract outcomes for P0 bug burn-down; harden request/response schema boundaries in `contact360.io/api` while advancing status truth table freeze.
- 🔴 Incompleted: **app**: define v1.1 contract outcomes for P0 bug burn-down; align UI payload contracts with backend enums in `contact360.io/app` while advancing status truth table freeze.
- 🔴 Incompleted: **jobs**: define v1.1 contract outcomes for P0 bug burn-down; lock worker message schema and retry metadata in `contact360.io/jobs` while advancing CSV queue correctness.
- 🔴 Incompleted: **sync**: define v1.1 contract outcomes for P0 bug burn-down; stabilize sync payload mapping and delta semantics in `contact360.io/sync` while advancing status truth table freeze.
- 🔴 Incompleted: **admin**: define v1.1 contract outcomes for P0 bug burn-down; formalize control-plane request contracts and guardrails in `contact360.io/admin` while advancing P0 bug burn-down.
- 🔴 Incompleted: **mailvetter**: define v1.1 contract outcomes for P0 bug burn-down; pin verifier payload expectations and score fields in `backend(dev)/mailvetter` while advancing P0 bug burn-down.
- 🔴 Incompleted: **emailapis**: define v1.1 contract outcomes for P0 bug burn-down; normalize provider adapter contract and fallback keys in `lambda/emailapis` while advancing CSV queue correctness.
- 🔴 Incompleted: **emailapigo**: define v1.1 contract outcomes for P0 bug burn-down; enforce Go adapter contract parity with shared models in `lambda/emailapigo` while advancing P0 bug burn-down.

### Service
- 🔴 Incompleted: **api**: deliver v1.1 service outcomes for P0 bug burn-down; implement strict handler guards and deterministic branching in `contact360.io/api` while advancing status truth table freeze.
- 🔴 Incompleted: **app**: deliver v1.1 service outcomes for P0 bug burn-down; wire client flows to canonical endpoints and failure states in `contact360.io/app` while advancing status truth table freeze.
```

(File continues after line 80.)

---

### 4. `d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\1.3 — Payment Gateway.md` (first 80 lines)

```markdown
# Version 1.3

- **Status:** planned
- **Era:** 1.x (Contact360 MVP core)
- **Summary:** Sub-minor within the 1.x era. Stage **1.3** is intentionally omitted in v1 numbering (reserved historically). Scope is defined when a planned stage is approved and the entry is added to `docs/versions.md`. Cross-service execution pack for this minor across contract, service, surface, data, and ops.

## Scope

- Target minor: `1.3.0` aligned to current roadmap mapping in this file.
- In scope: contract, service, surface, data, and ops tasks across core Contact360 services.
- Primary owners: API, App, Jobs, Sync, Admin, and supporting platform services.
- Exclusions: work outside this minor unless required for compatibility or incident risk reduction.
- Output: actionable per-service task breakdown and execution queue for release readiness.

## Flowchart

Delivery work for this minor follows the five-track model (contract, service, surface, data, ops) through a release gate.

```mermaid
flowchart TD
    stageNode["1.3.x placeholder — reserved stage number (historical gap)"]
    contract["Contract"]
    service["Service"]
    surface["Surface"]
    data["Data"]
    ops["Ops"]
    releaseGate["Release gate"]

    stageNode --> contract
    stageNode --> service
    stageNode --> surface
    stageNode --> data
    stageNode --> ops
    contract --> releaseGate
    service --> releaseGate
    surface --> releaseGate
    data --> releaseGate
    ops --> releaseGate
```

### Runtime focus (unique to this minor)

```mermaid
flowchart LR
    intake["v1.3 CSV queue correctness"]
    orchestrate["Email orchestration"]
    verify["Provider verify + score"]
    persist["Contracts and lineage"]
    releasegate["Minor release gate"]

    intake --> orchestrate --> verify --> persist --> releasegate
    orchestrate --> audittrail["Ops and audit signals"]
    verify --> feedback["credit contract lock feedback loop"]
    persist --> stabilize["bulk finder pipeline stabilization"]
    audittrail --> stabilize
    feedback --> releasegate
    stabilize --> releasegate
```

See also: [`docs/flowchart.md`](../flowchart.md) for system-wide and master views.


## Task tracks

### Contract
- 🔴 Incompleted: **api**: define v1.3 contract outcomes for CSV queue correctness; harden request/response schema boundaries in `contact360.io/api` while advancing credit contract lock.
- 🔴 Incompleted: **app**: define v1.3 contract outcomes for CSV queue correctness; align UI payload contracts with backend enums in `contact360.io/app` while advancing credit contract lock.
- 🔴 Incompleted: **jobs**: define v1.3 contract outcomes for CSV queue correctness; lock worker message schema and retry metadata in `contact360.io/jobs` while advancing bulk finder pipeline.
- 🔴 Incompleted: **sync**: define v1.3 contract outcomes for CSV queue correctness; stabilize sync payload mapping and delta semantics in `contact360.io/sync` while advancing credit contract lock.
- 🔴 Incompleted: **admin**: define v1.3 contract outcomes for CSV queue correctness; formalize control-plane request contracts and guardrails in `contact360.io/admin` while advancing CSV queue correctness.
- 🔴 Incompleted: **mailvetter**: define v1.3 contract outcomes for CSV queue correctness; pin verifier payload expectations and score fields in `backend(dev)/mailvetter` while advancing CSV queue correctness.
- 🔴 Incompleted: **emailapis**: define v1.3 contract outcomes for CSV queue correctness; normalize provider adapter contract and fallback keys in `lambda/emailapis` while advancing bulk finder pipeline.
- 🔴 Incompleted: **emailapigo**: define v1.3 contract outcomes for CSV queue correctness; enforce Go adapter contract parity with shared models in `lambda/emailapigo` while advancing CSV queue correctness.

### Service
- 🔴 Incompleted: **api**: deliver v1.3 service outcomes for CSV queue correctness; implement strict handler guards and deterministic branching in `contact360.io/api` while advancing credit contract lock.
- 🔴 Incompleted: **app**: deliver v1.3 service outcomes for CSV queue correctness; wire client flows to canonical endpoints and failure states in `contact360.io/app` while advancing credit contract lock.
- 🔴 Incompleted: **jobs**: deliver v1.3 service outcomes for CSV queue correctness; tune queue worker orchestration and idempotent retries in `contact360.io/jobs` while advancing bulk finder pipeline.
- 🔴 Incompleted: **sync**: deliver v1.3 service outcomes for CSV queue correctness; tighten replication loops and conflict-resolution behavior in `contact360.io/sync` while advancing credit contract lock.
- 🔴 Incompleted: **admin**: deliver v1.3 service outcomes for CSV queue correctness; harden operator workflows and privilege-aware actions in `contact360.io/admin` while advancing CSV queue correctness.
```

(File continues after line 80.)

---

### 5. `d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\1.4 — Usage Ledger.md` (first 80 lines)

```markdown
# Version 1.4

- **Status:** planned
- **Era:** 1.x (Contact360 MVP core)
- **Summary:** Sub-minor within the 1.x era. Scope is defined when a planned stage is approved and the entry is added to `docs/versions.md`. Cross-service execution pack for this minor across contract, service, surface, data, and ops.

## Scope

- Target minor: `1.4.0` aligned to current roadmap mapping in this file.
- In scope: contract, service, surface, data, and ops tasks across core Contact360 services.
- Primary owners: API, App, Jobs, Sync, Admin, and supporting platform services.
- Exclusions: work outside this minor unless required for compatibility or incident risk reduction.
- Output: actionable per-service task breakdown and execution queue for release readiness.

## Flowchart

Delivery work for this minor follows the five-track model (contract, service, surface, data, ops) through a release gate.

```mermaid
flowchart TD
    stageNode["1.4.x placeholder — finder engine slice (pre-ship)"]
    contract["Contract"]
    service["Service"]
    surface["Surface"]
    data["Data"]
    ops["Ops"]
    releaseGate["Release gate"]

    stageNode --> contract
    stageNode --> service
    stageNode --> surface
    stageNode --> data
    stageNode --> ops
    contract --> releaseGate
    service --> releaseGate
    surface --> releaseGate
    data --> releaseGate
    ops --> releaseGate
```

### Runtime focus (unique to this minor)

```mermaid
flowchart LR
    intake["v1.4 credit contract lock"]
    orchestrate["Email orchestration"]
    verify["Provider verify + score"]
    persist["Contracts and lineage"]
    releasegate["Minor release gate"]

    intake --> orchestrate --> verify --> persist --> releasegate
    orchestrate --> audittrail["Ops and audit signals"]
    verify --> feedback["bulk finder pipeline feedback loop"]
    persist --> stabilize["P0 bug burn-down stabilization"]
    audittrail --> stabilize
    feedback --> releasegate
    stabilize --> releasegate
```

See also: [`docs/flowchart.md`](../flowchart.md) for system-wide and master views.


## Task tracks

### Contract
- 🔴 Incompleted: **api**: define v1.4 contract outcomes for credit contract lock; harden request/response schema boundaries in `contact360.io/api` while advancing bulk finder pipeline.
- 🔴 Incompleted: **app**: define v1.4 contract outcomes for credit contract lock; align UI payload contracts with backend enums in `contact360.io/app` while advancing bulk finder pipeline.
- 🔴 Incompleted: **jobs**: define v1.4 contract outcomes for credit contract lock; lock worker message schema and retry metadata in `contact360.io/jobs` while advancing P0 bug burn-down.
- 🔴 Incompleted: **sync**: define v1.4 contract outcomes for credit contract lock; stabilize sync payload mapping and delta semantics in `contact360.io/sync` while advancing bulk finder pipeline.
- 🔴 Incompleted: **admin**: define v1.4 contract outcomes for credit contract lock; formalize control-plane request contracts and guardrails in `contact360.io/admin` while advancing credit contract lock.
- 🔴 Incompleted: **mailvetter**: define v1.4 contract outcomes for credit contract lock; pin verifier payload expectations and score fields in `backend(dev)/mailvetter` while advancing credit contract lock.
- 🔴 Incompleted: **emailapis**: define v1.4 contract outcomes for credit contract lock; normalize provider adapter contract and fallback keys in `lambda/emailapis` while advancing P0 bug burn-down.
- 🔴 Incompleted: **emailapigo**: define v1.4 contract outcomes for credit contract lock; enforce Go adapter contract parity with shared models in `lambda/emailapigo` while advancing credit contract lock.

### Service
- 🔴 Incompleted: **api**: deliver v1.4 service outcomes for credit contract lock; implement strict handler guards and deterministic branching in `contact360.io/api` while advancing bulk finder pipeline.
- 🔴 Incompleted: **app**: deliver v1.4 service outcomes for credit contract lock; wire client flows to canonical endpoints and failure states in `contact360.io/app` while advancing bulk finder pipeline.
- 🔴 Incompleted: **jobs**: deliver v1.4 service outcomes for credit contract lock; tune queue worker orchestration and idempotent retries in `contact360.io/jobs` while advancing P0 bug burn-down.
- 🔴 Incompleted: **sync**: deliver v1.4 service outcomes for credit contract lock; tighten replication loops and conflict-resolution behavior in `contact360.io/sync` while advancing bulk finder pipeline.
- 🔴 Incompleted: **admin**: deliver v1.4 service outcomes for credit contract lock; harden operator workflows and privilege-aware actions in `contact360.io/admin` while advancing credit contract lock.
```

(File continues after line 80.)

---

### 6. `d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\appointment360-user-billing-task-pack.md` (first 60 lines)

```markdown
# Appointment360 (contact360.io/api) — Era 1.x User, Billing & Credit Task Pack

## Contract track

| Task | Priority |
| --- | --- |
| Define `AuthQuery { me }` returning `UserType` with all profile fields | P0 |
| Define `AuthMutation { login, register, logout, refresh_token }` with typed inputs/outputs | P0 |
| Define `BillingQuery { billingInfo, plans, invoices }` | P0 |
| Define `BillingMutation { subscribe, purchaseAddon, submitPaymentProof, approvePayment, declinePayment }` | P0 |
| Define `UsageQuery { usage(feature) }` returning credits remaining / consumed | P0 |
| Define `UserQuery { user(uuid), users(), userStats() }` with admin-guarded overloads | P0 |
| Define `UserMutation { updateUser, deleteUser, promoteUser }` | P0 |
| Document all auth types in `docs/backend/apis/01_AUTH_MODULE.md` | P1 |
| Document all billing types in `docs/backend/apis/10_BILLING_MODULE.md` | P1 |

---

## Service track

| Task | Priority |
| --- | --- |
| Implement `login` mutation: validate credentials, issue HS256 JWT access + refresh tokens | P0 |
| Implement `register` mutation: hash password, create user, issue tokens | P0 |
| Implement `logout` mutation: insert token into `token_blacklist` table | P0 |
| Implement `refresh_token` mutation: validate refresh token, issue new access token | P0 |
| Implement `me` query: extract `user` from `Context`, return `UserType` | P0 |
| Implement `require_auth(info)` guard in `core/security.py` | P0 |
| Implement `require_admin(info)` guard for admin-only mutations | P0 |
| Implement credit deduction service: `deduct_credit(user_uuid, feature, amount)` | P0 |
| Implement `usage(feature)` query: read credit totals from `credits` table | P0 |
| Implement billing service: plan lookup, subscription creation, add-on purchase | P1 |
| Implement `submitPaymentProof` + admin `approvePayment`/`declinePayment` flow | P1 |
| Wire `idempotency` middleware to `subscribe`, `purchaseAddon`, `submitPaymentProof` mutations | P1 |

---

## Surface track

| Task | Priority |
| --- | --- |
| `/login` page → `mutation login` binding in `authService.ts` | P0 |
| `/register` page → `mutation register` binding | P0 |
| User profile page → `query me` + `mutation updateProfile` binding | P0 |
| Billing page → `query billingInfo` + `query plans` + `mutation subscribe` binding | P1 |
| Credits counter component (header bar) → `query usage` polling on route change | P0 |
| Admin user list page → `query users` + `mutation promoteUser` bindings | P1 |
| `useAuth` hook: login, logout, refresh token auto-retry on 401 | P0 |
| `useBilling` hook: subscribe, purchase add-on, submit payment proof | P1 |
| `useCredits` hook: poll credits, show low-credit warning modal | P1 |

---

## Data track

| Task | Priority |
| --- | --- |
| Create `credits` table: user_uuid, feature, total, consumed, reset_at | P0 |
| Create `plans` table: id, name, price, limits JSON | P0 |
| Create `subscriptions` table: user_uuid, plan_id, status, billing_period_start, billing_period_end | P0 |
```

(The file has more lines after 60.)

---

### All files in `d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\`

| # | Absolute path |
|---|----------------|
| 1 | `d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\README.md` |
| 2 | `d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\appointment360-user-billing-task-pack.md` |
| 3 | `d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\connectra-user-billing-task-pack.md` |
| 4 | `d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\contact-ai-user-billing-task-pack.md` |
| 5 | `d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\emailapis-user-billing-credit-task-pack.md` |
| 6 | `d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\emailcampaign-user-billing-task-pack.md` |
| 7 | `d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\jobs-user-billing-task-pack.md` |
| 8 | `d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\logsapi-user-billing-credit-task-pack.md` |
| 9 | `d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\mailvetter-user-billing-task-pack.md` |
| 10 | `d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\s3storage-user-billing-task-pack.md` |
| 11 | `d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\salesnavigator-user-billing-task-pack.md` |
| 12 | `d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\1.0 — User Genesis.md` |
| 13 | `d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\1.1 — Billing Maturity.md` |
| 14 | `d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\1.2 — Analytics Bedrock.md` |
| 15 | `d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\1.3 — Payment Gateway.md` |
| 16 | `d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\1.4 — Usage Ledger.md` |
| 17 | `d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\1.5 — Notification Rail.md` |
| 18 | `d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\1.6 — Admin Control Plane.md` |
| 19 | `d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\1.7 — Security Hardening.md` |
| 20 | `d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\1.8 — Credit Pack Maturity.md` |
| 21 | `d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\1.9 — Identity and Session Hardening.md` |
| 22 | `d:\code\ayan\contact\docs\1. Contact360 user and billing and credit system\1.10 — Billing and User Ops Exit Gate.md` |

**Note:** In the version files above, fenced blocks that start with ` ```mermaid ` are closed with ` ``` ` in the real files; those closing fences are omitted in items 2–5 here because the outer markdown code fence would break. Open each file in the editor for byte-for-byte fidelity including every closing fence.

