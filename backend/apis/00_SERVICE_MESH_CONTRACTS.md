# Service Mesh Contracts (0.3 Baseline)

This document freezes the gateway-to-service contract baseline for the 0.x mesh era. **Env var names below match `app/core/config.py` (`Settings`).**

## Downstream base URLs and env vars

| Gateway client | Target / role | Base URL env var(s) | API key / auth env var | Typical header |
| --- | --- | --- | --- | --- |
| `ConnectraClient` | Connectra VQL (`contact360.io/sync` or equivalent) | `CONNECTRA_BASE_URL` | `CONNECTRA_API_KEY` | `X-API-Key` |
| `TkdjobClient` | Job scheduler (tkdjob) | `TKDJOB_API_URL` | `TKDJOB_API_KEY` | `X-API-Key` |
| `LambdaEmailClient` | Email APIs | `LAMBDA_EMAIL_API_URL` | `LAMBDA_EMAIL_API_KEY` | `X-API-Key` |
| `LambdaAIClient` | Contact AI / Lambda | `LAMBDA_AI_API_URL` | `LAMBDA_AI_API_KEY` | `X-API-Key`, `X-User-ID` (when propagated) |
| `LambdaS3StorageClient` / `get_s3storage_client` | s3storage | `LAMBDA_S3STORAGE_API_URL` | `LAMBDA_S3STORAGE_API_KEY` (optional) | `X-API-Key` |
| Lambda logs pipeline | logs API | `LAMBDA_LOGS_API_URL` | `LAMBDA_LOGS_API_KEY` | `X-API-Key` |
| Sales Navigator bridge | salesnavigator service | `LAMBDA_SALES_NAVIGATOR_API_URL` | `LAMBDA_SALES_NAVIGATOR_API_KEY` | `X-API-Key` |
| DocsAI (optional) | Django docs/pages | `DOCSAI_API_URL` | _(service-specific; gateway may call unauthenticated)_ | — |
| Campaign satellite (optional) | Campaigns / sequences API | `CAMPAIGN_API_URL` | `CAMPAIGN_API_KEY` | `X-API-Key` |
| Resume AI (gateway → resumeai) | FastAPI resume microservice | `RESUME_AI_BASE_URL` | `RESUME_AI_API_KEY` | `X-API-Key` |

**Note:** Older docs sometimes referenced names like `LAMBDA_CONNECTRA_API_URL` or `LAMBDA_JOB_SCHEDULER_API_URL`. The gateway **`Settings`** fields above are authoritative.

Optional flags / timeouts (non-exhaustive): `LAMBDA_SALES_NAVIGATOR_ENABLED`, `DOCSAI_ENABLED`, `CONNECTRA_TIMEOUT`, `TKDJOB_API_TIMEOUT`, `LAMBDA_S3STORAGE_API_TIMEOUT`, `CAMPAIGN_API_TIMEOUT`, `RESUME_AI_TIMEOUT`.

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

- HTTP timeout target: `connect=5s`, `read=30s`, `write=30s` (per-client overrides in `Settings`).
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
