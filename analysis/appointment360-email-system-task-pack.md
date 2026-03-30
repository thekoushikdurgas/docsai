# Appointment360 (contact360.io/api) — Era 2.x Email System Task Pack

## Codebase file map (high-value for `2.x`)

Grounded in [`docs/codebases/appointment360-codebase-analysis.md`](../codebases/appointment360-codebase-analysis.md).

| Area | Paths (start here) | Notes |
| --- | --- | --- |
| GraphQL composition | `contact360.io/api/app/graphql/schema.py` | Root `Query`/`Mutation` assembly |
| Context lifecycle | `contact360.io/api/app/graphql/context.py` | JWT decode → `Context.user` |
| Email module | `contact360.io/api/app/graphql/modules/email/queries.py` and `mutations.py` | Finder/verifier/patterns mapping to Lambda Email |
| Jobs module | `contact360.io/api/app/graphql/modules/jobs/queries.py` and `mutations.py` | Create/list/poll/retry mapping to TKD Job |
| Downstream clients | `contact360.io/api/app/clients/lambda_email_client.py`, `tkdjob_client.py` | Outbound headers, timeouts, retries |
| Middleware and guards | `contact360.io/api/app/core/middleware.py` | Request/trace IDs, idempotency, abuse guard, rate limiting |

## 2.x GraphQL surface (canonical docs pointers)

| Domain | Docs contract | What must stay in sync |
| --- | --- | --- |
| Email module | `docs/backend/apis/15_EMAIL_MODULE.md` | Types, error envelopes, status vocabulary |
| Jobs module | `docs/backend/apis/16_JOBS_MODULE.md` | Job create/poll/retry semantics; `SchedulerJob` fields |
| AI chats (email risk) | `docs/backend/apis/17_AI_CHATS_MODULE.md` | `analyzeEmailRisk` if wired in era |

## Contract track

| Task | Priority |
| --- | --- |
| Define `EmailQuery { findEmails, findEmailsBulk, verifySingleEmail, verifyEmailsBulk }` types | P0 |
| Define `EmailMutation { addEmailPattern, addEmailPatternBulk }` | P0 |
| Define `JobQuery { job(jobId), jobs(limit,offset,status,jobType) }` | P0 |
| Define `JobMutation { createEmailFinderExport, createEmailVerifyExport, createEmailPatternImport, retryJob }` | P0 |
| Define shared `SchedulerJob` GraphQL type with `status`, `timeline`, `dag`, `result_url` | P0 |
| Define `EmailFinderInput`, `EmailVerifierInput`, `BulkEmailInput`, `EmailPatternInput` types | P0 |
| Document email module in `docs/backend/apis/15_EMAIL_MODULE.md` | P1 |
| Document jobs module in `docs/backend/apis/16_JOBS_MODULE.md` | P1 |

---

## Service track

| Task | Priority |
| --- | --- |
| Implement `LambdaEmailClient` in `app/clients/lambda_email_client.py` | P0 |
| Wire `findEmails` query → `LambdaEmailClient.find_single(email_input)` | P0 |
| Wire `findEmailsBulk` query → `LambdaEmailClient.find_bulk(...)` | P0 |
| Wire `verifySingleEmail` query → `LambdaEmailClient.verify_single(...)` | P0 |
| Wire `verifyEmailsBulk` query → `LambdaEmailClient.verify_bulk(...)` | P0 |
| Wire `addEmailPattern` mutation → `LambdaEmailClient.add_pattern(...)` | P0 |
| Implement `TkdjobClient` in `app/clients/tkdjob_client.py` | P0 |
| Wire `createEmailFinderExport` mutation → `TkdjobClient.create_email_export(...)` | P0 |
| Wire `createEmailVerifyExport` mutation → `TkdjobClient.create_email_verify(...)` | P0 |
| Wire `createEmailPatternImport` mutation → `TkdjobClient.create_email_pattern_import(...)` | P0 |
| Wire `job(jobId)` query → `TkdjobClient.get_job_status(job_id)` | P0 |
| Wire `jobs()` query → `TkdjobClient.list_jobs(...)` | P0 |
| Remove inline debug file writes from `email/queries.py` and `jobs/mutations.py` | P0 |
| Add credit deduction: deduct per email find/verify operation | P0 |

