# Runbook: satellite unhealthy (`satelliteHealth` red)

**Symptom:** `health.satelliteHealth` shows `error` for one named satellite (connectra, email, phone, …).

## Check

1. **Config** — `*_API_URL` and `*_API_KEY` set in gateway task definition.
2. **Network** — security groups allow gateway → EC2 host:port.
3. **Satellite** — SSH/SSM to host; `curl -s localhost:<port>/health` (or `/api/v1/health` for s3storage).

## Mitigate

- Restart service systemd unit or ECS task on satellite side.
- If Redis/Postgres dependency down, follow that provider’s playbook first.

## Comms

- Mark degraded in status page if customer-visible features break (e.g. Connectra down → CRM read/write).
