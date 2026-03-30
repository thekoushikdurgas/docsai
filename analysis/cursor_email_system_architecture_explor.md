# Email system architecture exploration
_Exported on 3/24/2026 at 01:26:16 GMT+5:30 from Cursor (2.6.20)_

---

**User**

Explore D:\code\ayan\contact\contact360.io\api with medium thoroughness. Focus on email-related architecture and behavior. Return: (1) architecture map, (2) key files/modules for email system, (3) end-to-end request flow to final email outcome including scoring/verification if present, (4) top risks/gaps and missing tests.

---

**Cursor**

I’ll scan `D:\code\ayan\contact\contact360.io\api` for email-related modules and trace how requests move through verification/scoring to final sending behavior, then summarize architecture, flow, and risks/tests gaps.

I found the dedicated email GraphQL module and Lambda client entry points; next I’m reading those files plus jobs/scheduler models to reconstruct the full verification/scoring/send flow.

I’ve traced the core email resolvers and clients; I’m now checking job input definitions and docs to confirm exact payload contracts and whether any in-API scoring exists versus passthrough from external services.

## 1) Architecture Map (Email System)

- **Entrypoint:** `POST /graphql` goes through FastAPI middleware, then Strawberry router, then resolver execution in `app/graphql/schema.py` and `app/graphql/context.py`.
- **Email API surface:** Root GraphQL `email` namespace wires to `EmailQuery` + `EmailMutation` (finder, verifier, pattern add) in `D:\code\ayan\contact\contact360.io\api\app\graphql\modules\email\queries.py` and `D:\code\ayan\contact\contact360.io\api\app\graphql\modules\email\mutations.py`.
- **External execution layer:** `LambdaEmailClient` calls Lambda Email endpoints (`/email/finder/`, `/email/finder/bulk`, `/email/single/verifier/`, `/email/bulk/verifier/`, `/email-patterns/add`, `/email-patterns/add/bulk`) in `D:\code\ayan\contact\contact360.io\api\app\clients\lambda_email_client.py`.
- **Async bulk/export path:** Email export/verify import flows delegate to Jobs module (`createEmailFinderExport`, `createEmailVerifyExport`, `createEmailPatternImport`), then call `TkdjobClient` in `D:\code\ayan\contact\contact360.io\api\app\clients\tkdjob_client.py`.
- **Persistence:** Local job metadata stored in `scheduler_jobs` model/repository at `D:\code\ayan\contact\contact360.io\api\app\models\scheduler_job.py` and `D:\code\ayan\contact\contact360.io\api\app\repositories\scheduler_job.py`.
- **Cross-cutting behavior:** Auth via `require_auth`, validation via input classes + `app\utils\validation.py`, activity logging via `ActivityService`, and credit charging via `CreditService`.

## 2) Key Files/Modules for Email

- `D:\code\ayan\contact\contact360.io\api\app\graphql\modules\email\queries.py`  
  Main email finder/verification resolvers + job convenience query fields.
- `D:\code\ayan\contact\contact360.io\api\app\graphql\modules\email\mutations.py`  
  Pattern creation mutations (`addEmailPattern`, `addEmailPatternBulk`).
- `D:\code\ayan\contact\contact360.io\api\app\graphql\modules\email\inputs.py`  
  Input contracts, limits (50 finder items, 10k verify emails), provider validation.
- `D:\code\ayan\contact\contact360.io\api\app\graphql\modules\email\types.py`  
  Output contracts including verification fields (`status`, `email_state`, `email_sub_state`, `certainty`).
- `D:\code\ayan\contact\contact360.io\api\app\clients\lambda_email_client.py`  
  External Lambda Email integration and request-level validation.
- `D:\code\ayan\contact\contact360.io\api\app\graphql\modules\jobs\mutations.py` + `.../jobs/inputs.py`  
  Bulk email export/verify/pattern-import job creation.
- `D:\code\ayan\contact\contact360.io\api\app\clients\tkdjob_client.py`  
  Scheduler API integration (`email-export`, `email-verify`, `email-pattern-import`).
- `D:\code\ayan\contact\contact360.io\api\app\services\credit_service.py` and `.../activity_service.py`  
  Credit deduction and operational audit logging.

## 3) End-to-End Request Flow to Final Email Outcome

### A. Real-time email find/verify
- Client sends GraphQL query under `email` (`findEmails`, `findEmailsBulk`, `verifySingleEmail`, `verifyEmailsBulk`).
- Resolver authenticates user (`require_auth`) and validates payload (`input.validate()` + string/email normalization).
- Resolver invokes `LambdaEmailClient` method.
- `BaseHTTPClient` performs outbound HTTP with retry policy and returns JSON.
- Resolver maps provider response into GraphQL types:
  - Finder returns candidate emails (`email`, `status`, `source`).
  - Verifier returns final verdict fields (`status`, `email_state`, `email_sub_state`, `certainty`).
- Post-processing:
  - Finder path may deduct credits for metered roles.
  - Activity log is written asynchronously (success/failure metadata).
- Response returned to caller as final immediate outcome.

### B. Bulk export/verification via scheduler jobs
- Client calls `jobs.createEmailFinderExport` or `jobs.createEmailVerifyExport` (or email convenience wrappers that delegate to jobs).
- Input typically references pre-uploaded CSV key from S3 upload flow.
- Resolver validates payload, calls `TkdjobClient` (`/api/v1/jobs/email-export` or `/api/v1/jobs/email-verify`).
- On success, API stores a local `scheduler_jobs` row with `job_id`, `job_type`, `status=open`, request/response payload.
- Client polls via `jobs.job` / `jobs.jobs` and live `statusPayload`/`timelinePayload`/`dagPayload`.
- Final email outcome is materialized by external job execution (not computed locally), while this API serves orchestration, ownership/access control, and status visibility.

### Scoring/verification presence
- **Verification is present** in email module (`verifySingleEmail`, `verifyEmailsBulk`) with fields such as `status` and `certainty`.
- **No internal scoring algorithm** for email deliverability is implemented here; verification/scoring-like signals are passthrough from Lambda provider responses.
- Separate risk scoring exists in AI chat area (email risk), but that is a different module and path, not the main email finder/verifier pipeline.

## 4) Top Risks/Gaps and Missing Tests

- **Hardcoded/fallback secrets in code paths:** `TKDJOB_API_KEY` default/fallback values and other default keys in config increase secret exposure risk if env handling is weak.
- **Debug file writes in production code:** Email/jobs resolvers include direct `open(..., "a")` debug log writes (`debug-2e7252.log`, `.cursor\debug.log`), which can leak data and cause filesystem coupling.
- **Retry on non-idempotent POSTs:** Base client retries 5xx/network errors for all requests, including POST create operations (`add_email_pattern`, job creation), which can duplicate side effects upstream.
- **Credit charging behavior ambiguity:** Finder credit deduction occurs after service call and is not clearly gated by `success=true`; partial/failed provider results may still consume credits.
- **Test coverage is very thin for email paths:** only one email-related GraphQL test exists (`test_jobs_email_verify.py`) and it checks just an input validation error.
- **Missing tests you likely need:**  
  - resolver success/error mapping for all email endpoints,  
  - provider failures/timeouts and retry outcomes,  
  - credit deduction rules by role and success/failure semantics,  
  - activity logging side effects,  
  - job creation + ownership/authorization + status hydration behavior,  
  - idempotency/duplicate protection for retried POSTs,  
  - provider field contract drift (`certainty`, states) handling.



