# Contact360 DocsAI Admin (Django)

Internal **admin.contact360.io** console for documentation, ops, jobs, and gateway-backed management. It talks to the central API gateway **[contact360.io/api](https://github.com/thekoushikdurgas/appointment360)** via **`GRAPHQL_URL`** (see [`docs/backend/endpoints/contact360.io/ROUTES.md`](../../docs/backend/endpoints/contact360.io/ROUTES.md) and [`AUTH-ENV.md`](../../docs/backend/endpoints/contact360.io/AUTH-ENV.md)).

## Quick start

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
cp .env.example .env
# Set DJANGO_ENV=development, SECRET_KEY, GRAPHQL_URL if needed
python manage.py migrate
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) (port may differ).

## Environment

| Variable | Purpose |
|----------|---------|
| `GRAPHQL_URL` | Gateway GraphQL endpoint (must end with `/graphql` or site root; see `config/settings/base.py` normalizer). Prefer **`https://api.contact360.io/graphql`** in production over HTTPS. |
| `GRAPHQL_INTERNAL_TOKEN` | Optional Bearer for server-to-server calls when no user session token is present. |
| `ALLOWED_HOSTS` | Include **`admin.contact360.io`** and **`34.201.10.84`** for the production EC2 + hostname. |
| `SECURE_SSL_REDIRECT` | Set **`true`** when serving over HTTPS (sets secure cookies; see `production.py`). |
| `CSRF_TRUSTED_ORIGINS` | e.g. `https://admin.contact360.io` when using HTTPS. |
| `AUTH_FALLBACK_LOCAL` | In production, default **`false`** — use gateway login; local Django staff only for break-glass. |

## Deploy

- **Hosts:** `http://34.201.10.84` (HTTP) and **`https://admin.contact360.io`** (TLS recommended).
- **Automation:** See [deploy/README.md](deploy/README.md) (`deploy-to-ec2.sh`, Gunicorn, Nginx).
- **Database:** Use PostgreSQL in production (`DATABASE_URL` in `.env` / `.env.prod`).

## Git

```bash
git remote add origin https://github.com/thekoushikdurgas/docsai.git
git branch -M docs
git push -u origin docs
```

## UI / CSS

Dashboard-style tokens and components live under [`static/admin/css/`](static/admin/css/) (`design-tokens.css`, `shell-eatio.css`, component partials). Conceptual alignment with the monorepo **Dashboard UI kit** ideas: [`docs/frontend/ideas/Dashboard ui kit`](../../docs/frontend/ideas/Dashboard%20ui%20kit).

## Related apps

- **User app:** [contact360.io/app](../app/README.md) → `app.contact360.io`
- **API gateway:** [contact360.io/api](../api/README.md) → `api.contact360.io`
