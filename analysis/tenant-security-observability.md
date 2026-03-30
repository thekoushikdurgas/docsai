# Tenant isolation, security posture, enterprise observability (Era 7 — Stages 7.6–7.8)

## Tenant isolation (current model)

- **Primary boundary:** authenticated user identity (`User.uuid`) from JWT — see `app/graphql/context.py`.
- **Data access:** Resolvers must scope queries by `user_id` / ownership (e.g. AI chats, uploads, resumes). Never trust client-supplied IDs without a DB ownership check.
- **Multi-tenant product (future):** explicit `tenant_id` on users and row-level policies — see Era 9 productization.

## Security posture (gateway)

| Control | Location |
| ------- | -------- |
| JWT access/refresh | `app/core/security.py`, auth mutations |
| CORS / trusted hosts | `app/main.py`, `CORSFriendlyTrustedHostMiddleware` |
| GraphQL complexity/depth | `GRAPHQL_*` settings, `app/graphql/extensions.py` |
| Rate limits | `GraphQLRateLimitMiddleware`, abuse guard — `docs/6. Contact360 Reliability and Scaling/performance-storage-abuse.md` |
| Idempotency (writes) | `docs/6. Contact360 Reliability and Scaling/slo-idempotency.md` |
| Production secrets | `SECRET_KEY` validation in `app/main.py` lifespan |

## Enterprise observability

- **Request correlation:** `X-Request-Id`, `X-Trace-Id` — `docs/6. Contact360 Reliability and Scaling/queue-observability.md`.
- **SLO snapshot:** `GET /health/slo` — `docs/6. Contact360 Reliability and Scaling/slo-idempotency.md`.
- **Structured logs:** JSON logging + optional Lambda Logs API — `LOG_*` settings.

## Hardening checklist

- 📌 Planned: No cross-user IDOR on GraphQL fields that return resources by ID.
- 📌 Planned: Introspection disabled in production if policy requires (`GRAPHQL_INTROSPECTION_ENABLED`).
- 📌 Planned: Secrets only via environment / secrets manager in production.
