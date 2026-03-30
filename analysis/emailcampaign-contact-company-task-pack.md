# Email Campaign Service — Era 3.x Task Pack
## Contact360 Contact and Company Data System

### Context
Era `3.x` introduces Connectra as the canonical source of truth for contacts and companies. The email campaign service must replace its CSV file-path audience model with Connectra-query-based or saved-segment-based recipient resolution, ensuring clean data lineage from source to delivered email.

---

## Track A — Contract

| Task | Description | Owner |
| --- | --- | --- |
| A-3.1 | Define audience source contract: `segment_id` OR `vql_query` OR `csv_upload` (priority order) | Backend + Product |
| A-3.2 | Specify Connectra API call for recipient resolution: `POST /contacts/search` with VQL | Backend |
| A-3.3 | Document recipient field mapping from Connectra `Contact` to `recipients` table schema | Backend |
| A-3.4 | Define per-campaign deduplication policy (Connectra UUID5 → recipient id) | Backend |

## Track B — Service

| Task | Description | Owner |
| --- | --- | --- |
| B-3.1 | Update `CampaignPayload` to support `audience_source`: `"segment"`, `"vql"`, or `"csv"` | Backend |
| B-3.2 | Implement `ResolveAudience(source)` function that calls Connectra `/contacts/search` | Backend |
| B-3.3 | Map Connectra `Contact` → `Recipient` struct: `id` = UUID5 from email, `name` = FirstName + LastName | Backend |
| B-3.4 | Keep CSV fallback path intact for backwards compatibility; deprecation flag | Backend |
| B-3.5 | Persist resolved audience list in recipients table before enqueueing worker | Backend |

## Track C — Surface

| Task | Description | Owner |
| --- | --- | --- |
| C-3.1 | Campaign wizard: audience step — "Use saved segment", "Run VQL query", or "Upload CSV" radio buttons | Frontend |
| C-3.2 | Audience step: contact count preview when segment/VQL selected (calls Connectra `countContacts`) | Frontend |
| C-3.3 | Recipient list view in campaign detail page: shows name, email, status per row | Frontend |

## Track D — Data

| Task | Description | Owner |
| --- | --- | --- |
| D-3.1 | Migration: add `audience_source TEXT`, `segment_id TEXT`, `vql_query TEXT` to `campaigns` | Backend |
| D-3.2 | Ensure `recipients.id` is deterministic from contact UUID5 to avoid duplicates | Backend |
| D-3.3 | Store Connectra `contact_id` reference in `recipients.contact_ref_id` for lineage | Backend |

## Track E — Ops

| Task | Description | Owner |
| --- | --- | --- |
| E-3.1 | Add `CONNECTRA_BASE_URL` env var to campaign service | DevOps |
| E-3.2 | Health check: campaign service pings Connectra `/api/v1/health` and surfaces as dependency | DevOps |

---

## Completion gate
- [ ] Campaign created with `audience_source: "segment"` resolves recipients from Connectra.
- [ ] No duplicate recipients in campaign for same email address.
- [ ] CSV fallback still works but logs deprecation warning.
- [ ] Audience count preview visible in wizard before campaign is saved.
