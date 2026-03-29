# Campaigns Module

**Service:** `backend(dev)/email campaign` (Go, Gin, Asynq)  
**Gateway proxy:** Appointment360 GraphQL (`createCampaign`, `getCampaign`, `listCampaigns`, `updateCampaign`, `deleteCampaign`)  
**Direct REST routes:** `POST /campaign`, `GET /health`, `GET /unsub`

---

## GraphQL operations (gateway-proxied)

| Operation | Type | Description | Era |
| --- | --- | --- | --- |
| `createCampaign` | Mutation | Enqueue a new campaign send job | `10.x` |
| `getCampaign` | Query | Get campaign by ID with full recipient/status detail | `10.x` |
| `listCampaigns` | Query | Paginated list of campaigns for org | `10.x` |
| `updateCampaign` | Mutation | Update campaign (pause, resume, reschedule) | `10.x` |
| `deleteCampaign` | Mutation | Delete campaign and associated recipients | `10.x` |
| `getCampaignStats` | Query | Aggregated open/click/unsubscribe rates | `10.x` |

---

## GraphQL input/output types

### `createCampaign` input

```graphql
input CreateCampaignInput {
  name: String!
  templateId: ID!
  audienceSource: AudienceSource!  # CSV | SEGMENT | VQL | SN_BATCH
  segmentId: ID
  vqlQuery: String
  scheduledAt: DateTime
  abTestEnabled: Boolean
}
```

### `Campaign` type

```graphql
type Campaign {
  id: ID!
  name: String!
  status: CampaignStatus!  # pending | sending | completed | completed_with_errors | failed | paused
  totalRecipients: Int!
  sent: Int!
  failed: Int!
  openRate: Float  # available after era 10.x tracking
  clickRate: Float
  unsubscribeCount: Int
  createdAt: DateTime!
  scheduledAt: DateTime
  completedAt: DateTime
  template: CampaignTemplate
  userId: ID
  orgId: ID
}

enum CampaignStatus {
  pending
  sending
  completed
  completed_with_errors
  failed
  paused
}

enum AudienceSource {
  CSV
  SEGMENT
  VQL
  SN_BATCH
}
```

---

## REST endpoints (direct, on campaign service)

### `POST /campaign`

**Auth:** JWT (Bearer token)  
**Request body:**

```json
{
  "template_id": "uuid",
  "name": "Campaign name",
  "filepath": "path/to/recipients.csv",
  "audience_source": "csv | segment | vql | sn_batch",
  "segment_id": "uuid (optional)",
  "vql_query": "string (optional)",
  "scheduled_at": "2026-03-24T10:00:00Z (optional)"
}
```

**Response `201`:**

```json
{
  "campaign_id": "uuid",
  "status": "pending"
}
```

**Error codes:** `400` Bad request | `401` Unauthorized | `402` Insufficient credits | `429` Entitlement limit exceeded

---

### `GET /unsub`

**Auth:** JWT in query parameter (`?token=...`)  
**Description:** Processes unsubscribe request; validates JWT, inserts to `suppression_list`, updates `recipients.status`.  
**Response:** HTML confirmation page or JSON  
**Error:** `401` Invalid/expired token

---

## Database tables

| Table | Read | Write |
| --- | --- | --- |
| `campaigns` | `getCampaign`, `listCampaigns` | `createCampaign`, `updateCampaign`, worker status updates |
| `recipients` | `getCampaign` (recipient list) | Worker fan-out, unsubscribe endpoint |
| `suppression_list` | Worker pre-send check | Unsubscribe endpoint, bounce webhooks |
| `templates` | Worker template fetch | `createCampaign` (template reference validation) |

---

## Frontend page bindings

| Page | Route | Operations used |
| --- | --- | --- |
| Campaigns list | `/campaigns` | `listCampaigns` |
| Campaign detail | `/campaigns/:id` | `getCampaign`, `getCampaignStats` |
| Campaign wizard | `/campaigns/new` | `createCampaign` |
| Campaign actions | All campaign pages | `updateCampaign`, `deleteCampaign` |

---

## Middleware and auth

- **JWT validation middleware:** Required on all routes except `/health` and `/unsub` (which validates its own token).
- **RBAC:** `campaign-manager` role for create/delete; `viewer` role for read.
- **Credit guard:** Pre-send credit check before enqueueing (era `1.x`+).
- **Entitlement guard:** Send-volume limit check per org tier (era `9.x`+).

---

## Campaign worker mapping

| Step | Code file | Description |
| --- | --- | --- |
| Task enqueue | `api/handlers.go:CreateCampaign` | HTTP → Asynq `campaign:send` |
| Task handler | `worker/campaign_worker.go:HandleCampaignTask` | Asynq consumer → sets status, loads audience |
| Email worker | `worker/email_worker.go:EmailWorker` | Goroutine → suppress check → render → SMTP send |
| Suppression check | `db/queries.go:IsEmailSuppressed` | Pre-send check against `suppression_list` |
| Unsubscribe token | `utils/token.go:GenerateUnsubToken` | JWT HS256 per recipient |

---

## Era task-pack index

| Era | Task pack |
| --- | --- |
| `0.x` | `docs/0. Foundation.../emailcampaign-foundation-task-pack.md` |
| `1.x` | `docs/1. User billing.../emailcampaign-user-billing-task-pack.md` |
| `2.x` | `docs/2. Email system.../emailcampaign-email-system-task-pack.md` |
| `3.x` | `docs/3. Contact360 contact and company data system/` — patches `3.N.P — *.md` (**Service task slices**; former `emailcampaign-contact-company-task-pack.md` merged) |
| `4.x` | `docs/4. Contact360 Extension and Sales Navigator maturity/` — patches `4.N.P — *.md` (**Service task slices**; former `emailcampaign-extension-sn-task-pack.md` merged) |
| `5.x` | `docs/5. Contact360 AI workflows/` — patches `5.N.P — *.md` (**Service task slices**; former `emailcampaign-ai-task-pack.md` merged) |
| `10.x` | `docs/10. Contact360 email campaign/` — patches `10.N.P — *.md` (**Micro-gate** + **Service task slices**; former `emailcampaign-email-campaign-task-pack.md` merged) |

Deep reference: `docs/codebases/emailcampaign-codebase-analysis.md`.

## 2026 blocker status

This module remains partially incomplete until `EC-0.1` to `EC-0.4` are resolved:

- schema parity (`templates`, `unsub_token`)
- unsubscribe query correctness fix
- SMTP auth wiring
- env-driven infrastructure config hardening
