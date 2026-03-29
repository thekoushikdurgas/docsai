# Analytics Module

## Overview

The Analytics module provides performance metrics tracking and aggregation functionality. It allows users to submit performance metrics (such as Core Web Vitals) and query aggregated statistics.
**Location:** `app/graphql/modules/analytics/`

## Queries and mutations – parameters and variable types

| Operation | Parameter(s) | Variable type (GraphQL) | Return type |
|-----------|---------------|-------------------------|-------------|
| **Queries** | | | |
| `performanceMetrics` | `metricName`, `startDate`, `endDate`, `limit`, `offset` | String, DateTime, DateTime, Int, Int | metrics connection |
| `aggregateMetrics` | `input` | AggregateMetricsInput! | MetricAggregation / list |
| **Mutations** | | | |
| `submitPerformanceMetric` | `input` | SubmitPerformanceMetricInput! | result |

Use camelCase in variables. submitPerformanceMetric is non-blocking (failures logged, don't fail response). performance_metrics table.

## Types

### PerformanceMetric

Represents a single performance metric record.

```graphql
type PerformanceMetric {
  id: ID!
  userId: ID!
  metricName: String!
  metricValue: Float!
  timestamp: DateTime!
  metadata: JSON
  createdAt: DateTime!
}
```

**Fields:**
- `id` (ID!): Metric ID
- `userId` (ID!): User who submitted the metric
- `metricName` (String!): Metric name (e.g., "LCP", "FID", "CLS", "TTFB")
- `metricValue` (Float!): Metric value (seconds for LCP, milliseconds for FID, score for CLS)
- `timestamp` (DateTime!): When the metric was measured
- `metadata` (JSON): Additional metadata (URL, user agent, connection type, endpoint, method)
- `createdAt` (DateTime!): When the metric was recorded

### MetricAggregation

Aggregated statistics for a metric.

```graphql
type MetricAggregation {
  avg: Float!
  min: Float!
  max: Float!
  p50: Float!
  p75: Float!
  p95: Float!
  count: Int!
}
```

**Fields:**
- `avg` (Float!): Average value
- `min` (Float!): Minimum value
- `max` (Float!): Maximum value
- `p50` (Float!): 50th percentile (median)
- `p75` (Float!): 75th percentile
- `p95` (Float!): 95th percentile
- `count` (Int!): Number of metrics aggregated

### PerformanceMetricResponse

Response after submitting a performance metric.

```graphql
type PerformanceMetricResponse {
  success: Boolean!
  message: String!
}
```

## Queries

### performanceMetrics

Get performance metrics for the current user.

**Parameters:**

| Name  | Type             | Required | Description                                      |
|-------|------------------|----------|--------------------------------------------------|
| input | GetMetricsInput  | No       | Optional: metricName, startDate, endDate, limit  |

```graphql
query GetPerformanceMetrics($input: GetMetricsInput) {
  analytics {
    performanceMetrics(input: $input) {
      id
      metricName
      metricValue
      timestamp
      metadata
      createdAt
    }
  }
}
```

**Variables:**
```json
{
  "input": {
    "metricName": "LCP",
    "startDate": "2024-01-01T00:00:00Z",
    "endDate": "2024-01-31T23:59:59Z",
    "limit": 100
  }
}
```

**Arguments:**
- `input` (GetMetricsInput): Optional filters

**Returns:** `[PerformanceMetric!]!`

**Authentication:** Required

**Validation:**
- `metricName`: Optional, max 100 characters if provided
- `limit`: Must be between 1 and 1000 (default: 100)
- `startDate` and `endDate`: If both provided, startDate must be before endDate

**Implementation Details:**
- Users can only view their own metrics (filtered by user_id)
- Metrics are retrieved from database via `PerformanceMetricsRepository`
- Results are ordered by timestamp (most recent first)

**Example Response:**
```json
{
  "data": {
    "analytics": {
      "performanceMetrics": [
        {
          "id": "1",
          "metricName": "LCP",
          "metricValue": 2.5,
          "timestamp": "2024-01-15T10:30:00Z",
          "metadata": {
            "url": "/dashboard",
            "userAgent": "Mozilla/5.0...",
            "connectionType": "4g"
          },
          "createdAt": "2024-01-15T10:30:01Z"
        }
      ]
    }
  }
}
```

### aggregateMetrics

Get aggregated statistics for a performance metric.

**Parameters:**

| Name  | Type                    | Required | Description                           |
|-------|-------------------------|----------|---------------------------------------|
| input | AggregateMetricsInput!  | Yes      | metricName, startDate, endDate        |

```graphql
query AggregateMetrics($input: AggregateMetricsInput!) {
  analytics {
    aggregateMetrics(input: $input) {
      avg
      min
      max
      p50
      p75
      p95
      count
    }
  }
}
```

**Variables:**
```json
{
  "input": {
    "metricName": "LCP",
    "startDate": "2024-01-01T00:00:00Z",
    "endDate": "2024-01-31T23:59:59Z"
  }
}
```

**Input:** `AggregateMetricsInput!`

**Returns:** `MetricAggregation`

**Authentication:** Required

**Validation:**
- `metricName`: Required, non-empty string, max 100 characters
- `startDate` and `endDate`: Required, startDate must be before endDate

**Implementation Details:**
- Users can only aggregate their own metrics (filtered by user_id)
- Aggregation calculates: avg, min, max, p50, p75, p95, count
- Metrics are aggregated from database via `PerformanceMetricsRepository`

**Example Response:**
```json
{
  "data": {
    "analytics": {
      "aggregateMetrics": {
        "avg": 2.3,
        "min": 1.2,
        "max": 5.8,
        "p50": 2.1,
        "p75": 2.8,
        "p95": 4.2,
        "count": 150
      }
    }
  }
}
```

## Mutations

### submitPerformanceMetric

Submit a performance metric for analytics tracking.

**Parameters:**

| Name  | Type                            | Required | Description                          |
|-------|---------------------------------|----------|--------------------------------------|
| input | SubmitPerformanceMetricInput!   | Yes      | name, value, timestamp, metadata    |

```graphql
mutation SubmitMetric($input: SubmitPerformanceMetricInput!) {
  analytics {
    submitPerformanceMetric(input: $input) {
      success
      message
    }
  }
}
```

**Variables:**
```json
{
  "input": {
    "name": "LCP",
    "value": 2.5,
    "timestamp": 1705312200000,
    "metadata": {
      "url": "/dashboard",
      "userAgent": "Mozilla/5.0...",
      "connectionType": "4g",
      "endpoint": "/api/graphql",
      "method": "POST"
    }
  }
}
```

**Input:** `SubmitPerformanceMetricInput!`

**Returns:** `PerformanceMetricResponse`

**Authentication:** Required

**Validation:**
- `name`: Required, non-empty string, max 100 characters
- `value`: Must be a number between 0 and 10,000,000,000
- `timestamp`: Must be a positive number (milliseconds since epoch)
- `metadata`: Optional JSON object

**Implementation Details:**
- **Non-Blocking**: Metric submission is non-blocking - if storage fails, the mutation still returns success
  - This ensures analytics tracking doesn't block client requests
  - Errors are logged but don't affect the response
  - Response message may indicate "Metric received (storage may have failed)" if storage failed
- Timestamp is converted from milliseconds to datetime (UTC)
- Metric is stored in database via `PerformanceMetricsRepository`
- Transaction is committed after successful storage

**Example Response:**
```json
{
  "data": {
    "analytics": {
      "submitPerformanceMetric": {
        "success": true,
        "message": "Metric received"
      }
    }
  }
}
```

## Input Types

### SubmitPerformanceMetricInput

Input for submitting a performance metric.

```graphql
input SubmitPerformanceMetricInput {
  name: String!
  value: Float!
  timestamp: BigInt!
  metadata: JSON
}
```

**Fields:**
- `name` (String!): Metric name (e.g., "LCP", "FID", "CLS", "TTFB", or custom) - max 100 characters
- `value` (Float!): Metric value (must be between 0 and 10,000,000,000)
- `timestamp` (BigInt!): Timestamp in milliseconds (Unix timestamp * 1000). Uses BigInt scalar to support large values beyond 32-bit Int range (max: 2,147,483,647). BigInt can handle millisecond timestamps for dates far into the future.
- `metadata` (JSON): Additional metadata (optional) - can include URL, user agent, connection type, endpoint, method

**Validation:**
- `name`: Required, non-empty, max 100 characters
- `value`: Must be a number between 0 and 10,000,000,000
- `timestamp`: Must be a positive integer (milliseconds since epoch). Supports large values via BigInt scalar. Must be a valid timestamp (converted to datetime for validation)
- Input validation is performed via `input.validate()` method

### GetMetricsInput

Input for querying performance metrics.

```graphql
input GetMetricsInput {
  metricName: String
  startDate: DateTime
  endDate: DateTime
  limit: Int
}
```

**Fields:**
- `metricName` (String): Optional metric name filter - max 100 characters if provided
- `startDate` (DateTime): Optional start date filter
- `endDate` (DateTime): Optional end date filter
- `limit` (Int): Maximum number of results (default: 100, max: 1000)

**Validation:**
- `metricName`: Optional, max 100 characters if provided
- `limit`: Must be between 1 and 1000 (default: 100)
- If both `startDate` and `endDate` are provided, startDate must be before endDate
- Input validation is performed via `input.validate()` method

### AggregateMetricsInput

Input for aggregating performance metrics.

```graphql
input AggregateMetricsInput {
  metricName: String!
  startDate: DateTime!
  endDate: DateTime!
}
```

**Fields:**
- `metricName` (String!): Name of the metric to aggregate - max 100 characters
- `startDate` (DateTime!): Start date for aggregation
- `endDate` (DateTime!): End date for aggregation

**Validation:**
- `metricName`: Required, non-empty, max 100 characters
- `startDate` and `endDate`: Required, startDate must be before endDate
- Input validation is performed via `input.validate()` method

## Error Handling

The Analytics module implements comprehensive error handling with input validation, database error handling, and response validation.

### Error Types

The Analytics module may raise the following errors:

- **ValidationError** (422): Input validation failed
  - Code: `VALIDATION_ERROR`
  - Extensions: `fieldErrors` (field-specific errors)
  - Occurs when: Invalid date range (startDate after endDate), invalid limit (must be 1-1000), invalid metric name, or invalid timestamp format
  - **Note**: The `timestamp` field uses `BigInt` scalar type to support large millisecond timestamps. If you receive an error about "Int cannot represent non 32-bit signed integer value", ensure you're using BigInt for the timestamp field.
- **BadRequestError** (400): Invalid request data
  - Code: `BAD_REQUEST`
  - Occurs when: Request format is invalid, required parameters are missing, or metric value is negative
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
          "limit": ["Limit must be between 1 and 1000"],
          "metricName": ["Metric name is required"]
        }
      }
    }
  ]
}
```

### Error Handling Patterns

- **Input Validation**: Metric names, values, timestamps, date ranges, and pagination parameters are validated before processing
- **Database Errors**: All database operations include transaction rollback on failure
- **Timestamp Conversion**: Timestamps are validated and converted from milliseconds to datetime
- **Error Logging**: Comprehensive error logging with context for debugging

## Usage Examples

### Complete Analytics Flow

```graphql
# 1. Submit a performance metric
mutation SubmitMetric {
  analytics {
    submitPerformanceMetric(input: {
      name: "LCP"
      value: 2.5
      timestamp: 1705312200000
      metadata: {
        url: "/dashboard"
        userAgent: "Mozilla/5.0..."
        connectionType: "4g"
      }
    }) {
      success
      message
    }
  }
}

