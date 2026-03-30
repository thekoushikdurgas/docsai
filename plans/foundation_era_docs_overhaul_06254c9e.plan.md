---
name: Foundation Era Docs Overhaul
overview: Overhaul all 22 files in the `docs/0. Foundation and pre-product stabilization and codebase setup/` folder by replacing generic boilerplate with minor-specific content derived from every codebase analysis, adding all missing structural sections, and enriching weak task packs to match the quality bar set by `appointment360-foundation-task-pack.md`.
todos:
  - id: master-checklist
    content: "Update 0.x-master-checklist.md: add cross-service risk matrix from codebase analyses, patch micro-gate template (5-item checklist per patch band), minor→specific-risk mapping table"
    status: completed
  - id: readme-update
    content: "Update README.md: add era summary paragraph, list new sections added to version files, update cross-references"
    status: completed
  - id: v0-0
    content: "Rewrite 0.0 — Pre-repo baseline.md: fix runtime focus to placeholder-only mermaid, replace generic task tracks with pre-repo-baseline specifics, add all 8 missing sections (Backend API scope, DB scope, Frontend scope, UI checklist, Flow delta, Cross-service ownership, Audit notes, Patch ladder + Release Gate)"
    status: completed
  - id: v0-1
    content: "Rewrite 0.1 — Monorepo bootstrap.md (Monorepo bootstrap): unique runtime focus showing FastAPI bootstrap→JWT→DB session→health chain; specific task tracks for appointment360 middleware stack, DB migration seed, service skeletons; all 8 missing sections"
    status: completed
  - id: v0-2
    content: "Rewrite 0.2 — Schema & migration bedrock.md (Schema & migration bedrock): unique runtime focus showing Alembic revision chain→DB separation→CI gate; task tracks covering migration policy, schema freeze, jobs/appointment360 DB split; all 8 missing sections"
    status: completed
  - id: v0-3
    content: "Rewrite 0.3 — Service mesh contracts.md (Service mesh contracts): unique runtime focus showing gateway client fan-out (ConnectraClient/TkdjobClient/LambdaEmailClient)→X-API-Key→error envelope; task tracks for timeout/retry/error-shape contracts; all 8 missing sections"
    status: completed
  - id: v0-4
    content: "Rewrite 0.4 — Identity & RBAC freeze.md (Identity & RBAC freeze): unique runtime focus showing JWT→role resolution→credit hook→RBAC guard→protected resolver; task tracks for token blacklist, @require_role decorator, credit deduction contract; all 8 missing sections"
    status: completed
  - id: v0-5
    content: "Rewrite 0.5 — Object storage plane.md (Object storage plane): unique runtime focus showing initiate-multipart→presign→S3 PUT→complete→metadata-worker-lambda; task tracks derived from s3storage-codebase-analysis.md gaps (durable multipart, env-driven worker name, metadata RMW); all 8 missing sections"
    status: completed
  - id: v0-6
    content: "Rewrite 0.6 — Async job spine.md (Async job spine): unique runtime focus showing job create→Kafka→consumer→processor registry→job_node state machine→job_events; task tracks from jobs-codebase-analysis.md (stale recovery, DAG degree, processor bootstrap); all 8 missing sections"
    status: completed
  - id: v0-7
    content: "Rewrite 0.7 — Search & dual-write substrate.md (Search & dual-write substrate): unique runtime focus showing VQL parse→ES query→ES ID list→PG hydrate→in-memory join→UUID5 dedup; task tracks from connectra-codebase-analysis.md (in-memory queue, CORS, ES/PG drift); all 8 missing sections"
    status: completed
  - id: v0-8
    content: "Rewrite 0.8 — UX shell & docs mirror.md (UX shell & docs mirror): unique runtime focus showing Next.js shell→GraphQL context→JWT gate→role→page visibility→DocsAI architecture.md→admin/constants.py sync; task tracks for app shell, admin DocsAI baseline, sidebar constants; all 8 missing sections"
    status: completed
  - id: v0-9
    content: "Rewrite 0.9 — Extension channel scaffold.md (Extension channel scaffold): unique runtime focus showing Chrome extension MV3→chrome.storage.local→lambdaClient.js→POST /v1/save-profiles→SN service→Connectra upsert; task tracks from extension/salesnavigator analyses; all 8 missing sections"
    status: completed
  - id: v0-10
    content: "Rewrite 0.10 — Ship & ops hardening.md (Ship & ops hardening): unique runtime focus showing Docker Compose→SAM template→/health probes per service→Secrets Manager→CI/CD exit gate; task tracks covering every service health endpoint, compose alignment, secret baseline; all 8 missing sections"
    status: completed
  - id: pack-connectra
    content: "Expand connectra-foundation-task-pack.md: add persistent queue task (replace in-memory channel), ES-PG reconciliation job, per-tenant rate-limit and scoped key tasks, VQL/filter contract test baseline, batch-upsert idempotency release gate"
    status: completed
  - id: pack-s3storage
    content: "Expand s3storage-foundation-task-pack.md: add durable multipart session store task, env-driven worker function name, concurrency-safe metadata.json write, E2E multipart+worker CI test, failure-path tests, CORS/auth tightening, SLO baseline"
    status: completed
  - id: pack-contact-ai
    content: "Expand contact-ai-foundation-task-pack.md: add ModelSelection enum freeze, global API_KEY→parameterized config, JSONB schema versioning baseline, silent Gemini fallback logging, distributed tracing stub"
    status: completed
  - id: pack-emailapis
    content: "Expand emailapis-foundation-task-pack.md: add provider drift control (Python/Go parity matrix), status semantic vocabulary freeze, bulk correctness test baseline, observability gap tasks (request-ID injection)"
    status: completed
  - id: pack-logsapi
    content: "Expand logsapi-foundation-task-pack.md: confirm S3 CSV as canonical store (not MongoDB), static API key rotation plan, query scalability baseline (pagination/index), cache consistency and compliance risk tasks"
    status: completed
