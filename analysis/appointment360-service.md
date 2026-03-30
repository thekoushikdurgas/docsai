# Appointment360 Service Reference (Era 8.x — Public & Private APIs)

## Service identity

- **Codebase**: `contact360.io/api`
- **Service name**: Appointment360 GraphQL Gateway
- **Primary interface**: `POST /graphql` (Strawberry GraphQL, Strawberry schema)
- **Health interfaces**: `GET /health`, `GET /health/db`, `GET /health/logging`, `GET /health/slo`
- **Auth**: HS256 JWT (Bearer header) + `X-API-Key` for public API surface (8.x+)
- **Deploy targets**: EC2 (uvicorn), AWS Lambda (Mangum), Docker

---

## GraphQL endpoint contract

### Endpoint

```
POST /graphql
Content-Type: application/json
Authorization: Bearer <access_token>        # for authenticated users
X-API-Key: <api_key>                        # for public API (8.x+)
X-Idempotency-Key: <uuid>                   # required for guarded mutations
X-Request-Id: <uuid>                        # optional — echoed in response
X-Trace-Id: <uuid>                          # optional — propagated to downstream
```

### Request envelope

```json
{
  "query": "query Contacts($query: VQLQueryInput!) { contacts(query: $query) { ... } }",
  "variables": { "query": { "where": "email:*@gmail.com", "page": 1, "per_page": 25 } },
  "operationName": "Contacts"
}
```

### Response envelope

```json
{
  "data": { "contacts": [ ... ] },
  "errors": null
}
```

### Error format

```json
{
  "data": null,
  "errors": [
    {
      "message": "UNAUTHENTICATED: Invalid or expired token",
      "locations": [{ "line": 1, "column": 7 }],
      "path": ["contacts"],
      "extensions": { "code": "UNAUTHENTICATED" }
    }
  ]
}
```

---

## Module surface (era 8.x baseline)

| Module | Query operations | Mutation operations |
| --- | --- | --- |
| `auth` | `me` | `login`, `register`, `logout`, `refresh_token` |
| `users` | `user(uuid)`, `users()`, `userStats()` | `updateUser`, `deleteUser`, `promoteUser` |
| `contacts` | `contact(uuid)`, `contacts(query)`, `contactCount(query)`, `filters()`, `filterData(input)` | `createContact`, `batchUpsertContacts`, `updateContact`, `deleteContact`, `exportContacts` |
| `companies` | `company(uuid)`, `companies(query)`, `companyCount(query)`, `companyContacts(uuid)`, `filters()`, `filterData(input)` | `createCompany`, `updateCompany`, `deleteCompany`, `exportCompanies` |
| `email` | `findEmails`, `findEmailsBulk`, `verifySingleEmail`, `verifyEmailsBulk` | `addEmailPattern`, `addEmailPatternBulk` |
| `jobs` | `job(jobId)`, `jobs(limit, offset, status, jobType)` | `createEmailFinderExport`, `createEmailVerifyExport`, `createEmailPatternImport`, `createContact360Export`, `createContact360Import`, `createAppointmentImport`, `retryJob` |
| `billing` | `billingInfo`, `plans`, `invoices` | `subscribe`, `purchaseAddon`, `submitPaymentProof`, `approvePayment`, `declinePayment` |
| `usage` | `usage(feature)` | `trackUsage`, `resetUsage` |
| `aiChats` | `aiChat(uuid)`, `aiChats()` | `createAiChat`, `sendAiMessage`, `deleteAiChat`, `generateCompanySummary`, `analyzeEmailRisk`, `parseContactFilters` |
| `resume` | `resumes()`, `resume(id)` | `createResume`, `updateResume`, `deleteResume` |
| `salesNavigator` | `salesNavigatorSearch()` | `saveSalesNavigatorProfiles`, `syncSalesNavigator` |
| `linkedin` | — | `upsertByLinkedinUrl`, `searchLinkedin`, `exportLinkedinResults` |
| `s3` | `files(bucket, prefix)`, `fileContent(key)` | `startCsvMultipartUpload`, `uploadCsvPart`, `completeCsvUpload` |
| `upload` | `uploadStatus(sessionId)` | `startMultipartUpload`, `uploadPart`, `completeMultipartUpload`, `abortMultipartUpload` |
| `savedSearches` | `savedSearch(id)`, `savedSearches(type)` | `createSavedSearch`, `updateSavedSearch`, `deleteSavedSearch` |
| `profile` | `apiKeys()`, `sessions()` | `createApiKey`, `deleteApiKey`, `updateProfile` |
| `twoFactor` | `twoFactorStatus()` | `enableTwoFactor`, `verifyTwoFactor`, `disableTwoFactor` |
| `notifications` | `notifications()` | `markNotificationRead(id)`, `markAllRead` |
| `analytics` | `analytics(...)` | `trackEvent(type, metadata)` |
| `admin` | `adminStats()`, `paymentSubmissions()`, `admin.users()` | `creditUser`, `adjustCredits`, `approvePayment`, `declinePayment` |
| `pages` | `page(id)`, `pages(type)` | — |
| `featureOverview` | `featureOverview()` | — |
| `activities` | `activities(limit, offset, type)` | — |

