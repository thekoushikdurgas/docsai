# Contact360 Docs Hub

Master navigation and execution entry for the `docs/` tree.

## Core source-of-truth files

Canonical markdown hubs live under **`docs/docs/`** (not the repo root). CI validates these paths.

- Architecture and ownership: `docs/docs/architecture.md`
- Compliance and controls: `docs/docs/audit-compliance.md`
- Backend operating map: `docs/docs/backend.md`
- Frontend operating map: `docs/docs/frontend.md`
- Roadmap stages: `docs/docs/roadmap.md`
- Version policy and era taxonomy: `docs/docs/version-policy.md`
- Release history and planning: `docs/docs/versions.md`
- Governance and sync runbook: `docs/docs/governance.md`, `docs/docs/docsai-sync.md`
- Codebase map: `docs/docs/codebase.md`
- PostgreSQL vs Redis scope (canonical): `docs/docs/data-stores-postgres.md`
- Python GraphQL spine vs Go/Gin satellite backends (canonical): `docs/docs/backend-language-strategy.md`
- Version maturity hub (also for CI): `docs/VERSION Contact360.md`
- Codebase TODO tag format (era/track/status): `docs/analysis/TODO-COMMENT-CONVENTION.md`

## Era map (`0.x.x` to `10.x.x`)

- `0.x.x` Foundation: `docs/0. Foundation and pre-product stabilization and codebase setup/README.md`
- `1.x.x` User/billing/credit: `docs/1. Contact360 user and billing and credit system/README.md`
- `2.x.x` Email system: `docs/2. Contact360 email system/README.md`
- `3.x.x` Contact/company data: `docs/3. Contact360 contact and company data system/README.md`
- `4.x.x` Extension and Sales Navigator: `docs/4. Contact360 Extension and Sales Navigator maturity/README.md`
- `5.x.x` AI workflows: `docs/5. Contact360 AI workflows/README.md`
- `6.x.x` Reliability and scaling: `docs/6. Contact360 Reliability and Scaling/README.md`
- `7.x.x` Deployment: `docs/7. Contact360 deployment/README.md`
- `8.x.x` Public/private APIs: `docs/8. Contact360 public and private apis and endpoints/README.md`
- `9.x.x` Ecosystem/productization: `docs/9. Contact360 Ecosystem integrations and Platform productization/README.md`
- `10.x.x` Email campaign: `docs/10. Contact360 email campaign/README.md`

### Where tasks live in each era folder

Work is planned in **every** era directory `docs/<0–10>. …/`, not only in `README.md`:

| What | Role |
| --- | --- |
| `README.md` | Era hub: theme, ladder, links to minors/patches. |
| `X.Y.0 — …` (minor) | Release line for that minor; holds detailed **## Tasks** / **## Task tracks**. |
| `X.Y.Z — …` (patch) | Patch-level execution; same task structure as minors. |

Under each **## Tasks** (or **## Task tracks**) block, use five tracks so the CLI can audit and fill consistently:

1. **Contract** — APIs, schemas, external guarantees.  
2. **Service** — backend logic, jobs, integrations.  
3. **Surface** — UI, CLI, extension, emails users see.  
4. **Data** — DB, migrations, lineage, retention.  
5. **Ops** — deploy, observability, runbooks, security ops.

**Mapping code → docs:** after reading code or `docs/codebases/*.md`, add or adjust bullets under the track that matches the change; then run `audit-tasks` and `task-report` for that era to confirm coverage.

**CLI era index** (`--era N`) matches folder order: `0` = Foundation … `10` = Email campaign (same order as the list above).

## Runtime documentation map

- Backend root: `docs/backend/README.md`
- Backend APIs: `docs/backend/apis/README.md`
- Backend data lineage: `docs/backend/database/README.md`
- Backend endpoint matrices: `docs/backend/endpoints/README.md`
- Backend service API pack: `docs/backend/services.apis/README.md`
- Backend Postman validation: `docs/backend/postman/README.md`
- Frontend root: `docs/frontend/README.md`
- Frontend detailed references: `docs/frontend/docs/README.md`
- Frontend page metadata: `docs/frontend/pages/README.md`
- Frontend export data: `docs/frontend/excel/README.md`

