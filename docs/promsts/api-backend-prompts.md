# API and Backend Prompts

## Endpoint Contract Prompt

- **Services:** `contact360.io/api`, `contact360.io/admin`, lambdas, backend(dev) services
- **Prompt:** Implement or update endpoint contract with validation, auth checks, error model, and docs.
- **Outputs:** endpoint code, tests, docs updates
- **Small Tasks:** design contract -> implement -> test -> document

## Data Integrity Prompt

- **Services:** API + data writers (`contact360.io/sync`, `contact360.io/jobs`, `lambda/*`)
- **Prompt:** Validate schema assumptions and guard against malformed/duplicate records.
- **Outputs:** guardrails, error handling, data consistency checks
- **Small Tasks:** identify invariants -> enforce checks -> add tests