# 2. Get metrics for a date range
query GetMetrics {
  analytics {
    performanceMetrics(input: {
      metricName: "LCP"
      startDate: "2024-01-01T00:00:00Z"
      endDate: "2024-01-31T23:59:59Z"
      limit: 100
    }) {
      id
      metricName
      metricValue
      timestamp
      metadata
    }
  }
}

# 3. Get aggregated statistics
query GetAggregated {
  analytics {
    aggregateMetrics(input: {
      metricName: "LCP"
      startDate: "2024-01-01T00:00:00Z"
      endDate: "2024-01-31T23:59:59Z"
    }) {
      avg
      min
      max
      p50
      p75
      p95
      count
    }
  }
}

# 4. Submit Core Web Vitals
mutation SubmitWebVitals {
  analytics {
    submitPerformanceMetric(input: {
      name: "LCP"
      value: 2.5
      timestamp: 1705312200000
      metadata: {
        url: "/dashboard"
      }
    }) {
      success
    }
  }
  analytics {
    submitPerformanceMetric(input: {
      name: "FID"
      value: 50.0
      timestamp: 1705312200000
      metadata: {
        url: "/dashboard"
      }
    }) {
      success
    }
  }
  analytics {
    submitPerformanceMetric(input: {
      name: "CLS"
      value: 0.1
      timestamp: 1705312200000
      metadata: {
        url: "/dashboard"
      }
    }) {
      success
    }
  }
}
```

## Implementation Details

### Analytics Service

- **PerformanceMetricsRepository**: Metrics are stored and retrieved via `PerformanceMetricsRepository`
  - All metric operations go through the repository layer
  - Repository handles database operations, validation, and business logic

### Metric Submission

- **Non-Blocking Pattern**: Metric submission is non-blocking - if storage fails, the mutation still returns success
  - This ensures analytics tracking doesn't block client requests
  - Errors are logged but don't affect the response
  - Response message may indicate "Metric received (storage may have failed)" if storage failed
  - Transaction rollback occurs on error, but success is still returned to client
- **Timestamp Conversion**: Timestamps are converted from milliseconds to datetime (UTC)
  - Input: BigInt (milliseconds since epoch)
  - Conversion: `datetime.fromtimestamp(timestamp / 1000, tz=UTC)`
  - Validation: Timestamp must be valid (not cause ValueError or OSError)
- **Transaction Management**: All database operations use transactions
  - Transaction commit after successful storage
  - Transaction rollback on failure (but still returns success to client)

### Metric Retrieval

- **User Isolation**: Users can only access their own metrics (filtered by user_id)
  - All queries filter by authenticated user's UUID
  - No cross-user metric access
- **Filtering**: Metrics can be filtered by:
  - Metric name (optional, case-insensitive)
  - Date range (startDate, endDate)
  - Limit (default: 100, max: 1000)
- **Ordering**: Results are ordered by timestamp (most recent first)

### Metric Aggregation

- **Aggregation Functions**: Statistics are calculated using database aggregation functions
  - `avg`: Average value
  - `min`: Minimum value
  - `max`: Maximum value
  - `p50`: 50th percentile (median)
  - `p75`: 75th percentile
  - `p95`: 95th percentile
  - `count`: Number of metrics aggregated
- **User Isolation**: Users can only aggregate their own metrics (filtered by user_id)
- **Date Range**: Aggregation requires both startDate and endDate
  - startDate must be before endDate

### Metadata Storage

- **JSON Storage**: Additional metadata is stored as JSON for flexible tracking
  - Can include: URL, user agent, connection type, endpoint, method
  - Optional field (can be null)
  - Flexible structure allows for future metadata additions

### Validation

- **Input Validation**: All inputs are validated before processing
  - Metric name: max 100 characters, must be non-empty
  - Metric value: must be between 0 and 10,000,000,000
  - Timestamp: must be positive, must be valid timestamp
  - Limit: must be between 1 and 1000 (default: 100)
  - Date range: startDate must be before endDate if both provided
- **Validation Methods**: Input validation is performed via `input.validate()` method
  - Raises ValueError with descriptive messages
  - Converted to ValidationError for GraphQL responses

### Error Handling

- **Non-Blocking Errors**: Metric submission failures don't block client requests
  - Errors are logged with context (user UUID, metric name)
  - Success response is returned even if storage fails
- **Database Error Handling**: Database operations use centralized error handlers
  - Transaction rollback on failure
  - Integrity errors are caught and converted to user-friendly errors
  - Database connection errors are converted to ServiceUnavailableError
- **Response Validation**: All service responses are validated before returning
  - Metric data structure validation
  - Aggregation data structure validation
  - Required fields validation

## Task breakdown (for maintainers)

1. **submitPerformanceMetric:** SubmitPerformanceMetricInput (metricName, metricValue, timestamp, metadata); insert into performance_metrics; user_id from context; non-blocking (log failure, don't fail response); validate metricName and value ranges.
2. **performanceMetrics query:** Filter by userId (context), metricName, startDate, endDate; validate_pagination; return connection; document Core Web Vitals names (LCP, FID, CLS, TTFB).
3. **aggregateMetrics:** AggregateMetricsInput (metricName, startDate, endDate, groupBy?); compute avg, min, max, p50, p75, p95, count; return MetricAggregation or list.
4. **Table:** performance_metrics; confirm schema (user_id, metric_name, metric_value, metric_metadata, timestamp, created_at).
5. **Admin/Health:** If Health.performanceStats or Admin use this data, document the relationship.

## Related Modules

- **Health Module**: Provides system-wide performance statistics
- **Admin Module**: Admin can view all user metrics
- **Usage Module** / **AI Chats** ([09_USAGE_MODULE.md](09_USAGE_MODULE.md), [17_AI_CHATS_MODULE.md](17_AI_CHATS_MODULE.md)): frontend performance metrics here are separate from `AI_CHAT` credit-style usage tracking

## Documentation metadata

- Era: `6.x`
- Introduced in: `TBD` (fill with exact minor)
- Frontend bindings: list page files from `docs/frontend/pages/*.json`
- Data stores touched: PostgreSQL/Elasticsearch/MongoDB/S3 as applicable

## Endpoint/version binding checklist

- Add operation list with `introduced_in` / `deprecated_in` tags.
- Map each operation to frontend page bindings and hook/service usage.
- Record DB tables read/write for each operation.

