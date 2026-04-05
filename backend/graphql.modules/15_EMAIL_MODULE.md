# Email Module

## Overview

The Email module provides email finder, verification, pattern management, optional **async satellite jobs**, and web discovery via the **Email API** Go service (`EC2/email.server`, also deployable as Lambda). It includes **finder/verifier/pattern queries**, **pattern + async job mutations**, `emailJobStatus` and `webSearch` queries. **S3 CSV export jobs** are invoked only via the [Jobs Module](16_JOBS_MODULE.md) (`jobs.createEmailFinderExport` / `jobs.createEmailVerifyExport`); they are not duplicated under `email` queries.
**Location:** `app/graphql/modules/email/`

**Email API base URL:** gateway env **`LAMBDA_EMAIL_API_URL`**; auth **`LAMBDA_EMAIL_API_KEY`** as **`X-API-Key`** (`app/core/config.py`). **REST reference (all paths, bodies, responses):** **[emailapis.api.md](../micro.services.apis/emailapis.api.md)** · Postman: **[EC2_email.server.postman_collection.json](../postman/EC2_email.server.postman_collection.json)**.

## API Endpoints Mapping

| GraphQL Field | Backend (EC2/email.server) | Description |
|---------------|---------|-------------|
| `findEmails` | `POST /email/finder/` (query: `first_name`, `last_name`, `domain`) | Find emails for one contact |
| `findEmailsBulk` | `POST /email/finder/bulk` | Bulk find (1–50 contacts) |
| `verifySingleEmail` | `POST /email/single/verifier/` | Verify one email |
| `verifyEmailsBulk` | `POST /email/bulk/verifier/` | Verify 1–10,000 emails |
| `emailJobStatus` | `GET /jobs/:id/status` | Async email satellite job progress |
| `webSearch` | `POST /web/web-search` | Full-name + domain discovery JSON |
| `addEmailPattern` | `POST /email-patterns/add` | Add one email pattern for a company (mutation) |
| `addEmailPatternBulk` | `POST /email-patterns/add/bulk` | Add multiple email patterns (mutation) |
| `createEmailFinderBulkJob` | `POST /email/finder/bulk/job` | Enqueue async finder rows (`202` + `job_id`) |
| `createEmailVerifyBulkJob` | `POST /email/bulk/verifier/job` | Enqueue async verify rows (`202` + `job_id`) |
| `createEmailFinderExport` | [Jobs](16_JOBS_MODULE.md) → `POST /email/finder/s3` | Finder S3 CSV stream job (`scheduler_jobs`) |
| `createEmailVerifyExport` | [Jobs](16_JOBS_MODULE.md) → `POST /email/verify/s3` | Verifier S3 CSV stream job (`scheduler_jobs`) |
| *(removed)* `createEmailPatternImportJob` | — | Removed in favor of supported patterns under `jobs` / email APIs; see [16_JOBS_MODULE.md](16_JOBS_MODULE.md) |

> **Note:** Finder and verification are **queries** under `email`; pattern add and async bulk jobs are **mutations** under `mutation.email`. S3 CSV exports use **`jobs`** mutations only.

## Verifier provider matrix (gateway + satellite)

| Provider | Single / bulk verify (GraphQL + REST) | Notes |
| --- | --- | --- |
| `truelist` | ✅ | Default |
| `icypeas` | ✅ | |
| `mailtester` | ✅ | Bulk async + S3 CSV task `email:s3csv:verify:mailtester` |
| `mailvetter` | ✅ | Bulk async + S3 CSV task `email:s3csv:verify:mailvetter` |

## Endpoint metadata references (`docs/backend/endpoints`)

Use these JSON metadata files as the canonical endpoint inventory for frontend binding, auth/rbac, and era tagging:

- `query_find_emails_graphql.json`
- `mutation_verify_single_email_graphql.json`
- `mutation_verify_bulk_emails_graphql.json`
- `mutation_add_email_pattern_graphql.json`
- `mutation_add_email_pattern_bulk_graphql.json`
- `mutation_find_single_email_graphql.json` (legacy compatibility surface)
- `mutation_export_emails_graphql.json` (jobs/export oriented flow)

These metadata files must stay aligned with:

