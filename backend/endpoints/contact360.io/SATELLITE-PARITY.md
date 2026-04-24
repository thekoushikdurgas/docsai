# Satellite parity (gateway)

**Last reviewed:** 2026-04-24 — keep aligned with [`../../../DECISIONS.md`](../../../DECISIONS.md).

| Satellite | GraphQL surface | Client | Transport / auth | Health probe |
|-----------|-----------------|--------|------------------|--------------|
| sync.server (Connectra) | `contacts`, companies, jobs, VQL | `ConnectraClient` | HTTPS; **`X-API-Key`** | `GET /health` → `satelliteHealth` **connectra** |
| email.server | `email` | `EmailServerClient` | HTTPS; **`X-API-Key`** | `GET /health` → **email** |
| phone.server | **`phone`** | `PhoneServerClient` | HTTPS; **`X-API-Key`** | `GET /health` → **phone** |
| ai.server | `aiChats` | `AIServerClient` | HTTPS; **`X-API-Key`** | `GET /health` → **ai_server** |
| s3storage.server | `s3`, `upload` | `S3StorageEC2Client` | HTTPS; **`X-API-Key`** | `GET /api/v1/health` → **s3storage** |
| log.server | `admin` logs | `LogsServerClient` | HTTPS; **`X-API-Key`** | `GET /health` → **logs** |
| extension.server | `salesNavigator` | `SalesNavigatorServerClient` | HTTPS; **`X-API-Key`** | `GET /health` → **sales_navigator** |
| campaign.server | `campaignSatellite`, `campaigns` | `CampaignServiceClient` | HTTPS; **`X-API-Key`**; CQL + preview | `GET /health` → **campaign** |
| **job.server** (Hiring signal) | **`hireSignal`** | `JobServerClient` | HTTPS; **`X-API-Key`** | `GET /health` → **job_server** |
| proxy.server | _(future / REST direct)_ | `ProxyServerClient` (planned) | HTTPS; **`X-API-Key`**; REST `/api/v1/*` | `GET /health` → **proxy** _(add to `satelliteHealth` when wired)_ |

## Gateway aggregation

Authenticated GraphQL query **`health.satelliteHealth`** returns a row per configured satellite (skipped when URL/key missing). Use for dashboards and on-call quick checks.

## Deploy target

Satellites default to **EC2** + systemd in reference deployments; **ECS Fargate** applies to stateless gateway/app tiers per [`../../../DEPLOYMENT-MATRIX.md`](../../../DEPLOYMENT-MATRIX.md).
