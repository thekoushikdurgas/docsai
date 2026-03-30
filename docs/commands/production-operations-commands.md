# Production Operations Commands

Operational commands for health, logs, incident response, and rollback.

## Health Checks

```bash
curl https://<HOST_OR_DOMAIN>/health
curl https://<HOST_OR_DOMAIN>/health/db
```

## Service Health Targets

- `contact360.io/api`: `/health`, `/health/db`
- `contact360.io/admin`: Django app health endpoint or service status
- `contact360.io/app`, `contact360.io/root`, `contact360.io/email`: HTTP root and key route checks
- `contact360.io/sync`, `contact360.io/jobs`, `lambda/*`, `backend(dev)/*`: service health route and logs

## AWS / SAM Logs

```bash
sam logs -n <FunctionName> --stack-name <StackName> --tail
aws logs tail /aws/lambda/<FunctionName> --follow
```

## Service Logs

```bash
pm2 logs <app-process>
sudo journalctl -u <service-name> -f
```

## PM2 Operations (if applicable)

```bash
pm2 list
pm2 logs <process-name>
pm2 restart <process-name>
```

## System Services (if applicable)

```bash
sudo systemctl status <service-name>
sudo systemctl restart <service-name>
```

## Rollback Pattern

```bash
git checkout <known-good-tag>
<build-command>
<restart-command>
```

## Frontend Rollback Pattern

```bash
git checkout <known-good-tag>
npm ci
npm run build
pm2 restart <process-name>
```

## Lambda Rollback Pattern

```bash
aws cloudformation describe-stacks --stack-name <StackName>
# redeploy known-good artifact or stack version
sam deploy
```

## Incident First Commands

```bash
date
git rev-parse HEAD
curl -I https://<HOST_OR_DOMAIN>
```

## Operational Guardrails

- Do not run destructive database commands in production from docs defaults.
- Always capture request IDs / trace IDs when triaging.
- Keep rollback references aligned with version tags from `docs/versions.md`.

## Small Task Breakdown

1. Confirm incident scope (service and environment).
2. Collect health and logs.
3. Identify last known good tag/commit.
4. Roll forward or rollback based on impact.
5. Verify health and close with evidence.

## Deep Task Breakdown (Incident Operations)

### I) Detection

- Confirm incident with health checks and user-facing signal.
- Identify impacted services and blast radius.

### II) Triage

- Gather logs and request/trace IDs.
- Correlate with deploy history and config changes.

### III) Mitigation

- Apply immediate mitigation (restart, rollback, traffic control).
- Validate partial recovery before full closure.

### IV) Recovery Validation

- Run health and smoke checks.
- Verify no regression in connected services.

### V) Closure

- Document timeline, root cause summary, mitigation command list, and follow-up tasks.