- GraphQL resolvers in `contact360.io/api/app/graphql/modules/email/`
- frontend service bindings in `contact360.io/app/src/services/graphql/emailService.ts`
- runtime routes in **`EC2/email.server/internal/api/router.go`** (canonical Go implementation; see [emailapis.api.md](../micro.services.apis/emailapis.api.md))

## Queries and mutations – parameters and variable types

All fields live under `email { ... }` on `Query` / `Mutation`.

| Operation | Parameter(s) | Variable type (GraphQL) | Return type |
|-----------|---------------|-------------------------|-------------|
| **Queries** | | | |
| `findEmails` | `input` | `EmailFinderInput!` | `EmailFinderResponse` |
| `findEmailsBulk` | `input` | `BulkEmailFinderInput!` | `BulkEmailFinderResponse` |
| `verifySingleEmail` | `input` | `SingleEmailVerifierInput!` | `SingleEmailVerifierResponse!` |
| `verifyEmailsBulk` | `input` | `BulkEmailVerifierInput!` | bulk verify result type |
| `emailJobStatus` | `jobId` | `String!` | `EmailJobStatusResponse` (async bulk / S3 job progress) |
| `webSearch` | `input` | `WebSearchInput!` | `JSON` (upstream discovery payload) |
| ~~`createEmailFinderExportJob`~~ | — | — | **Removed** — use `jobs.createEmailFinderExport` |
| ~~`createEmailVerifyExportJob`~~ | — | — | **Removed** — use `jobs.createEmailVerifyExport` |
| ~~`createEmailPatternImportJob`~~ | — | — | **Removed** from schema |
| `exportEmails` | — | — | `ComingSoonResponse` (stub) |
| `verifyexportEmail` | — | — | `ComingSoonResponse` (stub) |
| **Mutations** | | | |
| `addEmailPattern` | `input` | `EmailPatternAddInput!` | `EmailPatternResult!` |
| `addEmailPatternBulk` | `input` | `EmailPatternBulkAddInput!` | `EmailPatternBulkAddResponse!` |
| `createEmailFinderBulkJob` | `input` | `BulkEmailFinderJobInput!` | `EmailJobQueuedResponse` |
| `createEmailVerifyBulkJob` | `input` | `BulkEmailVerifyJobInput!` | `EmailJobQueuedResponse` |

Use camelCase in variables. Credit deduction (1 per find/verify for typical paid tiers); SuperAdmin/Admin often unlimited—see resolver. Input types: see Input Types section and [16_JOBS_MODULE.md](16_JOBS_MODULE.md) for export/import job inputs.

## Canonical SDL (gateway schema)

Regenerate the full schema from `contact360.io/api` with:

`python -c "from app.graphql.schema import schema; print(schema.as_str())"`

```graphql
type EmailQuery {
  findEmails(input: EmailFinderInput!): EmailFinderResponse!
  findEmailsBulk(input: BulkEmailFinderInput!): BulkEmailFinderResponse!
  verifySingleEmail(input: SingleEmailVerifierInput!): SingleEmailVerifierResponse!
  verifyEmailsBulk(input: BulkEmailVerifierInput!): BulkEmailVerifierResponse!
  emailJobStatus(jobId: String!): EmailJobStatusResponse!
  webSearch(input: WebSearchInput!): JSON!
  exportEmails: ComingSoonResponse!
  verifyexportEmail: ComingSoonResponse!
}

type EmailMutation {
  addEmailPattern(input: EmailPatternAddInput!): EmailPatternResult!
  addEmailPatternBulk(input: EmailPatternBulkAddInput!): EmailPatternBulkAddResponse!
  createEmailFinderBulkJob(input: BulkEmailFinderJobInput!): EmailJobQueuedResponse!
  createEmailVerifyBulkJob(input: BulkEmailVerifyJobInput!): EmailJobQueuedResponse!
}
```

`EmailFinderInput`, `BulkEmailFinderInput`, `SingleEmailVerifierInput`, `EmailPatternAddInput`, etc., are defined in the generated SDL.

## POST `/graphql` — full request and response

Headers: `Content-Type: application/json`, `Authorization: Bearer <access_token>`.

### `email.findEmails` (query)

