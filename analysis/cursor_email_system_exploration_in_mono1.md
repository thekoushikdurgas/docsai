# Email system exploration in monorepo
_Exported on 3/24/2026 at 01:27:20 GMT+5:30 from Cursor (2.6.20)_

---

**User**

Explore D:\code\ayan\contact\contact360.io as a monorepo with medium thoroughness. Focus specifically on the complete email system across repos/services. Return: (1) high-level architecture map of all components involved in email workflows, (2) key modules/files per component, (3) end-to-end flow from UI to final output including sync and async paths, (4) major cross-service risks/mismatches, (5) testing/observability gaps, (6) prioritized small task breakdown for improving the overall email system.

---

**Cursor**

I’ll map the email system across `contact360.io` end-to-end by first discovering repo structure, then tracing email-related modules (UI, APIs, workers, providers, templates, queues, logs/tests), and finally synthesize risks and a prioritized improvement plan. I’m starting with a broad scan and then drilling into the highest-signal files.

I hit an unexpected empty listing at the provided path, so I’m verifying parent directories to locate the actual monorepo contents before tracing email flows.

I can read files directly, so next I’m locating repo boundaries by searching for manifests and email-related filenames under `contact360.io`, then I’ll stitch the cross-service flow.

I’ve now traced the API layer and confirmed both synchronous email calls and async job creation paths. Next I’m reading the app-side GraphQL wiring plus jobs service processors to build a precise UI→API→worker flow map and identify mismatches.

## 1) High-level architecture map (email workflows across monorepo)

`contact360.io` has a split email system with **two execution planes**:

- **Synchronous plane (interactive UI actions)**  
  `app` (Next.js) -> `api` GraphQL (`email` module) -> `lambda email API` via `LambdaEmailClient` for:
  - single/bulk email finder
  - single/bulk email verifier
  - add email pattern (single/bulk)

- **Asynchronous plane (CSV batch jobs)**  
  `app` upload + job creation -> `api` GraphQL (`jobs` module) -> `tkdjob` REST -> `jobs` service (FastAPI + scheduler + consumer + processors) -> external email API + S3 output -> status reflected back in `api.scheduler_jobs` -> `app` Jobs page polling + download.

- **Admin/ops surface**  
  `admin` has its own `tkdjob_client` to inspect/retry scheduler jobs directly, parallel to main app.

---

## 2) Key components/modules/files by role

- **UI + client orchestration (`app`)**
  - `D:\code\ayan\contact\contact360.io\app\app\(dashboard)\email\page.tsx`
  - `D:\code\ayan\contact\contact360.io\app\src\services\graphql\emailService.ts`
  - `D:\code\ayan\contact\contact360.io\app\src\services\graphql\jobsService.ts`
  - `D:\code\ayan\contact\contact360.io\app\src\hooks\useEmailFinderSingle.ts`
  - `D:\code\ayan\contact\contact360.io\app\src\hooks\useEmailVerifierBulk.ts`
  - `D:\code\ayan\contact\contact360.io\app\src\hooks\useCsvUpload.ts`
  - `D:\code\ayan\contact\contact360.io\app\app\(dashboard)\jobs\page.tsx`
  - `D:\code\ayan\contact\contact360.io\app\src\lib\jobs\jobsMapper.ts`

- **GraphQL API orchestration (`api`)**
  - `D:\code\ayan\contact\contact360.io\api\app\graphql\modules\email\queries.py`
  - `D:\code\ayan\contact\contact360.io\api\app\graphql\modules\email\mutations.py`
  - `D:\code\ayan\contact\contact360.io\api\app\clients\lambda_email_client.py`
  - `D:\code\ayan\contact\contact360.io\api\app\graphql\modules\jobs\mutations.py`
  - `D:\code\ayan\contact\contact360.io\api\app\clients\tkdjob_client.py`
  - `D:\code\ayan\contact\contact360.io\api\app\graphql\modules\jobs\queries.py`
  - `D:\code\ayan\contact\contact360.io\api\app\repositories\scheduler_job.py`
  - `D:\code\ayan\contact\contact360.io\api\app\core\config.py`

- **Job scheduler/execution service (`jobs`)**
  - `D:\code\ayan\contact\contact360.io\jobs\app\api\v1\routes\jobs.py`
  - `D:\code\ayan\contact\contact360.io\jobs\app\schemas\jobs.py`
  - `D:\code\ayan\contact\contact360.io\jobs\app\processors\email_finder_export_stream.py`
  - `D:\code\ayan\contact\contact360.io\jobs\app\processors\email_verify_export_stream.py`
  - `D:\code\ayan\contact\contact360.io\jobs\app\processors\email_pattern_import_stream.py`
  - `D:\code\ayan\contact\contact360.io\jobs\app\clients\email_api.py`
  - `D:\code\ayan\contact\contact360.io\jobs\app\workers\scheduler.py`
  - `D:\code\ayan\contact\contact360.io\jobs\app\workers\consumer.py`
  - `D:\code\ayan\contact\contact360.io\jobs\app\metrics\collector.py`
  - docs: `jobs\docs\EMAIL_EXPORT.md`, `jobs\docs\EMAIL_PATTERN_IMPORT.md`, `jobs\docs\dags\*.md`

- **Admin job operations (`admin`)**
  - `D:\code\ayan\contact\contact360.io\admin\apps\admin\services\tkdjob_client.py`

---

## 3) End-to-end flow (UI -> final output), sync + async

- **Sync: single finder/verify**
  - User submits from Email page.
  - `app` calls GraphQL email operations from `emailService.ts`.
  - `api` validates input, authenticates, calls `LambdaEmailClient`.
  - Lambda email API responds immediately; GraphQL maps result and returns to UI.
  - `api` also does activity logging and (finder) credit deductions.

