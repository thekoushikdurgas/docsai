# Gateway `admin.*` GraphQL module

**Last reviewed:** 2026-04-21 (audit + two-person approval + `graphqlAuditEvents`)  
**Anchor:** [`DECISIONS.md`](../../../DECISIONS.md), [`public-private.md`](public-private.md)  
**Implementation:** `contact360.io/api/app/graphql/modules/admin/`

The `admin` namespace on `POST /graphql` is **authenticated** and **role-gated**. Decorators:

- `@require_super_admin_resolver` — field requires SuperAdmin at the GraphQL layer.
- `@require_admin_resolver` — field requires Admin or SuperAdmin.

Additional in-resolver checks repeat role validation against `UserProfile.role` (defence in depth).

## Queries (`AdminQuery`)

| GraphQL field | Strawberry name | Role (effective) | Downstream / data source |
| ------------- | --------------- | ---------------- | -------------------------- |
| `users` | `users` | SuperAdmin | Gateway Postgres (`UserRepository.list_all_users`) |
| `usersWithBuckets` | `usersWithBuckets` | Admin or SuperAdmin | Gateway Postgres (same list; bucket for storage UI) |
| `userStats` | `userStats` | Admin or SuperAdmin | Gateway Postgres aggregates |
| `schedulerJobs` | `schedulerJobs` | Admin or SuperAdmin | Gateway Postgres `scheduler_jobs` (`SchedulerJobRepository`) |
| `userHistory` | `userHistory` | SuperAdmin | `UserService.get_user_history` |
| `logStatistics` | `logStatistics` | SuperAdmin | `LogStatsRepository` (gateway-side stats; not raw log.server aggregate in all paths) |
| `logs` | `logs` | SuperAdmin | **log.server** via `LogsServerClient.query_logs` |
| `searchLogs` | `searchLogs` | SuperAdmin | **log.server** via `LogsServerClient.search_logs` |
| `graphqlAuditEvents` | `graphqlAuditEvents` | SuperAdmin | Gateway Postgres `graphql_audit_events` (append-only audit for `admin.*` mutations) |

## Mutations (`AdminMutation`)

| GraphQL field | Role | Downstream / data source |
| ------------- | ---- | ------------------------ |
| `updateUserRole` | SuperAdmin | Gateway Postgres `UserProfile` |
| `updateUserCredits` | SuperAdmin | Gateway + `BillingService` |
| `deleteUser` | SuperAdmin | Gateway user delete path; optional two-person `approvalId` (see below) |
| `promoteToAdmin` | SuperAdmin | Gateway profile role |
| `promoteToSuperAdmin` | SuperAdmin | Gateway profile role; optional two-person `approvalId` |
| `requestDangerousOperationApproval` | SuperAdmin | Creates `admin_dangerous_approvals` ticket (`delete_user` / `promote_super_admin`) |
| `createLog` | SuperAdmin | **log.server** via `LogsServerClient` |
| `createLogsBatch` | SuperAdmin | **log.server** |
| `updateLog` | SuperAdmin | **log.server** |
| `deleteLog` | SuperAdmin | **log.server** |
| `deleteLogsBulk` | SuperAdmin | **log.server** |
| `runSubscriptionExpirySweep` | SuperAdmin | Billing / subscription maintenance (gateway) |

### Two-person approval (optional)

- Env: `REQUIRE_TWO_PERSON_DANGEROUS_ADMIN=true` on the gateway — then `deleteUser` and `promoteToSuperAdmin` require a prior `requestDangerousOperationApproval` ticket and an `approvalId` on the mutation input. A **different** SuperAdmin than the requester must execute the mutation.
- Audit: each `admin.*` mutation appends `graphql_audit_events` with `detail.payload_sha256` over the detail object.

## Related gateway modules (operator console)

| Namespace | Notes |
| --------- | ----- |
| `health.apiMetadata` | Adds optional `buildSha`, `gitRef` (from `BUILD_SHA`, `GIT_REF`) for release badges. |
| `knowledge.*` | SuperAdmin CRUD for `knowledge_articles` (operator knowledge base). |
| `jobs.deadLetterJobs` | Admin/SuperAdmin list of scheduler jobs in `failed` status (Postgres DLQ-style). |
| `POST /api/v1/ai-chats/{chatId}/message/stream` | Authenticated SSE proxy to Contact AI (not under `admin.*`). |

## Policy for the Django admin UI

The internal console at `contact360.io/admin` should call these operations with a **user JWT** (operator session) that has Admin/SuperAdmin on the gateway. It must **not** hold satellite `X-API-Key` values in steady state; only the gateway talks to **log.server**, Connectra, etc.

## Other gateway namespaces consumed by the Django admin UI

These are **not** under `admin.*` but are called with the same operator JWT:

| Root field | Used for |
| ---------- | -------- |
| `contacts.contacts` | Read-only operator contact list (`/admin/ops/contacts-explorer/`). |
| `campaignSatellite.cqlParse` / `cqlValidate` / `renderTemplatePreview` | Campaign CQL lab (`/admin/ops/campaign-cql/`). |
| `aiChats` (queries + mutations) | AI chat sessions and messages (`/ai/`). |
| `health.apiMetadata` | Build name / version / docs link on system status. |
| `health.satelliteHealth` | Satellite ping table (also used on analytics). |
| `s3.deleteFile` | Optional deletes when `ADMIN_STORAGE_VIA_GATEWAY=true` (see admin `README.md`). |

## Related docs

- [`ROUTES.md`](ROUTES.md) — root Query/Mutation namespaces  
- [`PIPELINE.md`](PIPELINE.md) — admin logs pipeline  
- [`SATELLITE-PARITY.md`](SATELLITE-PARITY.md) — gateway → satellite mapping  
- One-page admin app overview: [`../../../codebases/admin.md`](../../../codebases/admin.md)