## Deploy on AWS (Docker on EC2)

- Topology, diagrams, subdomain matrix: `deploy/aws/SYSTEM_DESIGN.md`
- Data-plane checklist: `deploy/aws/INFRA.md`
- Phase 5 runbook (RDS, OpenSearch, S3/IAM): `deploy/aws/PHASE5_RUNBOOK.md`
- SAM legacy policy: `deploy/DEPRECATED_SAM.md`

## Planning and support hubs

- Deep analysis packs: `docs/analysis/README.md`
- Service deep dives: `docs/codebases/README.md`
- Command governance: `docs/commands/README.md`
- Prompt library: `docs/promsts/README.md`
- Incubation drafts: `docs/ideas/README.md`
- Plan artifacts: `docs/plans/README.md`

## Current execution focus

From `docs/roadmap.md` and `docs/versions.md`:

- Recently released: `1.1.0` (billing maturity).
- In-flight: `1.2.0` (analytics & security baseline) and `2.4` (bulk processing hardening).
- Immediate blockers: storage durability/auth controls, and mapping 1.2 roadmap stages to micro-gates.
- Near-term sequencing: close `1.2` + `2.4` hard gates before `3.x` + `4.x` scale-up.

### Service codebase status (consolidation snapshot)

Long-form risk registers and era tasks live in **`docs/codebases/*-codebase-analysis.md`**. This table is a **high-level delta** after the Docker + Postgres + docs-hygiene program; it is not a substitute for those analyses. **Never commit credentials** — see root `SECURITY.md` and rotate anything exposed historically.

| Area | Stack (target) | Client connection | Done / landed in repo | Still open (see codebases + era docs) |
| --- | --- | --- | --- | --- |
| `contact360.io/api` | GraphQL / FastAPI | **GraphQL** (primary) | Postgres-backed idempotency + upload sessions; local compose without Redis/Mongo; Docker-style downstream URLs in `config.py` | Campaigns module stub; production CORS/hosts tightening; 2FA/TOTP quality |
| `contact360.io/sync` | Go Connectra | **internal** / gateway | Module `contact360.io/sync`; Mongo client removed; `/health` checks PG + OpenSearch; `X-Request-ID`; `X-RateLimit-*` on throttle | SN provenance fields, VQL naming, OpenAPI, per-key rate limits |
| `contact360.io/jobs` + `EC2/job.server` | Python scheduler → **Go** `contact360.io/jobs` | **internal** / gateway | `EC2/job.server`: Dockerfile, `/api/v1` routes, metrics, job_events migration | Parity with Python DAG features; compose wiring |
| `contact360.io/app` / `root` / `email` | Next.js | **GraphQL** (app/root); **mixed** (email REST + GraphQL) | `NEXT_PUBLIC_GRAPHQL_URL` alignment; email `.env.example` + REST/GraphQL notes | Dashboard mocks, Mailhub IMAP security model, CSP, token storage |
| `contact360.io/admin` | Django DocsAI | **internal** | Roadmap/architecture mirrors | — |
| `extension/contact360` | Chrome MV3 | **GraphQL** + REST satellites | Narrow `host_permissions` + `api.contact360.io`; telemetry + GraphQL bearer + S3 presigned helpers | Sales Navigator DOM pipeline, moving save-profiles to GraphQL when ready |
| `lambda/*` (logs, s3storage, emailapis, emailapigo) | Python / Go → **EC2** satellites for logs/s3/ai/extension | **internal** | Dockerfiles; SAM is **legacy** (`deploy/DEPRECATED_SAM.md`); CI `sam-validate-legacy` is non-blocking | `EC2/s3storage.server`, `EC2/log.server`, `EC2/ai.server`, `EC2/extension.server` scaffolds |
| `backend(dev)/email campaign` | Go | **internal** | Module `contact360.io/emailcampaign`; `REDIS_ADDR`; Dockerfile; optional `.env` in containers | DB env consistency, tracking, scheduling, Connectra CSV |
| `backend(dev)/salesnavigator`, `contact.ai`, `mailvetter` | Python / Go | **internal** / **mixed** | Dockerfiles where listed in consolidation plan; compose in root stack | Template defaults, Lambda-vs-Docker config drift |
| `frontend(dev)/joblevel-next` | Next.js | App Router bridge + `lib/graphql`; Dockerfile; CI build; `joblevel` service + `joblevel.contact360.io` in nginx | Replace catch-all with native `app/` routes |
| **Repo infra** | Compose / AWS | `docker-compose.prod.yml`, `nginx/nginx.prod.conf`, `deploy/aws/INFRA.md`, `PHASE5_RUNBOOK.md` | Live RDS / OpenSearch / S3 / IAM in your AWS account |

