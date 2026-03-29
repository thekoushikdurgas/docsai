# Contact360 Docs Hub

Master navigation and execution entry for the `docs/` tree.

## Core source-of-truth files

- Architecture and ownership: `docs/architecture.md`
- Compliance and controls: `docs/audit-compliance.md`
- Backend operating map: `docs/backend.md`
- Frontend operating map: `docs/frontend.md`
- Roadmap stages: `docs/roadmap.md`
- Version policy and era taxonomy: `docs/version-policy.md`
- Release history and planning: `docs/versions.md`
- Governance and sync runbook: `docs/governance.md`, `docs/docsai-sync.md`

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

### Lambda services codebase task status

| Service | Codebase | P0 issues | Key tasks (era) |
| --- | --- | --- | --- |
| `lambda/logs.api` | Python FastAPI + S3 CSV | `.env.example` missing; `validate_env.py` MongoDB drift; no `LOG_TTL_DAYS` sweeper; `samconfig.toml` has hardcoded API key | `0.5` Ops, `6.4`–`6.6` Service, `7.0` Ops, `8.0`–`8.1` Contract |
| `lambda/s3storage` | Python FastAPI + S3 | `x_idempotency_key` NameError; `STORAGE_QUOTA_BYTES` missing; worker double-prefix; `FilesystemBackend.upload_file` absent; direct-backend leakage; SAM CORS `*`; `samconfig.toml` real secrets | `0.5` Service/Ops, `2.0` Contract/Service, `6.6` Service, `7.0` Ops, `8.0` Contract |
| `lambda/emailapis` | Python FastAPI + PostgreSQL | **`samconfig.toml` real secrets (P0)**; `CONNECTRA_BASE_URL` hardcoded IP; Truelist→Mailvetter migration incomplete; no tests; no `.env.example`; no samconfig dev/prod split | `0.3` Ops, `2.0` Service, `6.5` Service, `7.0` Ops, `8.0`/`8.1` Contract |
| `lambda/emailapigo` | Go Gin + PostgreSQL | `CONNECTRA_BASE_URL`/`MAILVETTER_BASE_URL` hardcoded IPs; no `samconfig.toml`; no tests; router TODO for missing endpoints; no `LOG_BASE_URL` wiring | `0.3` Ops, `2.0` Service, `6.4` Service, `7.0` Ops, `8.1` Contract |
| `extension/contact360` | Chrome MV3 + Python FastAPI (salesnavigator Lambda) | **`content.js` is 9-line stub** (no DOM scraping); **`background.js` no message handler** (no orchestration); `manifest.json` overly broad host_permissions; `graphqlSession.js` ES module in non-module context; **no `samconfig.toml`** for Lambda; **`CONNECTRA_API_URL` hardcoded IP** in template.yaml; `constants.js` missing; no `X-Idempotency-Key` on save-profiles; no CORS on Lambda; template.yaml Output references undefined resource | `0.3`/`0.9` Ops/Service, `3.0` Data, `4.0`–`4.2` Service/Surface, `6.4`/`6.5` Service, `7.0` Ops, `8.0` Contract |
| `contact360.io/sync` (Connectra) | Go Gin + PostgreSQL + Elasticsearch + S3 + Cobra CLI | **Module name is `vivek-ray`** (P0 hygiene); **`.env` committed** to repo; **`connectra.exe` binary committed**; **MongoDB dead code** in `clients/mongo.go`; `.example.env` missing 11+ fields; **SN provenance fields absent** from contacts schema (`source`, `lead_id`, `search_id`); **`uploadURLTTL` hardcoded** (ignores config); **no migration tool**; **global rate limiter** (not per-key); **no `X-Request-ID`**; **shallow `/health`** (no PG/ES check); **no `X-RateLimit-*` headers**; no docker-compose; no OpenAPI spec | `0.3` Ops/Service, `3.0` Data/Service, `4.2` Service, `6.4`/`6.5` Service, `7.0` Ops, `8.0` Contract |
| `contact360.io/root` (marketing site) | Next.js 16 + React 19 + TypeScript + GraphQL Pages API | **All marketing pages `"use client"`** -- no SSR/SSG, zero SEO HTML for crawlers; **no sitemap.xml / robots.txt**; **no per-page OpenGraph metadata**; **`.env.local` committed** to repo; **`AuthProvider` + `RoleProvider` in root layout** (auth overhead on every public page); **`IP_API_URL` uses HTTP** (`http://ip-api.com/json`) -- mixed content on HTTPS; **no CSP headers** in `next.config.js`; **live pricing never fetched** (`fetchPlans: false` default); **EC2 deploy script hardcodes IP** `54.196.224.143`; **no GitHub Actions CI/CD**; **no analytics** (GA4/Plausible); no dedicated `/pricing` page route | `0.3` Ops, `0.8` Surface, `7.0` Ops, `8.0` Contract/Surface, `9.0` Surface |
| `contact360.io/jobs` (job scheduler) | Python FastAPI + Kafka + PostgreSQL + OpenSearch + S3 (async job scheduler) | **`S3_UPLOAD_FILE_PATH_PRIFIX` typo** in config/env/compose; **docker-compose healthcheck for schedulers/consumer always passes** (`sys.exit(0)`); **healthcheck for API checks `/docs` not `/health/ready`**; **global rate limiter** (not per-API-key); **no `X-RateLimit-*` headers** on 429; **no `X-Request-ID` propagation**; **priority column added by migration but scheduler doesn't use it**; **OpenSearch scroll context leaks on failed exports**; **`example.env` missing 9 worker-pool tuning vars**; **no job cancellation endpoint**; VQL named `Vivek Query Language` (personal alias in prod code); single-stage Dockerfile | `0.6` Service/Data/Ops, `2.0` Service/Ops, `3.0` Data/Service, `6.4`/`6.5` Service, `7.0` Ops, `8.0` Contract, `10.0` Ops |
| `contact360.io/email` (Mailhub email client) | Next.js 16 + React 19 + TypeScript (IMAP email client frontend) | **IMAP password stored in `localStorage` in plaintext** (`imap-context.tsx` serializes `ImapConfig.password`); **`X-Email` + `X-Password` sent as headers on every email API call** (raw IMAP password on every GET request); **no `.env.example`** (`NEXT_PUBLIC_BACKEND_URL` non-null asserted without reference file); **`app/layout.tsx` title is `Create Next App`** (placeholder); **no route protection** (any unauthenticated user can navigate to `/inbox`); **`console.log(BACKEND_URL)`** in production landing page; **`data.json` mock stub checked in** (600-line template file not related to emails); **no compose email UI** (no compose route/component); **all `Authorization: Bearer` headers commented out** (no functioning JWT auth); userId stored but token never set | `0.3`/`0.8` Ops/Surface, `1.0` Service, `2.0` Surface, `5.0` AI, `7.0` Ops, `8.0` Contract, `9.0` Surface |
| `contact360.io/app` (Dashboard SPA) | Next.js 16 + React 19 + TypeScript + GraphQL (main user dashboard) | **AI Chat page is fully mocked** (`mockSend()` hardcoded, no real AI API connected); **Live Voice page is fully mocked** (fake `MOCK_TRANSCRIPTIONS`, no WebRTC); **no Content-Security-Policy headers** in `next.config.js`; **JWT tokens stored in `localStorage`** (XSS risk); **`graphqlClient.ts` retries non-idempotent billing mutations** (potential double-charge); **`settings/page.tsx` is a redirect stub** (no settings functionality); **`appointments` route is empty** (404); **`DashboardAccessGate` returns `null` for denied access** (no upgrade prompt); **`GRAPHQL_URL` defaults to HTTP** not HTTPS; **raw private IP in `.env.example`** | `0.3`/`0.8` Service/Surface, `1.0` Service, `2.0` Surface, `3.0` Surface, `4.2` Surface, `5.0` AI, `6.4`/`6.5` Service, `7.0` Ops, `8.0` Contract, `9.0` Surface |

