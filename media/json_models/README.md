# JSON Models Documentation (DocsAI)

This folder documents the **JSON models** used for each resource type in the Contact360 DocsAI codebase. Use these as the reference for structure, fields, validation, and storage.

| Document | Resource | Storage | Canonical schema |
|----------|----------|---------|-------------------|
| [pages_json_models.md](./pages_json_models.md) | Documentation pages | `media/pages/*.json` | Pydantic (`schemas/pydantic/models.py`) |
| [endpoints_json_models.md](./endpoints_json_models.md) | API endpoint docs | `media/endpoints/*.json` | Pydantic (`schemas/pydantic/models.py`) |
| [postman_json_models.md](./postman_json_models.md) | Postman configurations | `media/postman/*.json` | Pydantic (`schemas/pydantic/postman_models.py`) |
| [project_json_models.md](./project_json_models.md) | Project inventories & reports | `media/project/*.json` | None (script-generated) |
| [relationship_json_models.md](./relationship_json_models.md) | Page–endpoint relationships | `media/retations/*.json` | Pydantic (`schemas/pydantic/models.py`) |
| [n8n_json_models.md](./n8n_json_models.md) | n8n workflows | `media/n8n/**/*.json` | None (n8n export format) |

- **Pydantic-validated**: pages, endpoints, postman, relationship — use `lambda_models.validate_*` before persist.
- **No schema**: project (valid JSON only), n8n (lightweight structural check + optional `workflow_id`).

Path helpers: `apps/documentation/utils/paths.py` (`get_pages_dir`, `get_endpoints_dir`, `get_postman_dir`, `get_project_dir`, `get_relationships_dir`, `get_n8n_dir`).
