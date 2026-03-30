---
name: Contact360 Full System Plan
overview: "Comprehensive plan covering: (1) five new/enhanced Go/Gin services in `EC2/`, (2) documentation updates across all canonical hubs and era folders, (3) Python CLI normalization of all era task files with evidence-backed completion records."
todos:
  - id: job-rename
    content: Rename job.server go.mod module from vivek-ray to contact360.io/jobs and fix all internal imports
    status: pending
  - id: job-dockerfile
    content: Add Dockerfile to EC2/job.server (multi-stage, copy email campaign pattern)
    status: pending
  - id: job-complete
    content: "Add missing job.server features: health/live/ready, job/{uuid}, DAG convenience routes, worker pool in consumer, recovery loop, job_events writes, Processor registry"
    status: pending
  - id: s3storage-scaffold
    content: "Create EC2/s3storage.server scaffold: go.mod (contact360.io/s3storage), cmd/api/main.go, cmd/worker/main.go, Dockerfile"
    status: pending
  - id: s3storage-core
    content: Implement EC2/s3storage.server internal/s3store (AWS SDK v2) and internal/csv (field ordering, hourly key, append with mutex)
    status: pending
  - id: s3storage-routes
    content: "Implement EC2/s3storage.server Gin routes: /api/v1/health, /buckets, /files, /uploads (multipart), /analysis, /avatars"
    status: pending
  - id: s3storage-worker
    content: "Implement EC2/s3storage.server Asynq worker: storage:metadata task (port metadata_job.py: HEAD, range-read, sniff, row count)"
    status: pending
  - id: ai-scaffold
    content: "Create EC2/ai.server scaffold: go.mod (contact360.io/ai), cmd/api/main.go, cmd/worker/main.go, Dockerfile"
    status: pending
  - id: ai-hf-client
    content: "Implement EC2/ai.server internal/hf client: chat completions (stream + non-stream), embeddings, retry 503/429, model fallback list"
    status: pending
  - id: ai-routes
    content: "Implement EC2/ai.server Gin routes: /health, /ai/email/analyze, /ai/company/summary, /ai/filters/parse, /ai-chats CRUD + /message + /message/stream (SSE)"
    status: pending
  - id: ai-rag
    content: "Implement EC2/ai.server RAG: text chunking, HF embed batch, cosine similarity (port rag_service.py)"
    status: pending
  - id: log-scaffold
    content: "Create EC2/log.server scaffold: go.mod (contact360.io/logsapi), cmd/api/main.go, cmd/worker/main.go, Dockerfile"
    status: pending
  - id: log-core
    content: Implement EC2/log.server internal/csvlog (CSV write/read, hourly key, per-bucket mutex for append) and internal/s3store
    status: pending
  - id: log-routes
    content: "Implement EC2/log.server Gin routes: POST /logs, POST /logs/batch, GET /logs, GET /logs/search, GET/PUT/DELETE /logs/{id}, POST /logs/delete"
    status: pending
  - id: log-worker
    content: "Implement EC2/log.server Asynq worker: logs:flush (write-behind) and logs:sweep (TTL purge per LOG_TTL_DAYS)"
    status: pending
  - id: ext-scaffold
    content: "Create EC2/extension.server scaffold: go.mod (contact360.io/extension), cmd/api/main.go, cmd/worker/main.go, Dockerfile"
    status: pending
  - id: ext-core
    content: Implement EC2/extension.server internal/mapper (port mappers.py, normalization.py, utils.py) and internal/connectra HTTP client with retry
    status: pending
  - id: ext-routes
    content: "Implement EC2/extension.server Gin routes: POST /v1/save-profiles (dedup, chunk 500, parallel contact+company upsert). Document /v1/scrape as extension-side only."
    status: pending
  - id: ext-worker
    content: "Implement EC2/extension.server worker pool: bounded channel + N goroutines for Connectra chunk calls"
    status: pending
  - id: docs-arch
    content: "Update docs/docs/architecture.md: add Request paths subsection with mermaid, update service register with Go targets for new EC2 services"
    status: pending
  - id: docs-strategy
    content: "Update docs/docs/backend-language-strategy.md: add Satellite migration inventory table for s3storage, logs, ai, extension services"
    status: pending
  - id: docs-frontend
    content: "Update docs/docs/frontend.md: add Frontend stack policy subsection (Next.js-only for web; Django + Chrome MV3 exceptions), clarify email REST/GraphQL split"
    status: pending
  - id: docs-codebase
    content: "Update docs/docs/codebase.md: add Primary API entry column (GraphQL/REST/mixed) to service table"
    status: pending
  - id: docs-backend-map
    content: "Update docs/docs/backend.md: add Orchestration paragraph (Python gateway as facade to Go satellites)"
    status: pending
  - id: docs-flowchart
    content: "Update docs/docs/flowchart.md: update Core request flow mermaid to include new EC2 services and Next.js label"
    status: pending
  - id: docs-governance
    content: "Update docs/docs/governance.md: add rules for browser-facing APIs (GraphQL only) and new services (Go/Gin default)"
    status: pending
  - id: docs-compliance
    content: "Update docs/docs/audit-compliance.md: add compliance notes for new EC2 services"
    status: pending
  - id: docs-docsai
    content: "Update docs/docs/docsai-sync.md: add sync step for Go service list changes in architecture constants"
    status: pending
  - id: docs-backend-readme
    content: "Update docs/backend/README.md: add rows for s3storage.server, ai.server, log.server, extension.server with Target runtime: Go"
    status: pending
  - id: docs-main-readme
    content: "Update docs/README.md: align Stack column with Go targets, add connection column (GraphQL/mixed/internal)"
    status: pending
  - id: docs-frontend-readme
    content: "Update docs/frontend/README.md: add Django admin and Chrome extension exception rows"
    status: pending
  - id: cli-baseline
    content: "Run: cd docs && python cli.py scan && python cli.py audit-tasks && python cli.py task-report && python cli.py name-audit"
    status: pending
  - id: cli-era-0
    content: "Era 0: era-guide, task-report, audit-tasks, fill-tasks dry-run then apply, dedup-tasks, rename-docs"
    status: pending
  - id: cli-era-1
    content: "Era 1: era-guide, task-report, audit-tasks, fill-tasks dry-run then apply, dedup-tasks, rename-docs"
    status: pending
  - id: cli-era-2
    content: "Era 2: era-guide, task-report, audit-tasks, fill-tasks dry-run then apply, dedup-tasks, rename-docs"
    status: pending
  - id: cli-era-3
    content: "Era 3: era-guide, task-report, audit-tasks, fill-tasks dry-run then apply, dedup-tasks, rename-docs"
    status: pending
  - id: cli-era-4
    content: "Era 4: era-guide, task-report, audit-tasks, fill-tasks dry-run then apply, dedup-tasks, rename-docs"
    status: pending
  - id: cli-era-5
    content: "Era 5: era-guide, task-report, audit-tasks, fill-tasks dry-run then apply, dedup-tasks, rename-docs"
    status: pending
  - id: cli-era-6
    content: "Era 6: era-guide, task-report, audit-tasks, fill-tasks dry-run then apply, dedup-tasks, rename-docs"
    status: pending
  - id: cli-era-7
    content: "Era 7: era-guide, task-report, audit-tasks, fill-tasks dry-run then apply, dedup-tasks, rename-docs"
    status: pending
  - id: cli-era-8
    content: "Era 8: era-guide, task-report, audit-tasks, fill-tasks dry-run then apply, dedup-tasks, rename-docs"
    status: pending
  - id: cli-era-9
    content: "Era 9: era-guide, task-report, audit-tasks, fill-tasks dry-run then apply, dedup-tasks, rename-docs"
    status: pending
  - id: cli-era-10
    content: "Era 10: era-guide, task-report, audit-tasks, fill-tasks dry-run then apply, dedup-tasks, rename-docs"
    status: pending
  - id: evidence-format
    content: "After CLI structural pass: replace generic filled bullets with code-path + API-response + test-result evidence using the template: Evidence / API / Tests / Done because"
    status: pending
  - id: status-promote
    content: "For each era with evidence attached: python cli.py update --status completed --era N --dry-run then apply; sync versions.md + roadmap.md per governance rule"
    status: pending
