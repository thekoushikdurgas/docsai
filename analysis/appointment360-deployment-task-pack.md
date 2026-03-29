# Appointment360 (contact360.io/api) — Era 7.x Deployment Task Pack

## Contract track

| Task | Priority |
| --- | --- |
| Finalize environment variable naming convention across all `.env.*` files | P0 |
| Document EC2 vs Lambda execution differences in `README.md` | P0 |
| Define `/health` readiness contract for load balancer health checks | P0 |
| Specify Mangum Lambda event format and response envelope | P1 |
| Define resolver-level RBAC contract using `rbac-authz.md` role model (`admin`, `member`, `read_only`) | P0 |

---

## Service track

| Task | Priority |
| --- | --- |
| Validate Mangum handler Lambda cold-start time is < 3s | P0 |
| Add `lifespan` event handler (FastAPI `lifespan=`) for DB engine startup/shutdown | P0 |
| Configure `trusted_hosts` for production ALB host | P0 |
| Configure `CORS_ORIGINS` whitelist for production dashboard domain | P0 |
| Add graceful shutdown: complete in-flight requests before exit | P1 |
| Add health check-based deployment gate: Lambda alias swap only when `/health/db` passes | P0 |
| Configure Alembic to run migrations as separate Lambda invoke / ECS task (not at startup) | P1 |
| Add `--reload=false` for uvicorn production command | P0 |
| Enforce resolver and handler authz for privileged gateway mutations (no client-supplied role trust) | P0 |
| Emit audit evidence to `logs.api` for governance-sensitive mutations with actor + tenant + trace id | P0 |

---

## Surface track

| Task | Priority |
| --- | --- |
| Dashboard environment detection: use `NEXT_PUBLIC_GRAPHQL_URL` per deploy environment | P0 |
| Extension builds point to prod GraphQL endpoint (`wss://` for subscription readiness) | P1 |
| Dashboard graceful degradation when gateway is unreachable (network error boundary) | P1 |

---

## Data track

| Task | Priority |
| --- | --- |
| Ensure Alembic migration history is clean before production deploy | P0 |
| Create DB backup procedure before every migration | P0 |
| Add table index review for all high-frequency query patterns | P1 |

---

## Ops track

| Task | Priority |
| --- | --- |
| Write Dockerfile with multi-stage build: `pip install → copy app → CMD uvicorn` | P0 |
| Write `docker-compose.yml` for local dev: app + postgres + redis | P0 |
| Add GitHub Actions CI: lint (flake8/ruff), type-check (mypy), test (pytest) | P0 |
| Add GitHub Actions CD: build Docker → push ECR → deploy Lambda / EC2 | P1 |
| Set `ENVIRONMENT=production` guard: disable `DEBUG=true`, GraphiQL, introspection | P0 |
| Create Terraform / CDK module for appointment360 Lambda + ALB + RDS | P1 |
| Add CloudWatch alarm: Lambda invocation errors > 1% in 5 min | P1 |
| Document rollback procedure: previous Lambda version alias swap | P1 |

---

## Email app surface contributions (era sync)

- Standard Next.js build/start workflow defined for `contact360.io/email`.
- Environment dependency documented: `NEXT_PUBLIC_BACKEND_URL`.
- Deployment hardening tasks include environment validation and secure secret boundaries.
