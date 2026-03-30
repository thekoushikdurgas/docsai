# Admin Module

## Overview

The Admin module provides administrative operations for user management, statistics, logs, and system monitoring. Most operations require Admin or SuperAdmin role.
**Location:** `app/graphql/modules/admin/`

## Queries and mutations – parameters and variable types

| Operation | Parameter(s) | Variable type (GraphQL) | Return type |
|-----------|---------------|-------------------------|-------------|
| **Queries** (Admin/SuperAdmin) | | | |
| `users` | `limit`, `offset`, `isActive`, `role`, `search` | Int, Int, Boolean, String, String | `UserConnection` |
| `userStats` | — | — | `UserStats` |
| `userHistory` | `userUuid`, `limit`, `offset` | ID!, Int, Int | `UserHistoryConnection` |
| `logStatistics` | `input` | LogStatisticsInput | log stats type |
| `logs` | `limit`, `offset`, `level`, `logger`, `userId`, etc. | Int, Int, String, String, ID, ... | logs connection |
| `searchLogs` | `input` | SearchLogsInput! | search result |
| **Mutations** | | | |
| `updateUserRole` | `input` | UpdateUserRoleInput! | User |
| `updateUserCredits` | `input` | UpdateUserCreditsInput! | User |
| `deleteUser` | `input` | DeleteUserInput! | result |
| `promoteToAdmin` | `input` | PromoteToAdminInput! | User |
| `promoteToSuperAdmin` | `input` | PromoteToSuperAdminInput! | User |
| `createLog` | `input` | CreateLogInput! | result |
| `createLogsBatch` | `input` | CreateLogsBatchInput! | result |
| `updateLog` | `input` | UpdateLogInput! | result |
| `deleteLog` | `input` | DeleteLogInput! | result |
| `deleteLogsBulk` | `input` | DeleteLogsBulkInput! | DeleteLogsBulkResponse |

Use camelCase in variables. Logs operations call Lambda Logs API (MongoDB). See Input Types for each input's fields.

## Types

### UserConnection

Paginated connection of users.

```graphql
type UserConnection {
  items: [User!]!
  pageInfo: PageInfo!
}
```

### UserStats

User statistics for admin dashboard.

```graphql
type UserStats {
  totalUsers: Int!
  activeUsers: Int!
  usersByRole: JSON!
  usersByPlan: JSON!
}
```

### UserHistoryItem

User history record (registration/login events).

```graphql
type UserHistoryItem {
  id: ID!
  userId: ID!
  userEmail: String
  userName: String
  eventType: String!
  ip: String
  continent: String
  country: String
  city: String
  device: String
  createdAt: DateTime!
}
```

### UserHistoryConnection

Paginated connection of user history items.

```graphql
type UserHistoryConnection {
  items: [UserHistoryItem!]!
  pageInfo: PageInfo!
}
```

### LogEntry

Single log entry from system logs.

```graphql
type LogEntry {
  id: String!
  timestamp: DateTime!
  level: String!
  logger: String!
  message: String!
  context: JSON
  performance: JSON
  error: JSON
  userId: String
  requestId: String
}
```

### LogConnection

Paginated connection of log entries.

```graphql
type LogConnection {
  items: [LogEntry!]!
  pageInfo: PageInfo!
}
```

### LogSearchConnection

Paginated connection of log entries from search.

```graphql
type LogSearchConnection {
  items: [LogEntry!]!
  pageInfo: PageInfo!
  query: String!
}
```

### LogStatistics

Aggregated log statistics.

```graphql
type LogStatistics {
  timeRange: String!
  totalLogs: Int!
  byLevel: JSON!
  errorRate: Float!
  avgResponseTimeMs: Float!
  slowQueriesCount: Int!
  topErrors: [TopError!]!
  performanceTrends: [PerformanceTrend!]!
  userActivity: UserActivity!
  byLogger: JSON
}
```

### TopError

Top error pattern from log statistics.

```graphql
type TopError {
  type: String!
  count: Int!
  message: String!
  lastSeen: DateTime!
}
```

### PerformanceTrend

Performance trend data point.

```graphql
type PerformanceTrend {
  time: DateTime!
  avgDurationMs: Float!
  p95DurationMs: Float!
  slowQueriesCount: Int!
}
```

### TopUser

Top active user from log statistics.

```graphql
type TopUser {
  userId: String!
  requestCount: Int!
}
```

### UserActivity

User activity metrics from log statistics.

```graphql
type UserActivity {
  activeUsers: Int!
  requestsPerUserAvg: Float!
  topUsers: [TopUser!]!
}
```

## Queries

### users

List all users in the system with pagination.

**Parameters:**

| Name    | Type              | Required | Description          |
|---------|-------------------|----------|----------------------|
| filters | UserFilterInput   | No       | Optional pagination (limit, offset) |

```graphql
query ListAllUsers($filters: UserFilterInput) {
  admin {
    users(filters: $filters) {
      items {
        uuid
        email
        name
        isActive
        profile {
          role
          credits
        }
      }
      pageInfo {
        total
        limit
        offset
      }
    }
  }
}
```

**Arguments:**
- `filters` (UserFilterInput): Optional pagination filters

**Returns:** `UserConnection`

**Authentication:** Required

**Authorization:** SuperAdmin only

**Validation:**
- Pagination is validated via `validate_pagination` utility (limit, offset)

**Implementation Details:**
- Role check via `UserProfileRepository` (must be SuperAdmin)
- Uses `UserRepository.list_all_users` to retrieve all users
- Pagination is normalized for backward compatibility
- Response structure is validated before conversion to GraphQL types

### userStats

Get aggregated user statistics.

**Parameters:** None.

