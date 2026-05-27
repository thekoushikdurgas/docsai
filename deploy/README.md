# EC2 deploy scripts (Contact360 Admin)

| Script                 | Who runs            | Purpose                                                                 |
| ---------------------- | ------------------- | ----------------------------------------------------------------------- |
| `ec2-setup.sh`         | `sudo`              | One-time server: Node 20, PM2, nginx, UFW (once per host).            |
| `ec2-deploy.sh`        | app user (`ubuntu`) | Interactive first deploy: `npm install`, `next build`, PM2 start.       |
| `ec2-update.sh`        | app user            | Interactive update: `git pull`, rebuild, `pm2 reload`.                  |
| `ec2-github-deploy.sh` | app user / CI       | Non-interactive PM2 deploy (`npm ci`, build, PM2). Port **3000**.       |
| `lib.sh`               | _(sourced)_         | Shared helpers — **do not execute directly**.                           |

## Dedicated admin EC2 (production)

- **Host:** `18.207.217.168`
- **Domain:** `admin.contact360.io`
- Admin PM2: `contact360-admin` on port **3000**
- Nginx: `ec2-nginx-admin.conf` → `127.0.0.1:3000`

Full bootstrap: [EC2-ADMIN-HOST.md](./EC2-ADMIN-HOST.md)

## Same host as dashboard (legacy layout)

- Dashboard PM2: `contact360-dashboard` on port **3000**
- Admin PM2: `contact360-admin` on port **3001**
- Nginx: `ec2-nginx-admin.conf` (change `proxy_pass` to `:3001` if co-located)

## GitHub Actions

- **Monorepo**: [`.github/workflows/deploy-contact360-admin.yml`](../../../.github/workflows/deploy-contact360-admin.yml) on pushes under `contact360.io/admin/**`
- **Standalone**: [`.github/workflows/deploy.yml`](../.github/workflows/deploy.yml)

Set repository variable **`EC2_ADMIN_PATH`** (default `$HOME/contact360-admin`).

## Required files in admin root

- `package.json`, `next.config.ts`, `ecosystem.config.js`
- `.env.production` — copy from `.env.production.example`

## Environment variables

| Variable           | Meaning                                              |
| ------------------ | ---------------------------------------------------- |
| `PORT`             | Listen port (default `3000` on dedicated admin EC2)  |
| `PM2_APP_NAME`     | PM2 process name (default `contact360-admin`)        |
| `API_HEALTH_URL`   | Optional curl health check after deploy              |
| `SKIP_DB_CHECK`    | N/A — admin has no DB; API health only               |

## Nginx

See `ec2-nginx-admin.conf`.
