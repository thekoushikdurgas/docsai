# Email architecture and behavior exploration
_Exported on 3/24/2026 at 01:26:53 GMT+5:30 from Cursor (2.6.20)_

---

**User**

Explore D:\code\ayan\contact\contact360.io\app with medium thoroughness. Focus on email-related architecture and behavior in this app codebase. Return: (1) architecture map, (2) key files/modules for email system, (3) end-to-end user flow to final email outcomes (finder/verification/export if present), (4) top risks/gaps and testing gaps.

---

**Cursor**

I’ll map the email-related system by scanning `contact360.io/app` for email finder/verification/export flows, then read the core modules to reconstruct architecture, behavior, and risk/testing gaps. I’ll start by retrieving any prior project knowledge so the map aligns with existing patterns.

I couldn’t find readable Byterover tool descriptors in this workspace MCP metadata, so I’m proceeding with direct code exploration now and will focus on `contact360.io/app` internals for the architecture map and flow.

I’m hitting timeouts on broad scans, so I’m narrowing to likely code file patterns (`.py`, `.js/.ts`, configs) inside `contact360.io/app` and then drilling into email-specific hits.

I’ve identified the core email page, hooks, GraphQL services, and job-upload pipeline. Next I’m checking the shared infra (`graphqlClient`, config, types, jobs UI) and current test coverage so I can call out concrete architecture and risk gaps.

## 1) Email Architecture Map

`contact360.io/app` is a **Next.js frontend** with email features split into UI, hooks, GraphQL services, and job orchestration.

- **UI entry point**
  - `D:\code\ayan\contact\contact360.io\app\app\(dashboard)\email\page.tsx`
  - Drives tabbed Email Studio (`finder`, `verifier`, `assistant`) and sub-modes (`single`, `bulk`).

- **Presentation components**
  - `D:\code\ayan\contact\contact360.io\app\src\components\email\*`
  - Form UIs, drop zones, mapping modal/fields, result cards/tables, credits banner.

- **Client logic hooks**
  - `D:\code\ayan\contact\contact360.io\app\src\hooks\useEmailFinderSingle.ts`
  - `D:\code\ayan\contact\contact360.io\app\src\hooks\useEmailVerifierSingle.ts`
  - `D:\code\ayan\contact\contact360.io\app\src\hooks\useEmailVerifierBulk.ts`
  - `D:\code\ayan\contact\contact360.io\app\src\hooks\useCsvUpload.ts`
  - `D:\code\ayan\contact\contact360.io\app\src\hooks\useNewExport.ts` (shared Jobs modal flow)

- **Service layer (GraphQL)**
  - `D:\code\ayan\contact\contact360.io\app\src\services\graphql\emailService.ts`
    - `findEmails`, `findEmailsBulk`, `verifySingleEmail`, `verifyEmailsBulk`, pattern APIs
  - `D:\code\ayan\contact\contact360.io\app\src\services\graphql\jobsService.ts`
    - Creates async finder/verify export jobs
  - `D:\code\ayan\contact\contact360.io\app\src\services\graphql\s3Service.ts`
    - Multipart upload + download URL retrieval
  - `D:\code\ayan\contact\contact360.io\app\src\lib\graphqlClient.ts`
    - Auth headers, token refresh, retries, API error shaping

- **Utility/config/text**
  - `D:\code\ayan\contact\contact360.io\app\src\lib\email\emailUtils.ts` (CSV header parsing, mapping suggestions)
  - `D:\code\ayan\contact\contact360.io\app\src\lib\email\emailValidation.ts` (bulk email parsing/validation)
  - `D:\code\ayan\contact\contact360.io\app\src\lib\config.ts` (`GRAPHQL_URL`, `JOBS_S3_BUCKET`)
  - `D:\code\ayan\contact\contact360.io\app\src\text\email.ts` (all copy/toasts; indicates intended workflows)

- **Async outcomes surface**
  - `D:\code\ayan\contact\contact360.io\app\app\(dashboard)\jobs\page.tsx`
  - `D:\code\ayan\contact\contact360.io\app\src\lib\jobs\jobsMapper.ts`
  - `D:\code\ayan\contact\contact360.io\app\src\components\jobs\JobsTable.tsx`

---

## 2) Key Email Files/Modules

Most critical for behavior:

- `D:\code\ayan\contact\contact360.io\app\app\(dashboard)\email\page.tsx`  
  Orchestrates all user actions and mode switching.
- `D:\code\ayan\contact\contact360.io\app\src\services\graphql\emailService.ts`  
  Core finder/verifier API contract for immediate operations.
