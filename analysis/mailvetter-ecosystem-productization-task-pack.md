# Mailvetter — 9.x Ecosystem & Productization Task Pack

**Service:** `backend(dev)/mailvetter`  
**Era:** `9.x` — Ecosystem integration and platformization

## Contract track

- [ ] Define partner webhook event catalog (`completed`, `failed`, `partial_failed`).
- [ ] Define partner-grade SLA and retry guarantees.

## Service track

- [ ] Add webhook dead-letter and replay API.
- [ ] Add partner connector adapters for downstream systems.
- [ ] Add tenant-aware quotas and fairness controls.

## Surface track

- [ ] Admin partner dashboard: webhook delivery health and failure reasons.
- [ ] Partner key management screens in product admin.

## Data track

- [ ] Add `webhook_delivery_log` and `connector_events` tables.
- [ ] Add tenant usage aggregates and SLA evidence tables.

## Ops track

- [ ] Alerting for webhook retry exhaustion.
- [ ] Monthly ecosystem reliability and partner SLA reporting.