---

### Immediate execution queue (codebase-derived)

1. Remove all inline debug file writes in email/jobs GraphQL modules (explicit risk flagged by the codebase analysis).
2. Ensure `/graphql` production configuration enables rate limiting (do not rely on dev defaults).
3. Enforce and forward `X-Request-Id` and `X-Trace-Id` through **all** outbound clients.
4. Add contract parity tests: `docs/backend/apis/15_EMAIL_MODULE.md` and `16_JOBS_MODULE.md` → resolver/schema expectations.

## Surface track

| Task | Priority |
| --- | --- |
| `/email` page, Finder tab → `query findEmails` / `query findEmailsBulk` binding | P0 |
| `/email` page, Verifier tab → `query verifySingleEmail` / `query verifyEmailsBulk` binding | P0 |
| CSV upload on Email Verifier/Finder → `mutation createEmailFinderExport` / `createEmailVerifyExport` | P0 |
| Jobs list table on `/email` → `query jobs(jobType:"email_export")` binding | P0 |
| Job status progress bar → polling `query job(jobId)` every 2s | P0 |
| Download result button → `mutation s3.getDownloadUrl(key)` after job complete | P1 |
| `useEmailFinderSingle` hook: call `findEmails`, show spinner while pending | P0 |
| `useEmailFinderBulk` hook: upload CSV, create export job, poll status | P0 |
| `useEmailVerifierSingle` hook: call `verifySingleEmail` | P0 |
| `useJobStatus` hook: polling wrapper for `query job(jobId)` | P0 |
| Add email pattern modal → `mutation addEmailPattern` binding | P1 |

---

### Frontend hook bindings (expected callers)

Grounded in `docs/frontend/hooks-services-contexts.md` and UI bindings docs.

| UI capability | Hook/service | GraphQL operation |
| --- | --- | --- |
| Finder (single) | `useEmailFinderSingle` / `emailService` | `email.findEmails` |
| Finder (bulk/export) | `useEmailFinderBulk` + export UX | `jobs.createEmailFinderExport` + `jobs.job(jobId)` polling |
| Verifier (single) | `useEmailVerifierSingle` | `email.verifySingleEmail` |
| Verifier (bulk/export) | `useEmailVerifierBulk` + export UX | `jobs.createEmailVerifyExport` + `jobs.job(jobId)` polling |
| Jobs list/status | `useJobs` / `useJobStatus` | `jobs.jobs(...)` + `jobs.job(jobId)` |
| Files upload (bulk) | `useCsvUpload` / upload service | `upload`/`s3` modules (gateway → s3storage REST) |

## Data track

| Task | Priority |
| --- | --- |
| Create `scheduler_jobs` table (if managed in appointment360 DB): uuid, job_type, status, result_url, user_uuid, created_at | P1 |
| Record activity on email export creation: write to `activities` table | P0 |
| Track credit consumption per email finder/verifier call | P0 |
| Ensure tkdjob `job_id` is stored if job is deferred (for polling) | P0 |

---

## Ops track

| Task | Priority |
| --- | --- |
| Configure `LAMBDA_EMAIL_API_URL` and `LAMBDA_EMAIL_API_KEY` in `.env.example` | P0 |
| Configure `TKDJOB_API_URL` and `TKDJOB_API_KEY` in `.env.example` | P0 |
| Add Postman environment variables for Lambda Email + tkdjob | P1 |
| Write integration test: `findEmails` round-trip with mocked `LambdaEmailClient` | P1 |
| Write integration test: `createEmailFinderExport` → poll `job(jobId)` → status = done | P1 |

---

## Email app surface contributions (era sync)

- Mailbox folder surfaces (`inbox`, `sent`, `spam`, `draft`) use `EmailList` + `DataTable`.
- Email detail route fetches message by id and sanitizes HTML before render.
- Account settings supports IMAP connection and active mailbox switching.
