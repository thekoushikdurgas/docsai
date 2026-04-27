# Deployments and observability (ops)

## Deployments

The former Next.js `/admin/deployments` page was a stub (list/rollback not implemented against a real backend). **Deployments management is not exposed in the customer app.** When a product-backed deployments API exists, add a dedicated view under `admin_ops` that calls it (similar pattern to jobs and system health).

Operator-facing **GitHub Actions and EC2** flow (workflows, `remote-deploy.sh`, bootstrap): [github-actions-and-ec2-deploy.md](github-actions-and-ec2-deploy.md).

## Logs and observability

- **Django admin (`admin_ops`)** exposes **Logs** via the configured Logs HTTP API (`LOGS_API_URL`) and **Statistics** where implemented.
- **GraphQL `admin.logs`**, **`searchLogs`**, **`logStatistics`**, and **`userHistory`** remain available on the **gateway** for server-side tooling; they are no longer consumed by the Next.js app after the admin UI migration.
- If operators need a UI matching the old **Observability** tab (`logStatistics` time ranges), either extend `admin_ops` with GraphQL server-side calls (reuse the gateway token from the operator session) or use existing log analytics outside this repo.