Use the CLI commands in **Managing tasks across all era folders** to audit and fill tasks for each service.

## Managing tasks across all era folders (`0`–`10`)

Use this loop to keep **every** era folder’s task files consistent, auditable, and aligned with the codebase. Run commands from the `docs/` directory (`cd docs`).

### A. Orient (read hubs, then dashboards)

**Read first (human workflow):** open `docs/versions.md` and `docs/roadmap.md` for the target minor/patch; run `python cli.py era-guide` (or `--era N`) for the 0.x–10.x map; open that era’s `README.md` and the active `X.Y.Z — …md` files.

**CLI — Contact360 Docs Agent menu A** (same IDs as `python main.py`; see also `python cli.py list`):

| Menu | Command | Purpose |
| --- | --- | --- |
| A1 | `python cli.py scan` | Global dashboard: file counts, statuses, task bullet totals. |
| A2 | `python cli.py stats --era N` | Per-file status table for one era. |
| A3 | `python cli.py era-guide` | 0.x–10.x map: master docs, pointers, execution checklist (`--era N` for one era). |
| A4 | `python cli.py task-report [--era N]` | Per patch/minor: which of the five tracks have content (`✓` vs `—`). |
| A5 | `python cli.py stats` | Stats / per-era detail (use with or without `--era` per need). |

Run **A** before **B** when you want dashboards and coverage tables after you know which era to focus on.

### B. Measure (health of docs and tasks)

Workflow commands (**menu B** in `python main.py`):

| Menu | Command | Purpose |
| --- | --- | --- |
| B1 | `python cli.py audit-tasks [--era N]` | Missing tracks, empty sections, duplicate bullets (omit `--era` for **all** eras). |
| B2 | `python cli.py name-audit [--era N]` | Version/codename in filenames; duplicate `X.Y.Z` keys (omit `--era` for all folders). |
| B3 | `python cli.py validate-structure …` | Hub / era / frontend structure (`--prefix`, `--era`, `--kind hub\|era_task\|frontend_page`). |
| B4 | `python cli.py find-unused` | Heuristic: markdown files never referenced by filename elsewhere. |
| B5 | `python cli.py find-duplicate-files [--prefix PATH]` | Duplicate content by SHA-256 (optional prefix to narrow scan). |
| B6 | `python cli.py validate-all [--write-latest]` | Full tree: structure + task audit + naming → optional `docs/result/` + `docs/errors/` JSON. |
| B7 | `python cli.py validate-structure --kind backend_api` | Light prose checks under `backend/apis/`. |
| B8 | `python cli.py validate-structure --kind endpoint_md` | Light prose checks for `backend/endpoints/**/*.md`. |
| B9 | `python cli.py validate-structure --kind codebase_analysis` | Light prose checks under `codebases/`. |
| B10 | `python cli.py format-structure … [--apply]` | Same scope as validate-structure: LF, trim trailing space, EOF newline (default dry-run). |
| B11 | `python cli.py format-all [--apply] [--include-prose] [--write-latest]` | Format validate-all markdown scope; optional prose dirs + `format-latest.json`. |

### C. Fix structure (automated, review before write)