---

## Middleware and guard matrix

| Guard | Config key | Default | Effect |
| --- | --- | --- | --- |
| Body size limit | `GRAPHQL_MAX_BODY_BYTES` | 2MB | 413 if exceeded |
| Idempotency | `IDEMPOTENCY_REQUIRED_MUTATIONS` | billing mutations | 200 replay if same key |
| Mutation abuse guard | `ABUSE_GUARDED_MUTATIONS`, `MUTATION_ABUSE_GUARD_RPM` | 30 rpm | 429 if exceeded |
| Rate limit | `GRAPHQL_RATE_LIMIT_REQUESTS_PER_MINUTE` | 0 (disabled) | 429 if > limit (enable for prod) |
| Complexity | `GRAPHQL_COMPLEXITY_LIMIT` | 100 | 400 complexity error if exceeded |
| Timeout | `GRAPHQL_QUERY_TIMEOUT` | 30s | 504 / timeout error if exceeded |

---

## PostgreSQL tables owned by Appointment360

| Table | Era introduced | Key columns |
| --- | --- | --- |
| `users` | `0.x` | `uuid`, `email`, `password_hash`, `role`, `is_active`, `totp_secret` (8.x) |
| `token_blacklist` | `0.x` | `token_hash`, `expires_at` |
| `credits` | `1.x` | `user_uuid`, `feature`, `total`, `consumed`, `reset_at` |
| `plans` | `1.x` | `id`, `name`, `price`, `limits JSON` |
| `subscriptions` | `1.x` | `user_uuid`, `plan_id`, `status`, `billing_period_start`, `billing_period_end` |
| `payment_submissions` | `1.x` | `uuid`, `user_uuid`, `amount`, `proof_url`, `status`, `reviewed_by` |
| `activities` | `1.x` | `uuid`, `user_uuid`, `type`, `metadata JSON`, `created_at` |
| `ai_chats` | `5.x` | `uuid`, `user_uuid`, `title`, `created_at` |
| `ai_chat_messages` | `5.x` | `uuid`, `chat_uuid`, `role`, `content`, `created_at` |
| `resumes` | `5.x` | `uuid`, `user_uuid`, `content JSON`, `template_id`, `created_at` |
| `saved_searches` | `3.x` | `uuid`, `user_uuid`, `type`, `name`, `vql_json`, `created_at` |
| `api_keys` | `8.x` | `uuid`, `user_uuid`, `key_hash`, `name`, `last_used_at`, `created_at` |
| `sessions` | `8.x` | `uuid`, `user_uuid`, `ip`, `user_agent`, `created_at`, `last_seen_at` |
| `notifications` | `9.x` | `uuid`, `user_uuid`, `type`, `message`, `is_read`, `created_at` |
| `events` | `9.x` | `uuid`, `user_uuid`, `type`, `metadata JSON`, `created_at` |
| `feature_flags` | `9.x` | `feature`, `plan_id`, `enabled`, `credit_cost` |
| `workspaces` | `9.x` | `uuid`, `name`, `owner_uuid`, `plan_id` |

---

## Known gaps (as of initial 8.x audit)

| Gap | Severity | Action |
| --- | --- | --- |
| Inline debug file writes in `email/queries.py` and `jobs/mutations.py` | Critical | Remove before any public API promotion |
| `GRAPHQL_RATE_LIMIT_REQUESTS_PER_MINUTE=0` default | High | Set > 0 in all production environments |
| No `campaigns`/`sequences`/`templates` modules | Medium | 10.x implementation required |
| Idempotency + abuse guard in-memory state | Medium | Move to Redis for multi-replica deployments |
| SQL schema files missing locally (`sql/tables/`) | Medium | Restore or link to shared schema source |
| `DOCSAI_ENABLED=False` default, no health check | Low | Add health check for DocsAI dependency |
