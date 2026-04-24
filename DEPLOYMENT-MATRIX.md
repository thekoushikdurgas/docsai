# Deployment matrix (ECS-first)

**Owner:** platform · **Last reviewed:** 2026-04-24  
**Anchor:** [`DECISIONS.md`](DECISIONS.md) § ECS vs EKS — **default ECS Fargate** for stateless services; EC2 hosts satellites listed below.

This matrix maps **product components** → **repository / artifact** → **runtime** → **primary env vars** (see each service `AUTH-ENV.md`). Keep in sync with [`backend/endpoints/contact360.io/SATELLITE-PARITY.md`](backend/endpoints/contact360.io/SATELLITE-PARITY.md).

| Component | Repo / path | Artifact | Typical deploy target | Credential boundary |
| --------- | ----------- | -------- | --------------------- | ------------------- |
| **Gateway API** | `contact360.io/api` | Docker image → ECS service | ECS Fargate (or EC2) | JWT to callers; `X-API-Key` to satellites |
| **Dashboard** | `contact360.io/app` | Static / Node SSR | ECS or Vercel-style host | Browser → gateway only |
| **Admin** | `contact360.io/admin` | Docker | ECS | Operator JWT to gateway `POST /graphql`; **no satellite `X-API-Key` on admin in steady state** ([`ADMIN-MODULE.md`](backend/endpoints/contact360.io/ADMIN-MODULE.md), [`codebases/admin.md`](codebases/admin.md)) |
| **Connectra** (`sync.server`) | `EC2/sync.server` | Go binary + systemd, or container | **EC2** (reference) | `CONNECTRA_API_KEY` on gateway |
| **extension.server** | `EC2/extension.server` | Go binary | EC2 | `EXTENSION_API_KEY` |
| **email.server** | `EC2/email.server` | Go binary + worker | EC2 | `EMAIL_SERVER_API_KEY` |
| **phone.server** | `EC2/phone.server` | Go binary + worker | EC2 | `PHONE_SERVER_API_KEY` |
| **ai.server** | `EC2/ai.server` | Go binary + worker | EC2 | `AI_API_KEY` |
| **campaign.server** | `EC2/campaign.server` | Go binary + worker | EC2 | `CAMPAIGN_API_KEY` |
| **s3storage.server** | `EC2/s3storage.server` | Go binary + worker | EC2 | `S3STORAGE_SERVER_API_KEY` |
| **log.server** | `EC2/log.server` | Go binary + worker | EC2 | `LOGS_SERVER_API_KEY` |
| **job.server** (Hiring signal) | `EC2/job.server` | Go API + `cmd/worker` | **EC2** (Mongo + Redis) | `JOB_SERVER_API_KEY` |
| **proxy.server** | `unihost/proxy.server` | Go binary + worker | EC2 / unihost | `PROXY_SERVER_API_KEY` |
| **Chrome extension** | `contact360.io/extension` (or root extension pkg) | `.zip` Chrome Web Store | Client | JWT to gateway |

### CI → release

- Gateway and apps: GitHub Actions under each app’s `.github/workflows/` (see Phase 0 [`README`](0.Foundation%20and%20pre-product%20stabilization%20and%20codebase%20setup/README.md)).
- Satellites: `EC2/<service>/.github/workflows/deploy.yml` and root `.github/workflows/deploy-<name>.yml` where present.

### EKS note

EKS is **reserved** per `DECISIONS.md` until mesh/GPU/multi-region drivers appear. Do not fork deployment docs into an EKS-only path without updating this matrix.