- **Sync: bulk verifier via text area**
  - User pastes emails in UI bulk verifier text mode.
  - `useEmailVerifierBulk` parses list -> GraphQL `verifyEmailsBulk`.
  - Same synchronous `api -> LambdaEmailClient -> UI` loop; no scheduler job involved.

- **Async: CSV finder export**
  - User uploads CSV (`useCsvUpload` multipart S3 flow).
  - UI calls `createEmailFinderExport` GraphQL.
  - `api` `jobs.mutations` sends payload to tkdjob `/api/v1/jobs/email-export`, stores local scheduler row.
  - `jobs` service creates node `email_finder_export_stream`.
  - Scheduler/consumer execute processor: stream CSV from S3, verify existing/find missing emails, multipart-upload result CSV to S3, checkpoint progress.
  - UI Jobs page polls list/detail and uses returned S3 key for download.

- **Async: CSV verify export**
  - Same as above, but GraphQL mutation `createEmailVerifyExport` -> tkdjob `/email-verify` -> processor `email_verify_export_stream` annotates `email_status`.
  - Output is final verified CSV in S3.

- **Async: email pattern import**
  - SuperAdmin path.
  - UI or jobs modal sends `createEmailPatternImport` -> tkdjob `/email-pattern-import`.
  - Processor `email_pattern_import_stream` streams CSV rows and POSTs batched items to external `/email-patterns/add/bulk`; progress tracked by checkpoint bytes/rows.
  - No final CSV output; output is external API side-effects + job status.

---

## 4) Major cross-service risks/mismatches

- **Hardcoded credential fallback in API->tkdjob client**  
  `api/app/clients/tkdjob_client.py` uses `_TKDJOB_API_KEY_FALLBACK` when env key missing. This is high risk (secret leakage, accidental prod coupling).

- **Debug file writes embedded in GraphQL code paths**  
  `api/app/graphql/modules/jobs/mutations.py` and `api/app/graphql/modules/email/queries.py` include direct file logging (`open(..., "a")`) to local paths. Risk: unexpected I/O, environment mismatch, sensitive payload logging.

- **Naming/schema drift between docs and implementation**
  - Jobs README still describes legacy DAG job types, while processor registry now uses single-stream processors.
  - `jobs/docs` correctly mention single-stream; root README/older docs can mislead operators.
  - `EmailExportDAGRequest` includes `email_column`, but processors largely use `csv_columns` and add their own output columns; potential confusion.

- **Progress semantics can be misleading after resume**
  - Some processors use byte checkpoints while skipping/re-reading headers and/or scanning from start before resume logic, making percent less exact under retries.

- **Dual source of truth for job state**
  - `api` stores local `scheduler_jobs` and may hydrate from tkdjob on miss; potential divergence if sync/update fails.
  - UI maps status from `statusPayload` + `responsePayload`; status consistency depends on periodic refresh and update hygiene.

- **Async bulk verifier inefficiency**
  - In `email_verify_export_stream.py`, verification is effectively per-email wrapped around bulk API calls; this can amplify request count/latency under large files.

---

## 5) Testing + observability gaps

- **Sparse email integration tests**
  - API tests found mainly one validation test: `api/tests/graphql/test_jobs_email_verify.py`.
  - No strong end-to-end tests for: upload -> job create -> processor completion -> downloadable output validation.

- **No dedicated jobs email processor tests**
  - `jobs/tests` has no focused tests for `email_finder_export_stream`, `email_verify_export_stream`, `email_pattern_import_stream` behavior under retries, malformed CSV, partial uploads, resume correctness.

- **Observability mostly logs, limited traceability**
  - Metrics collector exists but appears in-memory singleton style and not clearly exported/persisted end-to-end.
  - Limited correlation IDs between `app` request, `api` mutation, tkdjob UUID, and downstream email API calls.
  - Runtime errors captured in payloads, but no clear alerting thresholds for repeated batch failures or degraded verifier success rates.

- **No explicit contract tests between `api` and `jobs` request/response schemas**
  - Given active evolution from DAG -> stream, contract drift risk is high without schema snapshot/contract tests.

---

## 6) Prioritized small task breakdown (incremental improvements)

- **P0 – Safety and correctness**
  - Remove hardcoded tkdjob API key fallback; fail fast when missing env.
  - Remove/guard ad-hoc file debug logging from hot paths; route through structured logger only.
  - Add a schema contract test suite for `api`->`tkdjob` payload/response for `email-export`, `email-verify`, `email-pattern-import`.

- **P1 – Reliability**
  - Add processor unit/integration tests for:
    - checkpoint resume correctness
    - partial multipart upload recovery
    - malformed/empty CSV handling
    - external API timeout/backoff behavior
  - Add one smoke e2e: upload sample CSV -> create job -> poll completion -> validate output file shape/status column.

- **P1 – Performance**
  - Refactor verify-export processor to use true batched verify calls (avoid per-email wrapper pattern).
  - Standardize batch size/concurrency env controls and enforce sane upper bounds in one shared config module.

- **P2 – Observability**
  - Introduce end-to-end correlation ID propagated from `app` -> `api` -> tkdjob -> processor logs.
  - Emit durable metrics counters (jobs started/completed/failed, API retry count, external email API latency/error rate) with dashboard + alerts.

- **P2 – Documentation alignment**
  - Consolidate email workflow docs into one canonical architecture doc; clearly deprecate legacy DAG docs/readme sections.
  - Add “source of truth” table for job types, payload keys, output keys, and owning service.

---

If you want, I can next produce a **single dependency/sequence diagram** (text + mermaid) for the email system, plus a **test matrix** mapping each risk to concrete tests.

