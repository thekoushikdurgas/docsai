# Health Module

## Overview

The Health module provides health check and monitoring functionality including API metadata, health status, VQL/Connectra health, and performance statistics. Some queries require SuperAdmin role.
**Location:** `app/graphql/modules/health/`

**Note:** This module also includes REST endpoints for health checks. See [REST Endpoints](#rest-endpoints) section below.

## Queries – parameters and variable types

| Query | Parameter(s) | Variable type (GraphQL) | Return type |
|-------|---------------|-------------------------|-------------|
| `apiMetadata` | — | — | `ApiMetadata` |
| `apiHealth` | — | — | `ApiHealth` |
| `vqlHealth` | — | — | `VQLHealth` |
| `vqlStats` | — | — | `VQLStats` |
| `performanceStats` | — | — | `PerformanceStats` (SuperAdmin only) |

No mutations. **Auth:** `apiMetadata`, `apiHealth` are public. **`vqlHealth`** and **`vqlStats`** require an authenticated user (Connectra check uses `CONNECTRA_BASE_URL`). **`performanceStats`** requires **SuperAdmin**.

**REST** (FastAPI, `app/main.py`): `GET /health`, `GET /health/db`, `GET /health/logging`, `GET /health/slo`, `GET /health/token-blacklist`. Also `GET /` (discovery JSON), `POST /graphql`.

## Types

### ApiMetadata

API metadata information.

```graphql
type ApiMetadata {
  name: String!
  version: String!
  docs: String!
}
```

**Fields:**
- `name` (String!): Project name
- `version` (String!): API version
- `docs` (String!): Documentation URL

### ApiHealth

Basic API health status.

```graphql
type ApiHealth {
  status: String!
  environment: String!
}
```

**Fields:**
- `status` (String!): Health status (typically "healthy")
- `environment` (String!): Environment name (development, staging, production)

### VQLHealth

VQL/Connectra health status.

```graphql
type VQLHealth {
  connectraEnabled: Boolean!
  connectraStatus: String!
  connectraBaseUrl: String!
  connectraDetails: ConnectraDetails
  connectraError: String
  monitoringAvailable: Boolean!
}
```

### ConnectraDetails

Detailed Connectra health information.

```graphql
type ConnectraDetails {
  status: String!
  version: String
  uptime: Int
}
```

### VQLStats

VQL query statistics.

```graphql
type VQLStats {
  message: String!
  note: String!
}
```

### PerformanceStats

Comprehensive performance statistics (SuperAdmin only).

```graphql
type PerformanceStats {
  cache: CacheStats!
  slowQueries: SlowQueriesStats!
  database: DatabaseHealth!
  s3: S3Health!
  endpointPerformance: EndpointPerformance!
}
```

### CacheStats

Query cache statistics.

```graphql
type CacheStats {
  enabled: Boolean!
  useRedis: Boolean!
  hits: Int!
  misses: Int!
  hitRate: Float!
  size: Int!
  maxSize: Int!
}
```

### SlowQueriesStats

Slow query tracking statistics.

```graphql
type SlowQueriesStats {
  thresholdMs: Int!
  countLastHour: Int!
}
```

### DatabaseHealth

Database connection pool health.

```graphql
type DatabaseHealth {
  status: String!
  poolSize: Int!
  activeConnections: Int!
  idleConnections: Int!
}
```

### S3Health

S3 connectivity status.

```graphql
type S3Health {
  status: String!
  bucket: String
  region: String
  message: String!
  error: String
}
```

### EndpointPerformance

Endpoint performance metrics.

```graphql
type EndpointPerformance {
  totalRequests: Int!
  averageResponseTimeMs: Float!
  p95ResponseTimeMs: Float!
  p99ResponseTimeMs: Float!
  slowEndpoints: [SlowEndpoint!]!
}
```

### SlowEndpoint

Information about a slow endpoint.

```graphql
type SlowEndpoint {
  endpoint: String!
  averageTimeMs: Float!
  requestCount: Int!
}
```

## Queries

### apiMetadata

Get basic API metadata including project name, version, and documentation URL.

**Parameters:** None.

```graphql
query GetApiMetadata {
  health {
    apiMetadata {
      name
      version
      docs
    }
  }
}
```

**Returns:** `ApiMetadata`

**Authentication:** Not required

**Implementation Details:**
- Returns metadata from application settings (PROJECT_NAME, VERSION, DOCS_URL)
- No external service calls or database queries
- Public endpoint for API discovery

**Example Response:**
```json
{
  "data": {
    "health": {
      "apiMetadata": {
        "name": "<from settings.PROJECT_NAME; often still 'Appointment GraphQL API' in config>",
        "version": "0.1.0",
        "docs": "/docs"
      }
    }
  }
}
```

### apiHealth

Get basic API health status.

**Parameters:** None.

```graphql
query GetApiHealth {
  health {
    apiHealth {
      status
      environment
    }
  }
}
```

**Returns:** `ApiHealth`

**Authentication:** Not required

**Implementation Details:**
- Returns basic health status ("healthy") and environment from settings
- No external service calls or database queries
- Public endpoint for basic health checks

**Example Response:**
```json
{
  "data": {
    "health": {
      "apiHealth": {
        "status": "healthy",
        "environment": "production"
      }
    }
  }
}
```

### vqlHealth

Check the health and status of the VQL/Connectra service.

**Parameters:** None.

```graphql
query GetVQLHealth {
  health {
    vqlHealth {
      connectraEnabled
      connectraStatus
      connectraBaseUrl
      connectraDetails {
        status
        version
        uptime
      }
      connectraError
      monitoringAvailable
    }
  }
}
```

**Returns:** `VQLHealth`

**Authentication:** Required

**Implementation Details:**
- Checks if Connectra is enabled via CONNECTRA_BASE_URL setting
- If disabled, returns unavailable status with error message
- If enabled, performs actual health check via `ConnectraClient.health_check`
- Parses health response and converts to GraphQL type
- Handles ConnectraClient errors gracefully (returns unhealthy status with error message)
- Returns detailed Connectra information (status, version, uptime) if available

**Example Response:**
```json
{
  "data": {
    "health": {
      "vqlHealth": {
        "connectraEnabled": true,
        "connectraStatus": "healthy",
        "connectraBaseUrl": "https://connectra.example.com",
        "connectraDetails": {
          "status": "operational",
          "version": "1.0.0",
          "uptime": 86400
        },
        "connectraError": null,
        "monitoringAvailable": true
      }
    }
  }
}
```

### vqlStats

Get VQL query statistics and metrics.

**Parameters:** None.

```graphql
query GetVQLStats {
  health {
    vqlStats {
      message
      note
    }
  }
}
```

**Returns:** `VQLStats`

**Authentication:** Required

**Implementation Details:**
- Returns informational message about VQL stats
- Stats are tracked by VQLMonitoringMiddleware
- Currently a placeholder - requires middleware integration for actual stats
- Can be accessed via monitoring dashboard when middleware is integrated

### performanceStats

Get performance statistics for monitoring.

**Parameters:** None.

```graphql
query GetPerformanceStats {
  health {
    performanceStats {
      cache {
        enabled
        hits
        misses
        hitRate
      }
      slowQueries {
        thresholdMs
        countLastHour
      }
      database {
        status
        poolSize
        activeConnections
        idleConnections
      }
      s3 {
        status
        bucket
        region
      }
      endpointPerformance {
        totalRequests
        averageResponseTimeMs
        p95ResponseTimeMs
        p99ResponseTimeMs
        slowEndpoints {
          endpoint
          averageTimeMs
          requestCount
        }
      }
    }
  }
}
```

**Returns:** `PerformanceStats`

**Authentication:** Required

**Authorization:** SuperAdmin only

**Implementation Details:**
- Role check via `UserProfileRepository` (must be SuperAdmin)
- Retrieves cache statistics from `get_query_cache()` (non-blocking - returns defaults if fails)
- Retrieves slow query statistics from `get_query_monitor()` (non-blocking - returns defaults if fails)
- Retrieves database pool statistics from `get_pool_stats()` (non-blocking - returns defaults if fails)
- Checks S3 health via `S3Service` (non-blocking - returns status based on configuration)
- Endpoint performance is a placeholder (requires middleware integration)
- All statistics retrieval is non-blocking - errors are logged but don't fail the query
- Returns default/zero values if any component fails

**Example Response:**
```json
{
  "data": {
    "health": {
      "performanceStats": {
        "cache": {
          "enabled": true,
          "hits": 1250,
          "misses": 350,
          "hitRate": 0.78125
        },
        "slowQueries": {
          "thresholdMs": 1000,
          "countLastHour": 5
        },
        "database": {
          "status": "healthy",
          "poolSize": 20,
          "activeConnections": 8,
          "idleConnections": 12
        },
        "s3": {
          "status": "healthy",
          "bucket": "my-bucket",
          "region": "us-east-1"
        },
        "endpointPerformance": {
          "totalRequests": 10000,
          "averageResponseTimeMs": 125.5,
          "p95ResponseTimeMs": 250.0,
          "p99ResponseTimeMs": 500.0,
          "slowEndpoints": [
            {
              "endpoint": "/graphql",
              "averageTimeMs": 200.0,
              "requestCount": 100
            }
          ]
        }
      }
    }
  }
}
```

## Error Handling

The Health module implements comprehensive error handling with input validation, external service error handling, and role-based access control.

### Error Types

The Health module may raise the following errors:

- **ForbiddenError** (403): Insufficient permissions
  - Code: `FORBIDDEN`
  - Extensions: `requiredRole: "SuperAdmin"`
  - Occurs when: User lacks SuperAdmin role required for `performanceStats` query
- **ServiceUnavailableError** (503): External service unavailable
  - Code: `SERVICE_UNAVAILABLE`
  - Extensions: `serviceName: "connectra"`, `"database"`, `"s3"`, or `"lambda_logs"`
  - Occurs when: External service (Connectra, database, S3, Lambda Logs) is down or connection fails
- **BadRequestError** (400): Invalid request data
  - Code: `BAD_REQUEST`
  - Occurs when: Request format is invalid or required parameters are missing

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

**Example: Service Unavailable**
```json
{
  "errors": [
    {
      "message": "Connectra service temporarily unavailable. Please try again later.",
      "extensions": {
        "code": "SERVICE_UNAVAILABLE",
        "statusCode": 503,
        "serviceName": "connectra"
      }
    }
  ]
}
```

### Error Handling Patterns

- **Input Validation**: Time range parameters and filter values are validated before processing
- **External Service Errors**: Health check errors from external services are caught and converted to appropriate GraphQL errors
- **Role-Based Access**: Performance stats query requires SuperAdmin role
- **Non-Blocking Errors**: Health check failures don't block the entire health response
- **Error Logging**: Comprehensive error logging with context for debugging

## Usage Examples

### Basic Health Checks

```graphql
# Get API metadata (no auth required)
query GetMetadata {
  health {
    apiMetadata {
      name
      version
      docs
    }
  }
}

# Get API health (no auth required)
query GetHealth {
  health {
    apiHealth {
      status
      environment
    }
  }
}

# Get VQL health (auth required)
query GetVQLHealth {
  health {
    vqlHealth {
      connectraEnabled
      connectraStatus
      connectraBaseUrl
      connectraDetails {
        status
        version
      }
    }
  }
}
```

### Performance Monitoring (SuperAdmin)

```graphql
# Get comprehensive performance stats
query GetPerformance {
  health {
    performanceStats {
      cache {
        enabled
        hits
        misses
        hitRate
        size
        maxSize
      }
      slowQueries {
        thresholdMs
        countLastHour
      }
      database {
        status
        poolSize
        activeConnections
        idleConnections
      }
      s3 {
        status
        bucket
        region
        message
      }
      endpointPerformance {
        totalRequests
        averageResponseTimeMs
        p95ResponseTimeMs
        p99ResponseTimeMs
        slowEndpoints {
          endpoint
          averageTimeMs
          requestCount
        }
      }
    }
  }
}
```

## REST Endpoints

In addition to GraphQL queries, the Health module provides REST endpoints for health checks.

### GET /health/logging

Get logging system health and metrics.

**Endpoint:** `GET /health/logging`

**Authentication:** Not required

**Response Format:** `status` is either `"healthy"` or `"degraded"`.

```json
{
  "status": "healthy",
  "metrics": {
    "logs_sent": 1250,
    "logs_failed": 5,
    "logs_in_queue": 12,
    "logs_in_fallback": 0,
    "api_calls": 1255,
    "api_errors": 5,
    "retry_count": 3,
    "health_check_count": 100,
    "health_check_failures": 0,
    "health_check_success_rate": 100.0,
    "last_success_time": "2024-01-15T10:30:00Z",
    "last_error_time": "2024-01-15T10:25:00Z",
    "last_health_check_time": "2024-01-15T10:30:00Z",
    "error_types": {
      "ConnectionError": 3,
      "TimeoutError": 2
    },
    "success_rate": 99.6,
    "total_logs": 1255
  },
  "request_id": "abc123"
}
```

**Status Codes:**
- `200 OK`: Logging system is healthy
- `503 Service Unavailable`: Logging system is degraded (success rate < 95% or queue/fallback issues)

**Health Determination:**
The endpoint returns `healthy` status when:
- Success rate >= 95%
- Queue size < 90% of max capacity
- Fallback buffer < 1000 entries

**Example Request:**
```bash
curl -X GET http://localhost:8000/health/logging
```

**Example Response (Healthy):**
```json
{
  "status": "healthy",
  "metrics": {
    "logs_sent": 10000,
    "logs_failed": 50,
    "logs_in_queue": 25,
    "logs_in_fallback": 0,
    "api_calls": 10050,
    "api_errors": 50,
    "retry_count": 45,
    "health_check_count": 500,
    "health_check_failures": 2,
    "health_check_success_rate": 99.6,
    "success_rate": 99.5,
    "total_logs": 10050
  },
  "request_id": "req-123"
}
```

**Example Response (Degraded):**
```json
{
  "status": "degraded",
  "metrics": {
    "logs_sent": 5000,
    "logs_failed": 1000,
    "logs_in_queue": 9500,
    "logs_in_fallback": 500,
    "api_calls": 6000,
    "api_errors": 1000,
    "retry_count": 800,
    "success_rate": 83.3,
    "total_logs": 6000
  },
  "request_id": "req-456"
}
```

**Metrics Fields:**
- `logs_sent`: Total logs successfully sent to Lambda API
- `logs_failed`: Total logs that failed to send
- `logs_in_queue`: Current number of logs waiting in queue
- `logs_in_fallback`: Current number of logs in fallback buffer
- `api_calls`: Total API calls made to Lambda Logs API
- `api_errors`: Total API errors encountered
- `retry_count`: Number of retry attempts made
- `health_check_count`: Number of health checks performed
- `health_check_failures`: Number of failed health checks
- `health_check_success_rate`: Percentage of successful health checks
- `success_rate`: Overall log sending success rate
- `error_types`: Breakdown of error types encountered
- `last_success_time`: Timestamp of last successful log send
- `last_error_time`: Timestamp of last error
- `last_health_check_time`: Timestamp of last health check

**Related Endpoints:**
- `GET /health` - Basic API health check
- `GET /health/db` - Database health check

## Implementation Details

### Public Endpoints

- **No Authentication**: `apiMetadata` and `apiHealth` queries don't require authentication
  - `apiMetadata`: Returns project name, version, and documentation URL from settings
  - `apiHealth`: Returns basic health status ("healthy") and environment from settings
  - Both are public endpoints for API discovery and basic health checks
  - No external service calls or database queries

### Authenticated Endpoints

- **Authentication Required**: `vqlHealth` and `vqlStats` require authentication
  - `vqlHealth`: Checks Connectra/VQL service health
  - `vqlStats`: Returns informational message about VQL statistics (placeholder)

### SuperAdmin Endpoints

- **SuperAdmin Only**: `performanceStats` requires SuperAdmin role
  - Role check via `UserProfileRepository`
  - Raises ForbiddenError if user is not SuperAdmin
  - Returns comprehensive performance statistics

### Connectra/VQL Health Check

- **ConnectraClient Integration**: Health check uses `ConnectraClient.health_check`
  - Checks if Connectra is enabled via CONNECTRA_BASE_URL setting
  - If disabled, returns unavailable status with error message
  - If enabled, performs actual health check
  - Parses health response and extracts status, version, uptime
  - Handles ConnectraClient errors gracefully via `handle_connectra_error`
  - Returns unhealthy status with error message if health check fails
- **Health Status Values**:
  - `healthy`: Connectra is operational
  - `unhealthy`: Connectra is not operational or returned unexpected response
  - `unavailable`: Connectra is not configured (CONNECTRA_BASE_URL not set)
  - `unknown`: Health check failed or returned invalid format

### Performance Statistics

- **Cache Statistics**: Query cache statistics from `get_query_cache()`
  - `enabled`: Whether query caching is enabled (from settings)
  - `useRedis`: Whether Redis cache is enabled (from settings)
  - `hits`: Number of cache hits
  - `misses`: Number of cache misses
  - `hitRate`: Cache hit rate (hits / total)
  - `size`: Current cache size
  - `maxSize`: Maximum cache size
  - Non-blocking: Returns default values if cache stats retrieval fails
- **Slow Query Statistics**: Slow query tracking from `get_query_monitor()`
  - `thresholdMs`: Slow query threshold in milliseconds (from settings)
  - `countLastHour`: Number of slow queries in the last hour
  - Non-blocking: Returns default values if slow query stats retrieval fails
- **Database Pool Statistics**: Database connection pool health from `get_pool_stats()`
  - `status`: Pool health status
  - `poolSize`: Maximum pool size (from settings)
  - `activeConnections`: Number of active connections
  - `idleConnections`: Number of idle connections
  - Non-blocking: Returns default values if pool stats retrieval fails
- **S3 Health**: S3 service health check via `S3Service`
  - `status`: S3 health status (healthy, not_configured, unhealthy)
  - `bucket`: S3 bucket name (if configured)
  - `region`: S3 region (if configured)
  - `message`: Status message
  - `error`: Error message (if unhealthy)
  - Non-blocking: Returns status based on configuration, errors are logged but don't fail query
- **Endpoint Performance**: Placeholder for endpoint performance metrics
  - Currently returns zero values
  - Requires middleware integration for actual tracking
  - Would track: total requests, average/p95/p99 response times, slow endpoints

### Error Handling

- **Non-Blocking Statistics**: All statistics retrieval is non-blocking
  - Errors are logged but don't fail the entire query
  - Returns default/zero values if any component fails
  - This ensures health checks remain available even if individual components fail
- **Connectra Error Handling**: Connectra health check errors are handled gracefully
  - Uses `handle_connectra_error` to convert errors to appropriate format
  - Returns unhealthy status with error message instead of raising exception
  - Fallback error handling if error handler fails
- **S3 Error Handling**: S3 health check errors are handled gracefully
  - Uses `handle_s3_error` to convert errors to appropriate format
  - Returns unhealthy status with error message instead of raising exception
  - Errors are logged but don't fail the query
- **Database Error Handling**: Database pool stats errors are handled gracefully
  - Returns unknown status with zero values if pool stats retrieval fails
  - Errors are logged but don't fail the query

### Configuration

- **Settings Integration**: Health checks use application settings
  - `PROJECT_NAME`: Project name for metadata
  - `VERSION`: API version for metadata
  - `DOCS_URL`: Documentation URL for metadata
  - `ENVIRONMENT`: Environment name for health status
  - `CONNECTRA_BASE_URL`: Connectra service URL (optional). **Note:** Connectra typically runs on port **8080** (not 8000); use `http://host:8080` when configuring.
  - `ENABLE_QUERY_CACHING`: Whether query caching is enabled
  - `ENABLE_REDIS_CACHE`: Whether Redis cache is enabled
  - `SLOW_QUERY_THRESHOLD`: Slow query threshold in seconds
  - `DATABASE_POOL_SIZE`: Maximum database connection pool size

### Monitoring Integration

- **VQL Monitoring**: VQL stats are tracked by VQLMonitoringMiddleware
  - Currently a placeholder endpoint
  - Requires middleware integration for actual stats
  - Can be accessed via monitoring dashboard when integrated
- **Query Monitoring**: Slow queries are tracked by query monitor
  - Tracks queries exceeding threshold
  - Provides count of slow queries in last hour
  - Threshold configurable via settings
- **Cache Monitoring**: Query cache statistics are tracked when caching is enabled
  - Tracks hits, misses, and hit rate
  - Provides cache size information
  - Supports both in-memory and Redis caching

### REST Endpoints

- **Logging Health**: REST endpoint `/health/logging` provides logging system metrics
  - Provides logging system health status
  - Includes metrics and health information
  - Separate from GraphQL health queries

## Task breakdown (for maintainers)

1. **Trace apiMetadata/apiHealth:** Return values from app settings (PROJECT_NAME, VERSION, DOCS_URL, ENVIRONMENT); no DB or external calls.
2. **vqlHealth/vqlStats:** Call Connectra (CONNECTRA_BASE_URL) for status; handle connectraEnabled false and connectraError; document ConnectraDetails shape.
3. **performanceStats:** SuperAdmin only; aggregates cache, slowQueries, database pool, S3 health, endpointPerformance; verify each sub-resolver and config (e.g. ENABLE_QUERY_CACHING).
4. **REST endpoints:** Ensure /health, /health/db, /health/logging are documented and implemented in main.py (or router); logging health from Lambda Logs API metrics.

## Related Modules

- **Admin Module**: Provides admin operations and monitoring
- **S3 Module**: S3 health is included in performance stats
- **Contact AI (separate service):** The FastAPI Contact AI Lambda (`backend(dev)/contact.ai`) exposes its own `GET /health` and `GET /api/v1/health`; those are **not** surfaced by this GraphQL Health module. See [17_AI_CHATS_MODULE.md](17_AI_CHATS_MODULE.md).

## Documentation metadata

- Era: `6.x`
- Introduced in: `TBD` (fill with exact minor)
- Frontend bindings: list page files from `docs/frontend/pages/*.json`
- Data stores touched: PostgreSQL/Elasticsearch/MongoDB/S3 as applicable

## Endpoint/version binding checklist

- Add operation list with `introduced_in` / `deprecated_in` tags.
- Map each operation to frontend page bindings and hook/service usage.
- Record DB tables read/write for each operation.

