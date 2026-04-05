# Usage Module

## Overview

The Usage module provides feature usage tracking functionality. It allows users to track their usage of various features, view current usage limits, and reset usage counters (for testing/admin purposes).
**Location:** `app/graphql/modules/usage/`

**Jobs in `featureOverview`:** The nested query returns **`SchedulerJob`** rows from the gateway database (same family as [16_JOBS_MODULE.md](16_JOBS_MODULE.md)). Long-running work may also touch **email.server** or **Connectra** (`EC2/sync.server`); the REST job API there is documented in **[connectra.api.md](../micro.services.apis/connectra.api.md)**.

## Queries and mutations – parameters and variable types

| Operation | Parameter(s) | Variable type (GraphQL) | Return type |
|-----------|---------------|-------------------------|-------------|
| **Queries** (under `usage { ... }`) | | | |
| `usage` | `feature` | `String` (optional; filters to one feature) | `UsageResponse!` |
| **Queries** (root field `featureOverview`) | | | |
| `featureOverview` | `feature` | `String!` (nested: `featureOverview { featureOverview(feature: ...) }`) | `FeatureOverview!` |

| **Mutations** (under `usage { ... }`) | | | |
| `trackUsage` | `input` | `TrackUsageInput!` | `TrackUsageResponse!` |
| `resetUsage` | `input` | `ResetUsageInput!` | `ResetUsageResponse!` |

Use camelCase in variables. `TrackUsageInput`: `feature: String!`, `amount: Int! = 1`. `ResetUsageInput`: `feature: String!`. Supported feature names: AI_CHAT, BULK_EXPORT, API_KEYS, EMAIL_FINDER, VERIFIER, LINKEDIN, BULK_VERIFICATION, etc. (see Supported Features below).

## Canonical SDL (gateway schema)

Regenerate the full schema from `contact360.io/api` with:

`python -c "from app.graphql.schema import schema; print(schema.as_str())"`

```graphql
type UsageQuery {
  usage(feature: String = null): UsageResponse!
}

type UsageMutation {
  trackUsage(input: TrackUsageInput!): TrackUsageResponse!
  resetUsage(input: ResetUsageInput!): ResetUsageResponse!
}

type FeatureOverviewQuery {
  featureOverview(feature: String!): FeatureOverview!
}

type FeatureOverview {
  feature: String!
  usage: FeatureUsageInfo
  activities: [Activity!]!
  jobs: [SchedulerJob!]!
}

input TrackUsageInput {
  feature: String!
  amount: Int! = 1
}

input ResetUsageInput {
  feature: String!
}
```

## POST `/graphql` — full request and response

Headers: `Content-Type: application/json`, `Authorization: Bearer <access_token>`.

### `usage.usage` (query)

```json
{
  "query": "query ($feature: String) { usage { usage(feature: $feature) { features { feature used limit remaining } } } }",
  "variables": { "feature": null }
}
```

### `featureOverview.featureOverview` (query)

```json
{
  "query": "query ($feature: String!) { featureOverview { featureOverview(feature: $feature) { feature usage { used limit } } } }",
  "variables": { "feature": "EMAIL_FINDER" }
}
```

### `usage.trackUsage` (mutation)

```json
{
  "query": "mutation ($input: TrackUsageInput!) { usage { trackUsage(input: $input) { feature used limit success } } }",
  "variables": { "input": { "feature": "EMAIL_FINDER", "amount": 1 } }
}
```

## Types

### FeatureUsageInfo

Feature usage information.

```graphql
type FeatureUsageInfo {
  feature: String!
  used: Int!
  limit: Int!
  remaining: Int!
  resetAt: String
}
```

**Fields:**

- `feature` (String!): Feature name
- `used` (Int!): Current usage count
- `limit` (Int!): Usage limit (999999 means unlimited)
- `remaining` (Int!): Remaining usage (limit - used, or -1 if unlimited)
- `resetAt` (String): ISO format datetime when usage period resets (null if no reset scheduled)

### UsageResponse

Response containing usage for all features.

```graphql
type UsageResponse {
  features: [FeatureUsageInfo!]!
}
```

### TrackUsageResponse

Response from tracking usage.

```graphql
type TrackUsageResponse {
  feature: String!
  used: Int!
  limit: Int!
  success: Boolean!
}
```

### ResetUsageResponse

Response from resetting usage.

```graphql
type ResetUsageResponse {
  feature: String!
  used: Int!
  limit: Int!
  success: Boolean!
}
```