```graphql
query GetUserStats {
  admin {
    userStats {
      totalUsers
      activeUsers
      usersByRole
      usersByPlan
    }
  }
}
```

**Returns:** `AdminUserStats`

**Authentication:** Required

**Authorization:** Admin or SuperAdmin

**Implementation Details:**
- Role check via `UserProfileRepository` (must be Admin or SuperAdmin)
- Uses SQLAlchemy queries to count total and active users
- Uses SQLAlchemy GROUP BY queries to aggregate users by role and subscription plan
- Uses `func.coalesce` to handle NULL values (defaults to "FreeUser" for role, "free" for plan)
- Database errors are handled centrally via `handle_database_exception`

### userHistory

Get user history records (registration/login events).

**Parameters:**

| Name    | Type                    | Required | Description        |
|---------|-------------------------|----------|--------------------|
| filters | UserHistoryFilterInput  | No       | user_id, event_type, limit, offset |

```graphql
query GetUserHistory($filters: UserHistoryFilterInput) {
  admin {
    userHistory(filters: $filters) {
      items {
        id
        userId
        userEmail
        eventType
        ip
        country
        city
        createdAt
      }
      pageInfo {
        total
      }
    }
  }
}
```

**Arguments:**
- `filters` (UserHistoryFilterInput): Optional filters

**Returns:** `UserHistoryConnection`

**Authentication:** Required

**Authorization:** SuperAdmin only

**Validation:**
- Pagination is validated via `validate_pagination` utility (limit, offset)
- `user_id`: Optional, must be valid UUID format if provided
- `event_type`: Optional, filters by event type (e.g., "register", "login")

**Implementation Details:**
- Role check via `UserProfileRepository` (must be SuperAdmin)
- Uses `UserService.get_user_history` to retrieve history records
- Pagination is normalized for backward compatibility
- Response structure is validated before conversion to GraphQL types
- History items include geolocation data (IP, continent, country, city, etc.)

### logs

Query system logs with filters.

**Parameters:**

| Name    | Type                 | Required | Description                    |
|---------|----------------------|----------|--------------------------------|
| filters | LogQueryFilterInput   | No       | level, logger, user_id, time range, limit, offset |

```graphql
query GetLogs($filters: LogQueryFilterInput) {
  admin {
    logs(filters: $filters) {
      items {
        id
        timestamp
        level
        logger
        message
        context
      }
      pageInfo {
        total
      }
    }
  }
}
```

**Arguments:**
- `filters` (LogQueryFilterInput): Optional filters

**Returns:** `LogConnection`

**Authentication:** Required

**Authorization:** SuperAdmin only

**Validation:**
- Pagination is validated via `validate_pagination` utility (limit, offset)
- `level`: Optional, filters by log level
- `logger`: Optional, max 200 characters if provided
- `user_id`: Optional, must be valid UUID format if provided
- `request_id`: Optional, max 100 characters if provided
- `start_time`: Optional, DateTime format
- `end_time`: Optional, DateTime format

**Implementation Details:**
- Role check via `UserProfileRepository` (must be SuperAdmin)
- Uses `LambdaLogsClient.query_logs` to retrieve logs from MongoDB
- Filters are validated and converted to appropriate format
- Pagination is normalized for backward compatibility
- Response structure is validated before conversion to GraphQL types
- Timestamps are converted from ISO format to datetime objects

### searchLogs

Search system logs.

**Parameters:**

| Name  | Type             | Required | Description        |
|-------|------------------|----------|--------------------|
| input | LogSearchInput!  | Yes      | query, limit, offset |

```graphql
query SearchLogs($input: LogSearchInput!) {
  admin {
    searchLogs(input: $input) {
      items {
        id
        timestamp
        level
        message
      }
      pageInfo {
        total
      }
      query
    }
  }
}
```

**Arguments:**
- `input` (LogSearchInput!): Search query and pagination

**Returns:** `LogSearchConnection`

**Authentication:** Required

**Authorization:** SuperAdmin only

**Validation:**
- `query`: Required, non-empty string, min 1 character, max 500 characters
- Pagination is validated via `validate_pagination` utility (limit, offset)

**Implementation Details:**
- Role check via `UserProfileRepository` (must be SuperAdmin)
- Uses `LambdaLogsClient.search_logs` to perform full-text search on log messages
- Query string is validated and trimmed before search
- Pagination is normalized for backward compatibility
- Response structure is validated before conversion to GraphQL types
- Returns search query in response for reference

### logStatistics

Get aggregated log statistics.

**Parameters:**

| Name      | Type   | Required | Description     |
|-----------|--------|----------|-----------------|
| timeRange | String!| Yes      | Time range for aggregation |

```graphql
query GetLogStats($timeRange: String!) {
  admin {
    logStatistics(timeRange: $timeRange) {
      timeRange
      totalLogs
      byLevel
      errorRate
      avgResponseTimeMs
      topErrors {
        type
        count
        message
      }
      userActivity {
        activeUsers
        requestsPerUserAvg
        topUsers {
          userId
          requestCount
        }
      }
    }
  }
}
```

**Arguments:**
- `timeRange` (String!): Time range (must be one of: "1h", "24h", "7d", "30d")

**Returns:** `LogStatistics`

**Authentication:** Required

**Authorization:** SuperAdmin only

**Validation:**
- `timeRange`: Required, must be one of: "1h", "24h", "7d", "30d"

**Implementation Details:**
- Role check via `UserProfileRepository` (must be SuperAdmin)
- Uses `LogStatsRepository.get_statistics` to retrieve aggregated statistics
- Returns empty statistics if no data is available
- Converts top_errors, performance_trends, and user_activity data to GraphQL types
- Timestamps are converted from ISO format to datetime objects

## Mutations

### updateUserRole

Update a user's role.

