# Deployment Commands

Deployment command reference grouped by service family.

## Appointment360 (`contact360.io/api`)

```bash
cd contact360.io/api
sam validate --lint
sam build --use-container --no-cached
sam deploy \
  --parameter-overrides \
    DeploymentStrategy=Canary10Percent5Minutes \
    SecretKey=<SECRET_KEY> \
    DatabaseUrl=<DATABASE_URL> \
    LambdaLogsApiKey=<LOGS_API_KEY>
sam logs -n <FunctionName> --stack-name <StackName> --tail
```

Blue/green note:

- Use `DeploymentStrategy=Canary10Percent5Minutes` for production rollouts.
- Use `DeploymentStrategy=AllAtOnce` only for emergency fixes with explicit approval.

## Connectra (`contact360.io/sync`)

```bash
cd contact360.io/sync
go mod tidy
go test ./... -v
sam validate --lint
sam build --use-container --no-cached
sam deploy
```

## TKD Job (`contact360.io/jobs`)

```bash
cd contact360.io/jobs
pip install -e .
pytest
job-scheduler-py api
job-scheduler-py scheduler first_time
job-scheduler-py consumer
```

## Django Admin / DocsAI (`contact360.io/admin`)

```bash
cd contact360.io/admin
python manage.py check --deploy
python manage.py migrate
python manage.py collectstatic --noinput
```

## Next.js Apps (`contact360.io/app`, `contact360.io/root`, `contact360.io/email`)

```bash
npm ci
npm run build
npm run start
```

## Extension (`extension/contact360`)

```bash
cd extension/contact360
# Load unpacked in chrome://extensions
# Package with zip for distribution
```

## Lambda Services (`lambda/<service>`)

```bash
cd lambda/<service>
sam validate --lint
sam build --use-container --no-cached
sam deploy
sam list stack-outputs --stack-name <StackName>
```

## Core Lambda Services

```bash
cd lambda/emailapis && sam deploy
cd lambda/emailapigo && sam deploy
cd lambda/logs.api && sam deploy
cd lambda/s3storage && sam deploy
```

## Backend(dev) Services

```bash
cd "backend(dev)/contact.ai" && sam deploy
cd "backend(dev)/salesnavigator" && sam deploy
cd "backend(dev)/mailvetter" && <service_deploy_command>
cd "backend(dev)/email campaign" && <service_deploy_command>
```

## Go Services

```bash
go mod tidy
go test ./... -v
go build ./...
```

## Deployment Validation

```bash
curl https://<HOST_OR_DOMAIN>/health
```

## Notes

- Use placeholders for secrets and credentials.
- Keep deployment docs aligned with `docs/governance.md` and `docs/roadmap.md`.
- For service-specific deploy scripts, use each service README as the final authority.

## Small Task Breakdown

1. Run pre-deployment tests for target service.
2. Validate build artifacts (`sam validate`, build, or package).
3. Deploy to target environment.
4. Verify health and stack outputs.
5. Capture deployment evidence for release checklist.

## Deep Task Breakdown (All Codebases)

### A) Preflight

- Confirm branch/tag and release scope.
- Validate environment variables and credentials (placeholder-safe in docs).
- Validate infra dependencies (Docker, SAM, AWS profile, PM2/systemd where required).

### B) Build and Package

- Python: dependency install + tests + packaging/build.
- Node: `npm ci`, lint/type/test, build artifact generation.
- Go: module tidy, tests, binary build.

### C) Deploy

- Lambda services: `sam deploy` path.
- EC2/process services: deploy scripts + process restart.
- Frontend services: build + process manager restart.

### D) Verify

- Health endpoint checks.
- Service logs inspection.
- Key functional smoke checks.

### E) Evidence

- Capture deploy timestamp, commit SHA/tag, health output, and rollback reference.