## Supported Features

The following features can be tracked:

- `AI_CHAT` - AI chat conversations (see [AI Chats Module](17_AI_CHATS_MODULE.md) / Contact AI service)
- `BULK_EXPORT` - Bulk export operations
- `API_KEYS` - API key usage
- `TEAM_MANAGEMENT` - Team management operations
- `EMAIL_FINDER` - Email finder queries
- `VERIFIER` - Email verification
- `LINKEDIN` - LinkedIn operations
- `DATA_SEARCH` - Data search queries
- `ADVANCED_FILTERS` - Advanced filter usage
- `AI_SUMMARIES` - AI summary generation
- `SAVE_SEARCHES` - Saved search operations
- `BULK_VERIFICATION` - Bulk email verification

## Queries

### usage

Get current feature usage for all features or a specific feature.

**Parameters:**

| Name   | Type   | Required | Description                                                                 |
|--------|--------|----------|-----------------------------------------------------------------------------|
| feature| String | No       | Filter by specific feature name (case-insensitive, e.g. "EMAIL_FINDER")    |

```graphql
query GetUsage($feature: String) {
  usage {
    usage(feature: $feature) {
      features {
        feature
        used
        limit
        remaining
        resetAt
      }
    }
  }
}
```

**Arguments:**

- `feature` (String, optional): Filter by specific feature name (case-insensitive, e.g., "EMAIL_FINDER" or "email_finder")

**Returns:** `UsageResponse`

**Authentication:** Required

**Implementation Details:**

- Usage records are auto-created on first track if they don't exist
- Feature names are normalized to uppercase for matching
- Unlimited limits are represented as 999999 (remaining is -1)
- Period-based resets: Usage resets monthly (at the start of each month)
- Role-based limits: Limits are determined by user role (FREE_USER vs PRO_USER)
  - SuperAdmin/Admin get PRO_USER level access (unlimited for most features)

**Example Query (All Features):**

```graphql
query GetUsage {
  usage {
    usage {
      features {
        feature
        used
        limit
        remaining
        resetAt
      }
    }
  }
}
```

**Example Query (Single Feature):**

```graphql
query GetUsage($feature: String) {
  usage {
    usage(feature: $feature) {
      features {
        feature
        used
        limit
        remaining
        resetAt
      }
    }
  }
}
```

**Variables:**

```json
{
  "feature": "EMAIL_FINDER"
}
```

**Example Response:**

```json
{
  "data": {
    "usage": {
      "usage": {
        "features": [
          {
            "feature": "EMAIL_FINDER",
            "used": 150,
            "limit": 1000,
            "remaining": 850,
            "resetAt": "2024-02-01T00:00:00Z"
          },
          {
            "feature": "VERIFIER",
            "used": 75,
            "limit": 500,
            "remaining": 425,
            "resetAt": "2024-02-01T00:00:00Z"
          },
          {
            "feature": "AI_CHAT",
            "used": 20,
            "limit": 999999,
            "remaining": -1,
            "resetAt": null
          }
        ]
      }
    }
  }
}
```

**Note:** When `limit` is 999999 (unlimited), `remaining` will be -1. The `resetAt` field indicates when the usage period resets (typically monthly).

### featureOverview

Get a combined view of **usage**, **activities**, and **jobs** for a single feature for the current user.

**Parameters:**

| Name   | Type   | Required | Description                                      |
|--------|--------|----------|--------------------------------------------------|
| feature| String!| Yes      | Feature name (e.g. "BULK_EXPORT", "EMAIL_FINDER")|

```graphql
query FeatureOverview($feature: String!) {
  featureOverview {
    featureOverview(feature: $feature) {
      feature
      usage {
        feature
        used
        limit
        remaining
        resetAt
      }
      activities {
        id
        service_type
        action_type
        status
        created_at
      }
      jobs {
        job_id
        job_type
        status
        created_at
      }
    }
  }
}
```

**Arguments:**

- `feature` (String!): Feature name (e.g., `"BULK_EXPORT"`, `"BULK_VERIFICATION"`, `"EMAIL_FINDER"`).

**Returns:** `FeatureOverview` object with:

- `feature`: Normalized feature name
- `usage`: `FeatureUsageInfo` for this feature (or `null` if not used yet)
- `activities`: Recent `UserActivity` records associated with this feature (email or jobs service types)
- `jobs`: `SchedulerJob` records associated with this feature (e.g., bulk exports / verifications)

