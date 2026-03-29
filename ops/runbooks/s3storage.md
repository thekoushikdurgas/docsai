# S3Storage Runbook

## Health endpoints and expected healthy payload
- `GET /api/v1/health`
- Expected payload fields: `status`, `service`, `version`

## Required environment variables and secret sources
- `S3STORAGE_S3_BUCKET_NAME`
- `S3STORAGE_S3_METADATA_WORKER_FUNCTION_NAME`
- `S3STORAGE_API_KEY`
- `S3STORAGE_LOG_BASE_URL`, `S3STORAGE_LOG_API_KEY`
- Source: environment variables (`lambda/s3storage/.env`)

## Deploy command(s) and rollback command(s)
- Deploy: `sam build && sam deploy` for lambda stack
- Rollback: deploy previous stack/template version and verify health

## Smoke checks to validate post-deploy behavior
- Health endpoint returns healthy payload
- Multipart flow: initiate -> part upload -> complete
- Protected endpoints reject missing/invalid API key

## Escalation path and ownership
- Owner: Storage service maintainers
- Escalate to platform/on-call for metadata worker or multipart failures