**Parameters:**

| Name  | Type                   | Required | Description  |
|-------|------------------------|----------|--------------|
| input | UpdateUserRoleInput!   | Yes      | userId, role  |

```graphql
mutation UpdateUserRole($input: UpdateUserRoleInput!) {
  admin {
    updateUserRole(input: $input) {
      uuid
      email
      profile {
        role
      }
    }
  }
}
```

**Variables:**

```json
{
  "input": {
    "userId": "123e4567-e89b-12d3-a456-426614174000",
    "role": "Admin"
  }
}
```

**Input:** `UpdateUserRoleInput!`

**Returns:** `User`

**Authentication:** Required

**Authorization:** SuperAdmin only

**Validation:**
- `user_id`: Required, must be valid UUID format
- `role`: Required, must be one of the valid roles (from VALID_ROLES constant)

**Implementation Details:**
- Role check via `UserProfileRepository` (must be SuperAdmin)
- Uses `UserRepository.get_by_uuid` to retrieve target user
- Uses `UserProfileRepository.get_by_user_id` to retrieve target profile
- Raises NotFoundError if user or profile doesn't exist
- Updates profile role and commits transaction
- Response structure is validated before conversion to GraphQL type

### updateUserCredits

Update a user's credits.

**Parameters:**

| Name  | Type                      | Required | Description  |
|-------|---------------------------|----------|--------------|
| input | UpdateUserCreditsInput!   | Yes      | userId, credits |

```graphql
mutation UpdateUserCredits($input: UpdateUserCreditsInput!) {
  admin {
    updateUserCredits(input: $input) {
      uuid
      profile {
        credits
      }
    }
  }
}
```

**Variables:**

```json
{
  "input": {
    "userId": "123e4567-e89b-12d3-a456-426614174000",
    "credits": 5000
  }
}
```

**Input:** `UpdateUserCreditsInput!`

**Returns:** `User`

**Authentication:** Required

**Authorization:** SuperAdmin only

**Validation:**
- `user_id`: Required, must be valid UUID format
- `credits`: Required, must be an integer, non-negative, max 1,000,000,000

**Implementation Details:**
- Role check via `UserProfileRepository` (must be SuperAdmin)
- Uses `UserRepository.get_by_uuid` to retrieve target user
- Uses `UserProfileRepository.get_by_user_id` to retrieve target profile
- Raises NotFoundError if user or profile doesn't exist
- Updates profile credits and commits transaction
- Response structure is validated before conversion to GraphQL type

### deleteUser

Delete a user and their profile.

**Parameters:**

| Name  | Type               | Required | Description  |
|-------|--------------------|----------|--------------|
| input | DeleteUserInput!   | Yes      | userId       |

```graphql
mutation DeleteUser($input: DeleteUserInput!) {
  admin {
    deleteUser(input: $input)
  }
}
```

**Variables:**

```json
{
  "input": {
    "userId": "123e4567-e89b-12d3-a456-426614174000"
  }
}
```

**Input:** `DeleteUserInput!`

**Returns:** `Boolean`

**Authentication:** Required

**Authorization:** SuperAdmin only

**Validation:**
- `user_id`: Required, must be valid UUID format
- Cannot delete your own account (raises BadRequestError)

**Implementation Details:**
- Role check via `UserProfileRepository` (must be SuperAdmin)
- Validates that user is not trying to delete their own account
- Uses `UserRepository.get_by_uuid` to retrieve target user
- Raises NotFoundError if user doesn't exist
- Uses `UserRepository.delete_user` to delete user (cascade deletes profile)
- Commits transaction after deletion

### promoteToAdmin

Promote a user to Admin role.

**Parameters:**

| Name  | Type                 | Required | Description  |
|-------|----------------------|----------|--------------|
| input | PromoteToAdminInput! | Yes      | userId       |

```graphql
mutation PromoteToAdmin($input: PromoteToAdminInput!) {
  admin {
    promoteToAdmin(input: $input) {
      uuid
      profile {
        role
      }
    }
  }
}
```

**Input:** `PromoteToAdminInput!`

**Returns:** `User`

**Authentication:** Required

**Validation:**
- `user_id`: Required, must be valid UUID format

**Authorization:** 
- SuperAdmin can promote any user
- Any authenticated user can self-promote (not recommended for production)

**Implementation Details:**
- Validates that user is promoting themselves OR user is SuperAdmin
- Uses `UserService.promote_user_to_admin` to update role
- Reloads user after promotion to get updated profile
- Raises NotFoundError if user doesn't exist
- Response structure is validated before conversion to GraphQL type

### promoteToSuperAdmin

Promote a user to SuperAdmin role.

**Parameters:**

| Name  | Type                        | Required | Description  |
|-------|-----------------------------|----------|--------------|
| input | PromoteToSuperAdminInput!   | Yes      | userId       |

```graphql
mutation PromoteToSuperAdmin($input: PromoteToSuperAdminInput!) {
  admin {
    promoteToSuperAdmin(input: $input) {
      uuid
      profile {
        role
      }
    }
  }
}
```

**Input:** `PromoteToSuperAdminInput!`

**Returns:** `User`

**Authentication:** Required

**Authorization:** SuperAdmin only

**Validation:**
- `user_id`: Required, must be valid UUID format

**Implementation Details:**
- Role check via `UserProfileRepository` (must be SuperAdmin)
- Uses `UserService.promote_user_to_super_admin` to update role
- Reloads user after promotion to get updated profile
- Raises NotFoundError if user doesn't exist
- Response structure is validated before conversion to GraphQL type

**Authorization:** SuperAdmin only

### createLog

Create a single log entry.

**Parameters:**

| Name  | Type             | Required | Description        |
|-------|------------------|----------|--------------------|
| input | CreateLogInput!  | Yes      | level, message, context, etc. |

