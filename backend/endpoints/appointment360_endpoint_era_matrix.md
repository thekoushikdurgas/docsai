---
title: "appointment360 — era matrix"
source_json: appointment360_endpoint_era_matrix.json
generator: json_to_markdown_endpoints.py
---

# appointment360

## Service metadata

| Field | Value |
| --- | --- |
| service | appointment360 |
| codebase | contact360.io/api |
| runtime | FastAPI + Strawberry GraphQL + asyncpg + PostgreSQL |
| primary_endpoint | POST /graphql |
| description | GraphQL-only gateway. All dashboard and extension requests enter through /graphql. No REST feature routes. 29 nested GraphQL namespaces in schema (plus 10.x campaign modules scaffold-only). Orchestrates Connectra, email.server/sync.server job APIs (via gateway clients), Lambda Email, Lambda AI, Resume AI, S3 Storage, Logs API, DocsAI. |
| data_lineage_reference | docs/backend/database/appointment360_data_lineage.md |
| era_task_packs | docs/backend/apis/APPOINTMENT360_ERA_TASK_PACKS.md |
| codebase_analysis | docs/codebases/appointment360-codebase-analysis.md |


## health_endpoints

- GET /health
- GET /health/db
- GET /health/logging
- GET /health/slo
- GET /health/token-blacklist

## auth_modes

- Bearer JWT (HS256)
- X-API-Key (8.x+)

## graphql_modules (by era)

| Era | Modules |
| --- | --- |
| 0.x | auth, health |
| 1.x | users, billing, usage, activities |
| 2.x | email, jobs, upload |
| 3.x | contacts, companies, s3, savedSearches |
| 4.x | linkedin, salesNavigator |
| 5.x | aiChats, resume |
| 6.x | analytics |
| 7.x | admin |
| 8.x | pages, profile, twoFactor |
| 9.x | notifications, featureOverview, webhooks, integrations |
| 10.x | campaigns, sequences, campaignTemplates (scaffold — not mounted in `schema.py` yet) |


## module_index