isProject: false
---

# Contact360 Full System Plan

## System Architecture (target state)

```mermaid
flowchart LR
  subgraph clients [Clients]
    AppNext["Next.js app"]
    RootNext["Next.js root"]
    EmailNext["Next.js email"]
    Extension["Chrome Extension MV3"]
    DocsAI["Django DocsAI admin"]
  end
  subgraph gateway [Python GraphQL Gateway]
    GQL["contact360.io/api\nFastAPI + Strawberry\nGraphQL"]
  end
  subgraph satellites [Go/Gin Satellite Services - EC2]
    Sync["EC2/sync.server\ncontact360.io/sync"]
    Jobs["EC2/job.server\ncontact360.io/jobs"]
    Email["EC2/email.server\ngithub.com/ayan/emailapigo"]
    Campaign["EC2/email campaign\ncontact360.io/emailcampaign"]
    S3["EC2/s3storage.server\ncontact360.io/s3storage NEW"]
    AI["EC2/ai.server\ncontact360.io/ai NEW"]
    Logs["EC2/log.server\ncontact360.io/logsapi NEW"]
    Ext["EC2/extension.server\ncontact360.io/extension NEW"]
  end
  subgraph workers [Background Workers]
    JobWorker["job.server consumer"]
    CampaignWorker["emailcampaign-worker"]
    S3Worker["s3storage-worker NEW"]
    AIWorker["ai-worker NEW"]
    LogWorker["log-worker NEW"]
    ExtWorker["extension-worker NEW"]
  end
  AppNext --> GQL
  RootNext --> GQL
  EmailNext --> GQL
  EmailNext -->|"REST mailbox"| Email
  Extension --> GQL
  Extension -->|"save-profiles REST"| Ext
  DocsAI --> GQL
  GQL --> Sync
  GQL --> Jobs
  GQL --> Email
  GQL --> Campaign
  GQL --> S3
  GQL --> AI
  GQL --> Logs
  GQL --> Ext
  Jobs --> JobWorker
  Campaign --> CampaignWorker
  S3 --> S3Worker
  AI --> AIWorker
  Logs --> LogWorker
  Ext --> ExtWorker
```