```json
{
  "query": "query ($input: EmailFinderInput!) { email { findEmails(input: $input) { success total emails { email status } } } }",
  "variables": {
    "input": {
      "firstName": "Jane",
      "lastName": "Doe",
      "domain": "example.com",
      "website": null
    }
  }
}
```

## Types

### EmailResult

Single email result from finder operations.

```graphql
type EmailResult {
  uuid: ID!
  email: String!
  status: String
  source: String
}
```

**Fields:**

- `uuid`: Contact UUID from the database
- `email`: Email address found
- `status`: Optional status (e.g., from verification)
- `source`: Source of the email (e.g., "connectra", "pattern", "generator")

### EmailFinderResponse

Response from `findEmails` query.

```graphql
type EmailFinderResponse {
  emails: [EmailResult!]!
  total: Int!
  success: Boolean!
}
```

### BulkEmailFinderResult

Single result item in bulk email finder response.

```graphql
type BulkEmailFinderResult {
  firstName: String!
  lastName: String!
  domain: String!
  emails: [EmailResult!]!
  source: String!
  total: Int!
  success: Boolean!
  error: String
}
```

### BulkEmailFinderResponse

Response from `findEmailsBulk` query.

```graphql
type BulkEmailFinderResponse {
  processedCount: Int!
  totalRequested: Int!
  totalSuccessful: Int!
  results: [BulkEmailFinderResult!]!
}
```

### VerifiedEmailResult

Result of email verification.

```graphql
type VerifiedEmailResult {
  email: String!
  status: String!
  emailState: String
  emailSubState: String
  certainty: String
}
```

**Status values:** `valid`, `invalid`, `catchall`, `unknown`

### SingleEmailVerifierResponse

Response from `verifySingleEmail` query.

```graphql
type SingleEmailVerifierResponse {
  result: VerifiedEmailResult!
  success: Boolean!
}
```

### BulkEmailVerifierResponse

Response from `verifyEmailsBulk` query.

```graphql
type BulkEmailVerifierResponse {
  results: [VerifiedEmailResult!]!
  total: Int!
  validCount: Int!
  invalidCount: Int!
  catchallCount: Int!
  unknownCount: Int!
  success: Boolean!
}
```

### EmailPatternResult

Single email pattern result (from `addEmailPattern` or item in `addEmailPatternBulk`).

```graphql
type EmailPatternResult {
  uuid: String!
  companyUuid: String!
  patternFormat: String
  patternString: String
  isAutoExtracted: Boolean
  domain: String!
  contactCount: Int
  createdAt: String
  updatedAt: String
}
```

### EmailPatternBulkAddResponse

Response from `addEmailPatternBulk` mutation.

```graphql
type EmailPatternBulkAddResponse {
  results: [EmailPatternResult!]!
  success: Boolean!
}
```

---

## Input Types

### EmailFinderInput

Input for `findEmails` query (single contact).

```graphql
input EmailFinderInput {
  firstName: String!
  lastName: String!
  domain: String
  website: String
}
```

**Validation:**

- `firstName`: Required, non-empty, max 100 characters
- `lastName`: Required, non-empty, max 100 characters
- `domain`: Optional, max 255 characters
- `website`: Optional, max 500 characters
- Either `domain` or `website` must be provided

### BulkEmailFinderItemInput

Single item for bulk email finder.

```graphql
input BulkEmailFinderItemInput {
  firstName: String!
  lastName: String!
  domain: String!
}
```

### BulkEmailFinderInput

Input for `findEmailsBulk` query (multiple contacts).

```graphql
input BulkEmailFinderInput {
  items: [BulkEmailFinderItemInput!]!
}
```

**Validation:**

- `items`: Required, 1-50 items
- Each item must have valid `firstName`, `lastName`, and `domain`

### SingleEmailVerifierInput

Input for `verifySingleEmail` query.

```graphql
input SingleEmailVerifierInput {
  email: String!
  provider: String
}
```

**Validation:**

- `email`: Required, must be valid email format
- `provider`: Optional. Supported values are runtime-dependent and include `truelist`, `mailvetter`, and `icypeas` (default remains `truelist` in current GraphQL examples).

### BulkEmailVerifierInput

Input for `verifyEmailsBulk` query.

```graphql
input BulkEmailVerifierInput {
  emails: [String!]!
  provider: String
}
```

**Validation:**

