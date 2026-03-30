# Security — Contact360 repository

## Committed secrets

If you ever committed real credentials (AWS keys, DB passwords, JWT secrets, API keys), **rotate them immediately** in the provider (AWS IAM, RDS, etc.) and **remove** them from git history if they were public (e.g. `git filter-repo` or BFG). This repo uses **placeholders** in code defaults; production values must come from **environment variables** or **AWS Secrets Manager / SSM Parameter Store**.

### Docs tooling config (`docs/scripts/config.json`)

Data/SQL helpers read PostgreSQL and S3 settings from `docs/scripts/config.json` (created on first run) and from **environment variables**, which override file values: `POSTGRES_*`, `DOCS_PG_*`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`, `DOCS_S3_BUCKET`, etc. **Never commit** real passwords or long-lived cloud keys into `config.json` or defaults under version control.

## Local development

- Copy each service’s `.env.example` to `.env` and fill in values.
- Do **not** commit `.env` or `samconfig.toml` (see root `.gitignore`).

## Production

- Restrict `ALLOWED_ORIGINS` and `TRUSTED_HOSTS` on the GraphQL API.
- Use IAM instance roles or task roles for S3 — avoid long-lived `AWS_ACCESS_KEY_ID` in env files.