```graphql
mutation CreateLog($input: CreateLogInput!) {
  admin {
    createLog(input: $input) {
      id
      timestamp
      level
      logger
      message
      context
      performance
      error
      userId
      requestId
    }
  }
}
```

**Variables:**

```json
{
  "input": {
    "level": "ERROR",
    "logger": "app.services.email",
    "message": "Failed to send email",
    "context": {
      "email": "user@example.com",
      "template": "welcome"
    },
    "error": {
      "type": "SMTPError",
      "message": "Connection timeout"
    },
    "userId": "123e4567-e89b-12d3-a456-426614174000",
    "requestId": "req-123"
  }
}
```

**Input:** `CreateLogInput!`

**Returns:** `LogEntry`

**Authentication:** Required

**Authorization:** SuperAdmin only

**Validation:**
- `level`: Required, must be one of: "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
- `logger`: Required, max 200 characters
- `message`: Required, non-empty string
- `request_id`: Optional, max 100 characters if provided
- `timestamp`: Optional, defaults to current time if not provided

**Implementation Details:**
- Role check via `UserProfileRepository` (must be SuperAdmin)
- Uses `LambdaLogsClient.create_log` to create log entry
- Log level is automatically uppercased
- Timestamp is set to current time if not provided
- Returns created log entry with generated ID

### createLogsBatch

Create multiple log entries in a single batch request.

**Parameters:**

| Name  | Type                     | Required | Description  |
|-------|--------------------------|----------|--------------|
| input | CreateLogsBatchInput!   | Yes      | logs (array of log entries) |

```graphql
mutation CreateLogsBatch($input: CreateLogsBatchInput!) {
  admin {
    createLogsBatch(input: $input) {
      id
      timestamp
      level
      logger
      message
    }
  }
}
```

**Variables:**

```json
{
  "input": {
    "logs": [
      {
        "level": "INFO",
        "logger": "app.services.user",
        "message": "User logged in",
        "userId": "123e4567-e89b-12d3-a456-426614174000"
      },
      {
        "level": "WARNING",
        "logger": "app.services.email",
        "message": "Email queue is full"
      }
    ]
  }
}
```

**Input:** `CreateLogsBatchInput!`

**Returns:** `[LogEntry!]!`

**Authentication:** Required

**Authorization:** SuperAdmin only

**Validation:**
- `logs`: Required, array of `CreateLogInput`, min 1, max 100 items
- Each log entry follows same validation as `createLog`

**Implementation Details:**
- Role check via `UserProfileRepository` (must be SuperAdmin)
- Uses `LambdaLogsClient.create_logs_batch` to create log entries
- All logs are created in a single API call for efficiency
- Returns array of created log entries with generated IDs

### updateLog

Update an existing log entry.

**Parameters:**

| Name  | Type               | Required | Description  |
|-------|--------------------|----------|--------------|
| input | UpdateLogInput!   | Yes      | id, message, context, etc. |

```graphql
mutation UpdateLog($input: UpdateLogInput!) {
  admin {
    updateLog(input: $input) {
      id
      message
      context
      timestamp
    }
  }
}
```

**Variables:**

```json
{
  "input": {
    "logId": "507f1f77bcf86cd799439011",
    "message": "Updated error message",
    "context": {
      "additionalInfo": "More details"
    }
  }
}
```

**Input:** `UpdateLogInput!`

**Returns:** `LogEntry`

**Authentication:** Required

**Authorization:** SuperAdmin only

**Validation:**
- `log_id`: Required, must be valid log ID (1-255 characters)
- `message`: Optional, new message text
- `context`: Optional, updated context object
- At least one of `message` or `context` must be provided

**Implementation Details:**
- Role check via `UserProfileRepository` (must be SuperAdmin)
- Uses `LambdaLogsClient.update_log` to update log entry
- Only provided fields are updated
- Returns updated log entry

### deleteLog

Delete a single log entry.

**Parameters:**

| Name  | Type              | Required | Description  |
|-------|-------------------|----------|--------------|
| input | DeleteLogInput!   | Yes      | id           |

```graphql
mutation DeleteLog($input: DeleteLogInput!) {
  admin {
    deleteLog(input: $input)
  }
}
```

**Variables:**

```json
{
  "input": {
    "logId": "507f1f77bcf86cd799439011"
  }
}
```

**Input:** `DeleteLogInput!`

**Returns:** `Boolean`

**Authentication:** Required

**Authorization:** SuperAdmin only

**Validation:**
- `log_id`: Required, must be valid log ID (1-255 characters)

**Implementation Details:**
- Role check via `UserProfileRepository` (must be SuperAdmin)
- Uses `LambdaLogsClient.delete_log` to delete log entry
- Returns `true` on success
- Raises NotFoundError if log doesn't exist

### deleteLogsBulk

Delete multiple log entries by filters.

**Parameters:**

| Name  | Type                   | Required | Description        |
|-------|------------------------|----------|--------------------|
| input | DeleteLogsBulkInput!   | Yes      | Filter criteria    |

```graphql
mutation DeleteLogsBulk($input: DeleteLogsBulkInput!) {
  admin {
    deleteLogsBulk(input: $input) {
      deletedCount
    }
  }
}
```

**Variables:**

```json
{
  "input": {
    "level": "DEBUG",
    "startTime": "2024-01-01T00:00:00Z",
    "endTime": "2024-01-31T23:59:59Z"
  }
}
```

**Input:** `DeleteLogsBulkInput!`

**Returns:** `DeleteLogsBulkResponse`

**Authentication:** Required

**Authorization:** SuperAdmin only

