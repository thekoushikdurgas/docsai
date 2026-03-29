# Email system architecture exploration
_Exported on 3/24/2026 at 01:26:29 GMT+5:30 from Cursor (2.6.20)_

---

**User**

Explore D:\code\ayan\contact\contact360.io\api with medium thoroughness. Focus on email-related architecture and behavior. Return: (1) architecture map, (2) key files/modules for email system, (3) end-to-end request flow to final email outcome including scoring/verification if present, (4) top risks/gaps and missing tests.

---

**Cursor**

I’ll inspect the `contact360.io/api` codebase now and map the email architecture, flow, and risks. I’ll start by locating the core email-related modules/endpoints, then trace request-to-outcome behavior and note test coverage gaps.

I’ve found the primary GraphQL email surface and config knobs; next I’m tracing the underlying clients, job/export pipeline, and tests to build the end-to-end flow and identify gaps.

I’ve confirmed the main email and scheduler mutation/query paths; next I’m checking job status/result retrieval and test coverage breadth to complete the end-to-end flow and risk assessment.

## 1) Architecture Map (Email System)

- **GraphQL entrypoints**: Email domain is exposed under `Query.email` and `Mutation.email` in `D:\code\ayan\contact\contact360.io\api\app\graphql\schema.py`.
- **Email query layer**: `D:\code\ayan\contact\contact360.io\api\app\graphql\modules\email\queries.py` handles:
  - `findEmails`, `findEmailsBulk`
  - `verifySingleEmail`, `verifyEmailsBulk`
  - convenience job creators: `createEmailFinderExportJob`, `createEmailVerifyExportJob`, `createEmailPatternImportJob`
- **Email mutation layer**: `D:\code\ayan\contact\contact360.io\api\app\graphql\modules\email\mutations.py` handles:
  - `addEmailPattern`, `addEmailPatternBulk`
- **External integration clients**:
  - `D:\code\ayan\contact\contact360.io\api\app\clients\lambda_email_client.py` -> Lambda Email API (finder/verifier/pattern endpoints)
  - `D:\code\ayan\contact\contact360.io\api\app\clients\tkdjob_client.py` -> tkdjob scheduler (async export/import workflows)
  - shared HTTP retry/error behavior in `D:\code\ayan\contact\contact360.io\api\app\clients\base.py`
- **Persistence for async jobs**:
  - model: `D:\code\ayan\contact\contact360.io\api\app\models\scheduler_job.py`
  - repository: `D:\code\ayan\contact\contact360.io\api\app\repositories\scheduler_job.py`
  - GraphQL read access: `D:\code\ayan\contact\contact360.io\api\app\graphql\modules\jobs\queries.py`
- **Cross-cutting behavior**:
  - Auth gate via `require_auth(...)`
  - Input validation in `email/inputs.py` + extra string/email validation helpers
  - Activity/usage/credit side effects in query/mutation handlers
  - Config wiring via `D:\code\ayan\contact\contact360.io\api\app\core\config.py` (`LAMBDA_EMAIL_*`, `TKDJOB_*`)

## 2) Key Files/Modules for Email System

- `D:\code\ayan\contact\contact360.io\api\app\graphql\modules\email\queries.py` (main request orchestration)
- `D:\code\ayan\contact\contact360.io\api\app\graphql\modules\email\mutations.py` (pattern creation)
- `D:\code\ayan\contact\contact360.io\api\app\graphql\modules\email\inputs.py` (request constraints: max 50 contacts, max 10k emails, provider values)
- `D:\code\ayan\contact\contact360.io\api\app\graphql\modules\email\types.py` (response model incl. verification fields)
- `D:\code\ayan\contact\contact360.io\api\app\clients\lambda_email_client.py` (all email API endpoint calls)
- `D:\code\ayan\contact\contact360.io\api\app\graphql\modules\jobs\mutations.py` (email export/import job creation)
- `D:\code\ayan\contact\contact360.io\api\app\graphql\modules\jobs\queries.py` + `jobs/types.py` (track final async outcome/status/timeline/DAG)
- `D:\code\ayan\contact\contact360.io\api\app\models\scheduler_job.py` + `repositories\scheduler_job.py` (job ownership/state storage)
- `D:\code\ayan\contact\contact360.io\api\app\clients\base.py` (retry rules, timeout/network/API error normalization)
- `D:\code\ayan\contact\contact360.io\api\app\core\config.py` (email and scheduler env configuration)

## 3) End-to-End Request Flow -> Final Email Outcome (including verification/scoring)

