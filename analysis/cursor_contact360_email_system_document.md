# Contact360 email system documentation retrieval
_Exported on 3/25/2026 at 01:50:33 GMT+5:30 from Cursor (2.6.21)_

---

**User**

Read the following files and return their content (full or first 80 lines each):
1. d:\code\ayan\contact\docs\2. Contact360 email system\README.md (full)
2. d:\code\ayan\contact\docs\2. Contact360 email system\2.0 — Email Foundation.md (first 80 lines)
3. d:\code\ayan\contact\docs\2. Contact360 email system\2.1 — Finder Engine.md (first 80 lines)
4. d:\code\ayan\contact\docs\2. Contact360 email system\2.4 — Bulk Processing.md (first 80 lines)
5. d:\code\ayan\contact\docs\2. Contact360 email system\email_system.md (first 60 lines)
6. d:\code\ayan\contact\docs\2. Contact360 email system\emailapis-email-system-task-pack.md (full)
7. d:\code\ayan\contact\docs\2. Contact360 email system\mailvetter-email-system-task-pack.md (full)
8. d:\code\ayan\contact\docs\2. Contact360 email system\emailcampaign-email-system-task-pack.md (full)

Also list ALL files in: d:\code\ayan\contact\docs\2. Contact360 email system\

Return the raw content.

---

**Cursor**


Reading the requested files and listing the directory.




Here is the **raw content** you asked for, plus a **full file list** for that folder.

---

## 1. `README.md` (full)

```markdown
# 2. Contact360 email system

## Era theme
- See `docs/version-policy.md` and `docs/versions.md` for canonical theme and release mapping for `2.x`.

## Service task-pack files
- `appointment360-email-system-task-pack.md`
- `connectra-email-system-task-pack.md`
- `contact-ai-email-system-task-pack.md`
- `emailapis-email-system-task-pack.md`
- `emailcampaign-email-system-task-pack.md`
- `jobs-email-system-task-pack.md`
- `logsapi-email-system-task-pack.md`
- `mailvetter-email-system-task-pack.md`
- `s3storage-email-system-task-pack.md`
- `salesnavigator-email-system-task-pack.md`

## Operational and supporting docs
- `email_system.md`

## Version notes
- Version detail files are stored as `version_<major>.<minor>.md` in this folder and indexed from `docs/versions.md`.
```

---

## 2. `2.0 — Email Foundation.md` (first 80 lines)

```markdown
# Version 2.0

- **Status:** planned
- **Target window:** TBD
- **Summary:** Connectra intelligence expansion. Cross-service execution pack for this minor across contract, service, surface, data, and ops.
- **Scope:** VQL filters, enrichment quality, deduplication, and advanced search UX.
- **Roadmap mapping:** `2.1` to `2.4`
- **Owner:** Search/Data Engineering

## Scope

- Target minor: `2.0.0` aligned to current roadmap mapping in this file.
- In scope: contract, service, surface, data, and ops tasks across core Contact360 services.
- Primary owners: API, App, Jobs, Sync, Admin, and supporting platform services.
- Exclusions: work outside this minor unless required for compatibility or incident risk reduction.
- Output: actionable per-service task breakdown and execution queue for release readiness.

## Flowchart

Delivery work for this minor follows the five-track model (contract, service, surface, data, ops) through a release gate.

```mermaid
flowchart TD
    stageNode["2.0.0 — Connectra intelligence (VQL, enrichment, dedup, search UX)"]
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
    intake["v2.0 Connectra enrich fanout"]
    orchestrate["Email orchestration"]
    verify["Provider verify + score"]
    persist["Contracts and lineage"]
    releasegate["Minor release gate"]

    intake --> orchestrate --> verify --> persist --> releasegate
    orchestrate --> audittrail["Ops and audit signals"]
    verify --> feedback["attribute confidence merge feedback loop"]
    persist --> stabilize["domain/entity enrichment stabilization"]
    audittrail --> stabilize
    feedback --> releasegate
    stabilize --> releasegate