| Step | Command | Notes |
| --- | --- | --- |
| C1 | `python cli.py fill-tasks --era N` | **Dry-run by default** — previews injected `### Contract` … `### Ops` sections and template bullets from `codebase_registry`. |
| C2 | `python cli.py fill-tasks --era N --apply` | Writes only after you agree with the dry-run. |
| C3 | `python cli.py fill-tasks --file path/to/file.md` | Single-file fill (path under `docs/`). |
| C4 | `python cli.py fill-tasks --all` | **All era folders** — use only when you intend a tree-wide pass; always dry-run first. |
| C5 | `python cli.py dedup-tasks --era N` | Dry-run: replace duplicate bullets across sibling patch files with patch-specific lines. |
| C6 | `python cli.py dedup-tasks --era N --apply` | Apply after review. |
| C7 | `python cli.py rename-docs --era N` | Dry-run canonical names `version — Codename.md` (em dash); `--apply` to execute. |

**Rule:** never pass `--apply` on `fill-tasks` or `dedup-tasks` until the dry-run output looks correct.

### D. Fix content (human — codebase-accurate bullets)

| Step | Action |
| --- | --- |
| D1 | Replace generic filled bullets with concrete tasks (files, services, endpoints) from the repo or `docs/backend/`, `docs/frontend/`, `docs/codebases/`. |
| D2 | Set status in the doc header and/or use `python cli.py update --status … --era N` or `--file …` (use `--dry-run` first). |
| D3 | Sync hubs in the same change set when scope is broad: `architecture.md`, `versions.md`, `audit-compliance.md`, `docsai-sync.md` as per `docs/governance.md`. |

### E. Full-tree pass (periodic housekeeping)

1. `python cli.py audit-tasks` (no `--era`) — snapshot of gaps everywhere.  
2. For each era with issues: `task-report` → `fill-tasks --era N` (dry-run) → edit → `--apply` if needed → `dedup-tasks`.  
3. `python cli.py name-audit` then `rename-docs` as needed.  
4. `python cli.py scan` to confirm dashboards.

### Interactive vs CLI

- **`python main.py`**: **Contact360 Docs Agent** — menus **A–G**: **A** orient (dashboards), **B** measure health (audit, structure, unused, duplicates, validate-all, prose kinds), **C** fix structure, **D** status/metadata, **E** maintenance and generation (including **api-test**), **F** data and DB (`data …`, `sql …`), **G** API tests and **`python cli.py list`** (catalog). CLI parity hints appear after each action.
- Same flags apply when you use `cli.py` directly for scripting or CI. Full command reference: [`docs/docs/CLI_README.md`](docs/docs/CLI_README.md).

## Extended docs CLI (structure, optimize, maintenance)

Run from `docs/` (`python cli.py …`). Policy and validation matrix: [`docs/docs/doc-folder-structure-policy.md`](docs/docs/doc-folder-structure-policy.md).

| Command | Purpose |
| --- | --- |
| `python cli.py list [--include-scripts]` | All menu-mapped commands (`docs/scripts/cli_catalog.py` is the catalog source). |
| `python cli.py validate-structure [--prefix PATH] [--era N] [--kind KIND]` | Structure checks. `KIND`: `hub`, `era_task`, `frontend_page` (tree layout), or prose: `backend_api`, `endpoint_md`, `codebase_analysis`. |
| `python cli.py validate-all [--write-latest]` | Merges validate-structure scope + `audit-tasks` + `name-audit` into `docs/result/latest.json` and `docs/errors/latest.json` when `--write-latest`. |
| `python cli.py format-structure … [--apply]` | Same `--prefix` / `--era` / `--kind` as `validate-structure`; whitespace/LF/EOF cleanup (default dry-run). |
| `python cli.py format-all [--apply] [--include-prose] [--write-latest]` | Format the same markdown scope as validate-all structure (optional prose dirs); optional `docs/result/format-latest.json`. |
| `python cli.py optimize-docs report` | Read-only aggregate: scan + task audit + naming + unused count. |
| `python cli.py optimize-docs fix-structure [--apply]` | Chain: `fill-tasks` + `dedup-tasks` + `rename-docs` (dry-run unless `--apply`). |
| `python cli.py maintain-era --era N\|--all --action enrich\|fix-readme-links\|update-minors [--apply] [--dry-run]` | Dispatch era maintenance scripts under `docs/scripts/`. |
| `python cli.py docs-gen create-patches [--eras …] [--apply]` | Subprocess wrapper for `docs_patch_creator.py`. |
| `python cli.py docs-gen flowcharts [--apply]` | Subprocess wrapper for `apply_unique_flowcharts.py`. |
| `python cli.py frontend link-endpoint-specs` | Refresh endpoint link blocks in `frontend/pages/*_page.md`. |
| `python cli.py frontend augment-page-specs [--dry-run\|--apply]` | Refresh design-nav blocks in page specs. |
| `python cli.py find-duplicate-files [--prefix PATH] [--ext .md,.json]` | Report duplicate files by SHA-256 under `docs/`. |
| `python cli.py prune-unused [--apply] [--quarantine PATH] [--include-era-patches]` | Quarantine unused candidates (era folders excluded by default). |
| `python cli.py data …` / `python cli.py sql …` | DB reports, ingest, SQL runner — see **CLI_README** (`data` / `sql` support `--dry-run` where applicable). |
| `python cli.py api-test --postman-env ENV …` | Postman-backed API helpers; put `--postman-env` **before** the subcommand — see **CLI_README**. |

