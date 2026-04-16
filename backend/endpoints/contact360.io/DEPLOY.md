# Deploy

- **Hosts:** `api.contact360.io`, `98.84.125.120`
- **Process:** Uvicorn `app.main:app` port **8000**; systemd unit `appointmentbackend` (see `deploy/appointmentbackend.service`).
- **Nginx:** `deploy/nginx-appointment360.conf` — proxy to `localhost:8000`, large body for GraphQL, `/graphql` buffering off.
- **TLS:** Uncomment HTTPS `server` block and HTTP→HTTPS redirect after Certbot; HSTS only on TLS listener.
- **CI/CD:** `contact360.io/api/.github/workflows/deploy.yml` — SSH to EC2, `git pull`, `deploy/remote-deploy.sh` (venv, `alembic upgrade head`, restart service).
- **Monorepo paths:** Workflow includes both `app/**` and `contact360.io/api/**` path filters.

Git remote: `https://github.com/thekoushikdurgas/appointment360.git` (branch `main`).