**Authentication:** Required

## Mutations

### trackUsage

Track feature usage for the current user.

**Parameters:**

| Name  | Type               | Required | Description                                |
|-------|--------------------|----------|--------------------------------------------|
| input | TrackUsageInput!   | Yes      | Object with `feature` (string) and `amount` (Int, default 1) |

```graphql
mutation TrackUsage($input: TrackUsageInput!) {
  usage {
    trackUsage(input: $input) {
      feature
      used
      limit
      success
    }
  }
}
```

**Variables:**

```json
{
  "input": {
    "feature": "EMAIL_FINDER",
    "amount": 1
  }
}
```

**Input:** `TrackUsageInput!`

**Returns:** `TrackUsageResponse`

**Authentication:** Required

**Validation:**

- `feature`: Required, non-empty string, max 100 characters, must be a valid feature name
- `amount`: Must be a non-negative integer, min: 1, max: 1,000,000 (default: 1)

**Implementation Details:**

- Increments usage count for the specified feature
- Usage records are auto-created if they don't exist
- Limits are updated if user role changed (e.g., upgraded subscription)
- Usage is capped at the limit (won't exceed limit)
- Unlimited features (limit is None or 0) keep used count at 0
- Role-based limits: Limits are determined by user role (FREE_USER vs PRO_USER)

**Example Response:**

```json
{
  "data": {
    "usage": {
      "trackUsage": {
        "feature": "EMAIL_FINDER",
        "used": 151,
        "limit": 1000,
        "success": true
      }
    }
  }
}
```

### resetUsage

Reset the usage counter for a specific feature to zero.

**Parameters:**

| Name  | Type                 | Required | Description                          |
|-------|----------------------|----------|--------------------------------------|
| input | ResetUsageInput!     | Yes      | Object with `feature` (string)       |

```graphql
mutation ResetUsage($input: ResetUsageInput!) {
  usage {
    resetUsage(input: $input) {
      feature
      used
      limit
      success
    }
  }
}
```

**Variables:**

```json
{
  "input": {
    "feature": "EMAIL_FINDER"
  }
}
```

**Input:** `ResetUsageInput!`

**Returns:** `ResetUsageResponse`

**Authentication:** Required

**Validation:**

- `feature`: Required, non-empty string, max 100 characters, must be a valid feature name

**Implementation Details:**

- Resets usage counter to zero for the specified feature
- Useful for testing or administrative purposes
- Usage records are auto-created if they don't exist

**Example Response:**

```json
{
  "data": {
    "usage": {
      "resetUsage": {
        "feature": "EMAIL_FINDER",
        "used": 0,
        "limit": 1000,
        "success": true
      }
    }
  }
}
```

## Input Types

### TrackUsageInput

Input for tracking feature usage.

```graphql
input TrackUsageInput {
  feature: String!
  amount: Int
}
```

**Fields:**

- `feature` (String!): Feature name (must be one of the supported features) - max 100 characters
- `amount` (Int): Amount to increment (default: 1, min: 1, max: 1,000,000)

**Validation:**

- `feature`: Required, non-empty, max 100 characters, must be a valid feature name
- `amount`: Must be a non-negative integer, min: 1, max: 1,000,000
- Input validation is performed via `input.validate()` method

### ResetUsageInput

Input for resetting feature usage.

```graphql
input ResetUsageInput {
  feature: String!
}
```

**Fields:**

- `feature` (String!): Feature name (must be one of the supported features) - max 100 characters

**Validation:**

- `feature`: Required, non-empty, max 100 characters, must be a valid feature name
- Input validation is performed via `input.validate()` method

## Error Handling

The Usage module implements comprehensive error handling with input validation, database error handling, and response validation.

### Error Types

The Usage module may raise the following errors:

- **NotFoundError** (404): User usage record not found
  - Code: `NOT_FOUND`
  - Extensions: `resourceType: "Usage"`, `identifier: <user_id>`
  - Occurs when: User usage record does not exist (usage records are auto-created on first track)
- **ValidationError** (422): Input validation failed
  - Code: `VALIDATION_ERROR`
  - Extensions: `fieldErrors` (field-specific errors)
  - Occurs when: Invalid feature name, invalid amount (must be at least 1), or missing required fields
- **BadRequestError** (400): Invalid request data
  - Code: `BAD_REQUEST`
  - Occurs when: Request format is invalid or required parameters are missing
- **ServiceUnavailableError** (503): Database service unavailable
  - Code: `SERVICE_UNAVAILABLE`
  - Extensions: `serviceName: "database"`
  - Occurs when: Database connection fails

### Error Response Examples

**Example: Validation Error**

```json
{
  "errors": [
    {
      "message": "Invalid feature: INVALID_FEATURE. Valid features: AI_CHAT, BULK_EXPORT, ...",
      "extensions": {
        "code": "VALIDATION_ERROR",
        "statusCode": 422,
        "fieldErrors": {
          "feature": ["Feature must be one of the supported features: AI_CHAT, BULK_EXPORT, API_KEYS, ..."],
          "amount": ["Amount must be at least 1"]
        }
      }
    }
  ]
}
```

**Example: Usage Record Not Found**

```json
{
  "errors": [
    {
      "message": "Usage with identifier '123e4567-e89b-12d3-a456-426614174000' not found",
      "extensions": {
        "code": "NOT_FOUND",
        "statusCode": 404,
        "resourceType": "Usage",
        "identifier": "123e4567-e89b-12d3-a456-426614174000"
      }
    }
  ]
}
```

### Error Handling Patterns

- **Input Validation**: Feature names and amounts are validated before processing
  - Feature name: max 100 characters, must be valid feature enum value
  - Amount: min 1, max 1,000,000, must be non-negative integer
- **Database Errors**: All database operations include transaction rollback on failure
  - Transaction rollback on error (automatic via FastAPI dependency)
  - Integrity errors are caught and converted to user-friendly errors
  - Database connection errors are converted to ServiceUnavailableError
- **Auto-Creation**: Usage records are automatically created when first tracked
- **Feature Validation**: Feature names are validated against supported features list
- **Error Logging**: Comprehensive error logging with context for debugging

## Implementation Details

### Usage Service

- **UsageService**: Feature usage tracking is handled by `UsageService`
  - All usage operations go through the service layer
  - Service handles database operations, validation, and business logic

### Role-Based Limits

- **Role Normalization**: User roles are normalized to FREE_USER or PRO_USER level
  - SuperAdmin/Admin: Get PRO_USER level access (unlimited for most features)
  - PRO_USER: Gets PRO_USER level access
  - All other roles: Get FREE_USER level access
- **Feature Limits**: Limits are defined per feature and role in `FEATURE_LIMITS` dictionary
  - FREE_USER limits: Specific numeric limits (e.g., EMAIL_FINDER: 10, VERIFIER: 5)
  - PRO_USER limits: None (unlimited) for most features
  - Some features are admin-only (TEAM_MANAGEMENT: 0 for FREE_USER, unlimited for PRO_USER)

### Feature Limits Configuration

The following feature limits are configured:

- **AI_CHAT**: FREE_USER: 0, PRO_USER: unlimited
- **BULK_EXPORT**: FREE_USER: 0, PRO_USER: unlimited
- **API_KEYS**: FREE_USER: 0, PRO_USER: unlimited
- **TEAM_MANAGEMENT**: FREE_USER: 0, PRO_USER: unlimited (Admin only)
- **EMAIL_FINDER**: FREE_USER: 10, PRO_USER: unlimited
- **VERIFIER**: FREE_USER: 5, PRO_USER: unlimited
- **LINKEDIN**: FREE_USER: 5, PRO_USER: unlimited
- **DATA_SEARCH**: FREE_USER: 20, PRO_USER: unlimited
- **ADVANCED_FILTERS**: FREE_USER: 0, PRO_USER: unlimited
- **AI_SUMMARIES**: FREE_USER: 0, PRO_USER: unlimited
- **SAVE_SEARCHES**: FREE_USER: 0, PRO_USER: unlimited
- **BULK_VERIFICATION**: FREE_USER: 0, PRO_USER: unlimited

### Usage Tracking

- **Auto-Creation**: Usage records are automatically created on first track
  - Created with current role-based limit
  - Period start/end dates are set (monthly periods)
- **Period-Based Resets**: Usage resets monthly at the start of each month
  - `period_start`: Start of current period
  - `period_end`: End of current period (start of next month)
  - Usage is reset to 0 when period ends
- **Limit Updates**: Limits are updated if user role changed (e.g., upgraded subscription)
  - Limit is recalculated based on current role
  - Used count is preserved (unless reset)
- **Usage Capping**: Usage is capped at the limit (won't exceed limit)
  - Formula: `used = min(used + amount, limit)`
- **Unlimited Features**: Features with unlimited access (limit is None or 0) keep used count at 0

### Unlimited Representation

- **Unlimited Limits**: Unlimited is represented as 999999 in responses
  - `limit`: 999999 means unlimited
  - `remaining`: -1 means unlimited
- **Internal Representation**: Internally, unlimited is represented as None
  - Converted to 999999 for API responses

### Database Operations

- **Usage Records**: Stored in `FeatureUsage` table
  - Fields: `user_id`, `feature`, `used`, `limit`, `period_start`, `period_end`, `updated_at`
  - Unique constraint on `(user_id, feature)`
- **Transaction Management**: All database operations use transactions
  - Transaction rollback on failure
  - Automatic flush after updates

### Error Handling

- **Input Validation**: All inputs are validated before processing
  - Feature name validation: max 100 characters, must be valid feature enum
  - Amount validation: min 1, max 1,000,000, must be non-negative integer
  - UUID validation for user IDs
- **Database Error Handling**: Database operations use centralized error handlers
  - Transaction rollback on failure
  - Integrity errors are caught and converted to user-friendly errors
  - Database connection errors are converted to ServiceUnavailableError
- **Response Validation**: All service responses are validated before returning
  - Usage data structure validation
  - Limit/used value validation

## Usage Examples

### Complete Usage Tracking Flow

```graphql
# 1. Get current usage for all features
query GetCurrentUsage {
  usage {
    usage {
      features {
        feature
        used
        limit
        remaining
        resetAt
      }
    }
  }
}

# 1a. Get current usage for a specific feature
query GetFeatureUsage($feature: String) {
  usage {
    usage(feature: $feature) {
      features {
        feature
        used
        limit
        remaining
        resetAt
      }
    }
  }
}

# 2. Track feature usage
mutation TrackEmailFinder {
  usage {
    trackUsage(input: {
      feature: "EMAIL_FINDER"
      amount: 1
    }) {
      feature
      used
      limit
      success
    }
  }
}

# 3. Track multiple uses
mutation TrackBulk {
  usage {
    trackUsage(input: {
      feature: "BULK_VERIFICATION"
      amount: 10
    }) {
      feature
      used
      limit
      success
    }
  }
}

# 4. Reset usage (for testing/admin)
mutation ResetUsage {
  usage {
    resetUsage(input: {
      feature: "EMAIL_FINDER"
    }) {
      feature
      used
      limit
      success
    }
  }
}

# 5. Check if feature is available (using feature parameter)
query CheckFeature($feature: String) {
  usage {
    usage(feature: $feature) {
      features {
        feature
        used
        limit
        remaining
        resetAt
      }
    }
  }
}
```

```

## Implementation Details

- **UsageService**: Usage tracking is handled by `UsageService`
- **Feature Limits**: Each feature has a usage limit (999999 means unlimited)
- **Automatic Creation**: Usage records are automatically created when first tracked
- **User Isolation**: Users can only track and view their own usage
- **Incremental Tracking**: Usage is incremented by the specified amount
- **Reset Functionality**: Usage can be reset to zero (useful for testing/admin)

## Task breakdown (for maintainers)

1. **Trace usage query:** UsageQuery.usage(feature?) → UsageService; feature_usage table filtered by user_id; optional feature filter (case-insensitive); validate feature name against supported list.
2. **featureOverview:** Separate resolver (FeatureOverviewQuery); document which fields it returns (e.g. list of features with limits/used).
3. **trackUsage:** Increment usage for feature; verify user_id from context; auto-create feature_usage row if missing; confirm amount default (1) and max.
4. **resetUsage:** Set used to 0 for feature; typically admin/testing; confirm authorization (e.g. self or Admin).
5. **Limits:** Document how limits are determined (subscription/role from user_profiles); 999999 = unlimited.

## Related Modules

- **Users Module**: User profile contains subscription information that may affect limits
- **Billing Module**: Subscription plans may affect usage limits

## Documentation metadata

- Era: `1.x`
- Introduced in: `TBD` (fill with exact minor)
- Frontend bindings: list page files from `docs/frontend/pages/*.json`
- Data stores touched: PostgreSQL/Elasticsearch/MongoDB/S3 as applicable

## Endpoint/version binding checklist

- Add operation list with `introduced_in` / `deprecated_in` tags.
- Map each operation to frontend page bindings and hook/service usage.
- Record DB tables read/write for each operation.