```

See also: [`docs/flowchart.md`](../flowchart.md) for system-wide and master views.


## Task tracks

### Contract
- 🔴 Incompleted: **api**: define v2.0 contract outcomes for Connectra enrich fanout; harden request/response schema boundaries in `contact360.io/api` while advancing attribute confidence merge.
- 🔴 Incompleted: **app**: define v2.0 contract outcomes for Connectra enrich fanout; align UI payload contracts with backend enums in `contact360.io/app` while advancing attribute confidence merge.
- 🔴 Incompleted: **jobs**: define v2.0 contract outcomes for Connectra enrich fanout; lock worker message schema and retry metadata in `contact360.io/jobs` while advancing domain/entity enrichment.
- 🔴 Incompleted: **sync**: define v2.0 contract outcomes for Connectra enrich fanout; stabilize sync payload mapping and delta semantics in `contact360.io/sync` while advancing attribute confidence merge.
- 🔴 Incompleted: **admin**: define v2.0 contract outcomes for Connectra enrich fanout; formalize control-plane request contracts and guardrails in `contact360.io/admin` while advancing Connectra enrich fanout.
- 🔴 Incompleted: **mailvetter**: define v2.0 contract outcomes for Connectra enrich fanout; pin verifier payload expectations and score fields in `backend(dev)/mailvetter` while advancing Connectra enrich fanout.
- 🔴 Incompleted: **emailapis**: define v2.0 contract outcomes for Connectra enrich fanout; normalize provider adapter contract and fallback keys in `lambda/emailapis` while advancing domain/entity enrichment.
- 🔴 Incompleted: **emailapigo**: define v2.0 contract outcomes for Connectra enrich fanout; enforce Go adapter contract parity with shared models in `lambda/emailapigo` while advancing Connectra enrich fanout.

### Service
- 🔴 Incompleted: **api**: deliver v2.0 service outcomes for Connectra enrich fanout; implement strict handler guards and deterministic branching in `contact360.io/api` while advancing attribute confidence merge.
- 🔴 Incompleted: **app**: deliver v2.0 service outcomes for Connectra enrich fanout; wire client flows to canonical endpoints and failure states in `contact360.io/app` while advancing attribute confidence merge.
```

*(File continues after line 80.)*

---

## 3. `2.1 — Finder Engine.md` (first 80 lines)

```markdown
# Version 2.1

- **Status:** planned
- **Era:** 2.x (Connectra intelligence)
- **Summary:** Sub-minor within the 2.x era. Scope is defined when a planned stage is approved and the entry is added to `docs/versions.md`. Cross-service execution pack for this minor across contract, service, surface, data, and ops.

## Scope

- Target minor: `2.1.0` aligned to current roadmap mapping in this file.
- In scope: contract, service, surface, data, and ops tasks across core Contact360 services.
- Primary owners: API, App, Jobs, Sync, Admin, and supporting platform services.
- Exclusions: work outside this minor unless required for compatibility or incident risk reduction.
- Output: actionable per-service task breakdown and execution queue for release readiness.

## Flowchart

Delivery work for this minor follows the five-track model (contract, service, surface, data, ops) through a release gate.

```mermaid
flowchart TD
    stageNode["2.1.x placeholder — VQL compiler and query planning slice"]
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
    intake["v2.1 attribute confidence merge"]
    orchestrate["Email orchestration"]
    verify["Provider verify + score"]
    persist["Contracts and lineage"]
    releasegate["Minor release gate"]

    intake --> orchestrate --> verify --> persist --> releasegate
    orchestrate --> audittrail["Ops and audit signals"]
    verify --> feedback["domain/entity enrichment feedback loop"]
    persist --> stabilize["profile merge consistency stabilization"]
    audittrail --> stabilize
    feedback --> releasegate
    stabilize --> releasegate