| `contact360.io/api` (GraphQL API) | Python FastAPI + Strawberry GraphQL + PostgreSQL + S3/AWS (main backend API) | **`.env` committed to repo** with real `SECRET_KEY`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, PostgreSQL password (P0 — rotate immediately); **`ALLOWED_ORIGINS=*` + `TRUSTED_HOSTS=*`** in production `.env` (CORS fully open); **`campaigns` module directory is empty** (no files, not even `__init__.py` — 10.x feature missing); **`endpoints` and `postman` module directories also empty**; **`two_factor/setup2FA` uses raw hex as TOTP secret** (not `pyotp` — 2FA non-functional); **`ENABLE_LAMBDA_LOGGING=False`** in production (all structured logs silently dropped); **`UPLOAD_SESSION_USE_REDIS=False`** (multi-worker upload sessions fail); **`docker-compose.yml` has stale MongoDB service** (unused); **`CONNECTRA_BASE_URL`/`TKDJOB_API_URL`/`DOCSAI_API_URL`** default to hardcoded EC2 IPs in `config.py` | `0.3` Ops/Service, `1.0` Service, `2.0` Service, `3.0` Data/Service, `4.2` Service, `5.0` AI, `6.4`/`6.5` Service, `7.0` Ops, `8.0` Contract, `9.0` Surface, `10.0` Ops |
| `contact360.io/admin` (Django Admin) | Python Django 4.x + SQLite/PostgreSQL + Tailwind CSS + Django-Q + GitHub Actions CI (22-app SuperAdmin panel) | **`.env` committed with real `AWS_ACCESS_KEY_ID=AKIAQWV3TPUBZ6LF4CEQ` + `AWS_SECRET_ACCESS_KEY` (second distinct AWS credential pair)**; **`db.sqlite3` committed to repo** (contains user/session/model data); **`.env.prod` is only 2 lines** (missing `SECRET_KEY`, `AWS_*`, `ALLOWED_HOSTS`, `DEBUG=False`, `GRAPHQL_ENABLED` — completely unusable for production); **`GRAPHQL_AUTH_ENABLED=True` but login checks `GRAPHQL_ENABLED`** (env var mismatch breaks login); **`USE_LOCAL_JSON_FILES=True`** (docs served from local files, not S3); **`operations/views.py` system status is hardcoded** `'operational'`; **`page_builder` is a shell** (no drag-and-drop, no save/preview); **`durgasflow` n8n library reads from local `media/`** (fails in stateless containers); **no user/billing management UI** (admin cannot manage users/subscriptions); **no campaign management UI** (10.x missing) | `0.3` Ops, `0.8` Surface, `1.0` Service/Surface, `5.0` AI, `6.4` Service, `7.0` Ops, `8.0` Contract, `9.0` Surface, `10.0` Surface |