**Paths:** `docs/scripts/paths.py` defines `DOCS_ROOT` / `REPO_ROOT` and `DOCS_RESULT_DIR` / `DOCS_ERRORS_DIR`; era globs in `cli.py` use this (fixes prior `scripts/` vs `docs/` mismatch).

**Separate Typer CLI:** API-only smoke tests via `python scripts/api_cli.py` (from `docs/`) — documented in **CLI_README** under “Contact360 API Testing CLI”.

## CLI Manager & Scripts

To manage documentation status, find orphaned files, and automate updates, use the local python scripts provided in the `docs` root.

### 1. Interactive Manager (`main.py`)

Run `python main.py` to start the **Contact360 Docs Agent** (Rich menu):

- **A–E:** Orient (scan, stats, era-guide, task-report), measure health (validate + `validate-all` + unused + duplicates + **B10/B11** `format-structure` / `format-all`), fix structure, status/metadata, maintenance (`maintain-era`, `docs-gen`, `frontend`, `prune-unused`, `api-test`).
- **F:** Data and DB — `data` subcommands and `sql` (see [`docs/docs/CLI_README.md`](docs/docs/CLI_README.md)).
- **G:** API tests and **`list`** — catalog of CLI equivalents (`cli_catalog.py`).

Version string is shown in the header (`DOCS_AGENT_VERSION` in `main.py`).

### 2. Command Line Interface (`cli.py`)

For headless or shell-scripted execution, use the CLI (see **Managing tasks across all era folders** and **Extended docs CLI**):

- `python cli.py scan`: Evaluates document parsing and yields the global dashboard.
- `python cli.py stats [--era <0-10>]`: Reports detailed file statuses per era.
- `python cli.py update --status <completed|in_progress|planned|incomplete> [--era <X> | --file <path> | --all] [--dry-run]`: Recursively apply tracking status mapping across subsets of docs constraints.
- `python cli.py normalize --status <status>`: Format everything to a consistent tracking structure.
- `python cli.py find-unused`: Scans index references locally mapping orphaned nodes across the directory.
- `python cli.py audit-tasks [--era <0-10>]`: Task-track coverage (Contract/Service/Surface/Data/Ops) and duplicate bullets.
- `python cli.py fill-tasks (--era <X> | --file <path> | --all) [--apply]`: Inject missing track sections (default dry-run).
- `python cli.py dedup-tasks (--era <X> | --all) [--apply]`: Normalize duplicate bullets across patch files (default dry-run).
- `python cli.py task-report [--era <0-10>]`: Per-file track coverage table.
- `python cli.py name-audit [--era <0-10>]`: Parsed version/codename per era `.md` file, duplicate `X.Y.Z` keys, malformed names.
- `python cli.py rename-docs (--era <X> | --all) [--apply]`: Rename to canonical `version — Codename.md` (em dash); default dry-run.
- `python cli.py era-guide [--era <0-10>] [--json]`: Master-docs map per era (roadmap/versions/architecture pointers + execution checklist); default prints all eras as a table.
- `python cli.py validate-all [--write-latest]`, `python cli.py list`: full-tree JSON and command catalog.
- `python cli.py validate-structure …` (including `--kind backend_api|endpoint_md|codebase_analysis`), `optimize-docs …`, `maintain-era …`, `docs-gen …`, `frontend …`, `find-duplicate-files …`, `prune-unused …`, `data …`, `sql …`, `api-test …`: see **Extended docs CLI** and **CLI_README**.

