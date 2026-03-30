# Sales Navigator — 8.x Public & Private APIs Task Pack

**Service:** `backend(dev)/salesnavigator`  
**Era:** `8.x` — Contact360 Public and Private APIs  
**Status:** Rate limits, versioned path, usage tracking, partner key scoping

---

## Contract track

- [ ] Migrate route prefix from `/v1/` to `/api/v1/` for consistency with other services (or document as intentional divergence)
- [ ] Add standard rate-limit response headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`, `Retry-After`
- [ ] Add `X-Request-ID` request/response header as first-class contract
- [ ] Publish OpenAPI spec to developer docs portal
- [ ] Define per-key quota model: free tier (N profiles/day), paid tiers, enterprise unlimited

## Service track

- [ ] Rate limiting middleware with `X-RateLimit-*` headers per API key
- [ ] `Retry-After` header on `429` response (seconds until quota reset)
- [ ] Usage counter increment on each `save-profiles` call — write to `api_usage` table keyed by `api_key_id`
- [ ] Return `X-Request-ID` in all responses

## Surface track

- [ ] API settings page: show SN ingest usage vs. quota (progress bar: N / quota)
- [ ] Developer docs: document `POST /v1/save-profiles` and `POST /v1/scrape` for private API consumers
- [ ] API key management: SN service key visible in key list with usage stats
- [ ] Quota exceeded state: `SNSaveButton` disabled with "Quota exceeded" tooltip; link to upgrade

## Data track

- [ ] `api_usage` table or row: `{api_key_id, service: "salesnavigator", date, call_count, profiles_saved}`
- [ ] Usage aggregation: daily and monthly totals per key
- [ ] Quota enforcement: check usage before processing; return `429` if exceeded

## Ops track

- [ ] API contract test in CI: schema validation for all request/response shapes
- [ ] Integration test: rate limit trigger → `429` → `Retry-After` header validated
- [ ] Monitoring: API usage dashboard per key; quota utilization alerts
- [ ] Compatibility gate: partner integrations tested before each versioned release

---

**References:**
- `docs/codebases/salesnavigator-codebase-analysis.md`
- `docs/backend/apis/SALESNAVIGATOR_ERA_TASK_PACKS.md`

---

## Extension surface contributions (era sync)

### Era 8.x — Public & Private APIs

**`extension/contact360` API governance:**
- `POST /v1/save-profiles` — documented as **private internal API** (extension → Lambda SN API); not publicly exposed
- `mutation auth.refreshToken` — documented as **public GraphQL API** surface (Appointment360); available to any authenticated client

**API contract documentation tasks:**
- [ ] Publish OpenAPI 3.0 spec for `POST /v1/save-profiles` including request/response schema, error codes, auth header
- [ ] Add `POST /v1/save-profiles` to `docs/backend/apis/` inventory
- [ ] Update `docs/backend/endpoints/` to include the Lambda SN API endpoint
- [ ] Confirm `auth.refreshToken` mutation signature in Appointment360 GraphQL schema docs