**Validation:**
- At least one filter must be provided
- `level`: Optional, must be one of: "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
- `logger`: Optional, max 200 characters
- `request_id`: Optional, max 100 characters
- `start_time` and `end_time`: Optional, must be valid datetime format

**Implementation Details:**
- Role check via `UserProfileRepository` (must be SuperAdmin)
- Uses `LambdaLogsClient.delete_logs_bulk` to delete logs matching filters
- Returns count of deleted logs
- All matching logs are deleted in a single operation

## Input Types

### UserFilterInput

Input for filtering users list.

```graphql
input UserFilterInput {
  limit: Int
  offset: Int
}
```

### UserHistoryFilterInput

Input for filtering user history.

```graphql
input UserHistoryFilterInput {
  userId: ID
  eventType: String
  limit: Int
  offset: Int
}
```

### UpdateUserRoleInput

Input for updating user role.

```graphql
input UpdateUserRoleInput {
  userId: ID!
  role: String!
}
```

**Valid roles:** `FreeUser`, `ProUser`, `Admin`, `SuperAdmin`

### UpdateUserCreditsInput

Input for updating user credits.

```graphql
input UpdateUserCreditsInput {
  userId: ID!
  credits: Int!
}
```

**Validation:** Credits must be non-negative

### DeleteUserInput

Input for deleting a user.

```graphql
input DeleteUserInput {
  userId: ID!
}
```

### PromoteToAdminInput

Input for promoting a user to admin.

```graphql
input PromoteToAdminInput {
  userId: ID!
}
```

### PromoteToSuperAdminInput

Input for promoting a user to super admin.

```graphql
input PromoteToSuperAdminInput {
  userId: ID!
}
```

### LogQueryFilterInput

Input for querying logs with filters.

```graphql
input LogQueryFilterInput {
  level: String
  logger: String
  userId: ID
  requestId: String
  startTime: DateTime
  endTime: DateTime
  limit: Int
  offset: Int
}
```

### LogSearchInput

Input for searching logs.

```graphql
input LogSearchInput {
  query: String!
  limit: Int
  offset: Int
}
```

### CreateLogInput

Input for creating a single log entry.

```graphql
input CreateLogInput {
  level: String!
  logger: String!
  message: String!
  context: JSON
  performance: JSON
  error: JSON
  userId: ID
  requestId: String
  timestamp: DateTime
}
```

**Fields:**
- `level` (String!): Log level, must be one of: "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
- `logger` (String!): Logger name, max 200 characters
- `message` (String!): Log message
- `context` (JSON): Optional context data
- `performance` (JSON): Optional performance metrics
- `error` (JSON): Optional error information
- `userId` (ID): Optional user ID associated with the log
- `requestId` (String): Optional request ID, max 100 characters
- `timestamp` (DateTime): Optional timestamp, defaults to current time

### CreateLogsBatchInput

Input for creating multiple log entries in batch.

```graphql
input CreateLogsBatchInput {
  logs: [CreateLogInput!]!
}
```

**Fields:**
- `logs` ([CreateLogInput!]!): Array of log entries, min 1, max 100 items

### UpdateLogInput

Input for updating a log entry.

```graphql
input UpdateLogInput {
  logId: ID!
  message: String
  context: JSON
}
```

**Fields:**
- `logId` (ID!): Log entry ID to update
- `message` (String): Optional new message text
- `context` (JSON): Optional updated context object
- At least one of `message` or `context` must be provided

### DeleteLogInput

Input for deleting a single log entry.

```graphql
input DeleteLogInput {
  logId: ID!
}
```

**Fields:**
- `logId` (ID!): Log entry ID to delete

### DeleteLogsBulkInput

Input for bulk deleting logs by filters.

```graphql
input DeleteLogsBulkInput {
  level: String
  logger: String
  userId: ID
  requestId: String
  startTime: DateTime
  endTime: DateTime
}
```

**Fields:**
- `level` (String): Optional filter by log level
- `logger` (String): Optional filter by logger name, max 200 characters
- `userId` (ID): Optional filter by user ID
- `requestId` (String): Optional filter by request ID, max 100 characters
- `startTime` (DateTime): Optional start time for time range filter
- `endTime` (DateTime): Optional end time for time range filter
- At least one filter must be provided

## Response Types

### DeleteLogsBulkResponse

Response for bulk log deletion.

```graphql
type DeleteLogsBulkResponse {
  deletedCount: Int!
}
```

**Fields:**
- `deletedCount` (Int!): Number of log entries deleted

## Error Handling

The Admin module implements comprehensive error handling with input validation, database error handling, role-based access control, and external service error handling.

### Error Types

The Admin module may raise the following errors:

- **ForbiddenError** (403): Insufficient permissions
  - Code: `FORBIDDEN`
  - Extensions: `requiredRole: "Admin"` or `requiredRole: "SuperAdmin"`
  - Occurs when: User lacks Admin or SuperAdmin role required for the operation
- **NotFoundError** (404): User not found
  - Code: `NOT_FOUND`
  - Extensions: `resourceType: "User"`, `identifier: <user_uuid>`
  - Occurs when: Requested user UUID does not exist
- **BadRequestError** (400): Invalid input data
  - Code: `BAD_REQUEST`
  - Occurs when: Invalid role value, negative credits, attempting to delete own account, or invalid request format
- **ValidationError** (422): Input validation failed
  - Code: `VALIDATION_ERROR`
  - Extensions: `fieldErrors` (field-specific errors)
  - Occurs when: Invalid UUID format, invalid role name, invalid credit value, or missing required fields
- **ServiceUnavailableError** (503): Database or Lambda Logs service unavailable
  - Code: `SERVICE_UNAVAILABLE`
  - Extensions: `serviceName: "database"` or `serviceName: "lambda_logs"`
  - Occurs when: Database connection fails or Lambda Logs API is unavailable