| number | module | era | doc | queries | mutations |
| --- | --- | --- | --- | --- | --- |
| 01 | auth | 0.x | 01_AUTH_MODULE.md | ['me', 'session'] | ['login', 'register', 'logout', 'refresh_token'] |
| 02 | users | 1.x | 02_USERS_MODULE.md | ['user', 'users', 'userStats'] | ['update_profile', 'upload_avatar', 'update_user', 'promote_to_admin', 'promote_to_super_admin'] |
| 03 | contacts | 3.x | 03_CONTACTS_MODULE.md | ['contact', 'contacts', 'contactCount', 'contactQuery', 'filters', 'filterData'] | ['createContact', 'batchCreateContacts', 'importContacts', 'updateContact', 'deleteContact', 'exportContacts'] |
| 04 | companies | 3.x | 04_COMPANIES_MODULE.md | ['company', 'companies', 'companyCount', 'companyQuery', 'companyContacts', 'filters', 'filterData'] | ['createCompany', 'exportCompanies', 'importCompanies', 'updateCompany', 'deleteCompany'] |
| 05 | notifications | 9.x | 05_NOTIFICATIONS_MODULE.md | ['notifications', 'notification', 'unreadCount', 'notificationPreferences'] | ['markNotificationAsRead', 'markNotificationsAsRead', 'deleteNotifications', 'updateNotificationPreferences'] |
| 06 | webhooks | 9.x | 06_WEBHOOKS_MODULE.md | [] | [] |
| 07 | s3 | 3.x | 07_S3_MODULE.md | ['s3Files', 's3FileData', 's3FileInfo', 's3FileDownloadUrl', 's3FileSchema', 's3FileStats', 's3BucketMetadata'] | ['initiateCsvUpload', 'completeCsvUpload', 'deleteFile'] |
| 08 | health | 0.x | 08_HEALTH_MODULE.md | ['apiMetadata', 'apiHealth', 'vqlHealth', 'vqlStats', 'performanceStats'] | [] |
| 09 | usage | 1.x | 09_USAGE_MODULE.md | ['usage', 'featureOverview'] | ['trackUsage', 'resetUsage'] |
| 10 | upload | 2.x | 10_UPLOAD_MODULE.md | ['uploadStatus', 'presignedUrl'] | ['initiateUpload', 'registerPart', 'completeUpload', 'abortUpload'] |
| 11 | activities | 1.x | 11_ACTIVITIES_MODULE.md | ['activities', 'activityStats'] | [] |
| 13 | admin | 7.x | 13_ADMIN_MODULE.md | ['users', 'usersWithBuckets', 'userStats', 'userHistory', 'logStatistics', 'logs', 'searchLogs'] | ['updateUserRole', 'updateUserCredits', 'deleteUser', 'promoteToAdmin', 'promoteToSuperAdmin', 'createLog', 'createLogsBatch', 'updateLog', 'deleteLog', 'deleteLogsBulk'] |
| 14 | billing | 1.x | 14_BILLING_MODULE.md | ['billing', 'plans', 'addons', 'invoices', 'paymentInstructions', 'paymentSubmissions'] | ['subscribe', 'purchaseAddon', 'submitPaymentProof', 'approvePayment', 'declinePayment'] |
| 15 | email | 2.x | 15_EMAIL_MODULE.md | ['findEmails', 'findEmailsBulk', 'verifySingleEmail', 'verifyEmailsBulk', 'emailJobStatus', 'webSearch', 'exportEmails', 'verifyexportEmail', 'predictEmailPattern', 'predictEmailPatternBulk'] | ['addEmailPattern', 'addEmailPatternBulk'] |
| 16 | jobs | 2.x | 16_JOBS_MODULE.md | ['job', 'jobs'] | ['createEmailFinderExport', 'createEmailVerifyExport', 'createEmailPatternExport', 'createContact360Export', 'createContact360Import', 'pauseJob', 'resumeJob', 'terminateJob', 'retryJob'] |
| 17 | aiChats | 5.x | 17_AI_CHATS_MODULE.md | ['aiChat', 'aiChats'] | ['createAIChat', 'updateAIChat', 'deleteAIChat', 'sendMessage', 'analyzeEmailRisk', 'generateCompanySummary', 'parseContactFilters'] |
| 18 | analytics | 6.x | 18_ANALYTICS_MODULE.md | ['performanceMetrics', 'aggregateMetrics'] | ['submitPerformanceMetric'] |
| 19 | pages | 8.x | 19_PAGES_MODULE.md | ['page', 'pages', 'pageContent', 'pagesByType', 'pageTypes', 'pageStatistics', 'pagesByState', 'pagesByStateCount', 'pagesByUserType', 'pagesByDocsaiUserType', 'myPages', 'pageAccessControl', 'pageSections', 'pageComponents', 'pageEndpoints', 'pageVersions', 'dashboardPages', 'marketingPages'] | [] |
| 20 | integrations | 9.x | 20_INTEGRATIONS_MODULE.md | [] | [] |
| 21 | linkedin | 4.x | 21_LINKEDIN_MODULE.md | [] | ['search', 'upsertByLinkedInUrl'] |
| 22 | campaigns | 10.x | 22_CAMPAIGNS_MODULE.md | [] | [] |
| 23 | salesNavigator | 4.x | 23_SALES_NAVIGATOR_MODULE.md | ['salesNavigatorRecords'] | ['saveSalesNavigatorProfiles'] |
| 24 | sequences | 10.x | 24_SEQUENCES_MODULE.md | [] | [] |
| 25 | campaignTemplates | 10.x | 25_CAMPAIGN_TEMPLATES_MODULE.md | [] | [] |
| 26 | savedSearches | 3.x | 26_SAVED_SEARCHES_MODULE.md | ['listSavedSearches', 'getSavedSearch'] | ['createSavedSearch', 'updateSavedSearch', 'deleteSavedSearch', 'updateSavedSearchUsage'] |
| 27 | twoFactor | 8.x | 27_TWO_FACTOR_MODULE.md | ['get2FAStatus'] | ['setup2FA', 'verify2FA', 'disable2FA', 'regenerateBackupCodes'] |
| 28 | profile | 8.x | 28_PROFILE_MODULE.md | ['listAPIKeys', 'listSessions', 'listTeamMembers'] | ['createAPIKey', 'deleteAPIKey', 'revokeSession', 'revokeAllOtherSessions', 'inviteTeamMember', 'updateTeamMemberRole', 'removeTeamMember'] |
| 29 | resume | 5.x | 29_RESUME_MODULE.md | ['resumes', 'resume'] | ['saveResume', 'deleteResume'] |