- `emails`: Required, 1-10,000 emails
- All emails must be valid email format
- `provider`: Optional. Supported values are runtime-dependent and include `truelist`, `mailvetter`, and `icypeas` (default remains `truelist` in current GraphQL examples).

### EmailPatternAddInput

Input for `addEmailPattern` mutation (POST /email-patterns/add).

```graphql
input EmailPatternAddInput {
  companyUuid: String!
  email: String!
  firstName: String!
  lastName: String!
  domain: String!
}
```

**Validation:** All fields required, non-empty; `email` must be valid email format.

### EmailPatternBulkItemInput

Single item for `addEmailPatternBulk` mutation.

```graphql
input EmailPatternBulkItemInput {
  companyUuid: String!
  email: String!
  firstName: String!
  lastName: String!
  domain: String!
}
```

### EmailPatternBulkAddInput

Input for `addEmailPatternBulk` mutation (POST /email-patterns/add/bulk).

```graphql
input EmailPatternBulkAddInput {
  items: [EmailPatternBulkItemInput!]!
}
```

**Validation:** `items` required, non-empty list; each item validated as above.

---

## Queries

### findEmails

Find emails by first name, last name, and company domain/website.

**Parameters:**

| Name  | Type               | Required | Description                    |
|-------|--------------------|----------|--------------------------------|
| input | EmailFinderInput!  | Yes      | firstName, lastName, domain/website |

**Endpoint:** POST /email/finder/

```graphql
query FindEmails($input: EmailFinderInput!) {
  email {
    findEmails(input: $input) {
      emails {
        uuid
        email
        status
        source
      }
      total
      success
    }
  }
}
```

**Variables:**

```json
{
  "input": {
    "firstName": "John",
    "lastName": "Doe",
    "domain": "example.com"
  }
}
```

**Authentication:** Required

**Credits:** 1 credit per search (FreeUser/ProUser only)

**Example Response:**

```json
{
  "data": {
    "email": {
      "findEmails": {
        "emails": [
          {
            "uuid": "123e4567-e89b-12d3-a456-426614174000",
            "email": "john.doe@example.com",
            "status": null,
            "source": "connectra"
          }
        ],
        "total": 1,
        "success": true
      }
    }
  }
}
```

---

### findEmailsBulk

Find emails for multiple contacts in parallel.

**Parameters:**

| Name  | Type                    | Required | Description        |
|-------|-------------------------|----------|--------------------|
| input | BulkEmailFinderInput!   | Yes      | List of contacts (max 50) |

**Endpoint:** POST /email/finder/bulk

**Maximum:** 50 contacts per request

```graphql
query FindEmailsBulk($input: BulkEmailFinderInput!) {
  email {
    findEmailsBulk(input: $input) {
      processedCount
      totalRequested
      totalSuccessful
      results {
        firstName
        lastName
        domain
        emails {
          uuid
          email
          source
        }
        source
        total
        success
        error
      }
    }
  }
}
```

**Variables:**

```json
{
  "input": {
    "items": [
      {
        "firstName": "John",
        "lastName": "Doe",
        "domain": "example.com"
      },
      {
        "firstName": "Jane",
        "lastName": "Smith",
        "domain": "example.com"
      }
    ]
  }
}
```

**Authentication:** Required

**Credits:** 1 credit per contact (FreeUser/ProUser only)

**Example Response:**

```json
{
  "data": {
    "email": {
      "findEmailsBulk": {
        "processedCount": 2,
        "totalRequested": 2,
        "totalSuccessful": 2,
        "results": [
          {
            "firstName": "John",
            "lastName": "Doe",
            "domain": "example.com",
            "emails": [
              {
                "uuid": "123e4567-e89b-12d3-a456-426614174000",
                "email": "john.doe@example.com",
                "source": "connectra"
              }
            ],
            "source": "connectra",
            "total": 1,
            "success": true,
            "error": null
          },
          {
            "firstName": "Jane",
            "lastName": "Smith",
            "domain": "example.com",
            "emails": [],
            "source": "unknown",
            "total": 0,
            "success": false,
            "error": "No emails found"
          }
        ]
      }
    }
  }
}
```

---

### verifySingleEmail

Verify a single email address.

**Parameters:**