```

See also: [`docs/flowchart.md`](../flowchart.md) for system-wide and master views.


## Task tracks

### Contract
- 🔴 Incompleted: **api**: define v2.1 contract outcomes for attribute confidence merge; harden request/response schema boundaries in `contact360.io/api` while advancing domain/entity enrichment.
- 🔴 Incompleted: **app**: define v2.1 contract outcomes for attribute confidence merge; align UI payload contracts with backend enums in `contact360.io/app` while advancing domain/entity enrichment.
- 🔴 Incompleted: **jobs**: define v2.1 contract outcomes for attribute confidence merge; lock worker message schema and retry metadata in `contact360.io/jobs` while advancing profile merge consistency.
- 🔴 Incompleted: **sync**: define v2.1 contract outcomes for attribute confidence merge; stabilize sync payload mapping and delta semantics in `contact360.io/sync` while advancing domain/entity enrichment.
- 🔴 Incompleted: **admin**: define v2.1 contract outcomes for attribute confidence merge; formalize control-plane request contracts and guardrails in `contact360.io/admin` while advancing attribute confidence merge.
- 🔴 Incompleted: **mailvetter**: define v2.1 contract outcomes for attribute confidence merge; pin verifier payload expectations and score fields in `backend(dev)/mailvetter` while advancing attribute confidence merge.
- 🔴 Incompleted: **emailapis**: define v2.1 contract outcomes for attribute confidence merge; normalize provider adapter contract and fallback keys in `lambda/emailapis` while advancing profile merge consistency.
- 🔴 Incompleted: **emailapigo**: define v2.1 contract outcomes for attribute confidence merge; enforce Go adapter contract parity with shared models in `lambda/emailapigo` while advancing attribute confidence merge.

### Service
- 🔴 Incompleted: **api**: deliver v2.1 service outcomes for attribute confidence merge; implement strict handler guards and deterministic branching in `contact360.io/api` while advancing domain/entity enrichment.
- 🔴 Incompleted: **app**: deliver v2.1 service outcomes for attribute confidence merge; wire client flows to canonical endpoints and failure states in `contact360.io/app` while advancing domain/entity enrichment.
- 🔴 Incompleted: **jobs**: deliver v2.1 service outcomes for attribute confidence merge; tune queue worker orchestration and idempotent retries in `contact360.io/jobs` while advancing profile merge consistency.
- 🔴 Incompleted: **sync**: deliver v2.1 service outcomes for attribute confidence merge; tighten replication loops and conflict-resolution behavior in `contact360.io/sync` while advancing domain/entity enrichment.
- 🔴 Incompleted: **admin**: deliver v2.1 service outcomes for attribute confidence merge; harden operator workflows and privilege-aware actions in `contact360.io/admin` while advancing attribute confidence merge.
```

*(File continues after line 80.)*

---

## 4. `2.4 — Bulk Processing.md` (first 80 lines)

```markdown
# Version 2.4

- **Status:** planned
- **Era:** 2.x (Connectra intelligence)
- **Summary:** Sub-minor within the 2.x era. Scope is defined when a planned stage is approved and the entry is added to `docs/versions.md`. Cross-service execution pack for this minor across contract, service, surface, data, and ops.

## Scope

- Target minor: `2.4.0` aligned to current roadmap mapping in this file.
- In scope: contract, service, surface, data, and ops tasks across core Contact360 services.
- Primary owners: API, App, Jobs, Sync, Admin, and supporting platform services.
- Exclusions: work outside this minor unless required for compatibility or incident risk reduction.
- Output: actionable per-service task breakdown and execution queue for release readiness.

## Flowchart

Delivery work for this minor follows the five-track model (contract, service, surface, data, ops) through a release gate.

```mermaid
flowchart TD
    stageNode["2.4.x placeholder — deduplication and merge policy slice"]
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
    intake["v2.4 enrichment fallback path"]
    orchestrate["Email orchestration"]
    verify["Provider verify + score"]
    persist["Contracts and lineage"]
    releasegate["Minor release gate"]

    intake --> orchestrate --> verify --> persist --> releasegate
    orchestrate --> audittrail["Ops and audit signals"]
    verify --> feedback["Connectra enrich fanout feedback loop"]
    persist --> stabilize["attribute confidence merge stabilization"]
    audittrail --> stabilize
    feedback --> releasegate
    stabilize --> releasegate
