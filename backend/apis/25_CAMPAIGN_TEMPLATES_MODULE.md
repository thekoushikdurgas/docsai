# Campaign Templates Module

**Service:** `backend(dev)/email campaign` (Go, Gin, S3)  
**Gateway proxy:** Appointment360 GraphQL (`createCampaignTemplate`, `getCampaignTemplate`, `listCampaignTemplates`, `deleteCampaignTemplate`, `previewCampaignTemplate`, `generateCampaignTemplate`)  
**Direct REST routes:** `POST /templates`, `GET /templates`, `GET /templates/:id`, `DELETE /templates/:id`, `POST /templates/:id/preview`, `POST /templates/generate` (era `5.x`+)

---

## GraphQL operations (gateway-proxied)

| Operation | Type | Description | Era |
| --- | --- | --- | --- |
| `createCampaignTemplate` | Mutation | Upload HTML template to S3 + create DB record | `10.x` |
| `getCampaignTemplate` | Query | Get template metadata and HTML body | `10.x` |
| `listCampaignTemplates` | Query | List all templates for org | `10.x` |
| `updateCampaignTemplate` | Mutation | Update template HTML/metadata | `10.x` |
| `deleteCampaignTemplate` | Mutation | Delete template from S3 and DB | `10.x` |
| `previewCampaignTemplate` | Query | Render template with sample data | `10.x` |
| `generateCampaignTemplate` | Mutation | AI-generate HTML template from prompt | `5.x`+ |

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