| Name  | Type                      | Required | Description     |
|-------|---------------------------|----------|-----------------|
| input | SingleEmailVerifierInput! | Yes      | email, provider |

**Endpoint:** POST /email/single/verifier/

```graphql
query VerifySingleEmail($input: SingleEmailVerifierInput!) {
  email {
    verifySingleEmail(input: $input) {
      result {
        email
        status
        emailState
        emailSubState
        certainty
      }
      success
    }
  }
}
```

**Variables:**

```json
{
  "input": {
    "email": "john.doe@example.com",
    "provider": "truelist"
  }
}
```

**Authentication:** Required

**Example Response:**

```json
{
  "data": {
    "email": {
      "verifySingleEmail": {
        "result": {
          "email": "john.doe@example.com",
          "status": "valid",
          "emailState": "deliverable",
          "emailSubState": null,
          "certainty": null
        },
        "success": true
      }
    }
  }
}
```

---

### verifyEmailsBulk

Verify multiple email addresses in bulk.

**Parameters:**

| Name  | Type                    | Required | Description      |
|-------|-------------------------|----------|------------------|
| input | BulkEmailVerifierInput! | Yes      | Emails (max 10,000) |

**Endpoint:** POST /email/bulk/verifier/

**Maximum:** 10,000 emails per request

```graphql
query VerifyEmailsBulk($input: BulkEmailVerifierInput!) {
  email {
    verifyEmailsBulk(input: $input) {
      results {
        email
        status
        emailState
        emailSubState
        certainty
      }
      total
      validCount
      invalidCount
      catchallCount
      unknownCount
      success
    }
  }
}
```

**Variables:**

```json
{
  "input": {
    "emails": [
      "john.doe@example.com",
      "jane.smith@example.com",
      "invalid@example.com"
    ],
    "provider": "truelist"
  }
}
```

**Authentication:** Required

**Example Response:**

```json
{
  "data": {
    "email": {
      "verifyEmailsBulk": {
        "results": [
          {
            "email": "john.doe@example.com",
            "status": "valid",
            "emailState": "deliverable",
            "emailSubState": null,
            "certainty": null
          },
          {
            "email": "jane.smith@example.com",
            "status": "valid",
            "emailState": "deliverable",
            "emailSubState": null,
            "certainty": null
          },
          {
            "email": "invalid@example.com",
            "status": "invalid",
            "emailState": "undeliverable",
            "emailSubState": null,
            "certainty": null
          }
        ],
        "total": 3,
        "validCount": 2,
        "invalidCount": 1,
        "catchallCount": 0,
        "unknownCount": 0,
        "success": true
      }
    }
  }
}
```

---

## Email Export and Verify-Export (Jobs Module)

The **email finder export** (CSV → find emails → CSV) and **email verify export** (CSV → verify emails → CSV) operations are long-running jobs handled by the **email.server** satellite (orchestrated via the gateway). Use the [Jobs Module](16_JOBS_MODULE.md) instead of the Email module for `scheduler_jobs` rows:

| Operation | GraphQL Mutation | Description |
|-----------|-----------------|-------------|
| Email finder export | `jobs.createEmailFinderExport(input)` | Create job: S3 CSV → stream → find emails → write CSV → S3 |
| Email verify export | `jobs.createEmailVerifyExport(input)` | Create job: S3 CSV → stream → verify emails → write CSV (with status column) → S3 |

After creating a job, use `jobs.job(jobId)` to poll status (`statusPayload` resolves against the email satellite when `sourceService=email_server`). The Jobs module stores a local record in `scheduler_jobs` for ownership and listing.

**Input CSV location:** For email finder export / verify-export, the client first uploads the CSV to S3 via the **Upload module** (multipart upload). The Upload module returns an S3 `file_key` (S3 object key), which must be passed as `input_csv_key` to `jobs.createEmailFinderExport(input)` (or `jobs.createEmailVerifyExport(input)`).

---

## Error Handling

### Error Types

The Email module may raise the following errors:

| Error | Code | Status | Description |
|-------|------|--------|-------------|
| ValidationError | `VALIDATION_ERROR` | 422 | Input validation failed |
| BadRequestError | `BAD_REQUEST` | 400 | Invalid request data |
| ServiceUnavailableError | `SERVICE_UNAVAILABLE` | 503 | Lambda Email API unavailable |

