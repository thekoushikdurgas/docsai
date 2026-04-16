# Connectra (`sync.server`) — deployment

## Ports

- **Container API:** listens on **8000** (`cmd/server.go`).
- **docker-compose:** maps `8000:8000` by default. To expose **3000** externally: `"3000:8000"` under the `api` service.
- **Gateway:** set `CONNECTRA_BASE_URL` in `contact360.io/api` to the public URL (include port).

## GitHub Actions

Workflow: [`EC2/sync.server/.github/workflows/deploy.yml`](../../../EC2/sync.server/.github/workflows/deploy.yml)

Required secrets:

| Secret | Purpose |
|--------|---------|
| `EC2_HOST` | SSH host |
| `EC2_USER` | SSH user |
| `EC2_SSH_KEY` | private key |
| `ENV_FILE` | full `.env` contents written on server |

Remote path: `/home/$EC2_USER/connectra.server` (must match repo layout).

## Stack on EC2

`docker compose up --build -d` starts:

- `api` — Gin HTTP API  
- `worker` — Asynq consumer (`RUN_COMMAND=jobs`)  
- `redis` — queues + job cache  
- `asynqmon` — optional UI on **8080**

## Health

`GET /health` returns `200` when Postgres, Redis, and OpenSearch all ping OK; `503` with `dependencies` detail if any check fails.
