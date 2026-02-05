# DocsAI Commands Reference

This document lists **all commands** available in the DocsAI project: Django management commands (custom and standard), npm scripts, and key scripts in `scripts/` and `deploy/`.

---

## 1. Django management commands (custom)

Run from project root: `python manage.py <command> [options]`.

### Core app (`apps.core.management.commands`)

| Command | Purpose | Options |
|---------|---------|---------|
| **validate_env** | Validate environment (Django, DB, AWS S3, GraphQL, Logs/Lambda API, AI, storage, cache, Django-Q); optional connectivity checks | `--skip-connectivity`, `--verbose` |
| **check_best_practices** | Run 100-point Django best-practices checklist (uses `scripts/django_checker.py`) | `--category "Security"`, `--output reports/check.json`, `--format json\|text\|both` |
| **create_superuser** | Legacy helper to create a Django superuser (used only for debugging/admin, not for main DocsAI access) | `--username`, `--email`, `--password`, `--noinput` |
| **sync_from_lambda** | Sync docs from Lambda API to S3 (pages, endpoints, relationships) | `--resource-type pages\|endpoints\|relationships\|all`, `--limit N` (default 100) |
| **rebuild_indexes** | Rebuild S3 indexes by scanning files | `--resource-type pages\|endpoints\|relationships\|all` |

### Documentation app (`apps.documentation.management.commands`)

| Command | Purpose | Options |
|---------|---------|---------|
| **normalize_media_indexes** | Normalize all index JSON under media; regenerate index.json, normalize full index files and relationship entries | `--write` (default dry-run) |
| **normalize_media_postman_n8n** | Normalize Postman configs and n8n workflow JSON under media | `--write`, `--skip-postman`, `--skip-n8n` |
| **normalize_media_relationships** | Normalize relationship JSON in media (Pydantic validators) | `--write` |
| **normalize_media_files** | Top-level media normalization: runs normalize_media_pages_endpoints, normalize_media_relationships, normalize_media_postman_n8n; validates remaining JSON | `--write` |
| **normalize_media_pages_endpoints** | Normalize pages and endpoints JSON in media (Pydantic validators) | `--write`, `--resources pages endpoints` |
| **import_pages** | Import documentation pages from markdown files in `docs/docs_ai_agent/docs/pages` (repo root relative) | (none) |

### Durgasflow app (`apps.durgasflow.management.commands`)

| Command | Purpose | Options |
|---------|---------|---------|
| **build_n8n_index** | Scan `media/n8n` for workflow JSON and build `index.json` for listing | `--force`, `--limit N` |

### Durgasman app (`apps.durgasman.management.commands`)

| Command | Purpose | Options |
|---------|---------|---------|
| **import_test** | Test Durgasman import (Postman collection/env, endpoint JSON) with sample data | `--type postman\|endpoints\|all`, `--user-id N` |
| **demo_data** | Create demo data for Durgasman (collections, API requests, environments) | (none) |

---

## 2. Standard Django commands (common)

| Command | Purpose |
|---------|---------|
| `makemigrations` | Create migrations |
| `migrate` | Apply migrations |
| `showmigrations` | Show migration status |
| `sqlmigrate <app> <migration>` | Show SQL for a migration |
| `createsuperuser` | Create superuser (Django built-in) |
| `changepassword <username>` | Change user password |
| `runserver` [port] | Development server; can start Django-Q cluster. Options: `--skip-qcluster`, `--skip-server`, `--noreload` |
| `qcluster` | Start Django-Q worker cluster |
| `qmonitor` | Monitor Django-Q tasks |
| `collectstatic` | Collect static files. Options: `--noinput`, `--clear` |
| `test` | Run Django test runner |
| `dbshell` | Database shell |
| `shell` | Django shell |

---

## 3. npm scripts (`package.json`)

| Script | Purpose |
|--------|---------|
| `npm run build-css` | Build Tailwind CSS (watch mode) |
| `npm run build-css-prod` | Build Tailwind CSS for production (minified) |
| `npm run test` | Run Jest tests |
| `npm run test:watch` | Jest watch mode |
| `npm run test:coverage` | Jest with coverage |

---

## 4. Root-level script

| File | Purpose |
|------|---------|
| **build-css.bat** | Runs `npm run build-css-prod` (Tailwind production build) |