### Error Response Examples

**Validation Error:**

```json
{
  "errors": [
    {
      "message": "Either domain or website must be provided",
      "extensions": {
        "code": "VALIDATION_ERROR",
        "statusCode": 422
      }
    }
  ]
}
```

**Service Unavailable:**

```json
{
  "errors": [
    {
      "message": "Email service error: Connection timeout",
      "extensions": {
        "code": "SERVICE_UNAVAILABLE",
        "statusCode": 503,
        "serviceName": "LambdaEmail"
      }
    }
  ]
}
```

**Invalid Provider:**

```json
{
  "errors": [
    {
      "message": "Invalid provider. Must be one of the currently enabled providers (for example: 'truelist', 'mailvetter', 'icypeas')",
      "extensions": {
        "code": "VALIDATION_ERROR",
        "statusCode": 422
      }
    }
  ]
}
```

---

## Usage Examples

### Complete Email Operations Flow

```graphql
# 1. Find emails for a single contact
query FindSingleContact {
  email {
    findEmails(input: {
      firstName: "John"
      lastName: "Doe"
      domain: "example.com"
    }) {
      emails {
        uuid
        email
        source
      }
      total
      success
    }
  }
}

# 2. Find emails for multiple contacts
query FindMultipleContacts {
  email {
    findEmailsBulk(input: {
      items: [
        { firstName: "John", lastName: "Doe", domain: "example.com" }
        { firstName: "Jane", lastName: "Smith", domain: "example.com" }
      ]
    }) {
      processedCount
      totalSuccessful
      results {
        firstName
        lastName
        emails {
          email
        }
        success
        error
      }
    }
  }
}

# 3. Verify a single email
query VerifySingle {
  email {
    verifySingleEmail(input: {
      email: "john.doe@example.com"
      provider: "truelist"
    }) {
      result {
        email
        status
        emailState
      }
      success
    }
  }
}

# 4. Verify multiple emails in bulk
query VerifyBulk {
  email {
    verifyEmailsBulk(input: {
      emails: [
        "john.doe@example.com"
        "jane.smith@example.com"
        "test@invalid.com"
      ]
      provider: "truelist"
    }) {
      results {
        email
        status
      }
      validCount
      invalidCount
      success
    }
  }
}
```

### Using Different Providers

```graphql
# Using Truelist provider (default)
query VerifyWithTruelist {
  email {
    verifySingleEmail(input: {
      email: "john.doe@example.com"
      provider: "truelist"
    }) {
      result {
        email
        status
      }
      success
    }
  }
}

# Using IcyPeas provider
query VerifyWithIcypeas {
  email {
    verifySingleEmail(input: {
      email: "john.doe@example.com"
      provider: "icypeas"
    }) {
      result {
        email
        status
        certainty
      }
      success
    }
  }
}
```

### Domain vs Website

```graphql
# Using domain
query FindByDomain {
  email {
    findEmails(input: {
      firstName: "John"
      lastName: "Doe"
      domain: "example.com"
    }) {
      emails { email }
      success
    }
  }
}

# Using website (domain is extracted automatically)
query FindByWebsite {
  email {
    findEmails(input: {
      firstName: "John"
      lastName: "Doe"
      website: "https://www.example.com/about"
    }) {
      emails { email }
      success
    }
  }
}
```

---

## Mutations

### addEmailPattern

