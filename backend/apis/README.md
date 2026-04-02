# GraphQL Modules Documentation

Authoritative module docs for the **Contact360 GraphQL gateway** (`contact360.io/api`, Strawberry + FastAPI). Runtime names in `Settings` may still say “Appointment” for legacy compatibility—see `app/core/config.py` for actual `PROJECT_NAME` / env wiring.

**Gateway environment:** Downstream URLs and keys are defined in `app/core/config.py` (e.g. `CONNECTRA_BASE_URL`, `TKDJOB_API_URL`, `LAMBDA_*`, `DOCSAI_*`, `CAMPAIGN_*`, `RESUME_AI_*`). A client-facing mesh summary lives in [00_SERVICE_MESH_CONTRACTS.md](00_SERVICE_MESH_CONTRACTS.md).

## Doc sync task breakdown (maintenance)

1. **Schema parity** — For each `NN_*_MODULE.md`, align operation names, argument names, and auth rules with `app/graphql/schema.py` and `app/graphql/modules/<module>/`.
2. **REST vs GraphQL** — Document `GET /health*`, `GET /`, and `POST /graphql` in `08_HEALTH_MODULE.md` (and any other HTTP routes in `app/main.py`).
3. **Env vars** — Keep [00_SERVICE_MESH_CONTRACTS.md](00_SERVICE_MESH_CONTRACTS.md) and billing/admin docs in sync with `Settings` fields; frontend public vars stay in [20_NEXT_PUBLIC_ENV_VARS.md](20_NEXT_PUBLIC_ENV_VARS.md).
4. **Stubs** — [06_WEBHOOKS_MODULE.md](06_WEBHOOKS_MODULE.md) reflects “not implemented” until a module exists.

## Root `Query` / `Mutation` fields (`app/graphql/schema.py`)

Operations live under these namespaces (examples: `query { health { apiHealth { status } } }`, `mutation { auth { login(input: {...}) { accessToken } } }`):

**Query:** `auth`, `users`, `contacts`, `companies`, `activities`, `analytics`, `billing`, `email`, `campaignSatellite`, `jobs`, `usage`, `featureOverview`, `pages`, `s3`, `upload`, `aiChats`, `notifications`, `salesNavigator`, `admin`, `health`, `savedSearches`, `twoFactor`, `profile`, `resume`.

**Mutation:** `auth`, `users`, `contacts`, `companies`, `billing`, `linkedin`, `jobs`, `email`, `usage`, `upload`, `s3`, `analytics`, `aiChats`, `notifications`, `salesNavigator`, `admin`, `savedSearches`, `twoFactor`, `profile`, `resume`.

## Folder reality snapshot

- Includes module docs `01` through `29` and multiple `*_ERA_TASK_PACKS.md` indexes.
- Covers both GraphQL modules and linked REST microservice references.
- This folder is the contract authority for resolver-level behavior and operation examples.

**When adding a new module:** Add its doc to the Module file list and Module Index below, and follow the documentation structure described in "Documentation Structure". For granular maintenance tasks per module, see [TASK_BREAKDOWN_APIS.md](TASK_BREAKDOWN_APIS.md).

## Parity with `docs/codebases/`