---

## 5. Scripts in `scripts/` (batch / runner)

| Script | Purpose |
|--------|---------|
| **check_django_best_practices.bat** | Run `django_checker.py` on project root; reports to `reports/` |
| **check_code_organization.bat** | Code organization checks |
| **check_deployment.bat** | Deployment checks |
| **check_models_database.bat** | Models/DB checks |
| **check_performance.bat** | Performance checks |
| **check_project_structure.bat** | Project structure checks |
| **check_security.bat** | Security checks |
| **check_testing.bat** | Testing checks |
| **check_views_apis.bat** | Views/API checks |
| **generate_check_report.bat** | Generate check report |
| **start_django_q_worker.bat** | Start Django-Q cluster (Windows; venv + `manage.py qcluster`) |
| **start_django_q_worker.sh** | Same for Linux/Mac |
| **integration_test.sh** | Integration test runner |

---

## 6. Scripts in `scripts/` (Python utilities)

| Script | Purpose |
|--------|---------|
| **django_checker.py** | 100-point Django best-practices checker (used by `check_best_practices` management command) |
| **validate_setup.py** | Validate files/dependencies before deployment |
| **run_tests.py** | Test runner |
| **generate_openapi_schema.py** | Generate OpenAPI schema |
| **generate_postman_collection.py** | Generate Postman collection |
| **list_api_v1_get_routes.py** | List API v1 GET routes |
| **rebuild_indexes.py** | Rebuild indexes (script version) |
| **seed_documentation_pages.py** | Seed documentation pages |
| **upload_all_docs_to_s3.py** | Upload all docs to S3 |
| **upload_docs_pages_to_s3.py** | Upload docs pages to S3 |
| **upload_docs_endpoints_to_s3.py** | Upload docs endpoints to S3 |
| **upload_docs_relationships_to_s3.py** | Upload docs relationships to S3 |
| **upload_index_files_to_s3.py** | Upload index files to S3 |
| **upload_json_to_s3.py** | Upload JSON to S3 |
| **generate_s3_json_files.py** | Generate S3 JSON files |
| **build_complete_collection.py** | Build complete (Postman) collection |
| **migrate_media_to_documentation_api.py** | Migrate media to documentation API |
| **migrate_routes.py** | Migrate routes |
| **validate_media_structure.py** | Validate media structure |

See **scripts/README.md** for full list and usage.

---

## 7. Deploy scripts (`deploy/`)

| Script | Purpose |
|--------|---------|
| **deploy.sh** | Master deploy for EC2/Ubuntu. Usage: `./deploy/deploy.sh <domain> <email>` or `./deploy/deploy.sh --http-only` |
| **deploy-to-ec2.sh** | Deploy to EC2 |
| **full-deploy.sh** | Full deployment |
| **remote-deploy.sh** | Remote deployment |
| **pre-deployment-check.sh** | Pre-deployment checks |
| **post-deployment-verify.sh** | Post-deployment verification |
| **setup-s3.sh** | S3 setup |
| **troubleshoot-gunicorn.sh** | Gunicorn troubleshooting |
| **nginx/install-nginx.sh** | Install Nginx |
| **systemd/install-systemd.sh** | Install systemd units |
| **ssl/setup-ssl.sh** | SSL setup |
| **logrotate/install-logrotate.sh** | Logrotate setup |

See **deploy/README.md** and **deploy/QUICK_START.md** for usage.

---

## 8. CI / tooling (from README / pyproject)

| Command | Purpose |
|---------|---------|
| `pytest` | Run tests (recommended) |
| `pytest --cov=apps --cov-report=html` | Tests with coverage |
| `black .` | Format code |
| `isort .` | Sort imports |
| `ruff format --check`, `ruff check` | Lint/format check |
| `mypy apps/` | Type checking |
| `pre-commit install`, `pre-commit run --all-files` | Pre-commit hooks |
| `gunicorn config.wsgi:application --bind 0.0.0.0:8000` | Run app in production |

---

## Related docs

- **README.md** – Quick Start, Management Commands summary
- **scripts/README.md** – Scripts directory structure and usage
- **deploy/README.md** – Deployment overview
- **API & routes:** [api.md](./api.md), [routes.md](./routes.md), [routes.txt](../routes.txt)
