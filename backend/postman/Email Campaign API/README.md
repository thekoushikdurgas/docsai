# Email Campaign API — Postman Collection

## Service

**Service:** `backend(dev)/email campaign`  
**Runtime:** Go 1.24, Gin, Asynq/Redis, PostgreSQL, AWS S3  
**Base URL:** `http://localhost:8081` (local dev)  
**Auth:** JWT Bearer token (planned; add `Authorization: Bearer <token>` header on all non-health routes)

---

## Collection variables

| Variable | Description | Example |
| --- | --- | --- |
| `campaign_base_url` | Base URL for campaign service | `http://localhost:8081` |
| `campaign_jwt_token` | Valid JWT for authenticated routes | `eyJhbGci...` |
| `campaign_id` | UUID of a created campaign | `abc123...` |
| `template_id` | UUID of a created template | `def456...` |
| `unsub_token` | JWT from email unsubscribe link | `eyJhbGci...` |

---

## Request collection

### Health

```
GET {{campaign_base_url}}/health
```

Expected: `200 OK` `{"status": "ok"}`

---

### Templates

#### Create Template

```
POST {{campaign_base_url}}/templates
Authorization: Bearer {{campaign_jwt_token}}
Content-Type: application/json

{
  "name": "Welcome Email",
  "subject": "Welcome {{.FirstName}}!",
  "html_body": "<html><body><h1>Hello {{.FirstName}}!</h1><p><a href='{{.UnsubscribeURL}}'>Unsubscribe</a></p></body></html>"
}
```

Expected: `201 Created` with `id`, `name`, `subject`, `s3_key`.

#### List Templates

```
GET {{campaign_base_url}}/templates
Authorization: Bearer {{campaign_jwt_token}}
```

#### Get Template

```
GET {{campaign_base_url}}/templates/{{template_id}}
Authorization: Bearer {{campaign_jwt_token}}
```

#### Preview Template

```
POST {{campaign_base_url}}/templates/{{template_id}}/preview
Authorization: Bearer {{campaign_jwt_token}}
```

Expected: `200 OK` with rendered HTML (sample TemplateData injected).

#### Delete Template

```
DELETE {{campaign_base_url}}/templates/{{template_id}}
Authorization: Bearer {{campaign_jwt_token}}
```

Expected: `204 No Content`

---

### Campaigns

#### Create Campaign

```
POST {{campaign_base_url}}/campaign
Authorization: Bearer {{campaign_jwt_token}}
Content-Type: application/json

{
  "template_id": "{{template_id}}",
  "name": "Test Campaign",
  "audience_source": "csv",
  "filepath": "/tmp/recipients.csv"
}
```

Expected: `201 Created` `{"campaign_id": "...", "status": "pending"}`

#### Unsubscribe

```
GET {{campaign_base_url}}/unsub?token={{unsub_token}}
```

Expected: `200 OK` with HTML confirmation. Email added to suppression_list. Recipient status = `unsubscribed`.

---

## Era alignment

| Era | Key test additions |
| --- | --- |
| `0.x` | Template CRUD, campaign create, unsubscribe, health |
| `1.x` | Auth guard (401 without JWT), credit 402 response |
| `2.x` | Bounce webhook test, rate-limit response |
| `3.x` | Campaign create with segment audience source |
| `5.x` | AI template generate endpoint |
| `6.x` | Campaign resume endpoint, idempotency test |
| `8.x` | GraphQL module tests, webhook subscription |
| `10.x` | Sequence create/trigger, analytics endpoint, tracking pixel |

---

## Known issues (must fix before collection runs cleanly)

1. Auth middleware not yet active — all routes currently unauthenticated. Auth guard tests will fail until middleware is added.
2. SMTP nil auth — campaign worker will fail to send without SMTP credentials.
3. Schema drift — `templates` table and `recipients.unsub_token` missing from schema.sql. DB bootstraps will fail on fresh install.