---

## Part 1 — Go/Gin Backend Services (`EC2/`)

### 1-A: Rename `job.server` module

**Problem:** `EC2/job.server/go.mod` uses module `vivek-ray` instead of `contact360.io/jobs`.

**Files:**

- `[EC2/job.server/go.mod](EC2/job.server/go.mod)` — change `module vivek-ray` → `module contact360.io/jobs`
- All `*.go` files under `EC2/job.server/` — update import paths
- Add missing `Dockerfile` (copy pattern from `[EC2/email campaign/Dockerfile](EC2/email campaign/Dockerfile)`)

### 1-B: `job.server` feature completion

**Source reference:** `backend(dev)/jobs/`

Missing vs Python source:

- `GET /health/live`, `GET /health/ready` (only `GET /health` exists)
- `GET /api/v1/jobs/{uuid}` (only `GET /jobs/` and bulk-insert exist)
- `POST /api/v1/jobs/email-export`, `contact360-import`, `contact360-export` convenience DAG builders
- Worker pool inside consumer (currently inline `switch job.JobType` with TODO)
- Stale `processing` recovery loop (`PROCESSING_TIMEOUT`)
- Per-job execution timeout
- `job_events` table writes on state transitions
- `Processor` interface + registry keyed by `job_type`
- Prometheus metrics endpoint

**Key files to create/extend:**