### Error Response Examples

**Example: Forbidden Error**

```json
{
  "errors": [
    {
      "message": "You do not have permission to perform this action",
      "extensions": {
        "code": "FORBIDDEN",
        "statusCode": 403,
        "requiredRole": "SuperAdmin"
      }
    }
  ]
}
```

**Example: Validation Error**

```json
{
  "errors": [
    {
      "message": "Invalid role value",
      "extensions": {
        "code": "VALIDATION_ERROR",
        "statusCode": 422,
        "fieldErrors": {
          "role": ["Role must be one of: FreeUser, ProUser, Admin, SuperAdmin"],
          "credits": ["Credits must be a non-negative integer"]
        }
      }
    }
  ]
}
```

**Example: Bad Request Error**

```json
{
  "errors": [
    {
      "message": "Cannot delete your own account",
      "extensions": {
        "code": "BAD_REQUEST",
        "statusCode": 400
      }
    }
  ]
}
```

**Example: User Not Found**

```json
{
  "errors": [
    {
      "message": "User with identifier '123e4567-e89b-12d3-a456-426614174000' not found",
      "extensions": {
        "code": "NOT_FOUND",
        "statusCode": 404,
        "resourceType": "User",
        "identifier": "123e4567-e89b-12d3-a456-426614174000"
      }
    }
  ]
}
```

### Error Handling Patterns

- **Input Validation**: UUIDs, roles, credits, and filter parameters are validated before processing
- **Role-Based Access**: All operations check for Admin or SuperAdmin role before execution
- **Database Errors**: All database operations include transaction rollback on failure
- **External Service Errors**: Lambda Logs API errors are caught and converted to appropriate GraphQL errors
- **Self-Protection**: Prevents users from deleting their own accounts or modifying their own roles
- **Error Logging**: Comprehensive error logging with context for debugging

## Usage Examples

### User Management

```graphql
# List all users (SuperAdmin)
query ListUsers {
  admin {
    users(filters: { limit: 50, offset: 0 }) {
      items {
        uuid
        email
        name
        profile {
          role
          credits
        }
      }
      pageInfo {
        total
      }
    }
  }
}

# Get user statistics (Admin/SuperAdmin)
query GetStats {
  admin {
    userStats {
      totalUsers
      activeUsers
      usersByRole
      usersByPlan
    }
  }
}

# Update user role (SuperAdmin)
mutation UpdateRole {
  admin {
    updateUserRole(input: {
      userId: "123e4567-e89b-12d3-a456-426614174000"
      role: "Admin"
    }) {
      uuid
      profile {
        role
      }
    }
  }
}

# Update user credits (SuperAdmin)
mutation UpdateCredits {
  admin {
    updateUserCredits(input: {
      userId: "123e4567-e89b-12d3-a456-426614174000"
      credits: 5000
    }) {
      uuid
      profile {
        credits
      }
    }
  }
}
```

### Log Management (SuperAdmin)

```graphql
# Query logs
query GetLogs {
  admin {
    logs(filters: {
      level: "ERROR"
      limit: 100
    }) {
      items {
        id
        timestamp
        level
        message
        context
      }
      pageInfo {
        total
      }
    }
  }
}

# Search logs
query SearchLogs {
  admin {
    searchLogs(input: {
      query: "user login failed"
      limit: 50
    }) {
      items {
        id
        timestamp
        message
      }
      query
    }
  }
}

# Get log statistics
query GetLogStats {
  admin {
    logStatistics(timeRange: "24h") {
      totalLogs
      byLevel
      errorRate
      topErrors {
        type
        count
        message
      }
    }
  }
}

# Create a log entry
mutation CreateLog {
  admin {
    createLog(input: {
      level: "ERROR"
      logger: "app.services.email"
      message: "Failed to send email"
      context: {
        email: "user@example.com"
      }
    }) {
      id
      timestamp
      level
      message
    }
  }
}

# Create multiple log entries
mutation CreateLogsBatch {
  admin {
    createLogsBatch(input: {
      logs: [
        {
          level: "INFO"
          logger: "app.services.user"
          message: "User logged in"
        },
        {
          level: "WARNING"
          logger: "app.services.email"
          message: "Email queue is full"
        }
      ]
    }) {
      id
      level
      message
    }
  }
}

# Update a log entry
mutation UpdateLog {
  admin {
    updateLog(input: {
      logId: "507f1f77bcf86cd799439011"
      message: "Updated error message"
      context: {
        additionalInfo: "More details"
      }
    }) {
      id
      message
    }
  }
}

# Delete a log entry
mutation DeleteLog {
  admin {
    deleteLog(input: {
      logId: "507f1f77bcf86cd799439011"
    })
  }
}

# Bulk delete logs
mutation DeleteLogsBulk {
  admin {
    deleteLogsBulk(input: {
      level: "DEBUG"
      startTime: "2024-01-01T00:00:00Z"
      endTime: "2024-01-31T23:59:59Z"
    }) {
      deletedCount
    }
  }
}
```

## Logging System Architecture

The application uses a centralized logging system that sends all logs to the Lambda Logs API, which stores them in MongoDB. Console logging is disabled by default in production.

### Architecture Overview

```
Application Code
    ↓ logger.info/error/warning()
    ↓
Python logging.Logger
    ↓
MongoDBLogHandler (Background Thread)
    ↓
In-Memory Queue (Thread-safe, bounded)
    ↓
Batch Collection (100 logs or 5 seconds)
    ↓
Retry Logic (3 attempts, exponential backoff)
    ↓
Lambda Logs API → MongoDB Storage
```

### Key Features

