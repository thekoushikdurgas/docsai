# Activities Module

## Overview

The Activities module provides comprehensive user activity tracking and statistics across all application modules. It allows users to view their activity history, filter activities by service type and action type, and get activity statistics. Activities are automatically logged for all user operations across Jobs, Imports, Contacts, Companies, Email, AI Chats, LinkedIn, and Sales Navigator modules.
**Location:** `app/graphql/modules/activities/`

GraphQL paths: `query { activities { activities(filters: { ... }) { ... } activityStats(filters: { ... }) { ... } } }`.

## Queries – parameters and variable types

| Query | Parameter(s) | Variable type (GraphQL) | Return type |
|-------|---------------|-------------------------|-------------|
| `activities` | `filters` | `ActivityFilterInput` (optional; `serviceType`, `actionType`, `status`, `startDate`, `endDate`, `limit`, `offset`) | `ActivityConnection` |
| `activityStats` | `filters` | `ActivityStatsInput` (optional; `startDate`, `endDate` only) | `ActivityStats` |

No mutations (activities are logged by other modules). Use camelCase in variables (e.g. `serviceType`, `startDate`). `ActivityStatsInput`: optional date range; `startDate` must be before `endDate` when both set. List pagination: `limit` 1–1000, `offset` ≥ 0 (enforced on `ActivityFilterInput`).

## Types

### Activity

User activity information.

```graphql
type Activity {
  id: Int!
  userId: ID!
  serviceType: String!
  actionType: String!
  status: String!
  requestParams: JSON
  resultCount: Int!
  resultSummary: JSON
  errorMessage: String
  ipAddress: String
  userAgent: String
  createdAt: DateTime!
}
```

**Fields:**
- `id` (Int!): Activity ID
- `userId` (ID!): User who performed the activity
- `serviceType` (String!): Service type (see Service Types below)
- `actionType` (String!): Action type (see Action Types below)
- `status` (String!): Activity status (success, failed, partial)
- `requestParams` (JSON): Request parameters
- `resultCount` (Int!): Number of results
- `resultSummary` (JSON): Summary of results
- `errorMessage` (String): Error message if failed
- `ipAddress` (String): IP address of request
- `userAgent` (String): User agent string
- `createdAt` (DateTime!): Activity timestamp

**Service Types:**
- `contacts` - Contact management operations
- `companies` - Company management operations
- `email` - Email finder and verification operations
- `ai_chats` - AI chat and Contact AI (Hugging Face–backed) operations
- `linkedin` - LinkedIn URL search and export operations
- `sales_navigator` - Sales Navigator scraping operations

**Action Types:**
- `create` - Create operations (e.g., create contact, create job)
- `update` - Update operations (e.g., update contact, update company)
- `delete` - Delete operations (e.g., delete chat, delete contact)
- `query` - Query/read operations (e.g., list contacts, get company)
- `search` - Search operations (e.g., email search, LinkedIn search)
- `export` - Export operations (e.g., export contacts, export emails)
- `import` - Import operations (e.g., CSV import)
- `send` - Send operations (e.g., send message in chat)
- `verify` - Verification operations (e.g., email verification)
- `analyze` - Analysis operations (e.g., email risk analysis)
- `generate` - Generation operations (e.g., company summary generation)
- `parse` - Parsing operations (e.g., parse contact filters)
- `scrape` - Scraping operations (e.g., Sales Navigator scraping)

**Status Values:**
- `success` - Operation completed successfully
- `failed` - Operation failed
- `partial` - Operation completed partially

### ActivityConnection

Paginated connection of activities.

```graphql
type ActivityConnection {
  items: [Activity!]!
  total: Int!
  limit: Int!
  offset: Int!
  hasNext: Boolean!
  hasPrevious: Boolean!
}
```

### ActivityStats

Activity statistics.

```graphql
type ActivityStats {
  totalActivities: Int!
  byServiceType: JSON!
  byActionType: JSON!
  byStatus: JSON!
  recentActivities: Int!
}
```

**Fields:**
- `totalActivities` (Int!): Total number of activities
- `byServiceType` (JSON!): Count grouped by service type
- `byActionType` (JSON!): Count grouped by action type
- `byStatus` (JSON!): Count grouped by status
- `recentActivities` (Int!): Number of activities in last 24 hours

## Queries

### activities

Get user's activity history with optional filtering and pagination.

**Parameters:**

| Name    | Type                  | Required | Description                                      |
|---------|-----------------------|----------|--------------------------------------------------|
| filters | ActivityFilterInput   | No       | Optional: serviceType, actionType, status, date range, limit, offset |