```

See also: [`docs/flowchart.md`](../flowchart.md) for system-wide and master views.


## Task tracks

### Contract
- 🔴 Incompleted: **api**: define v2.4 contract outcomes for enrichment fallback path; harden request/response schema boundaries in `contact360.io/api` while advancing Connectra enrich fanout.
- 🔴 Incompleted: **app**: define v2.4 contract outcomes for enrichment fallback path; align UI payload contracts with backend enums in `contact360.io/app` while advancing Connectra enrich fanout.
- 🔴 Incompleted: **jobs**: define v2.4 contract outcomes for enrichment fallback path; lock worker message schema and retry metadata in `contact360.io/jobs` while advancing attribute confidence merge.
- 🔴 Incompleted: **sync**: define v2.4 contract outcomes for enrichment fallback path; stabilize sync payload mapping and delta semantics in `contact360.io/sync` while advancing Connectra enrich fanout.
- 🔴 Incompleted: **admin**: define v2.4 contract outcomes for enrichment fallback path; formalize control-plane request contracts and guardrails in `contact360.io/admin` while advancing enrichment fallback path.
- 🔴 Incompleted: **mailvetter**: define v2.4 contract outcomes for enrichment fallback path; pin verifier payload expectations and score fields in `backend(dev)/mailvetter` while advancing enrichment fallback path.
- 🔴 Incompleted: **emailapis**: define v2.4 contract outcomes for enrichment fallback path; normalize provider adapter contract and fallback keys in `lambda/emailapis` while advancing attribute confidence merge.
- 🔴 Incompleted: **emailapigo**: define v2.4 contract outcomes for enrichment fallback path; enforce Go adapter contract parity with shared models in `lambda/emailapigo` while advancing enrichment fallback path.

### Service
- 🔴 Incompleted: **api**: deliver v2.4 service outcomes for enrichment fallback path; implement strict handler guards and deterministic branching in `contact360.io/api` while advancing Connectra enrich fanout.
- 🔴 Incompleted: **app**: deliver v2.4 service outcomes for enrichment fallback path; wire client flows to canonical endpoints and failure states in `contact360.io/app` while advancing Connectra enrich fanout.
- 🔴 Incompleted: **jobs**: deliver v2.4 service outcomes for enrichment fallback path; tune queue worker orchestration and idempotent retries in `contact360.io/jobs` while advancing attribute confidence merge.
- 🔴 Incompleted: **sync**: deliver v2.4 service outcomes for enrichment fallback path; tighten replication loops and conflict-resolution behavior in `contact360.io/sync` while advancing Connectra enrich fanout.
- 🔴 Incompleted: **admin**: deliver v2.4 service outcomes for enrichment fallback path; harden operator workflows and privilege-aware actions in `contact360.io/admin` while advancing enrichment fallback path.
```

*(File continues after line 80.)*

---

## 5. `email_system.md` (first 60 lines)

```markdown
You now have a **distributed email platform**, not a single service.  
After reading all the listed codebases, here is the deep, unified view of the **full email system** and a practical task breakdown.

## Full Email System Map

### 1) Product/UI Layer
- `contact360.io/app`
- Handles Email Studio UX: finder/verifier single/bulk, CSV upload, job creation, job polling/download.
- Talks to GraphQL only.

### 2) API Orchestration Layer
- `contact360.io/api`
- Auth, validation, credit deduction, activity logging.
- Routes synchronous email operations to Lambda email APIs.
- Routes async export/import operations to tkdjob (`contact360.io/jobs` service).

### 3) Async Job Execution Layer
- `contact360.io/jobs`
- Streaming CSV processors for:
  - email finder export
  - email verify export
  - email pattern import
- Uses worker pool + queue + S3 multipart + external email API batching.

### 4) Email API Runtime Layer
- `lambda/emailapigo` and `lambda/emailapis`
- Finder + verifier APIs, provider adapters, cache/pattern/generation/fallback orchestration.

### 5) Deep Verification/Scoring Engine Layer
- `backend(dev)/mailvetter`
- Signal collection (SMTP/DNS/OSINT/etc.) + scoring logic + status/reachability + bulk worker persistence.

### 6) Data Sync/Index Layer
- `contact360.io/sync`
- Imports/exports contact/company data including `email`/`email_status` into PG/ES.

### 7) Admin/Control Layer
- `contact360.io/admin`
- Workflow automation with email-send node.
- Operational monitor/retry interface for external job scheduler.

---

## End-to-End Email Flows

## A) Synchronous (interactive)
`app -> api (GraphQL email module) -> lambda email API -> result -> app`

- finder single/bulk
- verifier single/bulk
- pattern add/bulk add

## B) Asynchronous (CSV pipeline)
`app upload -> api job mutation -> jobs service create stream job -> worker executes -> S3 output -> api scheduler state -> app jobs download`

- email-export
- email-verify
- email-pattern-import

## C) Scoring core flow
```

