# Mailvetter — 8.x Public & Private APIs Task Pack

**Service:** `backend(dev)/mailvetter`  
**Era:** `8.x` — Public/private API and endpoint maturity

## Contract track

- [ ] Publish OpenAPI for `/v1/*` routes and error schemas.
- [ ] Define scoped API keys (`public`, `internal`, `admin`).
- [ ] Define webhook signature and retry contract as public spec.

## Service track

- [ ] Implement key scope enforcement middleware.
- [ ] Add key rotation and key revocation path.
- [ ] Add endpoint version header and deprecation metadata.

## Surface track

- [ ] Developer portal docs for verify, bulk, jobs, and results flows.
- [ ] Postman public collection aligned to v1 only (no legacy).

## Data track

- [ ] Add `api_key_scopes` and `api_key_audit` tables.
- [ ] Add request audit logs keyed by API key and endpoint.

## Ops track

- [ ] Public API rate-limit policy per scope.
- [ ] Public status page metrics for verifier availability and latency.
