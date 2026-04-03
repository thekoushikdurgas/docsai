# Health Envelope Matrix (0.10)

This document freezes the expected `/health` response families across the 11 core services and maps them to the health matrix compose.

## Compose matrix

- Local matrix compose: `docker-compose.health-matrix.yml`
- Goal: boot all core services and probe their canonical health endpoint.

## Service matrix

| Service | Family | Health endpoint | Required fields |
| --- | --- | --- | --- |
| Contact360 gateway (`contact360.io/api`) | FastAPI gateway | `/health` | `status`, `service`, `version` |

On success, the gateway sets `status` to `"healthy"` (not `"ok"`); see `app/main.py` `health_check`. Failure responses may use `status: "unhealthy"` with extra fields.
| Connectra (`contact360.io/sync`) | Go/Gin | `/health` | `status` |
| TKD Job (`contact360.io/jobs`) | FastAPI jobs | `/health` | `status` |
| Email APIs (`lambda/emailapis`) | FastAPI lambda-style | `/health` | `status`, `service`, `version` |
| Email API Go (`lambda/emailapigo`) | Go/Gin | `/health` | `status`, `service`, `version` |
| Logs API (`lambda/logs.api`) | FastAPI logging | `/health` | `status`, service identity fields |
| S3 Storage (`lambda/s3storage`) | FastAPI storage | `/api/v1/health` | `status`, storage connectivity field |
| Sales Navigator (`backend(dev)/salesnavigator`) | FastAPI integration | `/v1/health` | `status`, `service`, `version` |
| Contact AI (`backend(dev)/contact.ai`) | FastAPI AI | `/health` | `status`, database connectivity field |
| ResumeAI (`backend(dev)/resumeai`) | FastAPI AI | `/v1/health` | `status`, `service` |
| Mailvetter (`backend(dev)/mailvetter`) | Go/Gin verifier | `/v1/health` | `status`, `service`, `version` |

## Envelope families

### 1) Minimal Go/Gin envelope

```json
{
  "status": "ok"
}
```

### 2) Service identity envelope

```json
{
  "status": "ok",
  "service": "Service Name",
  "version": "x.y.z"
}
```

### 3) Component-aware envelope

```json
{
  "status": "ok",
  "diagnostics": {
    "component": true
  }
}
```

## 0.10 acceptance checks

1. `docker compose -f docker-compose.health-matrix.yml up -d`
2. Each container health status is `healthy`.
3. Every endpoint in the table returns HTTP `200` with required fields.
4. Any service-specific extra fields are allowed, but required fields must remain stable.