1. **Lambda-Only Logging**: All logs are sent to Lambda Logs API via background thread
   - No console output in production (configurable via `LOG_TO_CONSOLE`)
   - No file logging by default (optional via `ENABLE_FILE_LOGGING`)

2. **Batched Processing**: Logs are collected and sent in batches
   - Batch size: 100 logs (configurable via `LOG_BATCH_SIZE`)
   - Flush interval: 5 seconds (configurable via `LOG_FLUSH_INTERVAL`)
   - Reduces API calls and improves performance

3. **Resilience Mechanisms**:
   - **Retry Logic**: Automatic retries with exponential backoff (1s, 2s, 4s)
   - **Fallback Buffer**: Failed logs are stored in memory queue + file (`logs/failed_logs.jsonl`)
   - **Background Retry**: Periodic retry of failed logs (every 60 seconds)
   - **Health Checks**: Optional API health verification before sending

4. **Metrics & Monitoring**:
   - Success/failure counts
   - Queue and fallback buffer sizes
   - API call statistics
   - Error type breakdown
   - Success rates
   - Available via `/health/logging` REST endpoint

### Configuration

All logging configuration is done via environment variables:

```bash
# Logging Configuration
LOG_LEVEL=INFO                    # Log level (DEBUG, INFO, WARNING, ERROR)
LOG_FORMAT=json                   # Format: json or text
LOG_TO_CONSOLE=false              # Disable console logging (default)
ENABLE_FILE_LOGGING=false         # Disable file logging (default)

# Lambda Logs API
ENABLE_LAMBDA_LOGGING=true        # Enable Lambda logging (default: true)
LOG_BATCH_SIZE=100                # Batch size for log sending
LOG_FLUSH_INTERVAL=5.0            # Flush interval in seconds

# Resilience
LOG_FALLBACK_ENABLED=true         # Enable fallback buffer (default: true)
LOG_FALLBACK_FILE=logs/failed_logs.jsonl  # Fallback file path
LOG_RETRY_ATTEMPTS=3              # Number of retry attempts
LOG_RETRY_BACKOFF_BASE=1.0        # Base backoff time in seconds

# Queue Management
LOG_QUEUE_MAX_SIZE=10000          # Maximum queue size

# Health Checks
LOG_HEALTH_CHECK_ENABLED=false    # Enable health checks (default: false)
```

### Log Storage

- **Primary Storage**: MongoDB via Lambda Logs API
- **Fallback Storage**: Local file (`logs/failed_logs.jsonl`) for failed logs
- **Retention**: Configurable via `LOG_TTL_DAYS` (default: 90 days)

### Monitoring

The logging system health can be monitored via:

1. **REST Endpoint**: `GET /health/logging`
   - Returns health status and comprehensive metrics
   - No authentication required
   - See [Health Module](08_HEALTH_MODULE.md) for details

2. **GraphQL Queries**:
   - `admin.logs` - Query logs with filters
   - `admin.searchLogs` - Full-text search logs
   - `admin.logStatistics` - Get aggregated statistics

### Error Handling

- **Silent Error Handler**: Prevents recursion when logging handler itself fails
- **Graceful Degradation**: Application continues operating even when API is unavailable
- **No Log Loss**: Failed logs are preserved in fallback buffer for retry

## Implementation Details

### Role-Based Access Control

- **Role Requirements**: Operations have different role requirements
  - SuperAdmin only: `users`, `userHistory`, `logs`, `searchLogs`, `logStatistics`, `updateUserRole`, `updateUserCredits`, `deleteUser`, `promoteToSuperAdmin`
  - Admin or SuperAdmin: `userStats`
  - Self-promotion allowed: `promoteToAdmin` (any authenticated user can promote themselves)
- **Role Checking**: Uses `UserProfileRepository` to retrieve user role
  - `require_super_admin`: Helper function to check SuperAdmin role
  - `require_admin_or_super_admin`: Helper function to check Admin or SuperAdmin role
  - Raises ForbiddenError if role requirement is not met
- **User Isolation**: Regular users cannot access admin operations
  - All admin queries and mutations require authentication
  - Role checks are performed before any operation

### Repository Integration

- **UserRepository**: Handles user data operations
  - `list_all_users`: Lists all users with pagination
  - `get_by_uuid`: Retrieves user by UUID
  - `delete_user`: Deletes user (cascade deletes profile)
- **UserProfileRepository**: Handles user profile operations
  - `get_by_user_id`: Retrieves user profile by user ID
  - Used for role checking and profile updates
- **LogStatsRepository**: Handles log statistics
  - `get_statistics`: Retrieves aggregated log statistics for time range
- **UserService**: Handles user management operations
  - `get_user_history`: Retrieves user history records
  - `promote_user_to_admin`: Promotes user to Admin role
  - `promote_user_to_super_admin`: Promotes user to SuperAdmin role

### Lambda Logs Client Integration

- **LambdaLogsClient**: All log operations are handled via `LambdaLogsClient`
  - `query_logs`: Queries logs with filters and pagination
  - `search_logs`: Performs full-text search on log messages
  - Logs are stored in MongoDB and retrieved via Lambda Logs API
- **Log Filtering**: Supports multiple filter options
  - `level`: Filter by log level
  - `logger`: Filter by logger name (max 200 characters)
  - `user_id`: Filter by user UUID
  - `request_id`: Filter by request ID (max 100 characters)
  - `start_time`: Filter by start time (DateTime)
  - `end_time`: Filter by end time (DateTime)
- **Log Search**: Full-text search on log messages
  - Query string: min 1 character, max 500 characters
  - Returns search results with pagination
  - Includes search query in response for reference

### Statistics Aggregation