```graphql
query GetActivities($filters: ActivityFilterInput) {
  activities {
    activities(filters: $filters) {
      items {
        id
        serviceType
        actionType
        status
        resultCount
        createdAt
      }
      total
      limit
      offset
      hasNext
      hasPrevious
    }
  }
}
```

**Variables:**
```json
{
  "filters": {
    "serviceType": "ai_chats",
    "actionType": "create",
    "status": "success",
    "startDate": "2024-01-01T00:00:00Z",
    "endDate": "2024-01-31T23:59:59Z",
    "limit": 50,
    "offset": 0
  }
}
```

**Arguments:**
- `filters` (ActivityFilterInput): Optional filter criteria

**Returns:** `ActivityConnection`

**Authentication:** Required

**Validation:**
- Pagination is validated via `validate_pagination` utility (limit, offset)
- `serviceType`: Optional, must be valid ActivityServiceType enum value if provided
- `actionType`: Optional, must be valid ActivityActionType enum value if provided
- `status`: Optional, must be valid ActivityStatus enum value if provided
- `startDate` and `endDate`: Optional, if both provided, startDate must be before endDate
- Filter input validation via `filters.validate()` method

**Implementation Details:**
- Uses `UserActivityRepository.list_activities` to retrieve user's activities
- User isolation enforced - users can only view their own activities
- Enum values are validated with improved error messages (lists valid options)
- Date range filtering supported (startDate, endDate)
- Response structure is validated before conversion to GraphQL types
- Individual activity conversion errors are logged and raise BadRequestError
- Total count validation (must be non-negative integer)

**Example Response:**
```json
{
  "data": {
    "activities": {
      "activities": {
        "items": [
          {
            "id": 1,
            "serviceType": "ai_chats",
            "actionType": "create",
            "status": "success",
            "resultCount": 1,
            "createdAt": "2024-01-15T10:30:00Z"
          },
          {
            "id": 2,
            "serviceType": "contacts",
            "actionType": "query",
            "status": "success",
            "resultCount": 25,
            "createdAt": "2024-01-15T10:25:00Z"
          }
        ],
        "total": 1,
        "limit": 50,
        "offset": 0,
        "hasNext": false,
        "hasPrevious": false
      }
    }
  }
}
```

### activityStats

Get activity statistics for the current user.

**Parameters:**

| Name    | Type                 | Required | Description                    |
|---------|----------------------|----------|--------------------------------|
| filters | ActivityStatsInput   | No       | Optional date range (startDate, endDate) |

```graphql
query GetActivityStats($filters: ActivityStatsInput) {
  activities {
    activityStats(filters: $filters) {
      totalActivities
      byServiceType
      byActionType
      byStatus
      recentActivities
    }
  }
}
```

**Variables:**
```json
{
  "filters": {
    "startDate": "2024-01-01T00:00:00Z",
    "endDate": "2024-01-31T23:59:59Z"
  }
}
```

**Arguments:**
- `filters` (ActivityStatsInput): Optional date range filter

**Returns:** `ActivityStats`

**Authentication:** Required

**Validation:**
- `startDate` and `endDate`: Optional, if both provided, startDate must be before endDate
- Filter input validation via `filters.validate()` method

**Implementation Details:**
- Uses `UserActivityRepository.list_activities_for_stats` to retrieve all activities for stats
- User isolation enforced - users can only view their own statistics
- Statistics are calculated from all activities matching the date range filter
- Groups activities by service type, action type, and status
- Recent activities are defined as activities in the last 24 hours (UTC timezone)
- Timezone handling: Converts naive datetimes to UTC, handles timezone-aware datetimes
- Null safety: Skips activities with missing service_type, action_type, or status (logs warning)
- Response structure is validated before conversion to GraphQL types
- Recent count validation (must be non-negative, defaults to 0 if invalid)

**Example Response:**
```json
{
  "data": {
    "activities": {
      "activityStats": {
        "totalActivities": 150,
        "byServiceType": {
          "jobs": 20,
          "imports": 15,
          "contacts": 45,
          "companies": 30,
          "email": 25,
          "ai_chats": 35,
          "linkedin": 40,
          "sales_navigator": 10
        },
        "byActionType": {
          "create": 50,
          "update": 30,
          "delete": 5,
          "query": 80,
          "search": 45,
          "export": 25,
          "import": 15,
          "send": 20,
          "verify": 15,
          "analyze": 10,
          "generate": 8,
          "parse": 12,
          "scrape": 5
        },
        "byStatus": {
          "success": 140,
          "failed": 10
        },
        "recentActivities": 5
      }
    }
  }
}
```

