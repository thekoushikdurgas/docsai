# CI Required Checks (0.10)

This document freezes the required CI checks for foundation release gating.

Job IDs below match the `jobs:` keys in [`docs/.github/workflows/ci.yml`](../../.github/workflows/ci.yml) (monorepo CI). If workflows move or rename jobs, update this list in the same change.

## Required checks

1. `docs-and-structure-check`
2. `migration-smoke`
3. `health-smoke`
4. `lint-smoke`
5. `secret-scan`
6. `sam-validate`

## What each check enforces

- `docs-and-structure-check`: required top-level repo layout and canonical docs files.
- `migration-smoke`: Alembic migrations for `contact360.io/jobs`, `contact360.io/api`, and `backend(dev)/contact.ai` on an empty PostgreSQL database.
- `health-smoke`: targeted health endpoint tests for gateway/storage/integration services.
- `lint-smoke`: syntax lint baseline (`compileall`) across Python service packages.
- `secret-scan`: repository secret leakage scanning with Gitleaks.
- `sam-validate`: `sam validate --lint` across SAM templates for lambda/service packages.

## Lambda SAM templates covered

- `contact360.io/api/template.yaml`
- `lambda/emailapis/template.yaml`
- `lambda/emailapigo/template.yaml`
- `lambda/logs.api/template.yaml`
- `lambda/s3storage/template.yaml`
- `backend(dev)/salesnavigator/template.yaml`
- `backend(dev)/contact.ai/template.yaml`
- `backend(dev)/resumeai/template.yaml`
- `extension/contact360/template.yaml`