## era_by_era

### 0.x

- **description:** Service bootstrap — FastAPI app, middleware stack, DB session lifecycle, health endpoints
**active_modules**

- auth
- health

**db_tables_added**

- users
- token_blacklist

**downstream_clients_added**


**gaps_at_0x**

- No feature modules
- No downstream clients
- Rate limit not yet configured

**config_keys_required**

- SECRET_KEY
- ACCESS_TOKEN_EXPIRE_MINUTES
- DATABASE_URL
- POSTGRES_*


### 1.x

- **description:** User, billing, credit system — auth mutations, credit deduction, billing service
**active_modules**

- auth
- health
- users
- billing
- usage
- activities

**db_tables_added**

- credits
- plans
- subscriptions
- payment_submissions
- activities

**downstream_clients_added**


- **behavioral_changes:** Idempotency required on billing mutations. Credit deduction on all feature operations.
**config_keys_required**

- ACCESS_TOKEN_EXPIRE_MINUTES
- REFRESH_TOKEN_EXPIRE_DAYS
- IDEMPOTENCY_REQUIRED_MUTATIONS


### 2.x

- **description:** Email system — finder/verifier, jobs orchestration, bulk export/import
**active_modules**

- email
- jobs
- upload

**db_tables_added**


**downstream_clients_added**

- LambdaEmailClient
- EmailServerJobsClient

- **behavioral_changes:** Email find/verify credit deduction. Job polling UI via query job(jobId).
**bugs_to_fix**

- Remove debug file writes from email/queries.py and jobs/mutations.py

**config_keys_required**

- LAMBDA_EMAIL_API_URL
- LAMBDA_EMAIL_API_KEY
- CONNECTRA_BASE_URL
- CONNECTRA_API_KEY


### 3.x

- **description:** Contacts and companies — ConnectraClient, VQL converter, DataLoaders, saved searches
**active_modules**

- contacts
- companies
- s3
- savedSearches

**db_tables_added**

- saved_searches

**downstream_clients_added**

- ConnectraClient
- LambdaS3StorageClient

- **behavioral_changes:** All contact/company data routed through Connectra. VQLQueryInput → Connectra REST. DataLoaders required.
**config_keys_required**

- CONNECTRA_BASE_URL
- CONNECTRA_API_KEY
- CONNECTRA_TIMEOUT
- LAMBDA_S3STORAGE_API_URL
- LAMBDA_S3STORAGE_API_KEY


### 4.x

- **description:** Extension and Sales Navigator — LinkedIn mutations, SN search and save, extension session auth
**active_modules**

- linkedin
- salesNavigator

**db_tables_added**

- sessions

**downstream_clients_added**

- SalesNavigatorClient

- **behavioral_changes:** Extension Bearer tokens validated. SN search credit deduction. Upsert by LinkedIn URL.
**config_keys_required**

- LAMBDA_SN_API_URL
- LAMBDA_SN_API_KEY


### 5.x

- **description:** AI workflows — AI chats, company summary, email risk, NL filter parsing, resume
**active_modules**

- aiChats
- resume

**db_tables_added**

- ai_chats
- ai_chat_messages
- resumes

**downstream_clients_added**

- LambdaAIClient
- ResumeAIClient

- **behavioral_changes:** AI credit deduction per message. SSE streaming for sendAiMessage. Utility mutations stateless (no DB write).
**config_keys_required**

- LAMBDA_AI_API_URL
- LAMBDA_AI_API_KEY
- RESUME_AI_BASE_URL
- RESUME_AI_API_KEY


### 6.x

- **description:** Reliability and scaling — rate limiting, abuse guard, idempotency, complexity/timeout extensions, SLO
**active_modules**

- analytics

**db_tables_added**


- **behavioral_changes:** GRAPHQL_RATE_LIMIT_REQUESTS_PER_MINUTE must be > 0. Redis state for idempotency/abuse guard. QueryComplexityExtension and QueryTimeoutExtension enabled.
**config_keys_required**