## Input Types

### ActivityFilterInput

Input for filtering activities.

```graphql
input ActivityFilterInput {
  serviceType: String
  actionType: String
  status: String
  startDate: DateTime
  endDate: DateTime
  limit: Int
  offset: Int
}
```

**Fields:**
- `serviceType` (String): Filter by service type (jobs, imports, contacts, companies, email, ai_chats, linkedin, sales_navigator)
- `actionType` (String): Filter by action type (create, update, delete, query, search, export, import, send, verify, analyze, generate, parse, scrape)
- `status` (String): Filter by status (success, failed, partial)
- `startDate` (DateTime): Filter activities from this date
- `endDate` (DateTime): Filter activities until this date
- `limit` (Int): Maximum number of activities (default: 100, max: 1000)
- `offset` (Int): Number of activities to skip (default: 0)

**Validation:**
- `serviceType` must be one of: jobs, imports, contacts, companies, email, ai_chats, linkedin, sales_navigator
- `actionType` must be one of: create, update, delete, query, search, export, import, send, verify, analyze, generate, parse, scrape
- `status` must be one of: success, failed, partial
- Limit must be greater than 0 and not exceed 1000
- Offset cannot be negative
- If both startDate and endDate are provided, startDate must be before endDate

### ActivityStatsInput

Input for filtering activity statistics.

```graphql
input ActivityStatsInput {
  startDate: DateTime
  endDate: DateTime
}
```

**Fields:**
- `startDate` (DateTime): Calculate stats from this date
- `endDate` (DateTime): Calculate stats until this date

**Validation:**
- If both dates are provided, startDate must be before endDate

## Error Handling

The Activities module implements comprehensive error handling with input validation, database error handling, and response validation.

### Error Types

The Activities module may raise the following errors:

- **ValidationError** (422): Input validation failed
  - Code: `VALIDATION_ERROR`
  - Extensions: `fieldErrors` (field-specific errors)
  - Occurs when: Invalid date range (startDate after endDate), invalid enum values (serviceType, actionType, status), invalid limit (must be 1-1000), or invalid offset (must be non-negative)
- **ForbiddenError** (403): Insufficient permissions
  - Code: `FORBIDDEN`
  - Extensions: `requiredRole: <role>` (if applicable)
  - Occurs when: User lacks required permissions for the operation
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
      "message": "Invalid date range",
      "extensions": {
        "code": "VALIDATION_ERROR",
        "statusCode": 422,
        "fieldErrors": {
          "startDate": ["Start date must be before end date"],
          "serviceType": ["Service type must be one of: jobs, imports, contacts, companies, email, ai_chats, linkedin, sales_navigator"],
          "limit": ["Limit must be between 1 and 1000"]
        }
      }
    }
  ]
}
```

**Example: Forbidden Error**
```json
{
  "errors": [
    {
      "message": "You do not have permission to perform this action",
      "extensions": {
        "code": "FORBIDDEN",
        "statusCode": 403
      }
    }
  ]
}
```

### Error Handling Patterns

- **Input Validation**: Date ranges, enum values, pagination parameters, and filter values are validated before processing
- **Database Errors**: All database operations include transaction rollback on failure
- **User Isolation**: Users can only access their own activities
- **Enum Validation**: Service types, action types, and status values are validated against allowed values
- **Date Range Validation**: Start and end dates are validated to ensure startDate is before endDate
- **Error Logging**: Comprehensive error logging with context for debugging

## Usage Examples

### Complete Activity Tracking Flow

```graphql
# 1. Get recent activities
query GetRecentActivities {
  activities {
    activities(filters: {
      limit: 20
      offset: 0
    }) {
      items {
        id
        serviceType
        actionType
        status
        resultCount
        createdAt
      }
      total
    }
  }
}

# 2. Filter by service type
query GetAIChatsActivities {
  activities {
    activities(filters: {
      serviceType: "ai_chats"
      limit: 50
    }) {
      items {
        id
        actionType
        status
        resultCount
        createdAt
      }
    }
  }
}

# 3. Filter by multiple criteria
query GetContactsCreateActivities {
  activities {
    activities(filters: {
      serviceType: "contacts"
      actionType: "create"
      status: "success"
      limit: 50
    }) {
      items {
        id
        status
        resultCount
        createdAt
      }
    }
  }
}

