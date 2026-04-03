# Email Campaign API (REST)

**Last updated**: March 28, 2026  
**Service path**: `backend(dev)/email campaign`  
**Role**: Campaign queueing, templates (S3-backed), recipients, SMTP send path, unsubscribe/suppression.

## Documentation map

| Doc | Purpose |
| --- | --- |
| [SERVICE_TOPOLOGY.md](../endpoints/SERVICE_TOPOLOGY.md) | Campaign services in the platform graph |
| [emailcampaign_endpoint_era_matrix.md](../endpoints/emailcampaign_endpoint_era_matrix.md) | Era matrix (Markdown); JSON sibling in same folder |
| [emailcampaign_data_lineage.md](../database/emailcampaign_data_lineage.md) | Data ownership |
| [ENDPOINT_DATABASE_LINKS.md](../endpoints/ENDPOINT_DATABASE_LINKS.md) | GraphQL campaign ops ↔ DB scope |
| [s3storage.api.md](s3storage.api.md) | Template and artifact storage |

### Also in `docs/backend/endpoints/`

- **[README.md](../endpoints/README.md)** — endpoint metadata workflow.
- **[endpoints_index.md](../endpoints/endpoints_index.md)** — [emailcampaign_endpoint_era_matrix.md](../endpoints/emailcampaign_endpoint_era_matrix.md); product GraphQL for campaigns/sequences/templates: [index.md](../endpoints/index.md) (`graphql/*Campaign*`, `graphql/*Sequence*`, `graphql/*CampaignTemplate*`).
- **JSON source** — `emailcampaign_endpoint_era_matrix.json` (same folder as the `.md` mirror).

## Canonical references

- GraphQL-facing product docs: `docs/backend/apis/22_CAMPAIGNS_MODULE.md`, `24_SEQUENCES_MODULE.md`, `25_CAMPAIGN_TEMPLATES_MODULE.md`
- Endpoint era matrix: `docs/backend/endpoints/emailcampaign_endpoint_era_matrix.json`
- Data lineage: `docs/backend/database/emailcampaign_data_lineage.md`
- Runtime analysis: `docs/codebases/emailcampaign-codebase-analysis.md`

## Contract notes

- Treat **REST handlers** under this service as the source of truth for campaign HTTP semantics until a full OpenAPI file is checked in here.
- Keep **status vocabulary** aligned across docs, Go workers, and UI (`pending`, `sending`, `completed`, `failed`, `paused`, and any `completed_with_errors` once implemented).
- Prefer **s3storage** for new object workflows; document direct S3 usage as debt where it still exists in code.

## Auth

- Document per-deployment keys and admin middleware (e.g. `RequireAdminAPIKey`) in the same PR as handler changes.

## Small maintenance tasks

1. Diff `api/handlers.go`, `worker/campaign_worker.go`, `worker/email_worker.go` vs this folder’s module docs each release.
2. Update `emailcampaign_endpoint_era_matrix.json` when routes or era ownership change.
3. Sync Postman under `docs/backend/postman/Email Campaign API/` when request samples change.
