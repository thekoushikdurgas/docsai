# Contact AI — 8.x Public/Private APIs Task Pack

**Service:** `backend(dev)/contact.ai`  
**Era:** `8.x` — Public and private APIs and endpoints  
**Status:** Contact AI as a documented private API surface with scoped keys, rate limit headers, usage tracking

---

## Contract track

- [ ] Publish internal API documentation for `/api/v1/ai-chats/` and `/api/v1/ai/` in Contact360 developer docs.
- [ ] Define rate limit contract:
  - `X-RateLimit-Limit`: total requests per window
  - `X-RateLimit-Remaining`: remaining requests
  - `Retry-After`: seconds until reset
- [ ] Add `X-Request-ID` request tracing header to all responses.
- [ ] Define private API key scopes: `ai:chat`, `ai:utilities`; document in API key management.
- [ ] Lock OpenAPI spec as contract artifact for `8.x`; publish to DocsAI.

## Service track

- [ ] Implement rate limit response headers on all contact.ai endpoints (align with token bucket state).
- [ ] Implement scoped API key validation: key must have `ai:chat` scope for chat routes, `ai:utilities` for utility routes.
- [ ] Add `X-Request-ID` header generation and propagation through Lambda context.
- [ ] Implement AI usage counter per user/key: increment on each successful API call.
- [ ] Expose usage stats endpoint or integrate with `appointment360` usage tracking.

## Surface track

- [ ] API settings page: show AI-specific quota (chat calls/month, utility calls/month) alongside other API metrics.
- [ ] Rate limit exceeded UI: show `Retry-After` countdown in `AIErrorState` component.
- [ ] Developer documentation page: document AI endpoints, auth model, rate limits, request/response examples.

## Data track

- [ ] Add AI usage counters to `api_usage` table or dedicated `ai_usage_log` table: `{user_id, key_id, endpoint, model, timestamp}`.
- [ ] Document usage data schema in `contact_ai_data_lineage.md`.
- [ ] Confirm usage data does not contain message content (privacy).

## Ops track

- [ ] API gateway throttle policies: align Lambda concurrency limits with token bucket rate limits.
- [ ] Add contact.ai endpoints to public API monitoring dashboard.
- [ ] Publish contact.ai API to internal developer portal with OpenAPI spec and Postman collection.
- [ ] Run API contract tests in CI: validate response shape against OpenAPI spec on every deploy.

---

**References:**  
`docs/codebases/contact-ai-codebase-analysis.md` · `docs/backend/apis/CONTACT_AI_ERA_TASK_PACKS.md` · `docs/backend/endpoints/contact_ai_endpoint_era_matrix.json`