*(File continues after line 60.)*

---

## 6. `emailapis-email-system-task-pack.md` (full)

```markdown
# emailapis task pack — era 2.x

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

## 7. `mailvetter-email-system-task-pack.md` (full)

```markdown
# Mailvetter — 2.x Email System Task Pack

**Service:** `backend(dev)/mailvetter`  
**Era:** `2.x` — Core email verification system (primary era)

## Contract track

- 🔴 Incompleted: Freeze v1 endpoints: `POST /v1/emails/validate`, `POST /v1/emails/validate-bulk`, `GET /v1/jobs/:job_id`, `GET /v1/jobs/:job_id/results`.
- 🔴 Incompleted: Freeze status vocabulary: `valid`, `invalid`, `catch_all`, `risky`, `unknown`.
- 🔴 Incompleted: Freeze confidence score mapping and score breakdown schema.
- 🔴 Incompleted: Freeze webhook callback payload contract.

## Service track

- 🔴 Incompleted: Harden single verify path: syntax -> DNS -> SMTP -> scoring.
- 🔴 Incompleted: Harden bulk job path: dedupe, plan checks, queueing, worker updates.
- 🔴 Incompleted: Add explicit `failed` job status path for partial/system failures.
- 🔴 Incompleted: Add retry and dead-letter handling for poisoned tasks.

## Surface track

- 🔴 Incompleted: Map `/email` dashboard verifier tab to v1 contract fields.
- 🔴 Incompleted: Ensure progress bars consume `processed/total/percentage` consistently.
- 🔴 Incompleted: Show “why” diagnostics from `score_details` in verifier UI panel.

## Data track

- 🔴 Incompleted: Normalize key verification columns in `results` for queryable analytics.
- 🔴 Incompleted: Add job events timeline table (queued, started, completed, failed, retried).

## Ops track

- 🔴 Incompleted: Load-test bulk verification throughput for 10k email payload.
- 🔴 Incompleted: Add queue lag and worker saturation dashboards.
- 🔴 Incompleted: Add SMTP provider timeout/error budget alerts.
```

---

## 8. `emailcampaign-email-system-task-pack.md` (full)

```markdown
# Email Campaign Service — Era 2.x Task Pack
## Contact360 Email System

### Context
Era `2.x` hardens the core email delivery infrastructure. The campaign service evolves from a basic SMTP relay to a production-grade send engine with authentication, bounce handling, retry logic, DKIM signing awareness, and suppression-list accuracy.

---

## Track A — Contract

| Task | Description | Owner |
| --- | --- | --- |
| A-2.1 | Document supported SMTP providers (SendGrid, AWS SES, Mailgun) and auth configuration | Backend |
| A-2.2 | Define bounce/complaint handling webhook contract (provider → campaign service) | Backend |
| A-2.3 | Document retry policy: max attempts, backoff intervals, DLQ behaviour | Backend |

## Track B — Service

| Task | Description | Owner |
| --- | --- | --- |
| B-2.1 | SMTP auth: read username/password/host/port from env; pass `smtp.PlainAuth` to `smtp.SendMail` | Backend |
| B-2.2 | Per-message retry with exponential backoff and Asynq max-retry policy | Backend |
| B-2.3 | Implement bounce webhook receiver endpoint; auto-add bounced email to `suppression_list` | Backend |
| B-2.4 | Implement complaint webhook receiver (Spam/Abuse feedback); add to suppression | Backend |
| B-2.5 | Add DKIM header passthrough note or SES-managed signing recommendation | Backend |
| B-2.6 | Add configurable send-rate throttle (N emails/sec) to `EmailWorker` goroutines | Backend |
| B-2.7 | Campaign status: add `completed_with_errors` when `failed > 0 && sent > 0` | Backend |

## Track C — Surface

| Task | Description | Owner |
| --- | --- | --- |
| C-2.1 | Email settings page: input boxes for SMTP host, port, username; masked password field | Frontend |
| C-2.2 | Campaign list: colour-coded status badge (`pending`, `sending`, `completed`, `completed_with_errors`, `failed`) | Frontend |
| C-2.3 | Campaign detail: sent/failed/unsubscribed counts with mini progress bar | Frontend |