- Hub: [docs/backend/README.md](../README.md#codebase-analysis-registry) lists each `*-codebase-analysis.md` and the `apis/` / `endpoints/` / `database/` files to update together.
- **Gateway (`contact360.io/api`)**: [appointment360-codebase-analysis.md](../../codebases/appointment360-codebase-analysis.md) — keep every `NN_*_MODULE.md` here aligned with Strawberry schema and clients under `app/graphql/modules/` and `app/clients/`. **Era task checklist (granular):** [APPOINTMENT360_GATEWAY_TASK_BOARD.md](APPOINTMENT360_GATEWAY_TASK_BOARD.md) (with [APPOINTMENT360_ERA_TASK_PACKS.md](APPOINTMENT360_ERA_TASK_PACKS.md) linking per-era docs under `docs/0…10/`).
- **Data plane (`contact360.io/sync`)**: [sync-codebase-analysis.md](../../codebases/sync-codebase-analysis.md) and [connectra-codebase-analysis.md](../../codebases/connectra-codebase-analysis.md) — keep `03_CONTACTS_MODULE.md`, `04_COMPANIES_MODULE.md`, and `connectra_endpoint_era_matrix.json` aligned with Connectra HTTP/VQL behavior.
- **Dashboard (`contact360.io/app`)**: [app-codebase-analysis.md](../../codebases/app-codebase-analysis.md) — when UI work changes GraphQL usage, update the relevant module doc and `docs/backend/endpoints/` operation JSON in the same PR.
- **Marketing (`contact360.io/root`)**: [root-codebase-analysis.md](../../codebases/root-codebase-analysis.md) — public `Pages` / gateway usage; align `19_PAGES_MODULE.md` and any marketing-facing endpoint metadata.
- **Mailbox (`contact360.io/email`)**: [email-codebase-analysis.md](../../codebases/email-codebase-analysis.md) — IMAP app is not a GraphQL module; align product email flows with `15_EMAIL_MODULE.md` and security notes in frontend/docs.
- **Admin (DocsAI)**: [admin-codebase-analysis.md](../../codebases/admin-codebase-analysis.md) — align `13_ADMIN_MODULE.md` and admin-related lineage with Django admin and gateway behavior.
- **Browser extension**: [extension-codebase-analysis.md](../../codebases/extension-codebase-analysis.md) — align `21_LINKEDIN_MODULE.md`, `23_SALES_NAVIGATOR_MODULE.md`, and downstream REST matrices (`salesnavigator`, `emailapis`, etc.) when extension contracts change.

## Module file list

| File                                                         | Module          |
| ------------------------------------------------------------ | --------------- |
| [01_AUTH_MODULE.md](01_AUTH_MODULE.md)                       | Auth            |
| [02_USERS_MODULE.md](02_USERS_MODULE.md)                     | Users           |
| [03_CONTACTS_MODULE.md](03_CONTACTS_MODULE.md)               | Contacts        |
| [04_COMPANIES_MODULE.md](04_COMPANIES_MODULE.md)             | Companies       |
| [05_NOTIFICATIONS_MODULE.md](05_NOTIFICATIONS_MODULE.md)     | Notifications   |
| [06_WEBHOOKS_MODULE.md](06_WEBHOOKS_MODULE.md)                 | Webhooks (stub — no GraphQL module in gateway yet) |
| [07_S3_MODULE.md](07_S3_MODULE.md)                           | S3              |
| [08_HEALTH_MODULE.md](08_HEALTH_MODULE.md)                   | Health          |
| [09_USAGE_MODULE.md](09_USAGE_MODULE.md)                     | Usage           |
| [10_UPLOAD_MODULE.md](10_UPLOAD_MODULE.md)                   | Upload          |
| [11_ACTIVITIES_MODULE.md](11_ACTIVITIES_MODULE.md)           | Activities      |
| [13_ADMIN_MODULE.md](13_ADMIN_MODULE.md)                     | Admin           |
| [14_BILLING_MODULE.md](14_BILLING_MODULE.md)                 | Billing         |
| [15_EMAIL_MODULE.md](15_EMAIL_MODULE.md)                     | Email           |
| [16_JOBS_MODULE.md](16_JOBS_MODULE.md)                       | Jobs            |
| [17_AI_CHATS_MODULE.md](17_AI_CHATS_MODULE.md)               | AI Chats        |
| [18_ANALYTICS_MODULE.md](18_ANALYTICS_MODULE.md)             | Analytics       |
| [19_PAGES_MODULE.md](19_PAGES_MODULE.md)                     | Pages           |
| [20_INTEGRATIONS_MODULE.md](20_INTEGRATIONS_MODULE.md)         | Integrations (stub — no GraphQL module in gateway yet) |
| [21_LINKEDIN_MODULE.md](21_LINKEDIN_MODULE.md)               | LinkedIn        |
| [22_CAMPAIGNS_MODULE.md](22_CAMPAIGNS_MODULE.md)               | Campaigns       |
| [23_SALES_NAVIGATOR_MODULE.md](23_SALES_NAVIGATOR_MODULE.md) | Sales Navigator |
| [24_SEQUENCES_MODULE.md](24_SEQUENCES_MODULE.md)               | Sequences       |
| [25_CAMPAIGN_TEMPLATES_MODULE.md](25_CAMPAIGN_TEMPLATES_MODULE.md) | Campaign Templates |
| [26_SAVED_SEARCHES_MODULE.md](26_SAVED_SEARCHES_MODULE.md)   | Saved Searches  |
| [27_TWO_FACTOR_MODULE.md](27_TWO_FACTOR_MODULE.md)           | Two-Factor      |
| [28_PROFILE_MODULE.md](28_PROFILE_MODULE.md)                 | Profile         |
| [29_RESUME_AI_REST_SERVICE.md](29_RESUME_AI_REST_SERVICE.md) | Resume AI (REST microservice) |


## Module Index

### Core Modules

1. **[Auth Module](01_AUTH_MODULE.md)** - Authentication, login, registration, token management
2. **[Users Module](02_USERS_MODULE.md)** - User management, profiles, avatars, statistics
3. **[Health Module](08_HEALTH_MODULE.md)** - Health checks, performance monitoring, API metadata
4. **[Saved Searches Module](26_SAVED_SEARCHES_MODULE.md)** - Save and manage search queries with filters and sorting
5. **[Two-Factor Authentication Module](27_TWO_FACTOR_MODULE.md)** - 2FA setup, verification, and backup codes
6. **[Profile Module](28_PROFILE_MODULE.md)** - API keys, sessions, and team management

### Data Modules

1. **[Contacts Module](03_CONTACTS_MODULE.md)** - Contact queries, VQL queries, filtering, filter metadata
2. **[Companies Module](04_COMPANIES_MODULE.md)** - Company queries, VQL queries, company contacts, filter metadata
3. **[Activities Module](11_ACTIVITIES_MODULE.md)** - User activity tracking and statistics

### Communication Modules

1. **[Email Module](15_EMAIL_MODULE.md)** - Email finder, verification, pattern add (single and bulk); job-based exports via Jobs module
2. **[Notifications Module](05_NOTIFICATIONS_MODULE.md)** - Notification management, preferences
3. **[AI Chats Module](17_AI_CHATS_MODULE.md)** - AI chat conversations via **Contact AI** (Hugging Face inference; Postgres `ai_chats`) and utility operations (email risk, company summaries, filter parsing)

### File & Storage Modules

1. **[S3 Module](07_S3_MODULE.md)** - File operations and CSV reading via the `s3storage` service (per-user logical buckets)
2. **[Upload Module](10_UPLOAD_MODULE.md)** - Multipart file uploads orchestrated via `s3storage` and presigned URLs

### Business Modules

1. **[Billing Module](14_BILLING_MODULE.md)** - Subscriptions, plans, addons, invoices
2. **[Usage Module](09_USAGE_MODULE.md)** - Feature usage tracking
3. **[Analytics Module](18_ANALYTICS_MODULE.md)** - Performance metrics tracking

### Integration Modules

1. **[Jobs Module](16_JOBS_MODULE.md)** - Scheduler jobs (tkdjob): create, list, retry email/Contact360 export and import jobs; live status, timeline, and DAG via statusPayload, timelinePayload, dagPayload
2. **[LinkedIn Module](21_LINKEDIN_MODULE.md)** - LinkedIn URL search and export
3. **[Sales Navigator Module](23_SALES_NAVIGATOR_MODULE.md)** - Sales Navigator profile saving to Connectra

### Content Management Modules

1. **[Pages Module](19_PAGES_MODULE.md)** - Unified page management (docs, marketing, dashboard) with role-based access in auth response; all Pages queries are public (no auth required). Endpoints, Relationships, and Postman configs are served by DocsAI and are not documented in this folder.

### Microservices (REST, not GraphQL)

1. **[Resume AI REST Service](29_RESUME_AI_REST_SERVICE.md)** - FastAPI **resumeai** service (`backend(dev)/resumeai`): health, resume CRUD (JSON in s3storage), AI endpoints. Authenticated with **`X-API-Key`**. Postman: `backend(dev)/resumeai/postman/`.
2. **Contact AI (REST)** — FastAPI Lambda **`backend(dev)/contact.ai`**: `/api/v1/ai-chats`, `/api/v1/ai`, shared Postgres **`ai_chats`**. GraphQL uses `LambdaAIClient`; see [17_AI_CHATS_MODULE.md](17_AI_CHATS_MODULE.md). Postman: `docs/media/postman/Contact AI Service.postman_collection.json`.

### Administration Modules

1. **[Admin Module](13_ADMIN_MODULE.md)** - User management, statistics, logs, role/credit updates

### User Account Modules

1. **[Saved Searches Module](26_SAVED_SEARCHES_MODULE.md)** - Save and manage search queries with filters and sorting
2. **[Two-Factor Authentication Module](27_TWO_FACTOR_MODULE.md)** - 2FA setup, verification, and backup codes
3. **[Profile Module](28_PROFILE_MODULE.md)** - API keys, sessions, and team management

## Quick Reference

### Authentication Required

Most modules require authentication. Use the Auth module to get an access token.

### Admin/SuperAdmin Only

- Admin Module (most operations)
- Billing Module (plan/addon management)
- Jobs Module (`createEmailPatternImport`, `createContact360Import` require SuperAdmin; `retryJob` requires job ownership)

### Public Endpoints

- Health Module (`apiMetadata`, `apiHealth`)
- Health REST endpoints (`/health`, `/health/db`, `/health/logging`)
- Billing Module (`plans`, `addons`)
- Pages Module (all queries public—no auth required; e.g. `page`, `pages`, `pageContent`, `pagesByType`, `dashboardPages`, `marketingPages`. This API exposes Pages as query-only; create/update/delete may be via DocsAI.)

### Credit-Based Operations

- **Email Module**: 1 credit per search/verification operation (FreeUser/ProUser)
- **LinkedIn Module**: 1 credit per URL searched
- **Usage Module**: Tracks feature usage and enforces limits based on user role/subscription
- **SuperAdmin/Admin**: Unlimited credits (no deduction required)

## Module Dependencies

### External Services

- **Connectra Service** (VQL API):
  - Contacts Module (queries, filters, VQL, batch operations)
  - Companies Module (queries, filters, VQL, batch operations)
  - Configuration: `CONNECTRA_BASE_URL` (typically `http://host:8080`), `CONNECTRA_API_KEY`
  - Contact queries: denormalized company columns (`company_name`, etc.) are served via `company_config.populate` (Connectra `/contacts/` returns 500 if included in `select_columns`)
- **Lambda Services**:
  - Email Module → Lambda Email service (email finding, verification)
  - AI Chats Module → **Contact AI** service (`backend(dev)/contact.ai`): chat CRUD + Hugging Face inference; HTTP client `LambdaAIClient` (`LAMBDA_AI_API_URL`)
  - Admin Module → Lambda Logs API service (log queries, search, statistics)
- **DocsAI (Django)**:
  - Pages Module → DocsAI service (unified page management: docs, marketing, dashboard; endpoints, relationships, postman)
- **Storage Services**:
  - **s3storage service** (Lambda/FastAPI) → backing storage microservice used by the S3 and Upload modules. Handles AWS S3 access, per-user logical buckets, CSV preview/schema/stats, multipart and single-shot uploads, avatars, and bucket metadata.
  - **AWS S3** → underlying object store accessed indirectly via the s3storage service.
  - **Storage backend REST API:** `lambda/s3storage/docs/API.md`. Postman: `docs/backend/postman/Storage_Backend_s3storage.postman_collection.json` (set `storage_base_url` to s3storage API URL).
- **Resume AI service** (FastAPI, SAM):
  - REST API under `/v1` with **`X-API-Key`**; resume JSON stored via **s3storage** (`resume/` prefix). See [29_RESUME_AI_REST_SERVICE.md](29_RESUME_AI_REST_SERVICE.md). Postman: `backend(dev)/resumeai/postman/Resume_AI_Service.postman_collection.json`. GraphQL consumers use `contact360.io/api` **resume** module as a proxy.
- **Contact AI service** (FastAPI, SAM):
  - REST API under `/api/v1` with **`X-API-Key`** and **`X-User-ID`** on chat routes; chats in Postgres **`ai_chats`**. See [17_AI_CHATS_MODULE.md](17_AI_CHATS_MODULE.md). Postman: `docs/media/postman/Contact AI Service.postman_collection.json`.
- **Other Services**:
  - LinkedIn Module → LinkedIn service (URL search)
  - Sales Navigator Module → Sales Navigator Lambda service (profile saving)

### Internal Services

- **ActivityService**: Centralized activity logging (used by all modules)
- **CreditService**: Credit deduction logic (Email, LinkedIn modules)
- **UsageService**: Feature usage tracking (Usage module)
- **BillingService**: Subscription and billing management (Billing module)
- **NotificationService**: Notification management (Notifications module)
- **S3StorageClient**: HTTP client for the `s3storage` service. All CSV file operations, multipart/single-shot uploads, avatars, and bucket metadata go through `s3storage` using per-user logical buckets stored in `users.bucket`, instead of calling S3 directly from the Contact360 gateway. The storage REST API and Postman collection are documented under External Services above.

## Logging System

The application uses a centralized logging system that sends all logs to the Lambda Logs API (stored in MongoDB). Console logging is disabled by default in production.

### Key Features

- **Lambda-Only Logging**: All logs go to Lambda Logs API via background thread
- **Batched Processing**: Logs are collected and sent in batches (100 logs or 5 seconds)
- **Resilience**: Automatic retries, fallback buffer, and background recovery
- **Monitoring**: Metrics available via `/health/logging` REST endpoint
- **GraphQL Access**: Logs can be queried via `admin.logs`, `admin.searchLogs`, and `admin.logStatistics`

### Monitoring

- **REST Endpoint**: `GET /health/logging` - Get logging system health and metrics (no auth required)
- **GraphQL Queries**: Use Admin Module queries to access logs and statistics (SuperAdmin only)

For detailed information, see:

- [Admin Module - Logging System Architecture](13_ADMIN_MODULE.md#logging-system-architecture)
- [Health Module - REST Endpoints](08_HEALTH_MODULE.md#rest-endpoints)

## Getting Started

1. **Authenticate**: Use `auth.login` or `auth.register`
2. **Explore**: Use `health.apiMetadata` to get API information
3. **Query Data**: Use `contacts.contacts` or `companies.companies`
4. **Manage Account**: Use `users.updateProfile` or `billing.billing`

## JSON and GraphQL example conventions

- **GraphQL examples**: Use fenced blocks with ````graphql` for queries and mutations. Field names use camelCase in the schema (e.g. `pageId`, `pageType`).
- **JSON examples**: Use fenced blocks with ````json` for request/response and error examples. All JSON must be valid (double-quoted keys and values, no trailing commas, no `|` in values—use a single example value and describe alternatives in prose).
- **Variables**: GraphQL variables are passed as a JSON object in the `variables` key of the request body: `{ "query": "...", "variables": { ... } }`. Use **camelCase** for variable and field names in the JSON (e.g. `inputCsvKey`, `pageType`).

## Task breakdown for learning and maintenance

Each module doc includes a **"Task breakdown (for maintainers)"** section with 3–6 small, actionable tasks for that module. Use the sequence below to learn the codebase end-to-end, then drill into per-module tasks.


| #   | Task                                  | Focus                                                                                                                                                                                                                                                |
| --- | ------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **Run the app**                       | Venv, `.env` from `deploy/env.example`, `GET /health`, `POST /graphql` with a simple query (e.g. `health { apiHealth { status } }` or `auth { me { uuid } }`).                                                                                       |
| 2   | **Trace one request**                 | `main.py` → middleware → GraphQL router → `get_context` in `app/graphql/context.py` → one resolver (e.g. `AuthQuery.me` or `ContactQuery.contact`). Note where `db` and `user` are attached to context.                                              |
| 3   | **Auth flow**                         | Trace `auth.login` → `authenticate_user` in `app/services/users/auth.py` → repositories → JWT. Trace context: `Authorization` header → `decode_token` → `UserRepository.get_by_uuid` → `context.user`. See `require_auth` in a protected resolver.   |
| 4   | **One domain module (e.g. Contacts)** | Under `app/graphql/modules/contacts/`: read `types`, `inputs`, `queries`, `mutations`. Follow one query (e.g. `contact(uuid)`) and one mutation (e.g. `createContact`) from resolver → ConnectraClient / CRUD helpers. See how inputs map to VQL.    |
| 5   | **VQL and Connectra**                 | In `app/utils/vql_converter.py`, see how filters become `where` / keyword_match / range. In `app/clients/connectra_client.py`: `query_contacts` / `query_companies` and error handling. Optionally trace one contact mutation through the client.    |
| 6   | **Jobs and variables**                | In `app/graphql/modules/jobs/inputs.py`, review all input types. In `mutations.py`, see how e.g. `CreateEmailFinderExportInput` is passed to TkdjobClient and how `scheduler_jobs` is created. Confirm camelCase in GraphQL vs snake_case in Python. |
| 7   | **Database layer**                    | `app/db/session.py`: `get_db`, pool, session in context. One model (e.g. `app/models/user.py`) and one repo (e.g. `app/repositories/user.py`: `get_by_uuid`). See how the async session is used.                                                     |
| 8   | **DataLoaders**                       | In `app/graphql/dataloaders.py`, inspect one loader (e.g. `user_by_uuid`). Find a type that has a `user` or `company` field and see how the loader is used to avoid N+1.                                                                             |
| 9   | **Schema wiring**                     | In `app/graphql/schema.py`, list all Query and Mutation namespaces and match each to its folder under `app/graphql/modules/`.                                                                                                                        |
| 10  | **Config and clients**                | In `app/core/config.py`, list DB, JWT, Connectra, Lambda URLs/keys, S3, logging. Map each client in `app/clients/` to the config it uses.                                                                                                            |
| 11  | **Errors and validation**             | In `app/graphql/errors.py`, see custom errors and handler. Grep for `handle_graphql_error`, `handle_connectra_error`, `handle_database_exception` in resolvers.                                                                                      |
| 12  | **Extensions**                        | In `app/graphql/extensions.py`, see QueryComplexityExtension and QueryTimeoutExtension; how complexity/depth/cost and timeout are enforced.                                                                                                          |
| 13  | **API docs vs code**                  | For 2–3 modules, compare this folder's `*_MODULE.md` with the corresponding `queries.py`, `mutations.py`, and `inputs.py`; note any drift.                                                                                                           |
| 14  | **Tests**                             | In `tests/`: `conftest.py` (fixtures, DB, context), then run tests for auth, contacts, or Connectra and relate them to the code paths above.                                                                                                         |
| 15  | **Deploy and env**                    | Skim `deploy/` and env templates; see how production secrets and service URLs are used; run `deploy/pre-deployment-check.sh` and `scripts/validate_env.py` if available.                                                                             |


**Per-module task breakdowns:** Each of the module files (e.g. [01_AUTH_MODULE.md](01_AUTH_MODULE.md), [03_CONTACTS_MODULE.md](03_CONTACTS_MODULE.md), [16_JOBS_MODULE.md](16_JOBS_MODULE.md)) ends with a **"Task breakdown (for maintainers)"** section listing 3–6 tasks specific to that module (e.g. trace login flow, verify VQL conversion, confirm activity logging).

## Documentation Structure

Each module documentation follows a standardized structure:

1. **Overview** - Module description and location in codebase
2. **Queries and mutations – parameters and variable types** (or **Queries – parameters and return types** / **Mutations – parameters and return types**) - Summary table of each operation with parameter names, GraphQL variable types, and return types; reminder to use camelCase in variables
3. **Types** - All GraphQL types with field descriptions
4. **Queries** - All available queries (if any) with:
  - Parameters and return types
  - Validation rules
  - Implementation details
  - Authentication/authorization requirements
5. **Mutations** - All available mutations (if any) with:
  - Parameters and return types
  - Validation rules
  - Implementation details
  - Authentication/authorization requirements
6. **Input Types** - All input types used in queries/mutations with validation rules
7. **Error Handling** - Comprehensive error handling documentation:
  - Error types with codes and status codes
  - Error response examples with extensions
  - Error handling patterns (input validation, database errors, external service errors)
  - Field-level validation error examples
8. **Usage Examples** - Practical examples including:
  - Complete operation flows
  - Error scenario examples
  - Common use cases
9. **Implementation Details** - Technical implementation information:
  - External service integration details
  - Repository/service integration
  - Error handling implementation patterns
  - Transaction rollback mechanisms
  - Response validation processes
  - Non-blocking operations
  - User isolation
  - Pagination handling
10. **Related Modules** - Cross-references to related modules
11. **Task breakdown (for maintainers)** - 3–6 small, actionable tasks for learning and maintaining that module (trace resolvers, verify validation, confirm logging, etc.)

## Common Patterns

### Validation Patterns

All modules implement consistent validation patterns:

- **Pagination Validation**: Uses `validate_pagination` utility (limit: 1-1000, offset: non-negative)
- **UUID Validation**: UUID format validation for IDs
- **String Length Validation**: Max length limits for strings (varies by field)
- **Email Validation**: Email format validation using `validate_email_format`
- **Password Validation**: Minimum 8 characters using `validate_password`
- **Enum Validation**: Enum values validated with improved error messages listing valid options
- **Date Range Validation**: startDate must be before endDate if both provided
- **Input Validation**: All input types include `validate()` methods

### Non-Blocking Operations

Several modules use non-blocking patterns for secondary operations:

- **Activity Logging**: Activity logging failures don't prevent primary operations
- **Credit Deduction**: Credit deduction failures are logged but don't fail operations
- **User History**: User history creation during auth is non-blocking
- **Analytics Submission**: Analytics metric storage failures don't prevent success responses
- **Upload Session Cleanup**: Upload session cleanup failures are logged but don't fail operations

### User Isolation

All modules enforce user isolation:

- **Repository Level**: Queries filter by user_id at repository level
- **Service Level**: Services verify user ownership before operations
- **GraphQL Level**: Queries/mutations verify user context before processing
- **Error Handling**: Raises NotFoundError if resource doesn't belong to user

### Pagination

Consistent pagination across all list queries:

- **Default Limit**: 100 items (varies by module)
- **Max Limit**: 1000 items
- **Default Offset**: 0
- **Validation**: Uses `validate_pagination` utility
- **Response**: Includes total count, limit, offset, hasNext, hasPrevious

## Error Handling

All modules implement comprehensive error handling with:

- **Input Validation**: All inputs are validated before processing
- **Database Error Handling**: Centralized handling for SQLAlchemy and MongoDB errors via `handle_database_exception`
- **External Service Error Handling**: Centralized handling for all external APIs (Connectra, S3, Lambda services)
- **GraphQL Error Types**: Custom error types with extensions for detailed error information
- **Transaction Safety**: All database operations are atomic with rollback on failure
- **Response Validation**: All external API responses are validated
- **Comprehensive Logging**: All errors are logged with context for debugging

### Standard Error Types

- **UnauthorizedError** (401): Authentication required or invalid credentials
- **ForbiddenError** (403): Insufficient permissions
- **NotFoundError** (404): Resource not found
- **ValidationError** (422): Input validation failed (includes field-level errors)
- **BadRequestError** (400): Invalid request data
- **ServiceUnavailableError** (503): External service unavailable
- **RateLimitError** (429): Rate limit exceeded
- **InternalServerError** (500): Internal server error

All errors follow the GraphQL error format with `extensions` containing:

- `code`: Error code (e.g., "NOT_FOUND", "VALIDATION_ERROR")
- `statusCode`: HTTP status code
- Additional context (e.g., `resourceType`, `identifier`, `fieldErrors`, `serviceName`)

See individual module documentation for specific error scenarios and examples.

### Error Handling Utilities

- `**handle_graphql_error`**: Centralized GraphQL error handler
- `**handle_database_exception**`: Centralized database error handler
- `**handle_connectra_error**`: Connectra API error handler
- `**handle_s3_error**`: S3 service error handler
- `**handle_external_error**`: Generic external service error handler

## Module documentation contract

Each module file in this directory should include:

- Era ownership (`era`)
- Version introduction/deprecation mapping per operation
- Frontend binding references (`docs/frontend/pages/*.json`)
- Data-store touch points (tables/indexes/buckets)

## `s3storage` module maintenance requirements (cross-era)

For storage-impacting releases (`0.x`-`10.x`), keep module docs aligned across:

- `07_S3_MODULE.md` (file operations, CSV read/preview/schema/stats contract)
- `10_UPLOAD_MODULE.md` (multipart lifecycle and retry/idempotency expectations)

And ensure these references are synchronized in the same update:

- `docs/codebases/s3storage-codebase-analysis.md`
- `docs/roadmap.md` storage execution stream
- `docs/versions.md` storage execution spine

## `logs.api` module maintenance requirements

- Keep endpoint docs aligned with `lambda/logs.api/app/api/v1/endpoints/logs.py`.
- Keep era mapping aligned with `docs/backend/endpoints/logsapi_endpoint_era_matrix.json`.
- Reflect auth and contract changes in per-era task packs.

## `emailapis` / `emailapigo` module maintenance requirements

- Keep `15_EMAIL_MODULE.md` aligned with both runtimes (`lambda/emailapis`, `lambda/emailapigo`).
- Keep endpoint docs aligned with `docs/backend/endpoints/emailapis_endpoint_era_matrix.json`.
- Keep era mapping aligned with `docs/backend/apis/EMAILAPIS_ERA_TASK_PACKS.md` and per-era task pack docs.
- Provider drift (`truelist` vs `mailvetter`) must be documented with migration notes before release promotion.
- Any status semantics changes must update frontend binding docs and GraphQL examples in the same PR.

## `connectra` module maintenance requirements

- Deep runtime reference: [sync-codebase-analysis.md](../../codebases/sync-codebase-analysis.md) (normalized era map); [connectra-codebase-analysis.md](../../codebases/connectra-codebase-analysis.md) covers the same `contact360.io/sync` surface — avoid contradicting facts between the two; consolidate over time if duplicate.
- Keep `03_CONTACTS_MODULE.md` and `04_COMPANIES_MODULE.md` aligned with `contact360.io/sync` route behavior and VQL contract.
- Keep endpoint binding docs aligned with:
  - `docs/backend/endpoints/query_contacts_graphql.json`
  - `docs/backend/endpoints/query_companies_graphql.json`
  - `docs/backend/endpoints/count_contacts_graphql.json`
  - `docs/backend/endpoints/get_contact_filters_graphql.json`
  - `docs/backend/endpoints/get_company_filters_graphql.json`
- Keep era mapping aligned with `docs/backend/endpoints/connectra_endpoint_era_matrix.json`.
- Any VQL filter/operator changes must update `docs/3. Contact360 contact and company data system/vql-filter-taxonomy.md` in the same change.
- Any batch-upsert schema change must include idempotency and rollback evidence in docs before release promotion.

## `jobs` module maintenance requirements

- Keep `16_JOBS_MODULE.md` aligned with runtime behavior in `contact360.io/jobs` (`app/api/v1/routes/jobs.py`, scheduler/worker/processor contracts).
- Keep job lifecycle/status vocabulary synchronized with scheduler constants (`open`, `in_queue`, `processing`, `completed`, `failed`, `retry`).
- Keep era mapping aligned with `docs/backend/apis/JOBS_ERA_TASK_PACKS.md` and per-era `docs/0...10/jobs-*-task-pack.md`.
- Keep data lineage references synchronized with `docs/backend/database/jobs_data_lineage.md`.
- Any processor registry change must update REST endpoint mapping and UI binding docs in the same change.

## `contact.ai` module maintenance requirements

- Keep `17_AI_CHATS_MODULE.md` aligned with actual REST routes in `backend(dev)/contact.ai` (`/api/v1/ai-chats/`, `/api/v1/ai/`).
- Keep `ModelSelection` enum values synchronized between GraphQL schema and HF model IDs; `LambdaAIClient` mapping shim must be updated in the same change.
- Any new utility endpoint (`/api/v1/ai/…`) must update `contact_ai_endpoint_era_matrix.json` and the `CONTACT_AI_ERA_TASK_PACKS.md` index.
- Any JSONB `messages` schema change must update `contact_ai_data_lineage.md` and `17_AI_CHATS_MODULE.md` in the same PR.
- Keep era mapping aligned with `docs/backend/apis/CONTACT_AI_ERA_TASK_PACKS.md` and per-era `docs/0...10/contact-ai-*-task-pack.md`.
- Keep UI binding docs synchronized with `docs/frontend/contact-ai-ui-bindings.md`.

## `email campaign` module maintenance requirements

- REST service index: `docs/backend/services.apis/emailcampaign.api.md` (links modules, matrices, and runtime analysis).
- **Gateway today:** Root `Query.campaignSatellite` exposes read-only `campaigns`, `sequences`, and `campaignTemplates` as `JSON` (see `22`–`25` module docs and `app/graphql/modules/campaigns/queries.py`). **Mutations** and richer typed campaign GraphQL remain **planned**; track in [APPOINTMENT360_GATEWAY_TASK_BOARD.md](APPOINTMENT360_GATEWAY_TASK_BOARD.md) (section **10.x.x — Email campaign**).
- Keep `22_CAMPAIGNS_MODULE.md`, `24_SEQUENCES_MODULE.md`, and `25_CAMPAIGN_TEMPLATES_MODULE.md` aligned with the REST route surface in `backend(dev)/email campaign` (`api/handlers.go`, `template/handlers.go`).
- Campaign status vocabulary (`pending`, `sending`, `completed`, `completed_with_errors`, `failed`, `paused`) must stay synchronized between these docs, the Go worker code (`worker/campaign_worker.go`), and all frontend status badge components.
- Any template variable changes (e.g. adding `{{.Company}}`, `{{.Title}}`) must update `22_CAMPAIGNS_MODULE.md`, the Go `TemplateData` struct, and `docs/frontend.md` campaign UI section in the same change.
- Keep era mapping aligned with `docs/backend/endpoints/emailcampaign_endpoint_era_matrix.json` and per-era `docs/0...10/emailcampaign-*-task-pack.md`.
- Keep data lineage references synchronized with `docs/backend/database/emailcampaign_data_lineage.md`.
- Schema changes (new columns or tables) must update `db/schema.sql`, migration scripts, and the schema section in `docs/10. Contact360 email campaign/emailcampaign-service.md` in the same PR.
- Any Asynq task type change must update `tasks/campaign.go` and all documentation referencing `campaign:send` task type.
- Keep suppression list semantics in sync between `db/queries.go`, `worker/email_worker.go` suppression check, and unsubscribe endpoint contract docs.

## `sales navigator` module maintenance requirements

- Keep `23_SALES_NAVIGATOR_MODULE.md` aligned with actual REST routes in `backend(dev)/salesnavigator` (`/v1/scrape`, `/v1/save-profiles`).
- Any new endpoint must update `salesnavigator_endpoint_era_matrix.json` and the `SALESNAVIGATOR_ERA_TASK_PACKS.md` index.
- Docs drift must be fixed atomically: if `docs/api.md` documents a route, that route must be implemented (or the doc entry removed).
- Keep field mapping semantics in sync between `app/services/mappers.py`, `salesnavigator_data_lineage.md`, and `23_SALES_NAVIGATOR_MODULE.md`.
- Any change to UUID generation logic (`generate_contact_uuid`, `generate_company_uuid`) must update `salesnavigator_data_lineage.md` and the contract docs in the same PR.
- Keep era mapping aligned with `docs/backend/apis/SALESNAVIGATOR_ERA_TASK_PACKS.md` and per-era `docs/0...10/salesnavigator-*-task-pack.md`.
- Keep UI binding docs synchronized with `docs/frontend/salesnavigator-ui-bindings.md`.
- CORS policy changes must be documented in architecture notes and reviewed for security impact.

## `appointment360` module maintenance requirements

- **Era-level gateway tasks:** When scoping or closing `0.x.x`–`10.x.x` work for the GraphQL gateway, update [APPOINTMENT360_GATEWAY_TASK_BOARD.md](APPOINTMENT360_GATEWAY_TASK_BOARD.md) in the same change set as material schema or client edits; keep the mounted-vs-doc-only module table in [APPOINTMENT360_ERA_TASK_PACKS.md](APPOINTMENT360_ERA_TASK_PACKS.md) accurate.
- All `contact360.io/api` GraphQL module doc files (`01_AUTH_MODULE.md` through `29_RESUME_AI_REST_SERVICE.md` for gateway-facing ops) must stay synchronized with the actual Strawberry schema classes in `app/graphql/modules/` (and linked REST contracts where `29` applies).
- **Schema composition rule:** any module added to `app/graphql/schema.py` must have a corresponding `NN_MODULE.md` file added to this folder in the same PR. Module numbers must not be reused.
- **Downstream client rule:** any change to `app/clients/*.py` that changes request/response shape must update the relevant module doc and any associated endpoint JSON in `docs/backend/endpoints/`.
- **Debug write rule (critical):** no inline `open(...)` file writes may remain in any `app/graphql/modules/` file. Each PR must include a static check or evidence of removal.
- **Middleware order rule:** any change to the 8-layer middleware stack order in `app/main.py` must update the middleware table in `docs/codebases/appointment360-codebase-analysis.md` and `docs/architecture.md` in the same PR.
- **DataLoader rule:** any new resolver that fetches related entities by FK must include a DataLoader implementation. Direct ORM fetches in list resolvers are rejected in code review for `3.x+` modules.
- Keep era mapping aligned with `docs/backend/endpoints/appointment360_endpoint_era_matrix.json` and per-era `docs/0...10/appointment360-*-task-pack.md`.
- Keep data lineage references synchronized with `docs/backend/database/appointment360_data_lineage.md`.
- Any new PostgreSQL table in the appointment360 DB must update `appointment360_data_lineage.md` and the relevant era task-pack in the same PR.
- Keep UI binding docs synchronized with `docs/frontend.md` (Contact360 gateway section).

## `mailvetter` module maintenance requirements

- Standalone REST reference: `docs/backend/services.apis/mailvetter.api.md` (filename uses **mailvetter**; do not reintroduce the legacy `mailvaiter` spelling in new links).
- Keep verifier contract references in `15_EMAIL_MODULE.md` synchronized with actual mailvetter `/v1` route behavior and response schema.
- Keep endpoint mapping synchronized with `docs/backend/endpoints/mailvetter_endpoint_era_matrix.json`.
- Keep data lineage synchronized with `docs/backend/database/mailvetter_data_lineage.md`.
- `/v1` routes are canonical. Legacy `/verify|/upload|/status|/results` endpoints are compatibility-only and must not be referenced for new integrations.
- Any scoring/status semantics change in mailvetter (`internal/validator/scoring.go`) must update frontend status mapping docs (`docs/frontend.md`) and email module docs in the same PR.
- Any schema change in mailvetter `jobs`/`results` must update lineage docs and era task-pack index (`MAILVETTER_ERA_TASK_PACKS.md`) in the same change set.