- GRAPHQL_RATE_LIMIT_REQUESTS_PER_MINUTE
- GRAPHQL_COMPLEXITY_LIMIT
- GRAPHQL_QUERY_TIMEOUT
- REDIS_URL
- ENABLE_REDIS_CACHE
- SLO_ERROR_BUDGET_PERCENT


### 7.x

- **description:** Deployment hardening — CI/CD, Dockerfile, SuperAdmin RBAC guards, Alembic migration hygiene
**active_modules**

- admin

**db_tables_added**


- **behavioral_changes:** require_super_admin guard on all admin mutations. Production: DEBUG=false, GraphiQL disabled.
**config_keys_required**

- ENVIRONMENT
- DEBUG
- TRUSTED_HOSTS
- CORS_ORIGINS


### 8.x

- **description:** Public and private APIs — Pages/DocsAI, saved searches, profile/API keys, 2FA, X-API-Key public auth
**active_modules**

- pages
- profile
- twoFactor

**db_tables_added**

- api_keys
- sessions

**db_columns_added**

- {'table': 'users', 'column': 'totp_secret', 'type': 'TEXT NULL'}

**downstream_clients_added**

- DocsAIClient

- **behavioral_changes:** X-API-Key auth path added. Public API rate limiting separate from authenticated. DOCSAI_ENABLED flag.
**config_keys_required**

- DOCSAI_API_URL
- DOCSAI_API_KEY
- DOCSAI_ENABLED


### 9.x

- **description:** Ecosystem integrations — notifications, analytics events, admin panel, tenant model, webhooks
**active_modules**

- notifications
- featureOverview
- webhooks
- integrations

**db_tables_added**

- notifications
- events
- feature_flags
- workspaces

- **behavioral_changes:** Notifications polling every 30s from dashboard. Plan-based feature gates. Webhook outbound dispatch.
**config_keys_required**

- WEBHOOK_SECRET


### 10.x

- **description:** Email campaign — campaigns, sequences, campaign templates GraphQL modules; proxy to email campaign service (resolver modules exist as scaffold; not yet mounted on root schema)
**active_modules**

- campaigns (scaffold)
- sequences (scaffold)
- campaignTemplates (scaffold)

**db_tables_added**


**downstream_clients_added**

- CampaignServiceClient

- **behavioral_changes:** Campaign data owned by email campaign service DB. appointment360 records campaign_id in activities. Credit deduction per recipient count.
**prerequisites**

- email campaign service schema drift bugs must be fixed
- GetUnsubToken DB.Exec → DB.Get bug must be fixed
- SMTP nil auth bug must be fixed

**config_keys_required**

- CAMPAIGN_SERVICE_URL
- CAMPAIGN_SERVICE_API_KEY


## known_gaps

- AP-0.1 resolved: resolver/client debug artifact regression guard added (`tests/test_no_debug_artifacts.py`) and risky runtime paths are clean
- AP-0.2 resolved: production startup now fails closed for wildcard `ALLOWED_ORIGINS`/`TRUSTED_HOSTS` and enforces URL/API-key pairing (plus enablement checks) for downstream services
- AP-0.2 evidence: `deploy/env.example` and `deploy/env.production.template` now use redacted/empty placeholders (no real-looking API Gateway URLs or token-like keys)
- AP-1.2 resolved: abuse guard now supports PostgreSQL-backed shared window state (`graphql_abuse_guard_events`), and production enforces postgres backends for idempotency/upload sessions/abuse guard
- AP-1.3 resolved: `/health/slo` now exports guarded mutation SLI metrics (`guarded_mutation_sli`) including per-mutation request/success/error/rate-limited and latency fields
- 10.x GraphQL: `campaigns`, `sequences`, and `campaignTemplates` modules under `app/graphql/modules/campaigns/` are not imported in `schema.py`; `module_index` rows 22/24/25 use empty operation lists until wired

<!-- AUTO:db-graph:start -->

## Era alignment

See **era_focus** and route tables above — themes match [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md#era-tags-on-endpoints).

## Database & lineage

- Service: `appointment360`
- Use the matching row in [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md#lambda--worker-services-by-path) and the lineage file linked there.

## Related

- [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md)
- [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md)

<!-- AUTO:db-graph:end -->
---

*Generated from `appointment360_endpoint_era_matrix.json`. Re-run `python json_to_markdown_endpoints.py`.*
