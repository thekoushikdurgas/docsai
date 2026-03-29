# Mailvetter — 0.x Foundation Task Pack

**Service:** `backend(dev)/mailvetter`  
**Era:** `0.x` — Foundation and pre-product stabilization

## Contract track

- [ ] Freeze canonical API namespace: `/v1/*` (document legacy routes as deprecated compatibility only). (patch assignment: `0.2.0`–`0.2.2`)
- [ ] Define auth contract: `Authorization: Bearer <API_KEY>`. (patch assignment: `0.2.0`–`0.2.2`)
- [ ] Define baseline error envelope: `{status,error_code,message,details,timestamp}`. (patch assignment: `0.2.0`–`0.2.2`)
- [ ] Define health contract: `GET /v1/health`. (patch assignment: `0.2.0`–`0.2.2`)

## Service track

- [ ] Stabilize Gin bootstrap (`cmd/api/main.go`, `internal/api/router.go`). (patch assignment: `0.2.0`–`0.2.2`)
- [ ] Ensure API and worker binaries are independently bootable. (patch assignment: `0.2.0`–`0.2.2`)
- [ ] Verify Redis and Postgres init failure paths return clear startup errors. (patch assignment: `0.2.0`–`0.2.2`)
- [ ] Confirm graceful shutdown behavior for API and worker processes. (patch assignment: `0.2.0`–`0.2.2`)

## Surface track

- [ ] Keep `static/index.html` as legacy operator UI only; mark as non-product UI (no customer dashboard routes). (patch assignment: `0.2.3`–`0.2.6`)
- [ ] Add explicit “legacy UI” banner and route ownership note in docs, confirming no `/dashboard`/product navigation exists in `0.x`. (patch assignment: `0.2.3`–`0.2.6`)

## Data track

- [ ] Freeze foundational tables: `jobs`, `results`. (patch assignment: `0.2.0`–`0.2.2`)
- [ ] Document migration ownership (`internal/store/db.go`) and indexes. (patch assignment: `0.2.0`–`0.2.2`)
- [ ] Add schema checksum validation for startup. (patch assignment: `0.2.3`–`0.2.6`)

## Ops track

- [ ] Lock Docker build and compose baseline (API+worker+redis+postgres). (patch assignment: `0.2.3`–`0.2.6`)
- [ ] Add smoke checks for `/v1/health`, queue push/pop, DB write/read. (patch assignment: `0.2.3`–`0.2.6`)
- [ ] Add first release gate for migration success before service ready. (patch assignment: `0.2.7`–`0.2.9`)
