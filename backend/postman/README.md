# Contact360 GraphQL API – Postman Collections

This folder contains Postman collections for the Appointment360 backend.

**Parent index**: [`docs/backend/README.md`](../README.md) — how this folder fits with `apis/`, `endpoints/`, `database/`, and `services.apis/`.

## Parity with `docs/codebases/`

- Full registry: [Codebase analysis registry](../README.md#codebase-analysis-registry).
- When you add or change requests in canonical collections below, sync **endpoint JSON** in `../endpoints/` and the relevant **`docs/codebases/*-codebase-analysis.md`** if auth, paths, or contracts changed.

| Canonical collection / area | Related codebase analyses |
| --- | --- |
| Per-module GraphQL (`01_`–`28_*.postman_collection.json`), main GraphQL API | `appointment360-codebase-analysis.md`, `app-codebase-analysis.md` |
| `Storage_Backend_s3storage.postman_collection.json` | `s3storage-codebase-analysis.md` |
| `Connectra API` / Connectra GraphQL packs | `sync-codebase-analysis.md`, `connectra-codebase-analysis.md` |
| `23_Sales_Navigator_Module` | `salesnavigator-codebase-analysis.md`, `extension-codebase-analysis.md` |
| Contact AI (see `docs/media/postman/` path in `apis/README`) | `contact-ai-codebase-analysis.md` |
| Email Campaign API folder | `emailcampaign-codebase-analysis.md` |

## Files

- **Contact360_GraphQL_API.postman_collection.json** – Complete GraphQL API collection for Contact360/Appointment360.
- **Connectra_GraphQL_API.postman_collection.json** – GraphQL equivalent of Connectra REST API, same folder structure as Connectra REST Postman.
- **Storage_GraphQL_API.postman_collection.json** – GraphQL API for storage only: Auth, S3 (files, CSV upload, delete), and Upload (multipart status, presigned URL, register part, abort). Same endpoint as Contact360 GraphQL (`POST {{baseUrl}}/graphql`).
- **Storage_Backend_s3storage.postman_collection.json** – REST API for the s3storage (storage backend) service used by Appointment360 for CSV/files, multipart uploads, and avatars.

## Folder reality snapshot

- This folder contains canonical Contact360 collections and a very large set of imported third-party collections.
- Canonical release-gate collections are a small, controlled subset and must be explicitly identified.
- Imported collections are useful references but are not contract authorities for Contact360 releases.

### Per-module GraphQL collections

One Postman collection per GraphQL module for focused testing. Same endpoint: `POST {{baseUrl}}/graphql`. Set `baseUrl` and run **01_Auth_Module > Mutations > login** first to get `accessToken`; then set `Authorization: Bearer {{accessToken}}` for other modules (or use collection variables). API docs: `lambda/appointment360/sql/apis/`.

| Collection | Module | Doc |
|------------|--------|-----|
| 01_Auth_Module.postman_collection.json | Auth (me, session, login, register, logout, refreshToken) | 01_AUTH_MODULE.md |
| 02_Users_Module.postman_collection.json | Users (user, users, userStats, updateProfile, uploadAvatar, promote) | 02_USERS_MODULE.md |
| 03_Contacts_Module.postman_collection.json | Contacts (contact, contacts, filters, CRUD, export) | 03_CONTACTS_MODULE.md |
| 04_Companies_Module.postman_collection.json | Companies (company, companies, companyContacts, filters, CRUD, export) | 04_COMPANIES_MODULE.md |
| 05_Notifications_Module.postman_collection.json | Notifications (list, get, unreadCount, preferences, mark read, delete) | 05_NOTIFICATIONS_MODULE.md |
| 07_S3_Module.postman_collection.json | S3 (s3Files, s3FileData, s3FileInfo, s3FileDownloadUrl, initiateCsvUpload, completeCsvUpload, deleteFile) | 07_S3_MODULE.md |
| 08_Health_Module.postman_collection.json | Health (apiMetadata, apiHealth, vqlHealth, vqlStats, performanceStats) | 08_HEALTH_MODULE.md |
| 09_Usage_Module.postman_collection.json | Usage (usage, featureOverview, trackUsage, resetUsage) | 09_USAGE_MODULE.md |
| 10_Upload_Module.postman_collection.json | Upload (initiateUpload, presignedUrl, registerPart, completeUpload, abortUpload) | 10_UPLOAD_MODULE.md |
| 11_Activities_Module.postman_collection.json | Activities (activities, activityStats) | 11_ACTIVITIES_MODULE.md |
| 13_Admin_Module.postman_collection.json | Admin (users, userStats, logs, updateUserRole, updateUserCredits) | 13_ADMIN_MODULE.md |
| 14_Billing_Module.postman_collection.json | Billing (billing, plans, addons, invoices, subscribe, cancel, purchaseAddon) | 14_BILLING_MODULE.md |
| 15_Email_Module.postman_collection.json | Email (findEmails, verifySingleEmail, addEmailPattern; bulk variants) | 15_EMAIL_MODULE.md |
| 16_Jobs_Module.postman_collection.json | Jobs (job, jobs, createEmailFinderExport, createContact360Export, retryJob) | 16_JOBS_MODULE.md |
| 17_AI_Chats_Module.postman_collection.json | AI Chats (aiChats, aiChat, createAIChat, sendMessage, analyzeEmailRisk, parseContactFilters) | 17_AI_CHATS_MODULE.md |
| 18_Analytics_Module.postman_collection.json | Analytics (performanceMetrics, aggregateMetrics, submitPerformanceMetric) | 18_ANALYTICS_MODULE.md |
| 19_Pages_Module.postman_collection.json | Pages (page, pages, pageContent, dashboardPages, marketingPages; all public) | 19_PAGES_MODULE.md |
| 21_LinkedIn_Module.postman_collection.json | LinkedIn (search, export) | 21_LINKEDIN_MODULE.md |
| 23_Sales_Navigator_Module.postman_collection.json | Sales Navigator (saveProfiles) | 23_SALES_NAVIGATOR_MODULE.md |
| 26_Saved_Searches_Module.postman_collection.json | Saved Searches (listSavedSearches, getSavedSearch, create, update, delete) | 26_SAVED_SEARCHES_MODULE.md |
| 27_Two_Factor_Module.postman_collection.json | Two-Factor (get2FAStatus, setup2FA, verify2FA, disable2FA, regenerateBackupCodes) | 27_TWO_FACTOR_MODULE.md |
| 28_Profile_Module.postman_collection.json | Profile (listAPIKeys, listSessions, listTeamMembers, createAPIKey, inviteTeamMember) | 28_PROFILE_MODULE.md |

## Setup

1. **Import** the collection into Postman.
2. **Create an environment** (or use collection variables) and set:
   - `baseUrl` – e.g. `http://localhost:8000` or your API base URL.
   - `email` – user email for login.
   - `password` – user password for login.
3. **Run Auth > Login** to get tokens. Manually copy `accessToken` (and optionally `refreshToken`, `userId`) from the response into your environment.
4. All other requests use `Authorization: Bearer {{accessToken}}`.

Optional variables used by some requests: `fileKey`, `jobId`, `jobUuid`, `exportId`, `contactUuid`, `companyUuid`, `uploadId`.

**Variable naming:** The GraphQL schema uses **camelCase** for field and variable names. In Postman (and in the `variables` JSON of request bodies), use camelCase: e.g. `inputCsvKey`, `outputPrefix`, `s3Bucket`, `retryCount`, `savedSearchId`, `pageType`, `fileSize`, `partNumber`. Do not use snake_case (`input_csv_key`, etc.) or requests may fail validation. See **sql/apis/README.md** for the full list of module docs and the "Queries and mutations – parameters and variable types" section in each module doc.

For the **Storage (GraphQL API)** collection, use the same `baseUrl`, `email`, `password`, and `accessToken` as the main GraphQL collection; optional storage variables: `prefix`, `fileKey`, `upload_id`, `part_number`, `etag`. See subsection below.

For the **Storage Backend** collection, set `storage_base_url` to your s3storage API URL (see below).

## Folder → GraphQL root mapping

All requests are `POST {{baseUrl}}/graphql` with JSON body `{ "query": "...", "variables": { ... } }`.

| Postman folder              | GraphQL root   | Notes |
|----------------------------|----------------|--------|
| Auth                       | `auth`         | me, session, login, register, logout, refreshToken |
| Users                      | `users`        | get user, list, stats, update profile, avatar, promote |
| Health                     | `health`       | metadata, API health, VQL health, performance stats |
| Jobs                       | `jobs`         | job, jobs, retryJob; job includes statusPayload, timelinePayload, dagPayload (live Tkdjob status/timeline/DAG); upload URL → **upload**; export download → **s3** |
| Imports                    | `jobs`         | list jobs (jobType filter), job(jobId), createContact360Import, retryJob |
| Contacts                   | `contacts`     | contact, contacts, contactQuery, filters, CRUD, batch |
| Companies                  | `companies`    | company, companies, companyQuery, CRUD |
| Notifications              | `notifications`| list, get, unread count, preferences, mark read, delete |
| Exports                    | `jobs`         | job, jobs (jobType contact360_export_stream), createContact360Export, retryJob |
| S3                         | `s3`           | s3Files, s3FileData, s3FileInfo, s3FileDownloadUrl |
| Email                      | `email`        | find, verify; mutations: addEmailPattern, addEmailPatternBulk |
| Billing - Admin            | `billing`       | admin plan/addon/period CRUD |
| Billing                    | `billing`       | info, plans, addons, invoices, subscribe, cancel |
| Usage                      | `usage`        | get, track, reset |
| Activities                 | `activities`   | list, stats |
| AI Chats                   | `aiChats`      | list, get, create, send message, analyze, parse filters |
| Analytics                  | `analytics`    | performance metrics, aggregate, submit |
| LinkedIn                   | `linkedin`     | search, export |
| Sales Navigator            | `salesNavigator`| list scraping records, save profiles |
| Admin                      | `admin`        | list users, user stats, search logs, update role/credits |
| Dashboard Pages            | `pages`        | page(pageId, pageType: "dashboard"), dashboardPages |
| Documentation              | `pages`        | page(pageId, pageType: "docs"), pagesByType("docs"), pageContent |
| Marketing                  | `pages`        | page(pageId, pageType: "marketing"), marketingPages |
| Saved Searches             | `savedSearches`| list, get, create, update, delete, update usage |
| Two-Factor Authentication  | `twoFactor`    | status, setup, verify, disable, regenerate codes |
| Profile                    | `profile`      | API keys, sessions, team (list/create/delete/invite/revoke) |
| Upload                     | `upload`       | uploadStatus, presignedUrl; mutations: initiateUpload, completeUpload, abortUpload, etc. |

## Important alignments

- **Imports / Exports**: There is no `imports` or `exports` root. All operations use the **jobs** root: `jobs.job(jobId)`, `jobs.jobs(limit, offset, jobType)`, `jobs.createContact360Import(input)`, `jobs.createContact360Export(input)`, `jobs.retryJob(input)`. Request `statusPayload` in job query for live Tkdjob status.
- **Dashboard Pages, Documentation, Marketing**: There is no `dashboardPages`, `documentation`, or `marketing` root. All use the **pages** root: `pages.page(pageId, pageType)`, `pages.dashboardPages`, `pages.pagesByType("docs")`, `pages.pageContent(pageId)`, `pages.marketingPages`. The pages module is **query-only** in the current schema; create/update/delete for pages may be via DocsAI/Lambda API.
- **Get Upload URL** (in Jobs folder): Use **upload.initiateUpload(input)** (or **s3.initiateCsvUpload(input)** for CSV-specific flows) then **upload.presignedUrl(uploadId, partNumber)** for each part.
- **Get Export Download URL** (in Jobs folder): Use **s3.s3FileDownloadUrl(fileKey)**; `fileKey` is the S3 key (e.g. from job output stored via the S3/s3storage pipeline).

## Connectra GraphQL API (Connectra_GraphQL_API.postman_collection.json)

GraphQL equivalent of the Connectra REST API. Uses the same folder structure as the Connectra REST Postman collection.

**Setup:** Same as Contact360. Use `Auth > Login` first; all other requests use `Authorization: Bearer {{accessToken}}`.

**REST → GraphQL mapping:**

| Connectra REST                    | Appointment360 GraphQL              |
|-----------------------------------|-------------------------------------|
| GET /health                       | `health.apiHealth`                  |
| POST /contacts/ (VQL filter)      | `contacts.contactQuery(query)`      |
| POST /contacts/count              | `contacts.contactCount(query)`      |
| POST /contacts/batch-upsert       | `contacts.batchCreateContacts`      |
| POST /contacts/batch-upsert (uuid)| `contacts.updateContact(uuid,input)`|
| POST /companies/ (VQL filter)     | `companies.companyQuery(query)`     |
| POST /companies/count             | `companies.companyCount(query)`     |
| POST /companies/batch-upsert      | `companies.createCompany` / `updateCompany` |
| GET /common/:service/filters      | `contacts.filters` / `companies.filters` |
| POST /common/:service/filters/data| `contacts.filterData` / `companies.filterData` |
| POST /common/jobs/create          | `jobs.createContact360Import` / `contacts.exportContacts` / `companies.exportCompanies` |
| POST /common/jobs                 | `jobs.jobs`                         |
| GET /common/upload-url            | `upload.initiateUpload`             |

**Notes:**
- Connectra REST uses `X-API-Key`; Appointment360 uses JWT (`Authorization: Bearer {{accessToken}}`).
- Connectra typically runs on port **8080** (not 8000). Set `CONNECTRA_BASE_URL=http://host:8080` in backend `.env` when connecting to Connectra.
- Filters response (`contacts.filters`, `companies.filters`) includes `filterKey` and `filterType` (GraphQL camelCase).
- VQL filters in REST are converted to `VQLQueryInput.filters.conditions` format; use `all_of`/`any_of` for AND/OR logic.

**Collection generator:** Run `python generate_connectra_graphql.py` to regenerate the collection. Filter definitions are in `filters_data.json` to avoid Python parser issues with deeply nested inline structures.

## Storage (GraphQL API) – Storage_GraphQL_API.postman_collection.json

GraphQL subset for **storage-only** operations: Auth (login, me), S3 (list files, file info/data/download URL/schema, initiate/complete CSV upload, delete file), and Upload (upload status, presigned URL, register part, abort). Same endpoint as the full GraphQL API: `POST {{baseUrl}}/graphql`.

**Setup:**

1. Set **baseUrl** (e.g. `http://localhost:8000`), **email**, **password**.
2. Run **Auth > Login**; copy `accessToken` (and optionally `refreshToken`, `userId`) into your environment. The Login request includes an optional test script to set these from the response.
3. All S3 and Upload requests use `Authorization: Bearer {{accessToken}}`.

**Variables:** `prefix` (e.g. `upload/`), `fileKey`, `upload_id` (from s3.initiateCsvUpload), `part_number`, `etag` (from PUT response when uploading a part).

**CSV multipart flow:** s3.initiateCsvUpload → upload.presignedUrl (per part) → PUT part to URL → upload.registerPart → s3.completeCsvUpload.

**API reference:** `lambda/appointment360/sql/apis/07_S3_MODULE.md`, `10_UPLOAD_MODULE.md`. Task breakdown: `TASK_BREAKDOWN_STORAGE_GRAPHQL_POSTMAN.md`.

## Storage Backend (s3storage) – Storage_Backend_s3storage.postman_collection.json

REST API for the **s3storage** Lambda service. Appointment360 calls this service via `S3StorageClient` for buckets, file list/info/download/delete, multipart uploads, single-shot CSV upload, schema/preview/stats/metadata, and avatars. This collection lets you hit the storage API directly (e.g. for debugging or integration tests).

**Setup:**

1. Import **Storage_Backend_s3storage.postman_collection.json**.
2. Set **storage_base_url** to your s3storage API base URL, e.g.:
   - From env: `LAMBDA_S3STORAGE_API_URL`
   - From SAM deploy: `S3StorageApiUrl` (e.g. `https://<api-id>.execute-api.<region>.amazonaws.com`)
3. Optionally set **bucket_id**, **file_key**, **prefix**, **upload_id**, **part_number**, **limit**, **offset**, **expires_in** as needed.

**Folders:** Health, Buckets, Files, Multipart Upload, Analysis (schema, preview, stats, metadata).

**API reference:** `lambda/s3storage/docs/API.md`

---

## Task breakdown for Postman maintainers

1. **Per-module collections (01–28):** Each collection’s description references `sql/apis/XX_MODULE.md` and the "Queries and mutations – parameters and variable types" section. When adding or changing a request, use camelCase in the `variables` JSON and align operation names and input types with that doc.
2. **Upload flow (10_Upload, Storage_GraphQL):** InitiateUpload requires `fileSize` (and optionally `contentType`). registerPart is a mutation taking `input: RegisterPartInput!` (uploadId, partNumber, etag). completeUpload/abortUpload use `input: { uploadId }`. Response fields match UploadStatusResponse, PresignedUrlResponse, RegisterPartResponse, etc. (see 10_UPLOAD_MODULE.md).
3. **Jobs (16_Jobs, Contact360):** All job creation mutations use camelCase in input: `inputCsvKey`, `outputPrefix`, `s3Bucket`, `retryCount`, `savedSearchId`, `pageSize`, `vql`. retryJob takes `RetryJobInput` (jobId, retryCount, retryInterval, runAfter, data, priority).
4. **Sales Navigator (23):** Mutation name is `saveSalesNavigatorProfiles`; input type is `SaveProfilesInput` (profiles: array). Request body must use those names.
5. **Connectra / Contact360 / Storage:** Collection descriptions reference sql/apis and task breakdown docs. Keep folder→root mapping in this README in sync with `app/graphql/schema.py`.

## Endpoint

- **GraphQL**: `POST {{baseUrl}}/graphql`
- **Health** (REST): `GET {{baseUrl}}/health`, `GET {{baseUrl}}/health/db`, `GET {{baseUrl}}/health/logging`

## References

- Backend docs: `lambda/appointment360/docs/codebase.md`
- Schema: `lambda/appointment360/app/graphql/schema.py`
- Connectra REST docs: `lambda/connectra/docs/`
- Storage backend API: `lambda/s3storage/docs/API.md`
- Storage Postman task breakdown: `lambda/appointment360/sql/postman/TASK_BREAKDOWN_STORAGE_POSTMAN.md`
- Storage GraphQL Postman task breakdown: `lambda/appointment360/sql/postman/TASK_BREAKDOWN_STORAGE_GRAPHQL_POSTMAN.md`


## New planned collections
- Campaigns.postman_collection.json
- Webhooks.postman_collection.json
- Integrations.postman_collection.json

## `s3storage` Postman validation checklist

When storage contracts change, validate both collections:

- `Storage_GraphQL_API.postman_collection.json`
- `Storage_Backend_s3storage.postman_collection.json`

Required checks:

1. Multipart lifecycle success and retry behavior (`initiate`, `presigned part`, `register`, `complete`, `abort`).
2. CSV analysis endpoints (`schema`, `preview`, `stats`, `metadata`) against real uploaded files.
3. Download URL TTL behavior for object classes (`upload`, `photo`, `avatar`, `resume`).
4. Error contract parity with module docs (`07_S3_MODULE.md`, `10_UPLOAD_MODULE.md`).

## `logs.api` Postman validation checklist

- Validate API key auth and unauthenticated health behavior.
- Validate CRUD/query/search endpoints and error envelopes.
- Validate large-range query behavior and pagination/limits.

## Email runtime Postman collection (`emailapis` + `emailapigo`)

- Collection file: `Email_Runtime_emailapis_emailapigo.postman_collection.json`
- Purpose: direct runtime parity checks for finder/verifier/pattern/web-search endpoints independent of GraphQL gateway.
- Required variables:
  - `email_runtime_base_url`
  - `email_runtime_api_key`
  - payload variables (`first_name`, `last_name`, `domain`, `email`, `provider`, `company_uuid`)

Validation checklist:
1. Health and auth behavior for both runtimes.
2. Single + bulk finder parity (`/email/finder/`, `/email/finder/bulk`).
3. Single + bulk verifier parity (`/email/single/verifier/`, `/email/bulk/verifier/`).
4. Pattern add behavior and validation errors.
5. Web search fallback path and error envelope parity.
6. Provider drift checks (`truelist` vs `mailvetter`) documented in module docs.

## Connectra REST Postman validation checklist

- Collection folder: `docs/backend/postman/Connectra API/`
- Contract source: `contact360.io/sync` routes and `docs/3. Contact360 contact and company data system/connectra-service.md`

Required checks:
1. Health + API key auth behavior (`GET /health`, auth failure paths).
2. Contacts and companies query/count parity (`/contacts/`, `/contacts/count`, `/companies/`, `/companies/count`).
3. Filter contract parity (`/common/:service/filters`, `/common/:service/filters/data`) with VQL taxonomy docs.
4. Batch upsert idempotency and replay behavior (`/contacts/batch-upsert`, `/companies/batch-upsert`, `/common/batch-upsert`).
5. Job lifecycle behavior (`/common/jobs/create`, `/common/jobs`) including retry-state transitions.
6. Upload URL contract (`/common/upload-url`) and bulk-flow compatibility with jobs/import-export docs.

Boundary note:

- Connectra collection validates `contact360.io/sync` runtime contracts.
- TKD Job runtime (`contact360.io/jobs`) should be validated separately using:
  - `docs/backend/endpoints/jobs_endpoint_era_matrix.json`
  - `docs/backend/apis/16_JOBS_MODULE.md`

## `email campaign` service Postman validation checklist (`backend(dev)/email campaign`)

- Runtime contract source: `backend(dev)/email campaign/api/handlers.go`, `template/handlers.go`
- Module docs source: `docs/backend/apis/22_CAMPAIGNS_MODULE.md`, `24_SEQUENCES_MODULE.md`, `25_CAMPAIGN_TEMPLATES_MODULE.md`
- Endpoint matrix: `docs/backend/endpoints/emailcampaign_endpoint_era_matrix.json`
- Codebase analysis: `docs/codebases/emailcampaign-codebase-analysis.md`

Required collection variables:

- `campaign_base_url` (e.g. `http://localhost:8081`)
- `campaign_jwt_token` (valid JWT for authenticated routes)
- `campaign_id` (from a created campaign)
- `template_id` (from a created template)
- `unsub_token` (JWT token from a sent email)

Required checks:

1. **Health** (`GET /health`) — returns 200 with service liveness; verify no auth leak.
2. **Auth guard** — `POST /campaign` without JWT returns 401 (once auth middleware is active).
3. **Template CRUD:**
   - `POST /templates` with name/subject/html_body creates template and returns id + s3_key.
   - `GET /templates` returns list including newly created template.
   - `GET /templates/:id` returns correct template metadata.
   - `POST /templates/:id/preview` returns rendered HTML with sample data.
   - `DELETE /templates/:id` removes template from S3 and DB.
4. **Campaign create and enqueue:**
   - `POST /campaign` with valid JWT and template_id creates campaign, returns `{campaign_id, status: pending}`.
   - Verify campaign row exists in DB with correct title and status.
5. **Campaign worker (async verification):**
   - After campaign is enqueued, poll campaign status; verify transitions: `pending → sending → completed`.
   - Verify recipient rows inserted in DB with `campaign_id` FK.
   - Verify suppressed email is NOT sent (status remains `pending` or `skipped` for suppressed address).
6. **Unsubscribe flow:**
   - `GET /unsub?token=<valid_jwt>` — inserts email to suppression_list, updates recipient status to `unsubscribed`.
   - `GET /unsub?token=<expired_jwt>` — returns 401.
   - Verify re-send to unsubscribed email is suppressed.
7. **IMAP routes** (optional, requires IMAP credentials):
   - `GET /list/mailbox` returns mailbox list.
   - `GET /list/inbox` returns latest 10 inbox messages.
   - `GET /body/:uid` returns email body for given UID.

Boundary notes:

- Campaign service collection validates `backend(dev)/email campaign` runtime contracts (REST, not GraphQL).
- GraphQL campaign operations (via Appointment360 gateway) should be validated in the Contact360 GraphQL Postman collection under the `campaigns` module.
- Worker async validation requires Redis and Postgres to be running; use docker-compose local setup.

## `jobs` runtime Postman validation checklist (`contact360.io/jobs`)

- Runtime contract source: `contact360.io/jobs/app/api/v1/routes/jobs.py`
- Module docs source: `docs/backend/apis/16_JOBS_MODULE.md`
- Endpoint matrix: `docs/backend/endpoints/jobs_endpoint_era_matrix.json`

Required variables for direct runtime collection:

- `jobs_base_url`
- `jobs_api_key`
- `job_uuid`
- `s3_bucket`, `s3_key`, `output_prefix`
- optional `retry_count`, `retry_interval`

Required checks:

1. Health and readiness (`/health`, `/health/live`, `/health/ready`) without auth regression.
2. Create flows (`email-export`, `email-verify`, `email-pattern-import`, `contact360-import`, `contact360-export`) with valid/invalid payload coverage.
3. Lifecycle polling (`GET /api/v1/jobs/{uuid}/status`) confirms status vocabulary and `progress_percent` behavior.
4. Timeline and DAG checks (`/timeline`, `/dag`) verify event integrity and graph structure.
5. Retry semantics (`PUT /api/v1/jobs/{uuid}/retry`) verify `retry` status behavior and re-queue flow.
6. Metrics parity (`/api/v1/metrics`, `/api/v1/metrics/stats`) for observability readiness.

---

## Appointment360 GraphQL gateway validation checklist

The gateway is tested via GraphQL operations against `POST {{baseUrl}}/graphql`. Use per-module Postman collections (files `01_Auth_Module.postman_collection.json` through `28_Profile_Module.postman_collection.json`) listed above. A complete gateway validation run must cover all items below.

**Endpoint:** `POST {{baseUrl}}/graphql`
**Auth:** `Authorization: Bearer {{accessToken}}` (set via `01_Auth_Module > Mutations > login`)
**Public API Auth (8.x+):** `X-API-Key: {{apiKey}}` (set via `28_Profile_Module > createApiKey`)
**Runtime contract source:** `contact360.io/api/app/main.py`, `app/graphql/schema.py`
**Module docs source:** `docs/backend/apis/`
**Endpoint matrix:** `docs/backend/endpoints/appointment360_endpoint_era_matrix.json`

Required environment variables:

| Variable | Value | Notes |
| --- | --- | --- |
| `baseUrl` | `http://localhost:8000` | API server base URL |
| `email` | Test user email | |
| `password` | Test user password | |
| `accessToken` | Set after login | JWT access token |
| `refreshToken` | Set after login | JWT refresh token |
| `apiKey` | Set after createApiKey | Public API key |
| `contactUuid` | Existing contact UUID | For contact detail tests |
| `companyUuid` | Existing company UUID | For company detail tests |
| `jobId` | Existing job UUID | For job polling tests |
| `chatUuid` | Existing AI chat UUID | For AI chat tests |
| `savedSearchId` | Existing saved search UUID | For saved search tests |

Required validation checks:

1. **Auth lifecycle:** `register → login → me → logout → me (fails) → refresh_token → me (succeeds)`.
2. **Token blacklist:** use blacklisted token → must return `UNAUTHENTICATED`.
3. **Credit deduction:** `findEmails` call → `query usage("email_finder")` shows credit decrement.
4. **Contacts round-trip:** `contacts(query: { page: 1, per_page: 5 })` returns data with `contactCount` consistency.
5. **VQL filter flow:** `filters()` → `filterData(input)` → apply to `contacts(query: { where: "..." })`.
6. **Saved search:** `createSavedSearch` → `savedSearches(type: "contact")` → `deleteSavedSearch`.
7. **Email finder:** `findEmails(input: { firstName: "...", domain: "..." })` returns results.
8. **Bulk email job:** `createEmailFinderExport(input)` → `job(jobId)` polling → status progression.
9. **Retry job:** `retryJob(jobId)` on failed job → new status = `retry`.
10. **Idempotency guard:** `subscribe` mutation with same `X-Idempotency-Key` twice → second returns same response, not duplicate charge.
11. **Abuse guard:** fire `upsertByLinkedinUrl` > 30 times per minute → expect `429` after threshold.
12. **Rate limit (production only):** `GRAPHQL_RATE_LIMIT_REQUESTS_PER_MINUTE` > 0 → validate `429` after limit.
13. **Body size guard:** POST body > 2MB → expect `413`.
14. **Complexity guard:** deeply nested query exceeding complexity 100 → expect complexity error.
15. **AI chat:** `createAiChat` → `sendAiMessage` → `aiChat(uuid)` → `deleteAiChat`.
16. **Public API key auth (8.x+):** `createApiKey` → use `X-API-Key` header → `contacts` query succeeds.
17. **Two-factor auth (8.x+):** `enableTwoFactor` → `verifyTwoFactor(otp)` → `twoFactorStatus()` shows enabled.
18. **Notifications:** `notifications()` returns list → `markNotificationRead(id)` → poll again shows `is_read=true`.
19. **Admin panel (SuperAdmin only):** `adminStats()` with admin token → returns counts; with regular user → expect auth error.
20. **Health endpoints:** `GET /health`, `/health/db`, `/health/logging`, `/health/slo` → all return 200.
21. **Debug write regression:** no `logs/*.log` or `debug.log` files created after running any module test. (Known bug — verify removed from `email/queries.py` and `jobs/mutations.py`).

Known issues to verify are resolved before gateway production promotion:

| Issue | Location | Required fix |
| --- | --- | --- |
| Inline debug file writes | `app/graphql/modules/email/queries.py`, `jobs/mutations.py` | Remove all `open(..., 'a')` writes |
| Rate limit disabled by default | `config.py: GRAPHQL_RATE_LIMIT_REQUESTS_PER_MINUTE=0` | Set > 0 in production |
| No campaigns/sequences/templates modules | Schema gap | 10.x implementation required before campaign tests |
| SQL schema files missing locally | `sql/tables/` not in workspace | Restore before migration testing |

---

## Mailvetter verifier service validation checklist

**Runtime target:** `backend(dev)/mailvetter`  
**Canonical API:** `/v1/*`  
**Endpoint matrix:** `docs/backend/endpoints/mailvetter_endpoint_era_matrix.json`

Required variables:

- `mailvetter_base_url`
- `mailvetter_api_key`
- `job_id` (for status/results tests)

Required checks:

1. Health check: `GET /v1/health` returns 200 and service metadata.
2. Auth guard: missing/invalid Bearer key on `/v1/*` returns 401.
3. Single verify success: `POST /v1/emails/validate` returns `status`, `is_valid`, `validation_result`, `confidence_score`.
4. Single verify invalid payload: malformed email returns `INVALID_EMAIL_FORMAT`.
5. Bulk create success: `POST /v1/emails/validate-bulk` returns 202 with `job_id` and progress seed.
6. Bulk size limit: free-tier payload over plan limit returns `BULK_SIZE_EXCEEDED`.
7. Concurrent jobs limit: exceeding plan concurrency returns `CONCURRENT_JOB_LIMIT`.
8. Job status polling: `GET /v1/jobs/{job_id}` reflects `processed/valid/invalid/pending`.
9. Results JSON: `GET /v1/jobs/{job_id}/results?format=json` returns summary + pagination.
10. Results CSV: `GET /v1/jobs/{job_id}/results?format=csv` returns parseable CSV with expected headers.
11. Webhook callback: completed job emits signed callback with `X-Webhook-Signature`.
12. Rate headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset` present.
13. Legacy route parity warning: `/verify|/upload|/status|/results` tested only for compatibility, not new integrations.


## Collection governance policy

This directory contains both canonical Contact360 collections and imported third-party/example collections.

- Canonical collections are Contact360-owned artifacts used by this repository (`Contact360`, `Connectra`, `Storage`, and service runtime collections).
- Imported or third-party collections are reference material and should not be treated as release-gate contract sources.
- When endpoint contracts change, update canonical collections and this README in the same change set.
- Keep module docs under `docs/backend/apis/` and endpoint matrices under `docs/backend/endpoints/` in sync with canonical collections.

## Small-task breakdown for collection governance

- `Task 1 - Classify`: mark collection as canonical or reference.
- `Task 2 - Validate`: run required checks for impacted canonical collections.
- `Task 3 - Sync`: update matching module docs and endpoint matrices.
- `Task 4 - Harden`: verify auth, rate-limit, and error-envelope coverage.
- `Task 5 - Evidence`: record validation outputs for release gate packets.