### A) Finder flow (`findEmails` / `findEmailsBulk`)
1. GraphQL request hits `Query.email.findEmails` or `findEmailsBulk`.
2. `require_auth` enforces auth; inputs are validated (`email/inputs.py` + additional length checks).
3. Resolver calls `LambdaEmailClient.find_emails(...)` or `.find_emails_bulk(...)`.
4. `LambdaEmailClient` sends POST to:
   - `/email/finder/` (single)
   - `/email/finder/bulk` (bulk)
5. Response mapped into GraphQL types (`EmailResult`, `BulkEmailFinderResult`).
6. Non-blocking side effects:
   - credit deduction attempted (`findEmails`: 1, `findEmailsBulk`: `len(items)`)
   - activity logging attempted
7. Final immediate outcome: list of discovered emails with `status`, `source`, `total`, and bulk processing counts.

### B) Verification flow (`verifySingleEmail` / `verifyEmailsBulk`)
1. GraphQL request reaches email query resolver.
2. Email(s) normalized to lowercase; provider defaults to `"truelist"` (allowed: `truelist`, `icypeas`).
3. Calls `LambdaEmailClient.verify_single_email(...)` or `.verify_emails_bulk(...)` -> POST:
   - `/email/single/verifier/`
   - `/email/bulk/verifier/`
4. Resolver maps result(s) into `VerifiedEmailResult`.
5. Verification/scoring-style output exposed:
   - `status` (`valid`/`invalid`/`catchall`/`unknown`)
   - `email_state`, `email_sub_state`
   - `certainty` (confidence-like field from provider)
   - aggregate counts in bulk: `valid_count`, `invalid_count`, `catchall_count`, `unknown_count`
6. Activity logged (success/failed) non-blocking.
7. Final immediate outcome: verification decision and quality/confidence metadata per email.

### C) Pattern creation flow (`addEmailPattern`, `addEmailPatternBulk`)
1. Auth + input validation.
2. Resolver calls Lambda endpoints:
   - `/email-patterns/add`
   - `/email-patterns/add/bulk`
3. Response mapped to pattern records (`pattern_format`, `pattern_string`, `domain`, `contact_count`, timestamps).
4. Final immediate outcome: stored/inferred company email pattern metadata.

### D) Async export/import flow to “final outcome”
1. User triggers job mutations (`createEmailFinderExport`, `createEmailVerifyExport`, `createEmailPatternImport`) via `jobs` module (or email query convenience wrappers).
2. API builds payload and calls tkdjob endpoint (`/api/v1/jobs/email-export`, `/email-verify`, `/email-pattern-import`).
3. On success, local `scheduler_jobs` row is created with ownership and initial payloads.
4. User polls `jobs.job(...)` / `jobs.jobs(...)`; `SchedulerJob` type also exposes live fields:
   - `statusPayload` (progress/runtime errors)
   - `timelinePayload`
   - `dagPayload`
5. Final email outcome for async operations is represented by job terminal status (`completed` / `failed`) + scheduler payload content.

## 4) Top Risks/Gaps and Missing Tests

### Top risks/gaps
- **Hardcoded sensitive defaults in config/client**:
  - `TKDJOB_API_KEY` and fallback hardcoded in `config.py`/`tkdjob_client.py`; also several default URLs/keys present. This is a security risk and environment drift risk.
- **Side-effect durability gaps**:
  - Credit deduction and activity logging are non-blocking best-effort; failures don’t fail request. This can produce unbilled usage or incomplete audit trails.
- **Debug file writes inside request paths**:
  - Manual `_debug_log` file writes in email modules and extra debug append in jobs mutation can cause IO overhead, local path fragility, and potential data leakage.
- **Error normalization may leak upstream details**:
  - Service errors are surfaced as `"Email service error: ..."` / `"Job scheduler error: ..."`; depending on upstream messages this can expose internals.
- **Type/response contract fragility**:
  - Some handlers assume dict shape; when upstream schema shifts, code often degrades to `BadRequestError("Invalid response format...")` without fallback parsing.

### Missing tests (major)
- Only one focused email-related test found: `D:\code\ayan\contact\contact360.io\api\tests\graphql\test_jobs_email_verify.py` (validation error case only).
- Missing coverage for:
  - `findEmails`, `findEmailsBulk` success/error mapping
  - `verifySingleEmail`, `verifyEmailsBulk` provider validation + response mapping (`certainty`, counts)
  - `addEmailPattern`, `addEmailPatternBulk`
  - credit deduction behavior by role
  - activity logging fail-open behavior
  - tkdjob create + ownership checks + polling fields (`statusPayload`, `timelinePayload`, `dagPayload`)
  - retries/error handling from `BaseHTTPClient` for 5xx/timeouts/network errors

If you want, I can next give you a prioritized test plan (unit + integration) with concrete test cases and mock boundaries for these modules.

