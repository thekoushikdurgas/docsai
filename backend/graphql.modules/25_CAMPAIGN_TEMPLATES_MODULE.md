# Campaign Templates Module

## Contact360 gateway (actual)

| GraphQL | Path | Auth | Return |
| --- | --- | --- | --- |
| `campaignSatellite.campaignTemplates` | `query { campaignSatellite { campaignTemplates } }` | required | `JSON` (from satellite `GET /campaign-templates`, or `[]` if `CAMPAIGN_API_URL` unset) |

Field name in GraphQL is **`campaignTemplates`** (camelCase). There are **no** template CRUD mutations on the gateway’s `campaignSatellite` type today.

## Canonical SDL (gateway — read-only)

```graphql
type CampaignModuleQuery {
  campaigns: JSON!
  sequences: JSON!
  campaignTemplates: JSON!
}
```

Regenerate: `python -c "from app.graphql.schema import schema; print(schema.as_str())"` from `contact360.io/api`.

### POST `/graphql`

```json
{
  "query": "query { campaignSatellite { campaignTemplates } }"
}
```

---

## Planned / service-native GraphQL (not on gateway yet)

**Service:** `backend(dev)/email campaign` (Go, Gin, S3). **Direct REST** may include template upload/list/preview/generate (see service `API.md`).

| Operation | Type | Description | Era |
| --- | --- | --- | --- |
| `createCampaignTemplate` | Mutation | Upload HTML template to S3 + create DB record | planned |
| `getCampaignTemplate` | Query | Get template metadata and HTML body | planned |
| `listCampaignTemplates` | Query | List templates | overlaps read-only `campaignSatellite.campaignTemplates` |
| `updateCampaignTemplate` | Mutation | Update template HTML/metadata | planned |
| `deleteCampaignTemplate` | Mutation | Delete template from S3 and DB | planned |
| `previewCampaignTemplate` | Query | Render template with sample data | planned |
| `generateCampaignTemplate` | Mutation | AI-generate HTML template from prompt | planned |

---

## REST endpoints (direct)

### `POST /templates`

**Auth:** JWT
**Request:**

```json
{
  "name": "Welcome Email",
  "subject": "Welcome {{.FirstName}}!",
  "html_body": "<html><body>Hello {{.FirstName}}!</body></html>"
}
```

**Response `201`:**

```json
{
  "id": "uuid",
  "name": "Welcome Email",
  "subject": "Welcome {{.FirstName}}!",
  "s3_key": "templates/uuid.html",
  "created_at": "2026-03-24T00:00:00Z"
}
```

---

### `POST /templates/:id/preview`

**Auth:** JWT
**Request:** `{}` (uses sample TemplateData)
**Response `200`:** Rendered HTML string with sample `FirstName`, `LastName`, `Email`, `UnsubscribeURL`.

---

### `POST /templates/generate` (era `5.x`+)

**Auth:** JWT
**Request:**

```json
{
  "prompt": "Write a welcome email for a B2B SaaS product called Contact360",
  "subject_hint": "Welcome to Contact360"
}
```

**Response `201`:** Same as `POST /templates` — creates template in S3 and DB with `is_ai_generated=true`.

---

## Template variable reference

| Variable | Resolved from | Notes |
| --- | --- | --- |
| `{{.FirstName}}` | `recipients.name` (first word split) | Always available |
| `{{.LastName}}` | `recipients.name` (remainder split) | Always available |
| `{{.Email}}` | `recipients.email` | Always available |
| `{{.UnsubscribeURL}}` | JWT token URL generated per recipient | Always injected automatically |
| `{{.Company}}` | Connectra contact `company_name` | Available in `3.x`+ when Connectra integrated |
| `{{.Title}}` | Connectra contact `title` | Available in `5.x`+ |
| `{{.Industry}}` | Connectra contact `industry` | Available in `5.x`+ |

---

## S3 storage contract

| Operation | S3 key | Notes |
| --- | --- | --- |
| Upload | `templates/{id}.html` | PutObject on `POST /templates` |
| Fetch | `templates/{id}.html` | GetObject with in-memory cache (evicted on delete) |
| Delete | `templates/{id}.html` | DeleteObject + cache eviction + DB delete |

Cache: `template.Service.cache` — `map[string]string` with `sync.RWMutex`. Cache miss reads from S3.

---

## Database tables

| Table | Read | Write |
| --- | --- | --- |
| `templates` | `listCampaignTemplates`, `getCampaignTemplate` | `createCampaignTemplate`, `updateCampaignTemplate`, `deleteCampaignTemplate` |

---

## Frontend page bindings

| Page | Route | Operations used |
| --- | --- | --- |
| Templates list | `/campaigns/templates` | `listCampaignTemplates` |
| Template editor | `/campaigns/templates/:id/edit` | `getCampaignTemplate`, `updateCampaignTemplate`, `previewCampaignTemplate` |
| Template creation | `/campaigns/templates/new` | `createCampaignTemplate` |
| AI generation | Template builder AI panel | `generateCampaignTemplate` |
| Campaign wizard step 2 | `/campaigns/new` | `listCampaignTemplates`, `previewCampaignTemplate` |

---

## UI element reference

| Element | Component | Page |
| --- | --- | --- |
| Template grid | `TemplateGrid` | Templates list |
| AI badge | `AITemplateBadge` | Templates list (AI-generated indicator) |
| HTML editor | `TemplateEditor` (split view) | Template builder |
| Variable insertion | `VariableInsertionButtons` | Template builder |
| Subject line input | `Input` | Template builder |
| Preview panel | `TemplatePreviewPane` | Template builder |
| AI prompt textarea | `AIPromptDrawer` | Template builder |

---

## Era context

Template CRUD is available from `0.x` as the foundation. AI generation (`generateCampaignTemplate`) is a `5.x` feature. Full template analytics (open/click from template) requires `10.x` tracking infrastructure.