## Track D — Data

| Task | Description | Owner |
| --- | --- | --- |
| D-2.1 | Migration: add `bounced_at TIMESTAMP` and `complaint_at TIMESTAMP` to `recipients` | Backend |
| D-2.2 | Migration: add `provider TEXT` and `send_rate_limit INT` to `campaigns` | Backend |
| D-2.3 | Ensure suppression_list has index on `email` for fast pre-send lookup | Backend |

## Track E — Ops

| Task | Description | Owner |
| --- | --- | --- |
| E-2.1 | SMTP credential rotation: mount as Kubernetes secret or SSM parameter | DevOps |
| E-2.2 | Dead-letter queue monitoring: alert on tasks exceeding max-retry in Asynq dashboard | DevOps |

---

## Completion gate
- 🔴 Incompleted: Email delivered from real SMTP credentials without nil auth.
- 🔴 Incompleted: Bounce/complaint webhook adds email to suppression list and suppresses future sends.
- 🔴 Incompleted: Campaign with partial failures shows `completed_with_errors` status.
- 🔴 Incompleted: Per-second rate limit prevents exceeding SES/SendGrid quota.
```

---

## All files in `d:\code\ayan\contact\docs\2. Contact360 email system\` (23 files)

1. `d:\code\ayan\contact\docs\2. Contact360 email system\README.md`  
2. `d:\code\ayan\contact\docs\2. Contact360 email system\appointment360-email-system-task-pack.md`  
3. `d:\code\ayan\contact\docs\2. Contact360 email system\connectra-email-system-task-pack.md`  
4. `d:\code\ayan\contact\docs\2. Contact360 email system\contact-ai-email-system-task-pack.md`  
5. `d:\code\ayan\contact\docs\2. Contact360 email system\email_system.md`  
6. `d:\code\ayan\contact\docs\2. Contact360 email system\emailapis-email-system-task-pack.md`  
7. `d:\code\ayan\contact\docs\2. Contact360 email system\emailcampaign-email-system-task-pack.md`  
8. `d:\code\ayan\contact\docs\2. Contact360 email system\jobs-email-system-task-pack.md`  
9. `d:\code\ayan\contact\docs\2. Contact360 email system\logsapi-email-system-task-pack.md`  
10. `d:\code\ayan\contact\docs\2. Contact360 email system\mailvetter-email-system-task-pack.md`  
11. `d:\code\ayan\contact\docs\2. Contact360 email system\s3storage-email-system-task-pack.md`  
12. `d:\code\ayan\contact\docs\2. Contact360 email system\salesnavigator-email-system-task-pack.md`  
13. `d:\code\ayan\contact\docs\2. Contact360 email system\2.0 — Email Foundation.md`  
14. `d:\code\ayan\contact\docs\2. Contact360 email system\2.1 — Finder Engine.md`  
15. `d:\code\ayan\contact\docs\2. Contact360 email system\2.10 — Email System Exit Gate.md`  
16. `d:\code\ayan\contact\docs\2. Contact360 email system\2.2 — Verifier Engine.md`  
17. `d:\code\ayan\contact\docs\2. Contact360 email system\2.3 — Results Engine.md`  
18. `d:\code\ayan\contact\docs\2. Contact360 email system\2.4 — Bulk Processing.md`  
19. `d:\code\ayan\contact\docs\2. Contact360 email system\2.5 — Mailbox Core.md`  
20. `d:\code\ayan\contact\docs\2. Contact360 email system\2.6 — Provider Harmonization.md`  
21. `d:\code\ayan\contact\docs\2. Contact360 email system\2.7 — Mailvetter Hardening.md`  
22. `d:\code\ayan\contact\docs\2. Contact360 email system\2.8 — Bulk Observability.md`  
23. `d:\code\ayan\contact\docs\2. Contact360 email system\2.9 — Email Credit & Audit Maturity.md`

**Note:** `emailapis-email-system-task-pack.md` literally contains the placeholder `$(System.Collections.Hashtable.era)` where an era value was probably meant to be substituted.

