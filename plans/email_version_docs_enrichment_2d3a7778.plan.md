---
name: Email Version Docs Enrichment
overview: Systematically enrich all 121 version files (0.0 through 10.10) with email-system-specific content in every required section — Runtime focus flowchart, Task tracks, Task Breakdown, Immediate next execution queue, Cross-service ownership, and References — derived from the deep email system analysis across all 9 codebases.
todos:
  - id: era-0x
    content: "Enrich era 0.x files (0.0 — Pre-repo baseline.md through 0.10 — Ship & ops hardening.md, 11 files): email scaffolding/bootstrap theme — Runtime focus showing email service init, task tracks with base status schema + provider wiring tasks, execution queue with email contract foundation items, ownership + refs"
    status: completed
  - id: era-1x
    content: "Enrich era 1.x files (1.0 — User Genesis.md through 1.10 — Billing and User Ops Exit Gate.md, 11 files): MVP/bulk email theme — Runtime focus showing full sync/async email paths, P0 bug fix tasks (O365 correction, sync retry/CSV panic, admin EmailNode, jobs batch), contract freeze tasks, execution queue with email-specific items"
    status: completed
  - id: era-2x
    content: "Enrich era 2.x files (2.0 — Email Foundation.md through 2.10 — Email System Exit Gate.md, 11 files): Connectra enrichment theme — email confidence/provenance, domain matching, search-to-email workflow Runtime focus, enrichment-specific task tracks"
    status: completed
  - id: era-3x
    content: "Enrich era 3.x files (3.0 — Twin Ledger.md through 3.10 — Data Completeness.md, 11 files): Extension channel theme — email discovery via extension/Sales Navigator, email status propagation, enrichment consistency Runtime focus"
    status: completed
  - id: era-4x
    content: "Enrich era 4.x files (4.0 — Harbor.md through 4.10 — Exit Gate.md, 11 files): AI workflow theme — AI-assisted email generation, OpenAI ranking fallback safety, prompt governance, explanation/confidence fields Runtime focus"
    status: completed
  - id: era-5x
    content: "Enrich era 5.x files (5.0 — Neural Spine.md through 5.10 — Connectra Intelligence.md, 11 files): Reliability theme — email SLO, idempotent finder/verifier, checkpoint/resume for all email stream processors, error budgets, load/chaos drills Runtime focus"
    status: completed
  - id: era-6x
    content: "Enrich era 6.x files (6.0 — Reliability and Scaling era umbrella.md through 6.10 — Buffer - placeholder minor within the 6x reliability era.md, 11 files): Enterprise governance theme — email RBAC, audit trail for email ops, compliance-ready email status lifecycle Runtime focus"
    status: completed
  - id: era-7x
    content: "Enrich era 7.x files (7.0 — Deployment era baseline lock.md through 7.10 — Deployment overflow patch buffer inside era 7.md, 11 files): Analytics theme — email metrics (status distribution, provider latency, scoring drift), fallback usage analytics, email quality dashboards Runtime focus"
    status: completed
  - id: era-8x
    content: "Enrich era 8.x files (8.0 — API Era Foundation.md through 8.10 — API Era Buffer.md, 11 files): Integration ecosystem theme — email webhooks, public email API, partner integration for finder/verifier, connector framework Runtime focus"
    status: completed
  - id: era-9x
    content: "Enrich era 9.x files (9.0 — Ecosystem Foundation.md through 9.10 — Productization Buffer.md, 11 files): Productization theme — email entitlement per plan, quota enforcement for bulk ops, tenant-scoped provider config Runtime focus"
    status: completed
  - id: era-10x
    content: "Enrich era 10.x files (10.0 — Campaign Bedrock.md through 10.10 — Placeholder Policy.md, 11 files): Unified platform theme — email contract freeze, canonical status taxonomy lock, full lineage closure Runtime focus"
    status: completed
isProject: false
---

# Email System Version Docs Enrichment Plan

## What Exists vs. What Needs to Change

All 121 files already have the correct **skeleton** with every required section. The problem is the content is generic/templated:

- `Immediate next execution queue` — identical 8-bullet boilerplate in every file
- `Cross-service ownership` table — same "Version delivery focus" text repeated in every file
- `References` — no email system rule files cited
- `### Runtime focus` mermaid — shows era theme but not the email sub-system flow for that minor
- Task tracks for `emailapis`, `emailapigo`, `mailvetter` — have only shallow one-liners, not actionable email system specifics

## Changes Required Per File (4 targeted edits each)

### Edit 1 — `### Runtime focus` mermaid

Replace the generic era diagram with a version-specific **email system data flow** relevant to that minor's scope.

### Edit 2 — Task tracks + Task Breakdown (email service rows)

For services `emailapis`, `emailapigo`, `mailvetter`, `jobs` (email processors), `api` (email GraphQL module), `app` (Email Studio), `sync` (email field normalization), `admin` (email node) — replace generic one-liners with email-system-specific tasks derived from the P0/P1/P2 findings.

### Edit 3 — `Immediate next execution queue`

Replace the 8 identical generic bullets with 8 version-specific, email-system-anchored execution items.

### Edit 4 — `Cross-service ownership` + `References`

Update service ownership focus column to be version+email-specific. Add email system rule file refs to References section.

## Era → Email Theme Mapping

This drives what content each era's files get:

- **0.x (Foundation)**: Email service scaffolding, base status schema (`valid/invalid/catchall/risky/unknown`), provider client bootstrap, finder/verifier route registration
- **1.x (MVP/Bulk)**: Email Contract Spec freeze, bulk CSV pipeline hardening, P0 bug fixes (sync retry, CSV panic, admin EmailNode failure propagation, jobs batch alignment, mailvetter O365 correction), cross-boundary contract tests
- **2.x (Connectra)**: Email enrichment via Connectra, confidence/provenance metadata, domain-matching improvements, search-to-email workflows
- **3.x (Extension)**: Email discovery via extension/Sales Navigator ingestion, enrichment consistency, email status propagation to extension surface
- **4.x (AI workflows)**: AI-assisted email generation, OpenAI-based ranking with fallback safety, prompt governance, explanation/confidence fields
- **5.x (Reliability)**: Email SLO definition, idempotent finder/verifier paths, checkpoint/resume for all email stream processors, error budgets, load testing, chaos drills
- **6.x (Enterprise)**: Email governance, RBAC for email operations, audit trail for finder/verifier actions, compliance-ready email status lifecycle
- **7.x (Analytics)**: Email metrics (status distribution drift, provider latency, scoring distribution), fallback usage analytics, email quality dashboards
- **8.x (Integration)**: Email webhooks, public email API, partner integration for finder/verifier, connector framework for email providers
- **9.x (Productization)**: Email entitlement per plan, quota enforcement for bulk ops, tenant-scoped email provider config
- **10.x (Unified)**: Email contract freeze across all surfaces, canonical status taxonomy lock, full lineage from request → provider → outcome → consumption

## Key Email System Facts (from codebase analysis)

### Architecture layers (drives Runtime focus diagrams)

```
app (Email Studio) → api (GraphQL email module) → emailapigo/emailapis → mailvetter
app → api → jobs (email processors) → S3 → emailapigo/emailapis
sync (email field normalization to PG/ES)
admin (EmailNode workflow + tkdjob ops)
```

### P0 bugs to track in 1.x era files

- `mailvetter/internal/validator/scoring.go`: O365 zombie correction `o365ZombieCorrected` declared but inactive
- `sync/jobs/jobs.go`: `serverTime` outside consumer loop → stale retry base; `retry_count` not incremented
- `sync/utilities/common.go`: `CsvRowToMap` no bounds check → panic on malformed CSV
- `admin/apps/durgasflow/nodes/actions.py` `EmailNode.execute()`: catches exception, returns `{'sent': False}` instead of re-raising
- `jobs/app/processors/email_finder_export_stream.py`: partial batch extends by fixed `batch_limit` → result desync
- `emailapis/app/services/email_finder_service.py`: `find_emails_bulk` passes `website` arg to `find_emails` which rejects it

### Status taxonomy (drives contract tasks)

`valid` | `invalid` | `catchall` | `risky` | `unknown` — each layer uses different semantics; no single truth table exists.

### Key files to cite in References per version area

- `docs/.cursor/rules/email_system.md`
- `docs/.cursor/rules/cursor_contact360_email_integration_exp.md`
- `backend(dev)/mailvetter/internal/validator/scoring.go`
- `lambda/emailapis/app/services/email_finder_service.py`
- `lambda/emailapigo/internal/services/email_finder_service.go`
- `contact360.io/api/app/graphql/modules/email/queries.py`
- `contact360.io/jobs/app/processors/email_finder_export_stream.py`
- `contact360.io/sync/models/contact.pgsql.go`
- `contact360.io/admin/apps/durgasflow/nodes/actions.py`

## Execution Sequence

Work through files era by era. Each era is a task group of 11 files (0.x–10.x), each file gets 4 targeted edits:

- Era 0.x: `0.0 — Pre-repo baseline.md` → `0.10 — Ship & ops hardening.md` (11 files)
- Era 1.x: `1.0 — User Genesis.md` → `1.10 — Billing and User Ops Exit Gate.md` (11 files)
- Era 2.x: `2.0 — Email Foundation.md` → `2.10 — Email System Exit Gate.md` (11 files)
- Era 3.x: `3.0 — Twin Ledger.md` → `3.10 — Data Completeness.md` (11 files)
- Era 4.x: `4.0 — Harbor.md` → `4.10 — Exit Gate.md` (11 files)
- Era 5.x: `5.0 — Neural Spine.md` → `5.10 — Connectra Intelligence.md` (11 files)
- Era 6.x: `6.0 — Reliability and Scaling era umbrella.md` → `6.10 — Buffer - placeholder minor within the 6x reliability era.md` (11 files)
- Era 7.x: `7.0 — Deployment era baseline lock.md` → `7.10 — Deployment overflow patch buffer inside era 7.md` (11 files)
- Era 8.x: `8.0 — API Era Foundation.md` → `8.10 — API Era Buffer.md` (11 files)
- Era 9.x: `9.0 — Ecosystem Foundation.md` → `9.10 — Productization Buffer.md` (11 files)
- Era 10.x: `10.0 — Campaign Bedrock.md` → `10.10 — Placeholder Policy.md` (11 files)

Total: **121 file edits**, each with **4 targeted section replacements**.

## Files Being Modified

All files are under `[docs/versions/](docs/versions/)` — e.g. `[docs/versions/0.0 — Pre-repo baseline.md](docs/versions/0.0 — Pre-repo baseline.md)` through `[docs/versions/10.10 — Placeholder Policy.md](docs/versions/10.10 — Placeholder Policy.md)`.

Supporting context files (read-only reference):

- `[docs/versions.md](docs/versions.md)`
- `[.cursor/rules/email_system.md](.cursor/rules/email_system.md)`
- `[.cursor/rules/cursor_contact360_email_integration_exp.md](.cursor/rules/cursor_contact360_email_integration_exp.md)`