Add a new email pattern for a company (one contact's email used to infer pattern).

**Parameters:**

| Name  | Type                  | Required | Description                    |
|-------|-----------------------|----------|--------------------------------|
| input | EmailPatternAddInput! | Yes      | companyUuid, email, firstName, lastName, domain |

**Endpoint:** POST /email-patterns/add

**Authentication:** Required

```graphql
mutation AddEmailPattern($input: EmailPatternAddInput!) {
  email {
    addEmailPattern(input: $input) {
      uuid
      companyUuid
      patternFormat
      patternString
      domain
      contactCount
      createdAt
    }
  }
}
```

Variables (camelCase):

```json
{
  "input": {
    "companyUuid": "company-uuid-here",
    "email": "john.doe@example.com",
    "firstName": "John",
    "lastName": "Doe",
    "domain": "example.com"
  }
}
```

### addEmailPatternBulk

Add multiple email patterns in one request.

**Parameters:**

| Name  | Type                        | Required | Description        |
|-------|-----------------------------|----------|--------------------|
| input | EmailPatternBulkAddInput!   | Yes      | items (list of pattern inputs) |

**Endpoint:** POST /email-patterns/add/bulk

**Authentication:** Required

```graphql
mutation AddEmailPatternBulk($input: EmailPatternBulkAddInput!) {
  email {
    addEmailPatternBulk(input: $input) {
      results {
        uuid
        companyUuid
        domain
        createdAt
      }
      success
    }
  }
}
```

Variables (camelCase):

```json
{
  "input": {
    "items": [
      {
        "companyUuid": "company-uuid-1",
        "email": "john.doe@example.com",
        "firstName": "John",
        "lastName": "Doe",
        "domain": "example.com"
      }
    ]
  }
}
```

---

## Implementation Details

### LambdaEmailClient

All email operations use `LambdaEmailClient` (`app/clients/lambda_email_client.py`) with the following methods:

| Method | Endpoint | Description |
|--------|----------|-------------|
| `find_emails()` | POST /email/finder/ | Find emails for single contact |
| `find_emails_bulk()` | POST /email/finder/bulk | Find emails for multiple contacts |
| `verify_single_email()` | POST /email/single/verifier/ | Verify single email |
| `verify_emails_bulk()` | POST /email/bulk/verifier/ | Verify multiple emails |
| `add_email_pattern()` | POST /email-patterns/add | Add one email pattern for a company |
| `add_email_pattern_bulk()` | POST /email-patterns/add/bulk | Add multiple email patterns |

**Configuration:**

- `LAMBDA_EMAIL_API_URL`: Base URL for Lambda Email API
- `LAMBDA_EMAIL_API_KEY`: API key for authentication
- `LAMBDA_EMAIL_API_TIMEOUT`: Request timeout (default: 60s)

### Credit Management

| Operation | Credits | Notes |
|-----------|---------|-------|
| `findEmails` | 1 | Per search |
| `findEmailsBulk` | 1 per contact | Based on number of contacts |
| `verifySingleEmail` | 0 | Verification is free |
| `verifyEmailsBulk` | 0 | Verification is free |

- Credits are deducted **after** successful operation (non-blocking)
- SuperAdmin/Admin have unlimited credits
- Credit deduction failures are logged but don't fail the operation

### Activity Logging

All operations log activity with:

- User UUID
- Service type: `EMAIL`
- Action type: `SEARCH` or `VERIFY`
- Status: `SUCCESS` or `FAILED`
- Metadata: email count, verification results, etc.

Activity logging is non-blocking - failures don't affect the operation.

### Validation

**Input Validation:**

- `firstName`/`lastName`: Required, non-empty, max 100 characters
- `domain`: Optional, max 255 characters
- `website`: Optional, max 500 characters
- `email`: Must be valid email format
- `provider`: Must be one of the currently enabled providers (`truelist`, `mailvetter`, `icypeas` depending on runtime policy and rollout stage)

**Limits:**

- Bulk finder: Max 50 contacts
- Bulk verifier: Max 10,000 emails

### Providers

| Provider | Description |
|----------|-------------|
| `truelist` | Default provider in many GraphQL examples and Python-runtime aligned flows |
| `mailvetter` | Primary verifier in Go runtime health/verification pathways; use for migration-aligned verification flows |
| `icypeas` | Alternative provider with certainty-oriented responses |

---

## Task breakdown (for maintainers)

1. **findEmails/findEmailsBulk:** EmailFinderInput (e.g. contact uuid, first/last/domain); Lambda Email API POST /email/finder/ and /email/finder/bulk; map response to EmailFinderResponse/BulkEmailFinderResponse; credit deduction and usage tracking (EMAIL_FINDER, BULK_EXPORT).
2. **verifySingleEmail/verifyEmailsBulk:** SingleEmailVerifierInput / BulkEmailVerifierInput; Lambda /email/single/verifier/ and /email/bulk/verifier/ (1–10,000 emails); credit and usage (VERIFIER, BULK_VERIFICATION).
3. **addEmailPattern/addEmailPatternBulk:** Mutations; Lambda /email-patterns/add and /add/bulk; validate company and pattern payload; no job creation.
4. **S3 export jobs:** Use `jobs.createEmailFinderExport` / `jobs.createEmailVerifyExport` only; confirm `scheduler_jobs` row and activity log (JOBS/EXPORT, BULK_VERIFICATION).
5. **Error mapping:** Lambda errors via handle_external_error; validate response shape; document field-level validation (email format, bulk limits).

---

## Related Modules

- **LambdaEmailClient**: `app/clients/lambda_email_client.py`
- **Billing Module**: Credits are managed through billing
- **Usage Module**: Email operations track feature usage
- **AI Chats Module** ([17_AI_CHATS_MODULE.md](17_AI_CHATS_MODULE.md)): `analyzeEmailRisk` (Contact AI) complements verification workflows

---

## Migration Notes

### Breaking Changes (v2.0)

The Email module has been simplified to use only 4 queries:

**Removed Operations:**

- `findSingleEmail` mutation
- `verifySingle` mutation
- `verifyBulk` mutation
- `generateAndVerify` mutation
- `verifyAndFind` mutation
- `exportEmails` mutation

**New Operations:**

- `findEmails` query (single contact)
- `findEmailsBulk` query (multiple contacts)
- `verifySingleEmail` query (single email)
- `verifyEmailsBulk` query (multiple emails)

**Provider Changes:**

- Migration history includes shifts from legacy `bulkmailverifier` naming to `truelist`/`icypeas`, with current dual-runtime documentation also tracking `mailvetter` in Go pathways.

**Limit Changes:**

- Bulk verifier increased from 1,000 to 10,000 emails

## Documentation metadata

- Era: `2.x`
- Introduced in: `TBD` (fill with exact minor)
- Frontend bindings: list page files from `docs/frontend/pages/*.json`
- Data stores touched: PostgreSQL/Elasticsearch/MongoDB/S3 as applicable

## Endpoint/version binding checklist

- Add operation list with `introduced_in` / `deprecated_in` tags.
- Map each operation to frontend page bindings and hook/service usage.
- Record DB tables read/write for each operation.

## Era ownership

- Primary era: `2.x` (Contact360 email system)
- Cross-era impact: `1.x` (credits), `3.x` (contact/company enrichment), `6.x` (reliability), `8.x` (API contracts), `10.x` (campaign)

## Dual runtime endpoint mapping (Python + Go)

| Endpoint | Python runtime | Go runtime | Notes |
| --- | --- | --- | --- |
| `POST /email/finder/` | `lambda/emailapis` | `lambda/emailapigo` | core single finder |
| `POST /email/finder/bulk` | `lambda/emailapis` | `lambda/emailapigo` | bulk finder |
| `POST /email/single/verifier/` | `lambda/emailapis` | `lambda/emailapigo` | single verification |
| `POST /email/bulk/verifier/` | `lambda/emailapis` | `lambda/emailapigo` | bulk verification |
| `POST /email-patterns/add` | `lambda/emailapis` | `lambda/emailapigo` | pattern add |
| `POST /email-patterns/add/bulk` | `lambda/emailapis` | `lambda/emailapigo` | pattern add bulk |
| `POST /web/web-search` | `lambda/emailapis` | `lambda/emailapigo` | web fallback search |

## Provider drift note

Go runtime health and verification pathways prioritize `mailvetter` while some Python/default contracts and historical docs reference `truelist`. Treat this as an explicit migration surface and keep provider naming consistent across app, GraphQL, and runtime docs.

## Cross-era task breakdown (maintainers)

- `1.x`: verify credit-impact docs and error behavior for finder/verify actions.
- `2.x`: freeze endpoint payload/status contract and bulk semantics.
- `3.x`: validate contact/company enrichment linkage and domain identity mapping.
- `6.x`: verify retry, timeout, and failover policies with observability evidence.
- `8.x`: ensure public/private API documentation and compatibility notes are current.
- `10.x`: verify campaign deliverability/compliance linkage to email verification outputs.

## 2026 addendum

- Canonical Mailvetter path for new consumers is `/v1/*`; legacy routes are compatibility-only.
- Lifecycle vocabulary is frozen to `pending`, `processing`, `completed`, `failed` for job-level states.