- `EC2/job.server/server/routes.go` — add missing routes
- `EC2/job.server/jobs/consumers/base.go` — add worker pool (`chan` + N goroutines)
- `EC2/job.server/models/` — add `job_event.go` + repo
- `EC2/job.server/Dockerfile` — new, multi-stage

### 1-C: NEW `EC2/s3storage.server/`

**Source reference:** `backend(dev)/s3storage/`

Structure mirrors `[EC2/email campaign/](EC2/email campaign/)`:

```
EC2/s3storage.server/
├── cmd/api/main.go         -- Gin server
├── cmd/worker/main.go      -- Asynq worker
├── internal/config/        -- S3STORAGE_* env vars
├── internal/s3store/       -- AWS SDK v2: PutObject, GetObject, ListObjects, HeadBucket
├── internal/csv/           -- CSV read/write, field ordering, hourly-key helpers
├── internal/metadata/      -- Port metadata_job.py: HEAD, range-read, sniff, row-count
├── internal/api/router.go  -- /api/v1: health, buckets, files, uploads, analysis, avatars
├── go.mod                  -- module contact360.io/s3storage
└── Dockerfile
```

**Key contracts to match:**

- `POST /api/v1/uploads/initiate-csv` — multipart, with `X-Idempotency-Key`
- `GET /api/v1/uploads/{id}/parts/{n}` — presigned URL
- `POST /api/v1/uploads/{id}/complete`, `DELETE .../abort`
- `GET /api/v1/analysis/…` — schema, stats (port csv_analysis.py)
- `GET /api/v1/avatars/…`
- Worker task type: `storage:metadata` — enqueue after upload complete

### 1-D: NEW `EC2/ai.server/`

**Source references:** `backend(dev)/contact.ai/` + `backend(dev)/resumeai/`

Structure:

```
EC2/ai.server/
├── cmd/api/main.go         -- Gin server
├── cmd/worker/main.go      -- Asynq worker (heavy resume/ATS tasks)
├── internal/config/        -- HF_API_KEY, HF_CHAT_MODEL, HF_FALLBACK_MODELS, etc.
├── internal/hf/            -- HF router client: /v1/chat/completions, /v1/embeddings
│   ├── client.go           -- non-stream + stream, retry 503/429, model fallback
│   └── rag.go              -- chunk text, embed batch, cosine similarity
├── internal/api/router.go  -- routes below
├── internal/db/            -- ai_chats Postgres repo (sqlc or bun)
└── Dockerfile
```

**HF endpoint (from both codebases):**
`https://router.huggingface.co/v1/chat/completions`
`https://router.huggingface.co/v1/embeddings`

**Routes to implement (priority order):**

1. `GET /health`, `GET /health/ready`
2. `POST /ai/email/analyze` — email risk JSON
3. `POST /ai/company/summary` — company summary
4. `POST /ai/filters/parse` — NL → filter JSON
5. `POST /ai-chats/` CRUD + `/message` + `/message/stream` (SSE)
6. Worker: `ai:resume_parse`, `ai:ats_score` for heavy resume flows

### 1-E: NEW `EC2/log.server/`

**Source reference:** `backend(dev)/logs.api/`

Structure:

```
EC2/log.server/
├── cmd/api/main.go
├── cmd/worker/main.go      -- TTL sweeper + write-behind flush
├── internal/config/        -- API_KEY, S3_BUCKET_NAME, AWS_REGION
├── internal/s3store/       -- PutObject, GetObject, ListObjectsV2, DeleteObject, HeadBucket
├── internal/csvlog/        -- CSV write/read, field order, hourly key, append (with mutex)
├── internal/api/router.go  -- routes below
└── Dockerfile
```

**Critical design decision:** `append_logs_to_csv` is read-modify-write — Go port must use per-bucket mutex OR single-writer channel per hourly key to avoid lost rows.

**Routes:**

- `POST /logs` — single log
- `POST /logs/batch` — max 100
- `GET /logs` — filter + paginate
- `GET /logs/search` — full-text over CSV
- `GET /logs/{id}`, `PUT /logs/{id}`, `DELETE /logs/{id}`
- `POST /logs/delete` — bulk delete by body