isProject: false
---

# Foundation Era Docs Overhaul

## The problem (evidence)

Every `0.N — <Title>.md` currently has **two critical defects**:

1. **Identical "Runtime focus" diagram** — all 11 files show the same generic `Email orchestration → Provider verify + score` mermaid flow regardless of the minor's actual subject. `0.5` (Object storage plane) should show `initiate multipart → presign → complete → metadata-worker`. `0.6` (Async job spine) should show the DAG state machine. None of them do.
2. **Identical task-track bullets** — rotating the five phrases "bootstrap health path / env matrix lock / baseline service wiring / first smoke checks / startup contract shape" as filler, with no service-specific action.

Every file is also **missing** the following sections the user specified:

- Backend API and Endpoint Scope
- Database and Data Lineage Scope
- Frontend UX Surface Scope
- UI Elements Checklist
- Flow / Graph Delta for This Minor
- Cross-service ownership table
- Audit / Compliance notes
- Patch ladder (linking to codenames in `0.x-master-checklist.md`)
- Release Gate + Evidence (Master Task Checklist / Backend API / DB / Frontend / UI / Flow / Validation / Release Gate sub-sections)

Three task packs (`connectra`, `s3storage`, and implicitly `contact-ai`, `emailapis`, `logsapi`) are also **sparse** compared to the `appointment360` or `emailcampaign` packs.

---

## Unique Runtime Focus per minor

Each `0.N — <Title>.md` will receive a **unique** mermaid diagram replacing the generic one:

