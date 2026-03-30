# Service Mesh Contracts (0.3 Baseline)

This document freezes the gateway-to-service contract baseline for the 0.x mesh era.

## Downstream base URLs and env vars

| Gateway Client | Target Service | Base URL env var | Auth header |
| --- | --- | --- | --- |
| `ConnectraClient` | `contact360.io/sync` | `LAMBDA_CONNECTRA_API_URL` | `X-API-Key` |
| `TkdjobClient` | `contact360.io/jobs` | `LAMBDA_JOB_SCHEDULER_API_URL` | `X-API-Key` |
| `LambdaEmailClient` | `emailapis`/`emailapigo` | `LAMBDA_EMAIL_API_URL` | `X-API-Key` |
| `LambdaAIClient` | `contact.ai` | `LAMBDA_AI_API_URL` | `X-API-Key`, `X-User-ID` |
| `LambdaS3StorageClient` | `s3storage` | `LAMBDA_S3STORAGE_API_URL` | `X-API-Key` |
| `LambdaLogsClient` | `logs.api` | `LAMBDA_LOGS_API_URL` | `X-API-Key` |
| `LambdaSalesNavigatorClient` | `salesnavigator` | `LAMBDA_SN_API_URL` | `X-API-Key` |

## Unified error envelope

All downstream service errors should normalize to this shape before surfacing in GraphQL:

```json
{
  "error": {
    "code": "DOWNSTREAM_ERROR",
    "service": "s3storage",
    "message": "human readable summary",
    "request_id": "req_...",
    "trace_id": "trace_...",
    "status_code": 502,
    "details": {}
  }
}
```

GraphQL adapters should map this to either:

- `GraphQLError.extensions` for unexpected downstream failures, or
- typed `UserError` payloads for known validation/business errors.

## Timeout and pooling baseline

- HTTP timeout target: `connect=5s`, `read=30s`, `write=30s`.
- Gateway clients should reuse connection pools (no per-request client construction).
- Non-idempotent retries disabled by default; idempotent GET/health calls may retry with jittered backoff.

## Frozen email status vocabulary (Python + Go parity)

### Finder

- `found`
- `not_found`
- `pattern_only`

### Verifier

- `valid`
- `invalid`
- `risky`
- `catch_all`
- `unknown`

Any new value must be introduced in both `emailapis` and `emailapigo` in the same release, with docs and fixtures updated together.
