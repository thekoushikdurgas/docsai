# Contact360 — API Documentation

> **Base URL:** `https://api.contact360.io/v1`
> **Auth:** All endpoints require `Authorization: Bearer <JWT>` unless marked `[public]`
> **Content-Type:** `application/json`
> **Rate Limits:** 1000 req/min per org (default) · 100 req/min for bulk endpoints
> **API Version:** v1 · April 2026

---

## Global Response Format

### Success
```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "requestId": "req_abc123",
    "timestamp": "2026-04-14T01:25:00Z"
  }
}
```

### Error
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "email is required",
    "field": "email",
    "details": []
  },
  "meta": {
    "requestId": "req_abc123",
    "timestamp": "2026-04-14T01:25:00Z"
  }
}
```

### Standard Error Codes
| Code | HTTP | Description |
|------|------|-------------|
| `UNAUTHORIZED` | 401 | Missing or invalid JWT |
| `FORBIDDEN` | 403 | Insufficient role / wrong org |
| `NOT_FOUND` | 404 | Resource does not exist |
| `VALIDATION_ERROR` | 422 | Request body failed schema validation |
| `RATE_LIMIT` | 429 | Too many requests |
| `PROVIDER_ERROR` | 502 | External provider (Hunter, Twilio) failed |
| `JOB_QUEUED` | 202 | Request accepted, processing async |

---

## Pagination (all list endpoints)

```
GET /contacts?page=1&limit=25&sort=createdAt&order=desc
```

```json
{
  "data": [ ... ],
  "pagination": {
    "page": 1,
    "limit": 25,
    "total": 4820,
    "totalPages": 193,
    "hasNext": true,
    "hasPrev": false,
    "nextCursor": "eyJpZCI6MTAwfQ=="
  }
}
```

---

# EMAIL SERVICE · `/email`

## POST /email/generate

Generate a single professional email for a contact using AI.

**Auth:** Required · **Rate limit:** 60/min

### Request
```json
{
  "contactId": "cnt_abc123",
  "tone": "professional",
  "goal": "cold_outreach",
  "context": {
    "senderName": "Koushik",
    "senderRole": "Founder",
    "productName": "Contact360",
    "valueProposition": "AI-powered CRM that finds verified emails"
  },
  "templateId": "tmpl_xyz",
  "stream": false
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `contactId` | string | ✓ | Target contact ID (fetches name, company, title) |
| `tone` | enum | ✓ | `professional` · `friendly` · `formal` · `casual` |
| `goal` | enum | ✓ | `cold_outreach` · `follow_up` · `re_engage` · `proposal` |
| `context` | object | ✓ | Sender info + product context for grounding |
| `templateId` | string | — | Start from an existing template |
| `stream` | boolean | — | `true` = SSE token streaming, default `false` |

### Response (stream: false)
```json
{
  "success": true,
  "data": {
    "subject": "Quick question about your outreach at Acme, John",
    "body": "Hi John,

I came across your profile on LinkedIn...",
    "variables": ["firstName", "company", "senderName"],
    "wordCount": 124,
    "readabilityScore": 78,
    "model": "gpt-4o",
    "tokensUsed": 340
  }
}
```

### Response (stream: true)
```
Content-Type: text/event-stream

data: {"token": "Hi"}
data: {"token": " John"}
data: {"token": ","}
...
data: {"done": true, "subject": "Quick question...", "tokensUsed": 340}
```

---

## POST /email/validate

Validate a single email address through the full waterfall pipeline.

**Auth:** Required · **Rate limit:** 200/min

### Request
```json
{
  "email": "john.doe@acme.com",
  "depth": "full",
  "saveResult": true,
  "contactId": "cnt_abc123"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `email` | string | ✓ | Email address to validate |
| `depth` | enum | — | `syntax` · `mx` · `smtp` · `full` (default: `full`) |
| `saveResult` | boolean | — | Persist result to contact record |
| `contactId` | string | — | Associate result with contact |

### Response
```json
{
  "success": true,
  "data": {
    "email": "john.doe@acme.com",
    "status": "valid",
    "subStatus": "inbox_full",
    "confidence": 92,
    "checks": {
      "syntax":    { "pass": true },
      "mxRecord":  { "pass": true, "mx": "mail.acme.com" },
      "smtp":      { "pass": true, "responseCode": 250 },
      "catchAll":  { "isCatchAll": false },
      "disposable":{ "isDisposable": false },
      "dnd":       { "isDND": false }
    },
    "provider": "zerobounce",
    "responseTime": 1240
  }
}
```

**Status values:** `valid` · `invalid` · `risky` · `unknown` · `catch_all` · `disposable`

---

## POST /email/bulk-generate

Enqueue a bulk email generation job from a contact list or CSV.

**Auth:** Required · **Rate limit:** 10/min (bulk)

### Request
```json
{
  "source": "segment",
  "segmentId": "seg_q2leads",
  "tone": "professional",
  "goal": "cold_outreach",
  "context": {
    "senderName": "Koushik",
    "senderRole": "Founder",
    "productName": "Contact360",
    "valueProposition": "AI-powered CRM"
  },
  "templateId": "tmpl_xyz",
  "notifyOnComplete": true
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `source` | enum | ✓ | `segment` · `file` · `contactIds` |
| `segmentId` | string | cond. | Required if source=`segment` |
| `fileId` | string | cond. | Required if source=`file` |
| `contactIds` | string[] | cond. | Required if source=`contactIds` (max 500) |
| `tone` | enum | ✓ | Same as single generate |
| `goal` | enum | ✓ | Same as single generate |
| `context` | object | ✓ | Sender + product context |
| `templateId` | string | — | Base template |
| `notifyOnComplete` | boolean | — | Sends in-app + email notification |

### Response `202 Accepted`
```json
{
  "success": true,
  "data": {
    "jobId": "job_gen_abc123",
    "status": "queued",
    "estimatedContacts": 1240,
    "estimatedDuration": "4m",
    "streamUrl": "/v1/jobs/job_gen_abc123/stream"
  }
}
```

### Job Progress (SSE)
```
GET /v1/jobs/job_gen_abc123/stream
Content-Type: text/event-stream

data: {"processed": 100, "total": 1240, "failed": 2, "status": "running"}
data: {"processed": 500, "total": 1240, "failed": 5, "status": "running"}
data: {"processed": 1240, "total": 1240, "failed": 8, "status": "done", "outputFileId": "file_xyz"}
```

---

## POST /email/bulk-validate

Enqueue a bulk email validation job from CSV or contact segment.

**Auth:** Required · **Rate limit:** 10/min (bulk)

### Request
```json
{
  "source": "file",
  "fileId": "file_leads_q2",
  "emailColumn": "email",
  "depth": "full",
  "saveResults": true,
  "notifyOnComplete": true
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `source` | enum | ✓ | `file` · `segment` · `contactIds` |
| `fileId` | string | cond. | Required if source=`file` |
| `emailColumn` | string | cond. | CSV column name for email |
| `depth` | enum | — | `syntax` · `mx` · `smtp` · `full` |
| `saveResults` | boolean | — | Write back to contact records |

### Response `202 Accepted`
```json
{
  "success": true,
  "data": {
    "jobId": "job_val_def456",
    "status": "queued",
    "totalEmails": 5000,
    "estimatedDuration": "12m",
    "streamUrl": "/v1/jobs/job_val_def456/stream"
  }
}
```

### Result Download (after job completes)
```
GET /v1/files/file_xyz/download
→ Redirects to S3 presigned URL
```

**Result CSV columns:** `email, status, subStatus, confidence, mxRecord, isCatchAll, isDisposable, provider`

---

## POST /email/pattern

Run the pattern engine only — generates candidate email addresses from name + domain.

**Auth:** Required · **Rate limit:** 500/min

### Request
```json
{
  "firstName": "John",
  "lastName": "Doe",
  "domain": "acme.com",
  "verifyTop": 3
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `firstName` | string | ✓ | Contact first name |
| `lastName` | string | ✓ | Contact last name |
| `domain` | string | ✓ | Company domain |
| `verifyTop` | integer | — | Verify top N patterns via SMTP (0 = no verify) |

### Response
```json
{
  "success": true,
  "data": {
    "patterns": [
      { "email": "john.doe@acme.com",    "pattern": "{first}.{last}",   "confidence": 85, "verified": true },
      { "email": "jdoe@acme.com",        "pattern": "{f}{last}",        "confidence": 72, "verified": true },
      { "email": "john@acme.com",        "pattern": "{first}",          "confidence": 60, "verified": false },
      { "email": "johndoe@acme.com",     "pattern": "{first}{last}",    "confidence": 55, "verified": false },
      { "email": "j.doe@acme.com",       "pattern": "{f}.{last}",       "confidence": 50, "verified": false }
    ],
    "topCandidate": "john.doe@acme.com",
    "patternsChecked": 12
  }
}
```

---

# PHONE SERVICE · `/phone`

## POST /phone/search

Search and discover phone numbers for a contact by name + company.

**Auth:** Required · **Rate limit:** 100/min

### Request
```json
{
  "contactId": "cnt_abc123",
  "firstName": "John",
  "lastName": "Doe",
  "company": "Acme Inc",
  "country": "IN",
  "saveResult": true
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `contactId` | string | — | Pre-existing contact to enrich |
| `firstName` | string | ✓ | Contact first name |
| `lastName` | string | ✓ | Contact last name |
| `company` | string | — | Company name (improves accuracy) |
| `country` | string | — | ISO 2-letter country code |
| `saveResult` | boolean | — | Write result back to contact |

### Response
```json
{
  "success": true,
  "data": {
    "found": true,
    "phone": "+919876543210",
    "phoneFormatted": "+91 98765 43210",
    "countryCode": "IN",
    "carrier": "Airtel",
    "lineType": "mobile",
    "region": "Karnataka",
    "dnd": {
      "registered": false,
      "checkedAt": "2026-04-14T00:00:00Z"
    },
    "confidence": 82,
    "source": "truecaller",
    "alternates": [
      { "phone": "+919876543211", "confidence": 64, "source": "numverify" }
    ]
  }
}
```

---

## POST /phone/validate

Validate a known phone number — format, carrier, DND, and line type.

**Auth:** Required · **Rate limit:** 300/min

### Request
```json
{
  "phone": "+919876543210",
  "checks": ["format", "carrier", "dnd", "linetype"],
  "saveResult": true,
  "contactId": "cnt_abc123"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `phone` | string | ✓ | Phone number (E.164 format preferred) |
| `checks` | string[] | — | `format` · `carrier` · `dnd` · `linetype` · `all` (default: all) |
| `saveResult` | boolean | — | Write result to contact |
| `contactId` | string | — | Associate result with contact |

### Response
```json
{
  "success": true,
  "data": {
    "phone": "+919876543210",
    "valid": true,
    "e164": "+919876543210",
    "national": "098765 43210",
    "countryCode": "IN",
    "carrier": {
      "name": "Airtel",
      "type": "mobile",
      "mcc": "404",
      "mnc": "10"
    },
    "lineType": "mobile",
    "region": "Karnataka, India",
    "dnd": {
      "registered": false,
      "registeredAt": null,
      "source": "trai",
      "checkedAt": "2026-04-14T00:00:00Z",
      "cacheExpiresAt": "2026-04-15T00:00:00Z"
    },
    "reachable": true,
    "confidence": 95
  }
}
```

---

## POST /phone/bulk

Enqueue a bulk phone validation job from CSV or contact segment.

**Auth:** Required · **Rate limit:** 10/min (bulk)

### Request
```json
{
  "source": "file",
  "fileId": "file_phones_batch3",
  "phoneColumn": "phone",
  "checks": ["format", "carrier", "dnd"],
  "country": "IN",
  "saveResults": true,
  "notifyOnComplete": true
}
```

### Response `202 Accepted`
```json
{
  "success": true,
  "data": {
    "jobId": "job_phn_ghi789",
    "status": "queued",
    "totalPhones": 1100,
    "estimatedDuration": "6m",
    "streamUrl": "/v1/jobs/job_phn_ghi789/stream"
  }
}
```

### Bulk Result Summary (after job done)
```json
{
  "jobId": "job_phn_ghi789",
  "status": "done",
  "summary": {
    "total": 1100,
    "valid": 748,
    "invalid": 132,
    "dnd": 154,
    "unknown": 66,
    "mobile": 890,
    "landline": 142,
    "voip": 68
  },
  "outputFileId": "file_result_abc"
}
```

---

# CRM SERVICE · `/contacts` · `/companies`

## GET /contacts

Fetch a paginated, filtered list of contacts for the authenticated org.

**Auth:** Required · **Rate limit:** 500/min

### Query Parameters
| Param | Type | Description |
|-------|------|-------------|
| `q` | string | Full-text search (name, email, company) |
| `company` | string | Filter by company name |
| `tags` | string | Comma-separated tag IDs |
| `emailVerified` | boolean | Filter verified email only |
| `phoneVerified` | boolean | Filter verified phone only |
| `minScore` | integer | Min enrichment score (0–100) |
| `source` | string | `manual` · `csv_import` · `extension` · `api` |
| `page` | integer | Page number (default: 1) |
| `limit` | integer | Items per page (default: 25, max: 100) |
| `sort` | string | `createdAt` · `updatedAt` · `name` · `score` |
| `order` | string | `asc` · `desc` |
| `cursor` | string | Cursor for keyset pagination |

### Request
```
GET /v1/contacts?q=john&company=acme&emailVerified=true&minScore=70&sort=score&order=desc&limit=25
```

### Response
```json
{
  "success": true,
  "data": [
    {
      "id": "cnt_abc123",
      "orgId": "org_xyz",
      "name": "John Doe",
      "firstName": "John",
      "lastName": "Doe",
      "email": "john.doe@acme.com",
      "emailVerified": true,
      "emailConfidence": 92,
      "phone": "+919876543210",
      "phoneVerified": true,
      "phoneCarrier": "Airtel",
      "jobTitle": "VP of Sales",
      "company": { "id": "cmp_123", "name": "Acme Inc", "domain": "acme.com" },
      "linkedinUrl": "https://linkedin.com/in/johndoe",
      "enrichmentScore": 92,
      "source": "extension",
      "tags": [
        { "id": "tag_001", "name": "hot-lead", "color": "#e8af34" }
      ],
      "deals": [
        { "id": "deal_001", "title": "Acme Enterprise", "stage": "proposal", "value": 25000 }
      ],
      "lastActivity": { "type": "email_sent", "date": "2026-04-12T10:30:00Z" },
      "createdAt": "2026-03-01T08:00:00Z",
      "updatedAt": "2026-04-12T10:30:00Z"
    }
  ],
  "pagination": {
    "page": 1, "limit": 25, "total": 4820,
    "hasNext": true, "nextCursor": "eyJpZCI6MTAwfQ=="
  }
}
```

---

## POST /contacts

Create a new contact.

**Auth:** Required · **Rate limit:** 200/min

### Request
```json
{
  "name": "John Doe",
  "email": "john.doe@acme.com",
  "phone": "+919876543210",
  "jobTitle": "VP of Sales",
  "companyId": "cmp_123",
  "linkedinUrl": "https://linkedin.com/in/johndoe",
  "tags": ["tag_001"],
  "source": "manual",
  "customFields": {
    "leadSource": "LinkedIn",
    "priority": "high"
  },
  "autoEnrich": true
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✓ | Full name |
| `email` | string | — | Email address |
| `phone` | string | — | Phone (E.164 preferred) |
| `jobTitle` | string | — | Job title |
| `companyId` | string | — | Existing company ID |
| `companyName` | string | — | Creates company if not found |
| `linkedinUrl` | string | — | LinkedIn profile URL |
| `tags` | string[] | — | Tag IDs to apply |
| `source` | string | — | How created: `manual` · `api` · `csv_import` · `extension` |
| `customFields` | object | — | Org-defined custom fields |
| `autoEnrich` | boolean | — | Trigger async enrichment after create |

### Response `201 Created`
```json
{
  "success": true,
  "data": {
    "id": "cnt_new456",
    "name": "John Doe",
    "email": "john.doe@acme.com",
    "enrichmentScore": 0,
    "createdAt": "2026-04-14T01:25:00Z",
    "enrichJob": {
      "jobId": "job_enr_xyz",
      "status": "queued",
      "streamUrl": "/v1/jobs/job_enr_xyz/stream"
    }
  }
}
```

---

## GET /companies

Fetch companies with optional filtering.

**Auth:** Required · **Rate limit:** 500/min

### Query Parameters
| Param | Type | Description |
|-------|------|-------------|
| `q` | string | Full-text search (name, domain) |
| `domain` | string | Exact domain match |
| `industry` | string | Industry filter |
| `minContacts` | integer | Companies with N+ contacts |
| `page` | integer | Page number |
| `limit` | integer | Items per page |

### Response
```json
{
  "success": true,
  "data": [
    {
      "id": "cmp_123",
      "name": "Acme Inc",
      "domain": "acme.com",
      "industry": "Technology",
      "size": "51-200",
      "country": "US",
      "linkedinUrl": "https://linkedin.com/company/acme",
      "contactCount": 12,
      "dealCount": 3,
      "totalDealValue": 75000,
      "createdAt": "2026-03-01T08:00:00Z"
    }
  ],
  "pagination": { "page": 1, "limit": 25, "total": 340, "hasNext": true }
}
```

---

# CAMPAIGN SERVICE · `/campaign`

## POST /campaign/create

Create a new multi-channel outreach campaign.

**Auth:** Required · **Rate limit:** 60/min

### Request
```json
{
  "name": "Q2 SaaS Outreach",
  "goal": "demo_booking",
  "audienceType": "segment",
  "segmentId": "seg_saas_leads",
  "steps": [
    {
      "order": 1,
      "channel": "email",
      "delayDays": 0,
      "templateId": "tmpl_cold_outreach",
      "subject": "Quick question, {{firstName}}",
      "condition": null
    },
    {
      "order": 2,
      "channel": "email",
      "delayDays": 3,
      "templateId": "tmpl_followup_1",
      "subject": "Following up, {{firstName}}",
      "condition": "no_open"
    },
    {
      "order": 3,
      "channel": "whatsapp",
      "delayDays": 5,
      "templateId": "tmpl_wa_followup",
      "condition": "no_reply"
    },
    {
      "order": 4,
      "channel": "sms",
      "delayDays": 8,
      "templateId": "tmpl_sms_final",
      "condition": "no_reply"
    }
  ],
  "sendWindow": {
    "timezone": "Asia/Kolkata",
    "startHour": 9,
    "endHour": 18,
    "days": ["mon", "tue", "wed", "thu", "fri"]
  },
  "tags": ["q2", "saas"],
  "abTest": {
    "enabled": false
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✓ | Campaign name |
| `goal` | enum | ✓ | `awareness` · `demo_booking` · `re_engage` · `upsell` |
| `audienceType` | enum | ✓ | `segment` · `contactIds` · `file` |
| `segmentId` | string | cond. | BQL segment ID |
| `steps` | array | ✓ | Sequence steps (1–20) |
| `steps[].channel` | enum | ✓ | `email` · `whatsapp` · `sms` · `linkedin` |
| `steps[].delayDays` | integer | ✓ | Days after previous step |
| `steps[].condition` | enum | — | `no_open` · `no_click` · `no_reply` · `null` (always run) |
| `sendWindow` | object | — | Time window for sends |
| `abTest` | object | — | A/B test config (variants, split ratio) |

### Response `201 Created`
```json
{
  "success": true,
  "data": {
    "id": "cmp_q2_abc",
    "name": "Q2 SaaS Outreach",
    "status": "draft",
    "estimatedReach": 1240,
    "steps": 4,
    "createdAt": "2026-04-14T01:25:00Z"
  }
}
```

---

## POST /campaign/schedule

Activate and schedule a campaign (transitions from `draft` → `scheduled`).

**Auth:** Required · **Rate limit:** 30/min

### Request
```json
{
  "campaignId": "cmp_q2_abc",
  "startAt": "2026-04-15T09:00:00+05:30",
  "endAt": "2026-05-15T18:00:00+05:30",
  "dailyCap": 100,
  "dryRun": false
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `campaignId` | string | ✓ | Campaign to schedule |
| `startAt` | ISO8601 | ✓ | Campaign start datetime (with timezone) |
| `endAt` | ISO8601 | — | Hard stop date |
| `dailyCap` | integer | — | Max sends per day (default: unlimited) |
| `dryRun` | boolean | — | Simulate without sending |

### Response
```json
{
  "success": true,
  "data": {
    "campaignId": "cmp_q2_abc",
    "status": "scheduled",
    "startAt": "2026-04-15T09:00:00+05:30",
    "estimatedFirstSend": "2026-04-15T09:00:00+05:30",
    "estimatedCompletion": "2026-04-18T18:00:00+05:30",
    "estimatedReach": 1240,
    "firstBatchSize": 100
  }
}
```

---

## GET /campaign/stats

Fetch aggregated performance statistics for a campaign.

**Auth:** Required · **Rate limit:** 300/min

### Query Parameters
| Param | Type | Description |
|-------|------|-------------|
| `campaignId` | string | ✓ Required |
| `granularity` | enum | `hour` · `day` · `week` (default: `day`) |
| `from` | ISO8601 | Start date filter |
| `to` | ISO8601 | End date filter |
| `breakdown` | string | `channel` · `step` · `variant` |

### Request
```
GET /v1/campaign/stats?campaignId=cmp_q2_abc&granularity=day&breakdown=channel
```

### Response
```json
{
  "success": true,
  "data": {
    "campaignId": "cmp_q2_abc",
    "period": { "from": "2026-04-15", "to": "2026-04-14" },
    "summary": {
      "sent": 850,
      "delivered": 831,
      "opened": 289,
      "clicked": 102,
      "replied": 51,
      "bounced": 19,
      "unsubscribed": 4,
      "converted": 12,
      "openRate": 34.8,
      "clickRate": 12.3,
      "replyRate": 6.1,
      "bounceRate": 2.2,
      "conversionRate": 1.4
    },
    "byChannel": {
      "email":    { "sent": 600, "opened": 210, "clicked": 80, "replied": 40 },
      "whatsapp": { "sent": 180, "delivered": 175, "replied": 8 },
      "sms":      { "sent": 70, "delivered": 68, "replied": 3 }
    },
    "timeline": [
      { "date": "2026-04-15", "sent": 100, "opened": 34, "clicked": 12 },
      { "date": "2026-04-16", "sent": 100, "opened": 38, "clicked": 14 }
    ]
  }
}
```

---

# STORAGE SERVICE · `/file`

## POST /file/upload

Request a presigned S3 URL to upload a file directly from the client.

**Auth:** Required · **Rate limit:** 60/min

### Request
```json
{
  "filename": "leads_q2_2026.csv",
  "contentType": "text/csv",
  "size": 524288,
  "purpose": "email_enrichment",
  "metadata": {
    "description": "Q2 SaaS leads from LinkedIn"
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `filename` | string | ✓ | Original file name |
| `contentType` | string | ✓ | MIME type (`text/csv` · `application/json`) |
| `size` | integer | ✓ | File size in bytes (max: 50MB) |
| `purpose` | enum | ✓ | `email_enrichment` · `phone_validation` · `contact_import` |
| `metadata` | object | — | User-defined metadata |

### Response
```json
{
  "success": true,
  "data": {
    "fileId": "file_new_xyz789",
    "uploadUrl": "https://contact360-uploads.s3.ap-south-1.amazonaws.com/org_xyz/file_new_xyz789.csv?X-Amz-...",
    "uploadMethod": "PUT",
    "uploadHeaders": {
      "Content-Type": "text/csv",
      "x-amz-meta-org-id": "org_xyz",
      "x-amz-meta-purpose": "email_enrichment"
    },
    "expiresAt": "2026-04-14T02:25:00Z",
    "maxSizeBytes": 52428800
  }
}
```

**Upload flow:**
```
1. POST /file/upload          → get presigned URL
2. PUT {uploadUrl}            → upload directly to S3 (from browser/CLI)
3. S3 triggers Lambda         → validates CSV + creates enrichment job
4. GET /file/{fileId}/status  → poll or SSE for processing status
```

---

## GET /file/metadata

Fetch metadata for one or multiple uploaded files.

**Auth:** Required · **Rate limit:** 300/min

### Query Parameters
| Param | Type | Description |
|-------|------|-------------|
| `fileId` | string | Single file ID |
| `purpose` | string | Filter by purpose |
| `status` | string | `uploaded` · `processing` · `done` · `failed` |
| `page` | integer | Page number |
| `limit` | integer | Items per page |

### Request
```
GET /v1/file/metadata?purpose=email_enrichment&status=done&limit=10
```

### Response
```json
{
  "success": true,
  "data": [
    {
      "id": "file_new_xyz789",
      "orgId": "org_xyz",
      "filename": "leads_q2_2026.csv",
      "contentType": "text/csv",
      "size": 524288,
      "sizeHuman": "512 KB",
      "purpose": "email_enrichment",
      "status": "done",
      "rowCount": 5240,
      "columns": ["name", "email", "company", "linkedin_url"],
      "columnMapping": {
        "email": "email",
        "name": "full_name"
      },
      "uploadedBy": "usr_koushik",
      "uploadedAt": "2026-04-14T00:30:00Z",
      "processedAt": "2026-04-14T00:45:00Z",
      "jobId": "job_val_def456",
      "downloadUrl": "/v1/files/file_new_xyz789/download",
      "metadata": {
        "description": "Q2 SaaS leads from LinkedIn"
      }
    }
  ],
  "pagination": { "page": 1, "limit": 10, "total": 23, "hasNext": true }
}
```

---

# AI SERVICE · `/ai`

## POST /ai/query

Run a natural language query against the full CRM context using hybrid RAG.

**Auth:** Required · **Rate limit:** 60/min

### Request
```json
{
  "query": "Which contacts from SaaS companies haven't been contacted in 30 days and have a score above 80?",
  "context": {
    "includeDeals": true,
    "includeActivities": true,
    "maxContacts": 50
  },
  "model": "gpt-4o",
  "stream": true,
  "sessionId": "sess_abc123",
  "responseFormat": "structured"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `query` | string | ✓ | Natural language question |
| `context` | object | — | What data to include in retrieval |
| `model` | enum | — | `gpt-4o` · `claude-3-5-sonnet` · `gemini-1-5-pro` · `auto` |
| `stream` | boolean | — | Token-by-token streaming |
| `sessionId` | string | — | Maintain conversation context across turns |
| `responseFormat` | enum | — | `text` · `structured` · `table` · `markdown` |

### Response (stream: false)
```json
{
  "success": true,
  "data": {
    "answer": "Found 14 contacts matching your criteria. Top 5 by score: ...",
    "contacts": [
      { "id": "cnt_abc", "name": "John Doe", "score": 92, "daysSinceContact": 34 }
    ],
    "sources": [
      { "type": "opensearch", "query": "industry:saas score:>80", "hits": 28 },
      { "type": "pgvector", "similarity": 0.87, "chunks": 5 }
    ],
    "actions": [
      { "type": "suggest_campaign", "label": "Create re-engagement campaign for these 14 contacts" }
    ],
    "model": "gpt-4o",
    "tokensUsed": 1240,
    "latencyMs": 2100
  }
}
```

### Streaming Response
```
Content-Type: text/event-stream

data: {"type": "token",   "content": "Found"}
data: {"type": "token",   "content": " 14"}
data: {"type": "source",  "source": {"type": "opensearch", "hits": 28}}
data: {"type": "action",  "action": {"type": "suggest_campaign", "label": "..."}}
data: {"type": "done",    "tokensUsed": 1240}
```

---

## POST /ai/action

Execute an AI-triggered CRM action. Supports human-in-the-loop approval.

**Auth:** Required · **Rate limit:** 30/min

### Request
```json
{
  "action": "create_campaign",
  "params": {
    "name": "Re-engage: Dormant SaaS Leads",
    "contactIds": ["cnt_abc", "cnt_def", "cnt_ghi"],
    "goal": "re_engage",
    "channels": ["email", "whatsapp"],
    "templateSuggestion": "Use the re-engagement template with a 20% discount mention"
  },
  "approvalToken": "appr_xyz123",
  "sessionId": "sess_abc123"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `action` | enum | ✓ | `create_contact` · `create_deal` · `create_campaign` · `send_email` · `update_stage` · `add_tag` |
| `params` | object | ✓ | Action-specific parameters |
| `approvalToken` | string | cond. | Required for write actions (HITL gate) |
| `sessionId` | string | — | Tie to conversation session |

### Response
```json
{
  "success": true,
  "data": {
    "actionId": "act_new_001",
    "action": "create_campaign",
    "status": "pending_approval",
    "summary": "Creating campaign 'Re-engage: Dormant SaaS Leads' for 14 contacts via Email + WhatsApp",
    "approvalRequired": true,
    "approvalUrl": "/v1/ai/action/act_new_001/approve",
    "expiresAt": "2026-04-14T01:55:00Z"
  }
}
```

### Approve Action
```
POST /v1/ai/action/{actionId}/approve
Body: { "approved": true }
```

---

# CONNECTOR SERVICE (BQL) · `/bql`

## POST /bql/query

Execute a BQL (Business Query Language) query against multi-source CRM data.

**Auth:** Required · **Rate limit:** 100/min

### Request
```json
{
  "query": "SELECT contacts WHERE company.industry = 'SaaS' AND email.verified = true AND enrichmentScore > 70 AND deal.stage IN ('proposal', 'negotiation') ORDER BY enrichmentScore DESC LIMIT 100",
  "options": {
    "cache": true,
    "cacheTtl": 300,
    "includeCount": true,
    "explain": false
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `query` | string | ✓ | BQL query string |
| `options.cache` | boolean | — | Cache result in Redis (default: true) |
| `options.cacheTtl` | integer | — | Cache TTL in seconds (default: 300) |
| `options.includeCount` | boolean | — | Return total matching count |
| `options.explain` | boolean | — | Return execution plan without running |

### BQL Supported Operators
```
=, !=, >, >=, <, <=
IN (list), NOT IN (list)
LIKE "pattern%"
IS NULL, IS NOT NULL
AND, OR, NOT
BETWEEN val1 AND val2
NOW(), TODAY(), DAYS_AGO(n), MONTHS_AGO(n)
```

### BQL Supported Fields
```
contacts.*         name, email, phone, jobTitle, enrichmentScore, source, createdAt
email.*            verified, confidence, status, provider
phone.*            verified, carrier, lineType, dnd
company.*          name, domain, industry, size, country
deal.*             title, stage, value, closedAt
tag.*              name, color
activity.*         type, date, channel
```

### Response
```json
{
  "success": true,
  "data": {
    "results": [
      {
        "id": "cnt_abc123",
        "name": "John Doe",
        "email": "john.doe@acme.com",
        "enrichmentScore": 92,
        "company": { "name": "Acme Inc", "industry": "SaaS" },
        "deal": { "stage": "proposal", "value": 25000 }
      }
    ],
    "count": 48,
    "totalMatching": 48,
    "executionMs": 124,
    "sources": ["postgresql", "opensearch"],
    "cached": false,
    "cacheKey": "bql_abc123hash"
  }
}
```

### Explain Response (options.explain: true)
```json
{
  "plan": {
    "steps": [
      { "source": "opensearch", "filter": "industry:SaaS", "estimatedHits": 210 },
      { "source": "postgresql", "filter": "enrichmentScore > 70 AND email.verified = true", "estimatedRows": 80 },
      { "operation": "merge_intersect", "estimatedResult": 48 }
    ],
    "estimatedMs": 100
  }
}
```

---

## POST /bql/export

Export the results of a BQL query to a file (CSV or JSON).

**Auth:** Required · **Rate limit:** 20/min

### Request
```json
{
  "query": "SELECT contacts WHERE tags.name = 'hot-lead' ORDER BY createdAt DESC",
  "format": "csv",
  "columns": ["name", "email", "phone", "company.name", "enrichmentScore", "deal.stage"],
  "filename": "hot_leads_export.csv",
  "notifyOnComplete": true
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `query` | string | ✓ | BQL query to export |
| `format` | enum | ✓ | `csv` · `json` · `xlsx` |
| `columns` | string[] | — | Columns to include (default: all) |
| `filename` | string | — | Output file name |
| `notifyOnComplete` | boolean | — | Send notification when ready |

### Response `202 Accepted`
```json
{
  "success": true,
  "data": {
    "jobId": "job_exp_abc",
    "status": "queued",
    "estimatedRows": 340,
    "format": "csv",
    "streamUrl": "/v1/jobs/job_exp_abc/stream"
  }
}
```

---

## POST /bql/import

Import contacts or data from a CSV/JSON file into the CRM via BQL-mapped fields.

**Auth:** Required · **Rate limit:** 10/min

### Request
```json
{
  "fileId": "file_raw_contacts",
  "entity": "contacts",
  "columnMapping": {
    "Full Name": "name",
    "Work Email": "email",
    "Company Name": "company.name",
    "Job Title": "jobTitle",
    "LinkedIn URL": "linkedinUrl"
  },
  "options": {
    "deduplicateOn": ["email"],
    "updateExisting": true,
    "autoEnrich": true,
    "tags": ["tag_imported_apr2026"],
    "source": "csv_import"
  },
  "notifyOnComplete": true
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `fileId` | string | ✓ | Previously uploaded file ID |
| `entity` | enum | ✓ | `contacts` · `companies` · `deals` |
| `columnMapping` | object | ✓ | CSV column → CRM field mapping |
| `options.deduplicateOn` | string[] | — | Fields to use for dedup check |
| `options.updateExisting` | boolean | — | Update if duplicate found |
| `options.autoEnrich` | boolean | — | Trigger enrichment after import |
| `options.tags` | string[] | — | Tags to apply to all imported records |

### Response `202 Accepted`
```json
{
  "success": true,
  "data": {
    "jobId": "job_imp_def",
    "status": "queued",
    "estimatedRows": 800,
    "estimatedDuration": "3m",
    "streamUrl": "/v1/jobs/job_imp_def/stream"
  }
}
```

### Import Job Completion Event (SSE)
```json
{
  "jobId": "job_imp_def",
  "status": "done",
  "summary": {
    "total": 800,
    "created": 612,
    "updated": 142,
    "skipped": 28,
    "failed": 18,
    "enrichmentJobId": "job_enr_new"
  }
}
```

---

## Webhook Events (Outbound)

Configure webhooks at `POST /v1/webhooks` to receive real-time events.

```json
{
  "event": "contact.enriched",
  "timestamp": "2026-04-14T01:25:00Z",
  "orgId": "org_xyz",
  "data": {
    "contactId": "cnt_abc123",
    "email": "john.doe@acme.com",
    "emailVerified": true,
    "confidence": 92,
    "phone": "+919876543210",
    "phoneVerified": true
  },
  "signature": "sha256=abcdef1234..."
}
```

### Available Webhook Events
```
contact.created          contact.updated          contact.deleted
contact.enriched         deal.created             deal.stage_changed
campaign.sent            campaign.completed       job.done
job.failed               email.opened             email.clicked
email.replied            email.bounced
```

---

*Document version: v1.0 | April 2026 | Contact360 API Reference*