- `D:\code\ayan\contact\contact360.io\app\src\services\graphql\jobsService.ts`  
  Async job creation for CSV bulk/export pathways.
- `D:\code\ayan\contact\contact360.io\app\src\hooks\useCsvUpload.ts`  
  Multipart upload logic; retries/cancel/abort behavior.
- `D:\code\ayan\contact\contact360.io\app\src\hooks\useNewExport.ts`  
  Jobs-page export modal flow including email-finder/verify job creation.
- `D:\code\ayan\contact\contact360.io\app\src\hooks\useEmailVerifierBulk.ts`  
  Paste-based bulk verify (up to 10,000) in-page.
- `D:\code\ayan\contact\contact360.io\app\src\lib\email\emailUtils.ts` and `emailValidation.ts`  
  Header parsing/mapping and email parsing logic.
- `D:\code\ayan\contact\contact360.io\app\app\(dashboard)\jobs\page.tsx` + `jobsMapper.ts`  
  Job status polling and final download access.

---

## 3) End-to-End User Flow -> Final Email Outcomes

### A) Finder (single)
1. User enters first/last + domain/website on Email page.
2. `useEmailFinderSingle.search()` calls `emailService.findEmails`.
3. First returned email is shown in `EmailFinderResultCard`.
4. Outcomes: copy email to clipboard, “save” currently placeholder (“coming soon”).

### B) Verifier (single)
1. User enters one email + provider (`truelist` or `icypeas`).
2. `useEmailVerifierSingle.verify()` calls `emailService.verifySingleEmail`.
3. UI renders status/health fields in verifier result card.
4. Outcome: immediate verification insight in UI (no export unless user uses Jobs flow).

### C) Verifier (bulk paste, in-page)
1. User pastes one-email-per-line text.
2. `parseBulkEmails()` dedupes + validates.
3. `useEmailVerifierBulk.verify()` calls `emailService.verifyEmailsBulk`.
4. `EmailVerifierBulkResults` shows counts + row table.
5. Outcome: immediate in-page bulk result table (not a file download).

### D) Finder/Verifier bulk via CSV -> job/export outcome
1. User selects CSV in Email page bulk modes (or Jobs page New Export).
2. `useCsvUpload` / `useNewExport` uploads to S3 multipart.
3. `jobsService.createEmailFinderExport` or `createEmailVerifyExport` creates backend job.
4. Jobs page polls (`useJobs` + periodic refetch), maps payload via `jobsMapper`.
5. On completion, job exposes URL or S3 key -> download via `s3Service.getS3FileDownloadUrl`.
6. Final outcome: downloadable output file from Jobs table/card.

### E) Assistant tab
- Current behavior is local mock generation (`setTimeout` + hardcoded suggestions), no backend AI call.

---

## 4) Top Risks/Gaps + Testing Gaps

### Product/behavior risks

- **Hardcoded confidence/scoring in UI**
  - Finder sets score to fixed `98`; verifier maps status to fixed scores (`95/10/50`), which may misrepresent backend certainty.
- **CSV header parsing is simplistic**
  - `parseCsvHeaders()` splits first line on commas directly, so quoted headers with commas can map incorrectly.
- **Potential verify export path inconsistency**
  - Email page bulk verifier job uses `buildEmailExportOutputPrefix` while shared export hook uses `buildEmailVerifyOutputPrefix` for verify jobs; could split outputs inconsistently.
- **Feature gating is mostly UX-level**
  - `featureAccess.ts` says bulk verification is pro-only, but Email page mainly shows a banner; hard gating appears backend-dependent.
- **Assistant is non-production logic**
  - No API call; deterministic static suggestions may be mistaken for real AI behavior.
- **Error details are flattened**
  - Several hooks catch errors and emit generic messages (“Finder failed”, “Verification failed”), reducing diagnosability.

### Testing gaps

- **No email-flow unit tests found** for:
  - `useEmailFinderSingle`, `useEmailVerifierSingle`, `useEmailVerifierBulk`
  - `emailService` GraphQL operation handling
  - CSV mapping/parsing edge cases (`emailUtils`, `emailValidation`)
- **No integration tests found** for:
  - CSV upload -> job creation -> jobs polling -> download path
  - mode transitions/reset behavior on Email page
- **Regression risk areas needing explicit tests**
  - Mapping defaults for varied header names
  - malformed CSV headers / large files / partial upload failures
  - mixed job payload download resolution (`url`, `s3_key`, `final_s3_key`)
  - role/plan-based access controls for bulk actions

If useful, I can next give a prioritized test matrix (unit + integration + edge-case fixtures) tailored to this email module.