**Worker tasks:** `logs:flush` (write-behind batch), `logs:sweep` (TTL purge)

### 1-F: NEW `EC2/extension.server/`

**Source reference:** `backend(dev)/salesnavigator/`

Structure:

```
EC2/extension.server/
├── cmd/api/main.go
├── cmd/worker/main.go      -- bounded parallel Connectra chunks
├── internal/config/        -- API_KEY, CONNECTRA_API_URL, CONNECTRA_API_KEY
├── internal/connectra/     -- HTTP client with tenacity-equivalent retry
├── internal/mapper/        -- port mappers.py, normalization.py, utils.py
├── internal/api/router.go  -- /v1/save-profiles, /v1/scrape (optional)
└── Dockerfile
```

**Priority:** `POST /v1/save-profiles` — profile dedup, map, chunk (500), parallel contacts + companies via Connectra.
**Optional/defer:** `POST /v1/scrape` (BeautifulSoup → goquery, fragile; document as "parse in extension, not server").

---

## Part 2 — Documentation Updates

### 2-A: Canonical Hub Files (edit first, derive others from these)

**Files to update:**

1. `[docs/docs/architecture.md](docs/docs/architecture.md)`
  - Add **"Request paths"** subsection with the mermaid diagram above
  - Update **Service register** table: add EC2 targets (`s3storage.server`, `ai.server`, `log.server`, `extension.server`) with current lang = Python → target = Go
  - Update **Canonical service ownership** table language column
2. `[docs/docs/backend-language-strategy.md](docs/docs/backend-language-strategy.md)`
  - Add **"Satellite migration inventory"** table: service, current lang, target Go, blocker, evidence link
  - Remove `logs.api`, `s3storage`, `salesnavigator` from "still Python" once Go services ship
3. `[docs/docs/frontend.md](docs/docs/frontend.md)`
  - Add **"Frontend stack policy"** subsection: Next.js-only for web apps; Django DocsAI + Chrome MV3 are explicit exceptions
  - Clarify email REST vs GraphQL split explicitly
4. `[docs/docs/codebase.md](docs/docs/codebase.md)`
  - Add `Primary API entry` column to repo table: GraphQL / REST / mixed
5. `[docs/docs/backend.md](docs/docs/backend.md)`
  - Add **"Orchestration pattern"** paragraph: Python gateway as facade to Go satellites
6. `[docs/docs/flowchart.md](docs/docs/flowchart.md)`
  - Update **"Core request flow"** mermaid to include new EC2 services and Next.js explicit label
7. `[docs/docs/governance.md](docs/docs/governance.md)`
  - Add rule: new browser-facing data APIs → GraphQL only; exceptions require doc approval
  - Add rule: new HTTP services → Go/Gin by default
8. `[docs/docs/audit-compliance.md](docs/docs/audit-compliance.md)`
  - Add compliance notes for new EC2 services (s3storage, logs, extension, ai)
9. `[docs/docs/docsai-sync.md](docs/docs/docsai-sync.md)`
  - Add sync step when Go service list changes (architecture constants mirror)
10. `[docs/docs/version-policy.md](docs/docs/version-policy.md)` and `[docs/docs/versions.md](docs/docs/versions.md)`
  - No changes unless a migration milestone is scheduled; add only if Go services are version-tagged

### 2-B: Backend Doc Tree

1. `[docs/backend/README.md](docs/backend/README.md)`
  - Registry table: add rows for `s3storage.server`, `ai.server`, `log.server`, `extension.server` pointing to their codebase analyses
    - Note "Target runtime: Go" column
2. `[docs/backend/services.apis/](docs/backend/services.apis/)`
  - Add or update `s3storage.api.md`, `logsapi.api.md`, `contact.ai.api.md`, `salesnavigator.api.md` with Go target notes
3. `[docs/backend/endpoints/](docs/backend/endpoints/)`
  - Update `*_endpoint_era_matrix` files for new Go services when routes finalize