| `backend(dev)/contact.ai` (Contact AI Lambda) | Python 3.12 FastAPI + SQLAlchemy asyncpg + PostgreSQL + Hugging Face Inference + AWS Lambda/SAM (NexusAI CRM assistant microservice) | **`samconfig.toml` NOT in `.gitignore`** and contains real credentials: `ApiKey=bc7a0177...`, `DatabaseUrl=postgresql+asyncpg://koushik:koushik9933454265@98.81.200.121:5432/contact360`, `HfApiKey=hf_TlQQLXgAmHb...` (P0 — rotate all); **`template.yaml` Lambda `Timeout: 30s` but `HF_TIMEOUT_SECONDS=120`** (Lambda cuts off AI inference calls mid-response); **`template.yaml` uses `python3.11`** but dev is Python 3.12 (runtime mismatch); **`AI_RATE_LIMIT_*` configured but never enforced** (no middleware wired); **`HF_EMBED_MODEL` configured but no embedding endpoint exists**; **no `.env.example`** (15+ required env vars undocumented); **CORS `allow_origins=["*"]`** in main.py | `0.3` Ops/Contract, `5.0` AI/Service, `6.4` Service, `7.0` Ops, `8.0` Contract |
| `backend(dev)/email campaign` (Email Campaign Engine) | Go 1.24 + Gin + Asynq/Redis + PostgreSQL + AWS S3 + SMTP + IMAP (email campaign delivery microservice) | **`.env` committed** with real `EMAIL_PASSWORD="yddx thnr krqg egzb"` (Gmail app password), `DB_HOST=98.81.200.121`, `DB_USER=koushik`, `DB_PASSWORD=koushik9933454265`, `AWS_ACCESS_KEY_ID=AKIAQWV3TPUB3YHK6ZHW`, `AWS_SECRET_ACCESS_KEY=...`, `JWT_SECRET=...` (**fourth distinct AWS credential pair** — rotate all); **Go module name is `github.com/RajRoy75/email-campaign`** (personal handle in production code); **Redis hardcoded to `localhost:6379`** in both API and worker (non-deployable); **`cmd/main.go` validates `DATABASE_URL` but `db.Connect()` uses `DB_HOST/PORT/USER/PASS`** (env var mismatch); **no Dockerfile or docker-compose** (cannot deploy to cloud); **no open/click tracking** (only delivery counts); **no campaign scheduling** (`scheduled_at` field missing); **no `GET /campaigns` list endpoint** (`ListCampaigns()` exists but not wired); **template cache has no TTL** (stale renders after S3 update); **recipients only from CSV** (no Connectra integration) | `0.3` Ops, `2.0` Service, `6.4` Service, `7.0` Ops, `8.0` Contract, `10.0` Service/Data |
| `backend(dev)/salesnavigator` (Sales Navigator Lambda) | Python 3.11 FastAPI + BeautifulSoup4 + httpx/tenacity + Pydantic v2 + Mangum + AWS Lambda/SAM (SN HTML scraping and profile save microservice) | **`.example.env` contains real production credentials** (`API_KEY=bc7a0177...`, `CONNECTRA_API_URL=http://18.234.210.191:8000`, `CONNECTRA_API_KEY=3e6b8811...` — committed example file with live keys; rotate immediately); **`template.yaml` `ConnectraApiUrl` default is hardcoded EC2 IP** `http://18.234.210.191:8000`; **`template.yaml` uses `python3.11`** (P1 — mismatch with 3.12 ecosystem); **in-process rate limiter (`threading.Lock`) not effective in Lambda** (per-container, bypassed by concurrent invocations); **no Account/company search result scraping** (only LEAD type); **no CI/CD pipeline**; **no CloudWatch structured metrics**; **no OpenAPI snapshot in `docs/backend/apis/`** | `0.3` Ops, `4.2` Service, `6.4` Service, `7.0` Ops, `8.0` Contract |

