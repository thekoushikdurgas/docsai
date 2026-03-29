# Health Response Contract

Foundation `0.10` requires a shared health payload shape across FastAPI, Gin, and Lambda-backed services.

## Required fields

- `status`: `healthy` | `degraded` | `unhealthy`
- `service`: stable service name
- `version`: service version string

## Optional fields

- `request_id`: correlation id for request tracing
- `details`: nested object for component checks (`db`, `queue`, `logging`)

## Family examples

### FastAPI

```json
{
  "status": "healthy",
  "service": "appointment360",
  "version": "1.1.0",
  "request_id": "req-123"
}
```

### Gin

```json
{
  "status": "healthy",
  "service": "email-campaign",
  "version": "0.1.0"
}
```

### Lambda/API Gateway

```json
{
  "status": "healthy",
  "service": "salesnavigator",
  "version": "0.1.0",
  "details": {
    "handler": "ok"
  }
}
```
