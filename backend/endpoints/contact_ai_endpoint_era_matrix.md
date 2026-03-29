---
title: "backend(dev)/contact.ai — era matrix"
source_json: contact_ai_endpoint_era_matrix.json
generator: json_to_markdown_endpoints.py
---

# backend(dev)/contact.ai

## Service metadata

| Field | Value |
| --- | --- |
| service | backend(dev)/contact.ai |
| base_path | /api/v1 |
| description | Contact AI FastAPI Lambda service — AI chat CRUD, message send (sync + SSE), and utility AI endpoints |


## HTTP / route inventory

| method | path | eras |
| --- | --- | --- |
| GET | /api/v1/ai-chats/ | 5.x, 6.x, 7.x, 8.x, 9.x, 10.x |
| POST | /api/v1/ai-chats/ | 5.x, 6.x, 7.x, 8.x, 9.x, 10.x |
| GET | /api/v1/ai-chats/{chat_id}/ | 5.x, 6.x, 7.x, 8.x, 9.x, 10.x |
| PUT | /api/v1/ai-chats/{chat_id}/ | 5.x, 6.x, 7.x, 8.x, 9.x, 10.x |
| DELETE | /api/v1/ai-chats/{chat_id}/ | 5.x, 6.x, 7.x, 8.x, 9.x, 10.x |
| POST | /api/v1/ai-chats/{chat_id}/message | 5.x, 6.x, 7.x, 8.x, 9.x, 10.x |
| POST | /api/v1/ai-chats/{chat_id}/message/stream | 5.x, 6.x, 7.x, 8.x, 9.x, 10.x |
| POST | /api/v1/ai/email/analyze | 2.x, 3.x, 4.x, 5.x, 6.x, 7.x, 8.x, 9.x, 10.x |
| POST | /api/v1/ai/company/summary | 3.x, 4.x, 5.x, 6.x, 7.x, 8.x, 9.x, 10.x |
| POST | /api/v1/ai/parse-filters | 3.x, 4.x, 5.x, 6.x, 7.x, 8.x, 9.x, 10.x |
| POST | /api/v1/ai/email/generate | 10.x |
| GET | /health | 0.x, 1.x, 2.x, 3.x, 4.x, 5.x, 6.x, 7.x, 8.x, 9.x, 10.x |
| GET | /health/db | 0.x, 1.x, 2.x, 3.x, 4.x, 5.x, 6.x, 7.x, 8.x, 9.x, 10.x |
| GET | /metrics | 6.x, 7.x, 8.x, 9.x, 10.x |


## era_focus

| Era | Focus |
| --- | --- |
| 0.x | Service skeleton, health endpoints, DDL baseline |
| 1.x | User FK integrity, IAM hardening |
| 2.x | analyzeEmailRisk contract lock |
| 3.x | parseContactFilters + generateCompanySummary contract lock |
| 4.x | SN contact object compatibility, extension CSP |
| 5.x | ALL chat endpoints live; streaming SSE; all utility endpoints live |
| 6.x | SLO tuning, SSE reliability, Prometheus metrics, chat TTL |
| 7.x | RBAC enforcement, audit trail, retention policy |
| 8.x | Rate limit headers, scoped API keys, usage tracking |
| 9.x | Webhook delivery, ecosystem connector adapter |
| 10.x | Campaign email generation endpoint, compliance evidence bundles |


## references

- docs/codebases/contact-ai-codebase-analysis.md
- docs/backend/apis/17_AI_CHATS_MODULE.md
- docs/backend/apis/CONTACT_AI_ERA_TASK_PACKS.md
- docs/backend/database/contact_ai_data_lineage.md
- docs/frontend/contact-ai-ui-bindings.md
- backend(dev)/contact.ai/app/api/v1/endpoints/ai_chats.py
- backend(dev)/contact.ai/app/api/v1/endpoints/ai.py

<!-- AUTO:db-graph:start -->

## Era alignment

See **era_focus** and route tables above — themes match [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md#era-tags-on-endpoints).

## Database & lineage

- Service: `backend(dev)/contact.ai`
- Use the matching row in [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md#lambda--worker-services-by-path) and the lineage file linked there.

## Related

- [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md)
- [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md)

<!-- AUTO:db-graph:end -->
---

*Generated from `contact_ai_endpoint_era_matrix.json`. Re-run `python json_to_markdown_endpoints.py`.*