### 2-C: Frontend Doc Tree

1. `[docs/frontend/README.md](docs/frontend/README.md)`
  - Already has 3 Next.js rows; add explicit "Django admin = exception, extension = MV3" row

### 2-D: Main Hub

1. `[docs/README.md](docs/README.md)`
  - Service consolidation table: align Stack column with target Go for 5 services
    - Add connection column: GraphQL / mixed / internal

---

## Part 3 — Era Task Normalization (Python CLI)

### 3-A: Baseline scan (read-only, run first)

```bash
cd docs
python cli.py scan
python cli.py audit-tasks          # full tree gaps
python cli.py task-report          # all eras
python cli.py name-audit           # filename hygiene
```

### 3-B: Per-era CLI pass (eras 0–10, sequential)

For each era N:

```bash
python cli.py era-guide --era N                    # read master docs
python cli.py task-report --era N                  # see which files need tracks
python cli.py audit-tasks --era N                  # find empty/missing/dup
python cli.py fill-tasks --era N                   # DRY-RUN, review output
python cli.py fill-tasks --era N --apply           # only after dry-run approval
python cli.py dedup-tasks --era N                  # DRY-RUN
python cli.py dedup-tasks --era N --apply
python cli.py name-audit --era N                   # filename check
python cli.py rename-docs --era N                  # DRY-RUN, then --apply if needed
```

### 3-C: Evidence-backed task completion (per era, human-driven)

**Template per completed bullet** (to add in the task file):

```markdown
- [x] <task description>
  - Evidence: <code path OR test command + result>
  - API: <GraphQL operation OR REST route + status + key response fields>
  - Tests: <pytest/go test scope; green on commit XYZ or CI job name>
  - Done because: <one sentence reason>
```

**Era-to-evidence mapping:**


| Era | Contract evidence                              | Test evidence                            |
| --- | ---------------------------------------------- | ---------------------------------------- |
| 0   | Compose health, CI yml                         | `docker compose config`, smoke health    |
| 1   | `14_BILLING_MODULE.md`, `09_USAGE_MODULE.md`   | Billing + credit integration tests       |
| 2   | `15_EMAIL_MODULE.md`, bulk endpoints           | Email pipeline + bulk job tests          |
| 3   | `03_CONTACTS_MODULE.md`, VQL contract          | Search, import/export tests              |
| 4   | `23_SALES_NAVIGATOR_MODULE.md`, extension save | Extension contract + save-profiles tests |
| 5   | `17_AI_CHATS_MODULE.md`, HF chat/embed         | AI service tests, rate-limit behavior    |
| 6   | SLO baselines, idempotency spec                | Load/retry/chaos tests                   |
| 7   | Deploy runbooks, RBAC matrix                   | Staged deploy checklist, authz tests     |
| 8   | Public API matrices, compat suite              | Contract tests, partner compat           |
| 9   | Webhook + entitlement contracts                | Integration + security tests             |
| 10  | Campaign send/track contracts                  | Campaign worker tests                    |


### 3-D: Status promotion

After evidence is attached per era:

```bash
python cli.py update --status completed --era N --dry-run
python cli.py update --status completed --era N   # after review
```

Sync hubs per `docs/docs/governance.md` rule: when any era file changes status, update `docs/docs/versions.md` + `docs/docs/roadmap.md` in the same change set.

---

## Execution Order

1. **Part 1-A** — Fix `job.server` module name (unblocks correct imports for 1-B)
2. **Part 1-B** — Complete `job.server` feature gaps
3. **Part 1-C through 1-F** — Create 4 new EC2 services (can be done in parallel)
4. **Part 2-A** — Update canonical hub docs (architecture, frontend, strategy, governance)
5. **Part 2-B through 2-D** — Backend/frontend/hub sub-docs
6. **Part 3-A** — CLI baseline scan
7. **Part 3-B** — Per-era CLI structural normalization (eras 0–10)
8. **Part 3-C through 3-D** — Evidence attachment and status promotion per era