- `0.0` — placeholder node only (no shipped scope)
- `0.1` — FastAPI bootstrap → JWT decode → `get_db()` session → `GET /health` → 8-layer middleware chain
- `0.2` — Alembic revision chain → `appointment360` DB ↔ `tkdjob` DB separation → migration CI gate → schema freeze
- `0.3` — Gateway clients: `ConnectraClient` / `TkdjobClient` / `LambdaEmailClient` → `X-API-Key` contract → timeout/error envelope
- `0.4` — JWT → role resolution → credit hook → `@require_role` guard → protected GraphQL resolver
- `0.5` — Client → `POST /uploads/initiate` → presigned S3 URL → S3 multipart PUT → `POST /uploads/complete` → `s3storage-metadata-worker` lambda
- `0.6` — `POST /jobs/create` → Kafka `JOBS_TOPIC` → consumer → processor registry → `job_node` state machine (`open→in_queue→processing→completed`) → `job_events`
- `0.7` — VQL parse → ES `match_phrase` / `match` → ES ID list → PG hydrate → in-memory join → UUID5 dedup → response
- `0.8` — Next.js shell → GraphQL context → JWT Bearer → role gate → page visibility logic → DocsAI `architecture.md` → `admin/constants.py` sync
- `0.9` — Chrome extension MV3 → `chrome.storage.local` → `lambdaClient.js` → `POST /v1/save-profiles` → Sales Navigator service → Connectra bulk upsert
- `0.10` — Docker Compose health-check → SAM `template.yaml` → `/health` probe per service → Secrets Manager baseline → CI/CD pipeline exit gate

---

## Files to change

### Group A — Master checklist and index

- `[docs/0. Foundation.../0.x-master-checklist.md](docs/0.%20Foundation%20and%20pre-product%20stabilization%20and%20codebase%20setup/0.x-master-checklist.md)` — add cross-service risk matrix, patch micro-gate template, and minor→risk mapping table.
- `[docs/0. Foundation.../README.md](docs/0.%20Foundation%20and%20pre-product%20stabilization%20and%20codebase%20setup/README.md)` — add era summary and cross-reference to new sections in version files.

### Group B — Version files (all 11)

Each gets the **same structural treatment** with **different content** per minor:

- Replace generic "Runtime focus" diagram with minor-specific mermaid
- Replace all task-track bullets with specific, service-anchored tasks
- Add 8 missing sections (Backend API scope, DB lineage scope, Frontend UX scope, UI elements checklist, Flow/Graph delta, Cross-service ownership, Audit/Compliance, Patch ladder + Release Gate + Evidence)

Files: `0.0 — Pre-repo baseline.md` through `0.10 — Ship & ops hardening.md`

### Group C — Sparse task packs (5 files to expand)

- `[connectra-foundation-task-pack.md](./README.md)` — expand with `connectra-codebase-analysis.md` execution queue (persistent queue, ES-PG reconciliation, per-tenant rate limits, VQL contract tests)
- `[s3storage-foundation-task-pack.md](./README.md)` — expand with `s3storage-codebase-analysis.md` gaps (durable multipart, env-driven worker name, metadata RMW race, E2E upload tests)
- `[contact-ai-foundation-task-pack.md](./README.md)` — add `ModelSelection` enum freeze, global `API_KEY` parameterization, JSONB schema baseline
- `[emailapis-foundation-task-pack.md](./README.md)` — add provider drift control, status semantic vocabulary freeze, bulk correctness tests
- `[logsapi-foundation-task-pack.md](./README.md)` — add S3 CSV lineage (not MongoDB), static API key rotation plan, query scalability baseline

---

## Section template (applied to every version file)

Every `0.N — <Title>.md` will have these sections after the existing Flowchart + Task Tracks:

```
## Backend API and Endpoint Scope
## Database and Data Lineage Scope
## Frontend UX Surface Scope
## UI Elements Checklist
## Flow / Graph Delta for This Minor
## Cross-service ownership
## Audit and Compliance Notes
## Patch ladder (0.N.0 – 0.N.9)
## Release Gate and Evidence
### Master Task Checklist
### Backend API and Endpoints
### Database and Data Lineage
### Frontend UX
### UI Elements
### Flow and Graph
### Validation
### Release Gate
```

---

## Key source files used for content

- Codebase analyses: `docs/codebases/*.md` (per service)
- Architecture: `docs/architecture.md`
- Backend: `docs/backend.md`
- Audit: `docs/audit-compliance.md`
- Flowchart: `docs/flowchart.md`
- Versions: `docs/versions.md`, `docs/version-policy.md`