# 4. Filter by date range
query GetActivitiesByDate {
  activities {
    activities(filters: {
      startDate: "2024-01-01T00:00:00Z"
      endDate: "2024-01-31T23:59:59Z"
      limit: 100
    }) {
      items {
        id
        serviceType
        actionType
        createdAt
      }
      total
    }
  }
}

# 5. Get activity statistics
query GetStats {
  activities {
    activityStats {
      totalActivities
      byServiceType
      byActionType
      byStatus
      recentActivities
    }
  }
}

# 6. Get statistics for date range
query GetStatsForPeriod {
  activities {
    activityStats(filters: {
      startDate: "2024-01-01T00:00:00Z"
      endDate: "2024-01-31T23:59:59Z"
    }) {
      totalActivities
      byServiceType
      byActionType
      byStatus
    }
  }
}
```

## Implementation Details

### UserActivityRepository Integration

- **UserActivityRepository**: Handles activity data operations
  - `list_activities`: Lists activities for a user with filters and pagination
  - `list_activities_for_stats`: Lists all activities for statistics calculation
  - User isolation enforced at repository level
  - Supports filtering by service_type, action_type, status, and date range
- **User Isolation**: Users can only access their own activities
  - All queries filter by user_id
  - Statistics are calculated only for user's own activities
  - Prevents unauthorized access to other users' activities

### ActivityService Integration

- **ActivityService**: Centralized activity logging service (`app/services/activity_service.py`)
  - Automatically logs activities for all operations across all modules
  - Non-blocking pattern: Activity logging failures don't prevent primary operations
  - Logs service type, action type, status, request params, result count, error messages
  - Includes IP address and user agent for request tracking

### Validation

- **Input Validation**: All inputs are validated before processing
  - Filter input validation via `filters.validate()` method
  - Pagination validation via `validate_pagination` utility (limit, offset)
  - Enum validation for service_type, action_type, and status (with improved error messages)
  - Date range validation (startDate must be before endDate if both provided)
- **Enum Validation**: Enum values are validated with improved error messages
  - Lists valid options when invalid value is provided
  - Service type: 8 valid values (jobs, imports, contacts, companies, email, ai_chats, linkedin, sales_navigator)
  - Action type: 13 valid values (create, update, delete, query, search, export, import, send, verify, analyze, generate, parse, scrape)
  - Status: 3 valid values (success, failed, partial)
- **Response Validation**: Service responses are validated before conversion
  - Checks for required structure (activities must be list, total must be non-negative integer)
  - Individual activity conversion errors are logged and raise BadRequestError
  - Recent count validation (must be non-negative, defaults to 0 if invalid)

### Error Handling

- **Input Validation**: All inputs are validated before processing
  - Filter input validation via `filters.validate()` method
  - Enum validation with improved error messages
  - Date range validation
  - Pagination validation
- **Database Error Handling**: Database errors are handled centrally via `handle_database_exception`
  - UserActivityRepository errors are caught and converted to appropriate GraphQL errors
  - Transaction rollback on failure
  - Context information included in error handling
- **Response Validation**: Service responses are validated before conversion
  - Checks for required structure
  - Validates total count (non-negative integer)
  - Individual activity conversion errors are logged and raise BadRequestError
- **Statistics Calculation Errors**: Statistics calculation errors are handled gracefully
  - Null safety: Skips activities with missing attributes (logs warning)
  - Timezone handling errors are logged and skipped
  - Recent count validation (defaults to 0 if invalid)

### Pagination

- **Pagination Support**: List queries support pagination
  - `limit`: Maximum number of items to return (default: 100, max: 1000)
  - `offset`: Number of items to skip (default: 0)
  - Total count is included in response
- **Pagination Validation**: Pagination parameters are validated
  - Uses `validate_pagination` utility
  - Validates limit (must be 1-1000) and offset (must be non-negative)

### Date Filtering

- **Date Range Filtering**: Activities can be filtered by date range
  - `startDate`: Filter activities from this date
  - `endDate`: Filter activities until this date
  - Both dates are optional
  - If both provided, startDate must be before endDate
- **Timezone Handling**: Timezone-aware date handling
  - Recent activities cutoff uses UTC timezone
  - Converts naive datetimes to UTC
  - Handles timezone-aware datetimes (converts to UTC)
  - Timezone conversion errors are logged and skipped

### Statistics Calculation

- **Statistics Aggregation**: Statistics are calculated from all activities matching the filters
  - Groups activities by service type
  - Groups activities by action type
  - Groups activities by status
  - Counts recent activities (last 24 hours)
- **Recent Activities**: Recent activities are defined as activities in the last 24 hours
  - Calculated using UTC timezone
  - Handles timezone-aware and naive datetimes
  - Timezone conversion errors are logged and skipped
- **Null Safety**: Statistics calculation handles missing attributes gracefully
  - Skips activities with missing service_type (logs warning)
  - Skips activities with missing action_type (logs warning)
  - Skips activities with missing status (logs warning)
  - Continues processing other activities if one fails

### Service Types and Action Types

- **Service Types**: 8 service types supported
  - `jobs`: Background job operations
  - `imports`: CSV import operations
  - `contacts`: Contact management operations
  - `companies`: Company management operations
  - `email`: Email finder and verification operations
  - `ai_chats`: AI chat and Contact AI operations
  - `linkedin`: LinkedIn URL search and export operations
  - `sales_navigator`: Sales Navigator scraping operations
- **Action Types**: 13 action types supported
  - `create`: Create operations (e.g., create contact, create job)
  - `update`: Update operations (e.g., update contact, update company)
  - `delete`: Delete operations (e.g., delete chat, delete contact)
  - `query`: Query/read operations (e.g., list contacts, get company)
  - `search`: Search operations (e.g., email search, LinkedIn search)
  - `export`: Export operations (e.g., export contacts, export emails)
  - `import`: Import operations (e.g., CSV import)
  - `send`: Send operations (e.g., send message in chat)
  - `verify`: Verification operations (e.g., email verification)
  - `analyze`: Analysis operations (e.g., email risk analysis)
  - `generate`: Generation operations (e.g., company summary generation)
  - `parse`: Parsing operations (e.g., parse contact filters)
  - `scrape`: Scraping operations (e.g., Sales Navigator scraping)

### Status Values

- **Status Values**: 3 status values supported
  - `success`: Operation completed successfully
  - `failed`: Operation failed
  - `partial`: Operation completed partially

### Error Tracking

- **Error Tracking**: Failed operations are logged with error messages for debugging
  - Error messages stored in `errorMessage` field
  - Includes request parameters and result summary
  - IP address and user agent tracked for debugging

### Metadata Storage

- **Metadata Storage**: Activities include metadata about the operation
  - `requestParams`: JSON object with request parameters
  - `resultSummary`: JSON object with result summary
  - `resultCount`: Number of results
  - `ipAddress`: IP address of request
  - `userAgent`: User agent string
  - Flexible JSON structure for custom data

## Activity Tracking Coverage

All user operations are automatically tracked:

- **Contacts Module**: CREATE, UPDATE, DELETE, QUERY actions
- **Companies Module**: CREATE, UPDATE, DELETE, QUERY actions
- **Email Module**: SEARCH, VERIFY, EXPORT actions
- **AI Chats Module**: CREATE, UPDATE, DELETE, SEND, ANALYZE, GENERATE, PARSE, QUERY actions
- **LinkedIn Module**: SEARCH, EXPORT actions
- **Sales Navigator Module**: SCRAPE, QUERY actions

## Task breakdown (for maintainers)

1. **Trace activities list:** ActivityQuery.activities → repository filtered by user_id; validate_pagination; optional filters (serviceType, actionType, status, startDate, endDate); return ActivityConnection.
2. **activityStats:** ActivityStatsInput (startDate, endDate); aggregate by service/action/status; validate date range (startDate < endDate).
3. **Activity logging:** Confirm ActivityService.log_activity_async / log_activity_safe usage across Jobs, Contacts, Email, AI Chats, LinkedIn, Sales Navigator; non-blocking where documented.
4. **Enums:** Document serviceType and actionType allowed values (contacts, companies, email, ai_chats, linkedin, sales_navigator; create, update, query, export, etc.) and where they are validated.
5. **Admin access:** If admin can view all activities, verify repository method accepts optional user_id override for Admin/SuperAdmin.

## Related Modules

- **Users Module**: Activities are associated with users
- **Admin Module**: Admin can view all user activities
- **All Modules**: All modules automatically log activities via ActivityService

## Documentation metadata

- Era: `6.x`
- Introduced in: `TBD` (fill with exact minor)
- Frontend bindings: list page files from `docs/frontend/pages/*.json`
- Data stores touched: PostgreSQL/Elasticsearch/MongoDB/S3 as applicable

## Endpoint/version binding checklist

- Add operation list with `introduced_in` / `deprecated_in` tags.
- Map each operation to frontend page bindings and hook/service usage.
- Record DB tables read/write for each operation.

