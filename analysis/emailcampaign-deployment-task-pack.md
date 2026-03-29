# Email Campaign Service — Era 7.x Task Pack
## Contact360 Deployment

### Context
Era `7.x` formalises the deployment pipeline for all Contact360 services. The campaign service requires a production-grade Kubernetes deployment (two workloads: API + worker), secret management for SMTP credentials, environment promotion gates, and deployment rollback strategy.

---

## Track A — Contract

| Task | Description | Owner |
| --- | --- | --- |
| A-7.1 | Define Helm chart or Kubernetes manifests for API and worker deployments | DevOps |
| A-7.2 | Specify liveness vs readiness probe endpoints for each binary | DevOps + Backend |
| A-7.3 | Document secret management: SMTP credentials, JWT secret, AWS keys via Kubernetes Secret / Vault | DevOps |

## Track B — Service

| Task | Description | Owner |
| --- | --- | --- |
| B-7.1 | `/health` endpoint returns JSON with `{status, db, redis, s3_accessible}` | Backend |
| B-7.2 | Separate `/ready` probe that validates all dependencies ready before serving traffic | Backend |
| B-7.3 | RBAC: add role-based permission guards on campaign routes (`admin`, `member`, `read_only`) | Backend |
| B-7.4 | Audit log emission to `logs.api` per campaign-create, send-complete, unsubscribe events | Backend |

## Track C — Surface

| Task | Description | Owner |
| --- | --- | --- |
| C-7.1 | Deployment status badge visible in admin dashboard | Frontend |
| C-7.2 | Role-gated UI: non-admin users see campaigns read-only | Frontend |

## Track D — Data

| Task | Description | Owner |
| --- | --- | --- |
| D-7.1 | Postgres connection pool tuning parameters via env vars | DevOps |
| D-7.2 | Redis TLS and AUTH configuration for production | DevOps |

## Track E — Ops

| Task | Description | Owner |
| --- | --- | --- |
| E-7.1 | CI/CD pipeline: lint → test → build Docker images → push to registry → deploy API + worker | DevOps |
| E-7.2 | Blue-green or rolling update strategy for API; graceful draining for worker | DevOps |
| E-7.3 | Alert rules: campaign worker pod restart, Asynq queue depth spike, SMTP error rate | DevOps |

---

## Completion gate
- [ ] Both API and worker Dockerfiles build and run in Kubernetes.
- [ ] Secrets not in env files; mounted from secret store.
- [ ] RBAC role check tested: `admin`/`member` can create according to policy, `read_only` cannot.
- [ ] Audit events visible in `logs.api` for campaign create and send complete.
