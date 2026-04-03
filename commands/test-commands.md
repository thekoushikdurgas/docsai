# Test Commands

## Python Services

```bash
pytest
pytest -v
pytest --cov=app --cov-report=term-missing
```

## Appointment360 (`contact360.io/api`)

```bash
cd contact360.io/api
pytest tests/ -v
pytest tests/graphql/ -v
ruff check app
mypy app
```

## Connectra (`contact360.io/sync`)

```bash
cd contact360.io/sync
go test ./... -v
golangci-lint run
go fmt ./...
```

## TKD Job (`contact360.io/jobs`)

```bash
cd contact360.io/jobs
pytest
pytest tests/unit/ -v
pytest tests/integration/ -v
```

## Django (`contact360.io/admin`)

```bash
cd contact360.io/admin
pytest
python manage.py check
python manage.py check --deploy
```

## Next.js Apps

```bash
npm run test
npm run test:coverage
npm run test:e2e
```

## Frontend Codebases

```bash
cd contact360.io/app && npm run test && npm run typecheck && npm run lint
cd contact360.io/root && npm run test && npm run typecheck && npm run lint
cd contact360.io/email && npm run test && npm run typecheck && npm run lint
```

## Go Services

```bash
go test ./... -v
```

## Lambda and Backend(dev) Services

```bash
cd lambda/emailapis && pytest tests/ -v
cd lambda/emailapigo && go test ./... -v
cd lambda/logs.api && pytest tests/ -v
cd lambda/s3storage && pytest tests/ -v
cd "backend(dev)/contact.ai" && pytest tests/ -v
cd "backend(dev)/salesnavigator" && pytest tests/ -v
cd "backend(dev)/mailvetter" && <service_test_command>
cd "backend(dev)/email campaign" && <service_test_command>
```

## Lint and Type Safety

```bash
ruff check .
ruff format .
mypy .
npm run lint
npm run typecheck
```

## Minimum Pre-Release Test Gate

- Unit tests pass
- Integration tests pass
- Lint/type checks pass
- Core health endpoints return expected status

## Small Task Breakdown

1. Run unit tests.
2. Run integration and e2e tests where available.
3. Run lint and type checks.
4. Fix regressions and rerun.
5. Attach test evidence to release cut.

## Deep Task Breakdown (Test Strategy)

### 1) Contract-Level Tests

- API contract tests (GraphQL/REST schema and status mappings)
- Backward compatibility checks for critical fields

### 2) Service-Level Tests

- Unit tests per service
- Integration tests for service dependencies (DB, queue, storage, external clients)

### 3) Surface-Level Tests

- Dashboard/marketing/email UI unit and e2e checks
- Extension flow smoke checks

### 4) Non-Functional Checks

- Lint and type checks
- Basic performance smoke for critical paths where available

### 5) Release Evidence

- Include command outputs, pass/fail summary, and unresolved exceptions (if any)