- **Log Statistics**: Aggregated statistics from log data
  - `timeRange`: Supported ranges: "1h", "24h", "7d", "30d"
  - `total_logs`: Total number of logs in time range
  - `by_level`: Logs grouped by level (JSON)
  - `error_rate`: Percentage of error logs
  - `avg_response_time_ms`: Average response time in milliseconds
  - `slow_queries_count`: Number of slow queries
  - `top_errors`: Top error patterns with counts and messages
  - `performance_trends`: Performance trend data points
  - `user_activity`: User activity statistics (active users, requests per user, top users)
  - `by_logger`: Logs grouped by logger (JSON, optional)
- **Empty Statistics**: Returns empty statistics if no data is available
  - All counts set to 0
  - Empty arrays for top_errors and performance_trends
  - Default UserActivity with zero values

### User History

- **User History Tracking**: Tracks registration and login events
  - `event_type`: Type of event (e.g., "register", "login")
  - `user_id`: Optional filter by user UUID
  - Includes geolocation data: IP, continent, country, city, region, timezone, ISP, etc.
  - Includes device information
  - Pagination support for large history sets
- **Geolocation Data**: Comprehensive geolocation information
  - IP address, continent, country, region, city, district, zip
  - Latitude, longitude, timezone, currency
  - ISP, organization, proxy, hosting information

### Validation

- **Input Validation**: All inputs are validated before processing
  - UUID validation via `validate_uuid` utility (user_id fields)
  - String length validation via `validate_string_length` utility (logger max 200, request_id max 100, query max 500)
  - Pagination validation via `validate_pagination` utility (limit, offset)
  - Role validation (must be in VALID_ROLES)
  - Credits validation (non-negative integer, max 1,000,000,000)
  - Time range validation (must be one of: "1h", "24h", "7d", "30d")
- **Self-Deletion Prevention**: Users cannot delete their own account
  - Validates that target_user_id != current_user.uuid
  - Raises BadRequestError if attempting self-deletion

### Error Handling

- **Input Validation**: All inputs are validated before processing
  - UUID format validation (user_id)
  - String length validation (logger, request_id, query)
  - Pagination validation (limit, offset)
  - Role validation (must be in VALID_ROLES)
  - Credits validation (non-negative, max 1B)
  - Time range validation (must be valid range)
- **Database Error Handling**: Database errors are handled centrally via `handle_database_exception`
  - UserRepository errors are caught and converted to appropriate GraphQL errors
  - UserProfileRepository errors are caught and converted to appropriate GraphQL errors
  - Transaction rollback on failure
  - Transaction commit after successful operations
- **External Service Error Handling**: LambdaLogsClient errors are handled centrally
  - Errors are caught and logged
  - Converted to appropriate GraphQL errors
- **Response Validation**: Service responses are validated before conversion
  - Checks for required structure (dict, list)
  - Validates response format matches expected structure
  - Conversion errors are caught and logged
- **Role-Based Access Control**: Operations require specific roles
  - Role check performed before any operation
  - Raises ForbiddenError if user lacks required role
- **Not Found Handling**: Raises NotFoundError for missing resources
  - User not found
  - UserProfile not found
  - Returns empty statistics if no log data available

### Database Operations

- **Transaction Management**: All database operations use transactions
  - Transaction rollback on failure
  - Transaction commit after successful operations
  - Refresh objects after commit to get updated data
- **Cascade Deletion**: User deletion cascades to profile
  - Deleting a user automatically deletes their profile
  - Handled by database foreign key constraints
- **SQLAlchemy Queries**: Direct SQLAlchemy queries for statistics
  - Uses `func.count` for counting
  - Uses `func.coalesce` to handle NULL values
  - Uses GROUP BY for aggregation
  - Outer joins to include users without profiles

### Pagination

- **Pagination Support**: All list queries support pagination
  - `limit`: Maximum number of items to return
  - `offset`: Number of items to skip
  - Pagination is normalized for backward compatibility
  - Total count is included in response
- **Pagination Validation**: Pagination parameters are validated
  - Uses `validate_pagination` utility
  - Normalizes limit and offset values

## Task breakdown (for maintainers)

1. **Role checks:** Every admin query/mutation must verify Admin or SuperAdmin via profile.role; document which operations require SuperAdmin (e.g. deleteUser, promoteToSuperAdmin).
2. **users/userStats/userHistory:** UserRepository and UserHistoryRepository; user isolation only for non-admin; admin sees all; validate_pagination for list.
3. **Logs (logStatistics, logs, searchLogs):** Lambda Logs API client; map GraphQL filters to Lambda API params; handle empty/error responses; document LogStatisticsInput and SearchLogsInput.
4. **updateUserRole/updateUserCredits/deleteUser:** Validate target user exists; credits/role update on user_profiles; deleteUser cascades (see SCHEMA_ANALYSIS); confirm transaction rollback on failure.
5. **createLog/createLogsBatch/updateLog/deleteLog/deleteLogsBulk:** Lambda Logs API write operations; validate input (level, logger, message, userId, etc.); document DeleteLogsBulkInput (at least one filter required).

## Related Modules

- **Users Module**: Provides user data for admin operations
- **Health Module**: Provides system health and performance stats
- **AI Chats Module** ([17_AI_CHATS_MODULE.md](17_AI_CHATS_MODULE.md)): Contact AI observability is via that service’s logs/health; not all AI errors surface in Admin log queries unless forwarded

## Documentation metadata

- Era: `7.x`
- Introduced in: `TBD` (fill with exact minor)
- Frontend bindings: list page files from `docs/frontend/pages/*.json`
- Data stores touched: PostgreSQL/Elasticsearch/MongoDB/S3 as applicable

## Endpoint/version binding checklist

- Add operation list with `introduced_in` / `deprecated_in` tags.
- Map each operation to frontend page bindings and hook/service usage.
- Record DB tables read/write for each operation.