Interactive `python main.py` exposes the same capabilities via the Contact360 Docs Agent menu (**A–G**).

### 3. Internal Scripts Architecture (`scripts/`)

Behind the scenes, the root CLI files are backed by this modular python ecosystem:

- `scanner.py`: Extracts and parses documentation header metadata (Status, Coverage, Version).
- `stats.py`: Transforms logic into visually robust `rich` UI tracking boards.
- `updater.py`: Handles string substitution and AST-like structural text modifications safely.
- `unused.py`: Validates the referential integrity mapping and flags dangling docs files.
- `doc_scan_models.py` + `models/`: Doc `Status` / `DocFile` types live in `doc_scan_models.py`; SQLAlchemy ORM models live in `models/database.py` and are re-exported from `models/__init__.py`.
- `task_auditor.py` / `task_filler.py` / `task_templates.py` / `codebase_registry.py`: Task audit, fill, and registry-backed templates.
- `era_naming.py`: Era folder filename parsing, uniqueness checks, canonical rename planning.
- `contact360_era_guide.py`: Era 0.x–10.x map (master docs, pointers, execution checklist) for `cli.py era-guide`.

## Recommended execution order (single release line)

1. Select minor target in `docs/versions.md` (`X.Y.0`).
2. Confirm stage dependency chain in `docs/roadmap.md`.
3. In the matching era folder under `docs/<N>. …/`, edit minor and patch docs (`X.Y.Z`) with five-track **## Tasks** slices (Contract → Ops).
4. Run `python cli.py task-report --era N` and `python cli.py audit-tasks --era N`; use `fill-tasks` / `dedup-tasks` only where structure is missing or duplicated (dry-run first).
5. Sync impacted docs in the same change set:
   - architecture / roadmap / versions
   - backend endpoint matrix and APIs
   - frontend page bindings
6. Run release micro-gate evidence checks before status promotion (`docs/audit-compliance.md`, `docs/commands/` as applicable).

## Small-task breakdown for maintainers

Use these as a checklist; combine with **Managing tasks across all era folders** for CLI steps.

| # | Task |
| --- | --- |
| 1 | Choose era index `N` (`0`–`10`), target minor `X.Y`, and owning team. |
| 2 | Run `era-guide --era N`; open era `README.md` and patch ladder (`X.Y.0` … `X.Y.9`). |
| 3 | `stats --era N` + `task-report --era N` to see which files need work. |
| 4 | Draft or refine tasks from code / `docs/codebases/`; place bullets under the correct **Contract** … **Ops** track. |
| 5 | `audit-tasks --era N`; fix gaps with manual edits or `fill-tasks --era N` (dry-run → `--apply`). |
| 6 | `dedup-tasks --era N` if duplicate bullets appear across patches (dry-run → `--apply`). |
| 7 | Verify contract parity: `docs/backend/apis`, `docs/backend/endpoints`. |
| 8 | Verify data: `docs/backend/database` lineage when schema or storage changes. |
| 9 | Verify surfaces: `docs/frontend/docs`, `docs/frontend/pages`. |
| 10 | Verify compliance: `docs/audit-compliance.md` for the era. |
| 11 | Sync DocsAI constants per `docs/docsai-sync.md` when architecture or roadmap text changes. |
| 12 | `update --status …` for affected files; record release evidence in `docs/versions.md`. |
| 13 | `name-audit --era N` before release; rename with `rename-docs` if filenames are non-canonical. |
