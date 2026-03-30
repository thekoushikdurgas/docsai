---
name: Mailvetter v1 API Migration
overview: Refactor `lambda/mailvetter` to adopt the Gin framework (from `emailapigo`), implement the full Mailvaiter v1 API contract (from the API docs), keep the existing durable Redis+Postgres bulk pipeline, and add webhooks, rate limiting, and plan tiers (from `lambda/1/mailvetter`).
todos:
  - id: t01
    content: Add Gin, gin-contrib/cors, gin-contrib/gzip to go.mod and run go mod tidy
    status: pending
  - id: t02
    content: "Create internal/plans/plans.go: PlanConfig, Plans map, APIKey, APIKeyStore, context helpers"
    status: pending
  - id: t03
    content: "Create internal/middleware/auth.go: Gin Bearer auth middleware using APIKeyStore"
    status: pending
  - id: t04
    content: "Create internal/middleware/ratelimit.go: fixed-window rate limiter Gin middleware + X-RateLimit-* headers"
    status: pending
  - id: t05
    content: "Create internal/schemas/requests.go and responses.go: all typed request/response structs + ErrorResponse envelope"
    status: pending
  - id: t06
    content: "Add VerifyOptions to internal/validator/logic.go: gate SMTP collector and disposable check on options"
    status: pending
  - id: t07
    content: "Extend DB schema in internal/store/db.go: add valid_count, invalid_count, started_at, updated_at, job_name, callback_url, callback_events, webhook_sent, owner_key to jobs; add is_valid, processed_at to results; add filter index"
    status: pending
  - id: t08
    content: "Create internal/services/validate_service.go: BuildValidationResponse mapping engine result to doc schema"
    status: pending
  - id: t09
    content: "Create internal/services/job_service.go: CreateJob, GetJobStatus, GetJobResults (with filter/pagination), EnqueueBulk"
    status: pending
  - id: t10
    content: "Create internal/handlers/health.go: Gin handler returning health JSON"
    status: pending
  - id: t11
    content: "Create internal/handlers/validate.go: ValidateSingleHandler and ValidateBulkHandler (plan limit + concurrent job check)"
    status: pending
  - id: t12
    content: "Create internal/handlers/jobs.go: JobStatusHandler and JobResultsHandler (JSON + CSV format, filter support)"
    status: pending
  - id: t13
    content: "Create internal/api/router.go: Gin engine, middleware chain, v1 route group wiring all handlers"
    status: pending
  - id: t14
    content: "Rewrite cmd/api/main.go: keep boot sequence, replace stdlib mux with Gin router from api.SetupRouter"
    status: pending
  - id: t15
    content: "Update internal/worker/runner.go: populate is_valid/processed_at/valid_count/invalid_count/started_at/updated_at, extend Task struct with VerifyOptions fields"
    status: pending
  - id: t16
    content: "Create internal/webhook/dispatcher.go: HMAC-signed POST with 3-attempt exponential backoff, mark webhook_sent in DB"
    status: pending
  - id: t17
    content: Add 30-day job retention cleanup goroutine in cmd/worker/main.go
    status: pending
  - id: t18
    content: Add legacy /verify and static file routes in router.go for backward compatibility with existing UI
    status: pending
isProject: false
---

# Mailvetter v1 API Migration Plan

## Current State vs Target

### Current `lambda/mailvetter`

- `cmd/api/main.go` - stdlib `http.New