Use the CLI commands in **Managing tasks across all era folders** to audit and fill tasks for each service.

## Managing tasks across all era folders (`0`–`10`)

Use this loop to keep **every** era folder’s task files consistent, auditable, and aligned with the codebase. Run commands from the `docs/` directory (`cd docs`).

### A. Orient (what to read, what to ship)

| Step | Action |
| --- | --- |
| A1 | Open `docs/versions.md` and `docs/roadmap.md` for the target minor/patch. |
| A2 | Run `python cli.py era-guide` for the full 11-era map, or `python cli.py era-guide --era N` for one era’s master-doc pointers and execution checklist. |
| A3 | Open that era’s `README.md` and the active `X.Y.Z — …md` files listed there. |

### B. Measure (health of docs and tasks)

| Step | Command | Purpose |
| --- | --- | --- |
| B1 | `python cli.py scan` | Global dashboard: file counts, statuses, task bullet totals. |
| B2 | `python cli.py stats --era N` | Per-file status table for one era. |
| B3 | `python cli.py task-report --era N` | Per patch/minor file: which of the five tracks have content (`✓` vs `—`). |
| B4 | `python cli.py audit-tasks --era N` | Missing tracks, empty sections, duplicate bullets (omit `--era` for **all** eras). |
| B5 | `python cli.py name-audit --era N` | Version/codename in filenames; duplicate `X.Y.Z` keys (omit `--era` for all folders). |

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

- **`python main.py`**: menus **7–9** mirror `audit-tasks`, `fill-tasks`, `dedup-tasks`; **10–11** mirror `name-audit` / `rename-docs`; **12** is `era-guide`.  
- Same flags apply when you use `cli.py` directly for scripting or CI.

## CLI Manager & Scripts

To manage documentation status, find orphaned files, and automate updates, use the local python scripts provided in the `docs` root.

### 1. Interactive Manager (`main.py`)

Run `python main.py` to start an interactive wizard with options to:

- View status dashboards and detailed progress per Era.
- Bulk update status markers across era-folders or single files.
- Normalize all markers for consistency.
- Find unused/unreferenced files in the tree.
- Task audit / fill / dedup, era filename audit, canonical file renames, and era guide (menus 7–12).

### 2. Command Line Interface (`cli.py`)

For headless or shell-scripted execution, use the CLI (see **Managing tasks across all era folders** above for workflows):

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

Interactive `python main.py` also exposes these flows (menus 7–12).

### 3. Internal Scripts Architecture (`scripts/`)

Behind the scenes, the root CLI files are backed by this modular python ecosystem:

- `scanner.py`: Extracts and parses documentation header metadata (Status, Coverage, Version).
- `stats.py`: Transforms logic into visually robust `rich` UI tracking boards.
- `updater.py`: Handles string substitution and AST-like structural text modifications safely.
- `unused.py`: Validates the referential integrity mapping and flags dangling docs files.
- `models.py`: Establishes strictly typed enumerations representing document logic layers (like `Status`).
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
