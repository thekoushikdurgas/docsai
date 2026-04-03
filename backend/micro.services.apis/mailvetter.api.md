# Mailvetter API Documentation

**Version**: 1.0.0  
**Last Updated**: March 28, 2026  
**Service path**: `backend(dev)/mailvetter` (Go API + worker)  
**Canonical v1 base URL**: deploy-specific (e.g. `https://<host>/v1`); new integrations must use `/v1/*` only.

## Documentation map

| Doc | Purpose |
| --- | --- |
| [SERVICE_TOPOLOGY.md](../endpoints/SERVICE_TOPOLOGY.md) | Mailvetter in the platform graph |
| [mailvetter_endpoint_era_matrix.md](../endpoints/mailvetter_endpoint_era_matrix.md) | Era and route maturity |
| [mailvetter_data_lineage.md](../database/mailvetter_data_lineage.md) | Verification pipeline data |
| [emailapis.api.md](emailapis.api.md) | Finder/verify family alongside Mailvetter |
| [index.md](../endpoints/index.md) | GraphQL verify operations that delegate here |
| [ENDPOINT_DATABASE_LINKS.md](../endpoints/ENDPOINT_DATABASE_LINKS.md) | Delegation and table scope on gateway specs |

### Also in `docs/backend/endpoints/`

- **[README.md](../endpoints/README.md)** — `mailvetter` row in matrix ↔ codebase table.
- **[endpoints_index.md](../endpoints/endpoints_index.md)** — [mailvetter_endpoint_era_matrix.md](../endpoints/mailvetter_endpoint_era_matrix.md); GraphQL: [index.md](../endpoints/index.md) for `graphql/VerifySingleEmail`, bulk verify, and any op with **`lambda_services`** referencing Mailvetter.

---

## Table of Contents

1. [Authentication](#authentication)
2. [Core Endpoints](#core-endpoints)
3. [Single Email Validation](#single-email-validation)
4. [Bulk Email Validation](#bulk-email-validation)
5. [Status & Results](#status--results)
6. [Error Handling](#error-handling)
7. [Rate Limiting](#rate-limiting)
8. [Examples](#examples)

---

## Authentication

All protected API requests require an API key in the `Authorization` header as `Bearer <token>`, or the configured shared secret per deployment.

```bash
Authorization: Bearer YOUR_API_KEY
```

**Obtaining an API Key**:
- Provision via deployment config (`API_SECRET_KEY` / key store) for your Contact360 environment.
- Rotate keys through your ops runbook; do not embed keys in client-side code.

---

## Core Endpoints

### Endpoint Summary

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/emails/validate` | Validate a single email |
| POST | `/emails/validate-bulk` | Validate multiple emails |
| GET | `/jobs/{job_id}` | Get bulk validation job status |
| GET | `/jobs/{job_id}/results` | Download validation results |
| GET | `/health` | Service health check |

---

## Single Email Validation

### Validate Single Email

Validate a single email address with comprehensive verification checks.

**Endpoint**:
```
POST /emails/validate
```

**Request Headers**:
```
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

**Request Body**:
```json
{
  "email": "user@example.com",
  "verify_smtp": true,
  "check_disposable": true,
  "full_details": false
}
```

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `email` | string | Yes | Email address to validate |
| `verify_smtp` | boolean | No | Enable SMTP verification (slower but more accurate). Default: `true` |
| `check_disposable` | boolean | No | Check against disposable email list. Default: `true` |
| `full_details` | boolean | No | Return detailed validation info. Default: `false` |

**Response (200 OK)**:
```json
{
  "status": "success",
  "email": "user@example.com",
  "is_valid": true,
  "validation_result": {
    "syntax_valid": true,
    "domain_valid": true,
    "smtp_valid": true,
    "is_disposable": false,
    "is_catchall": false
  },
  "confidence_score": 0.95,
  "details": {
    "domain": "example.com",
    "email_provider": "gmail",
    "mx_records_found": 5,
    "smtp_response_code": 250,
    "validation_time_ms": 1200
  }
}
```

**Response Fields**:

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | `success` or `error` |
| `email` | string | Input email address |
| `is_valid` | boolean | Overall validation result |
| `validation_result` | object | Detailed validation checks |
| `confidence_score` | number | 0-1 confidence level of validation |
| `details` | object | Extended metadata (if `full_details: true`) |

---

## Bulk Email Validation

### Validate Multiple Emails

Validate hundreds or thousands of emails asynchronously. Returns a job ID for tracking progress.

**Endpoint**:
```
POST /emails/validate-bulk
```

**Request Headers**:
```
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

**Request Body**:
```json
{
  "emails": [
    "user1@example.com",
    "user2@gmail.com",
    "user3@company.org"
  ],
  "verify_smtp": true,
  "check_disposable": true,
  "callback_url": "https://your-domain.com/webhook",
  "callback_events": ["completed", "failed"]
}
```

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `emails` | array | Yes | Array of email addresses (max 10,000 per request) |
| `verify_smtp` | boolean | No | Enable SMTP verification. Default: `true` |
| `check_disposable` | boolean | No | Check disposable emails. Default: `true` |
| `callback_url` | string | No | Webhook URL for job completion notification |
| `callback_events` | array | No | Events to trigger callback: `["completed", "failed"]` |

**Response (202 Accepted)**:
```json
{
  "status": "processing",
  "job_id": "job_550e8400e29b41d4a716446655440000",
  "job_name": "bulk_validation_2026_03_18_001",
  "total_emails": 3,
  "progress": {
    "processed": 0,
    "valid": 0,
    "invalid": 0,
    "pending": 3,
    "percentage": 0
  },
  "estimated_completion_time": "2026-03-18T10:15:00Z",
  "created_at": "2026-03-18T10:05:00Z"
}
```

**Response Fields**:

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | `processing`, `completed`, or `failed` |
| `job_id` | string | Unique job identifier for tracking |
| `total_emails` | number | Total emails submitted |
| `progress.processed` | number | Emails validated |
| `progress.percentage` | number | Overall completion percentage (0-100) |
| `estimated_completion_time` | string | ISO 8601 timestamp |

---

## Status & Results

### Get Bulk Job Status

Check the current status and progress of a bulk validation job.

**Endpoint**:
```
GET /jobs/{job_id}
```

**Request Headers**:
```
Authorization: Bearer YOUR_API_KEY
```

**Path Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `job_id` | string | Job ID returned from bulk validation request |

**Response (200 OK)**:
```json
{
  "status": "processing",
  "job_id": "job_550e8400e29b41d4a716446655440000",
  "total_emails": 3,
  "progress": {
    "processed": 2,
    "valid": 1,
    "invalid": 1,
    "pending": 1,
    "percentage": 66.67,
    "success_rate": 50.0
  },
  "estimated_completion_time": "2026-03-18T10:15:00Z",
  "started_at": "2026-03-18T10:05:00Z",
  "updated_at": "2026-03-18T10:10:00Z"
}
```

**Progress Fields**:

| Field | Type | Description |
|-------|------|-------------|
| `processed` | number | Emails validated so far |
| `valid` | number | Valid emails count |
| `invalid` | number | Invalid emails count |
| `pending` | number | Emails awaiting validation |
| `percentage` | number | Completion percentage (0-100) |
| `success_rate` | number | Valid emails percentage |

### Get Validation Results

Retrieve detailed results of a completed bulk validation job.

**Endpoint**:
```
GET /jobs/{job_id}/results
```

**Query Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `format` | string | No | Response format: `json` or `csv`. Default: `json` |
| `filter` | string | No | Filter results: `all`, `valid`, or `invalid`. Default: `all` |
| `page` | number | No | Pagination: page number (1-indexed). Default: 1 |
| `limit` | number | No | Results per page (max 1000). Default: 100 |

**Response (200 OK - JSON Format)**:
```json
{
  "status": "completed",
  "job_id": "job_550e8400e29b41d4a716446655440000",
  "total_emails": 3,
  "summary": {
    "valid": 2,
    "invalid": 1,
    "valid_percentage": 66.67,
    "invalid_percentage": 33.33,
    "processing_time_seconds": 305
  },
  "results": [
    {
      "email": "user1@example.com",
      "is_valid": true,
      "validation_result": {
        "syntax_valid": true,
        "domain_valid": true,
        "smtp_valid": true,
        "is_disposable": false,
        "is_catchall": false
      },
      "confidence_score": 0.98,
      "processed_at": "2026-03-18T10:05:30Z"
    },
    {
      "email": "user2@gmail.com",
      "is_valid": true,
      "validation_result": {
        "syntax_valid": true,
        "domain_valid": true,
        "smtp_valid": true,
        "is_disposable": false,
        "is_catchall": false
      },
      "confidence_score": 0.97,
      "processed_at": "2026-03-18T10:05:35Z"
    },
    {
      "email": "user3@invalid.com",
      "is_valid": false,
      "validation_result": {
        "syntax_valid": true,
        "domain_valid": false,
        "smtp_valid": false,
        "is_disposable": false,
        "is_catchall": false
      },
      "confidence_score": 0.02,
      "processed_at": "2026-03-18T10:05:40Z"
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 1,
    "total_results": 3
  }
}
```

**Response (200 OK - CSV Format)**:
```csv
email,is_valid,syntax_valid,domain_valid,smtp_valid,is_disposable,confidence_score,processed_at
user1@example.com,true,true,true,true,false,0.98,2026-03-18T10:05:30Z
user2@gmail.com,true,true,true,true,false,0.97,2026-03-18T10:05:35Z
user3@invalid.com,false,true,false,false,false,0.02,2026-03-18T10:05:40Z
```

---

## Error Handling

### HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | OK | Successful validation request |
| 202 | Accepted | Bulk job accepted, processing started |
| 400 | Bad Request | Invalid email format or missing parameter |
| 401 | Unauthorized | Invalid or missing API key |
| 403 | Forbidden | Account restricted or rate limit exceeded |
| 404 | Not Found | Job ID not found |
| 422 | Unprocessable Entity | Validation logic error |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Server Error | Internal server error |
| 503 | Service Unavailable | Service temporarily unavailable |

### Error Response Format

```json
{
  "status": "error",
  "error_code": "INVALID_EMAIL_FORMAT",
  "message": "The provided email address has invalid syntax",
  "details": {
    "email": "user@",
    "reason": "Missing domain"
  },
  "timestamp": "2026-03-18T10:05:00Z"
}
```

### Common Error Codes

| Code | Description | HTTP Status |
|------|-------------|-------------|
| `INVALID_EMAIL_FORMAT` | Email syntax is invalid | 400 |
| `MISSING_PARAMETER` | Required parameter is missing | 400 |
| `INVALID_API_KEY` | API key is invalid or expired | 401 |
| `RATE_LIMIT_EXCEEDED` | Too many requests made | 429 |
| `JOB_NOT_FOUND` | Job ID does not exist | 404 |
| `BULK_SIZE_EXCEEDED` | More than 10,000 emails submitted | 422 |
| `INTERNAL_ERROR` | Server-side validation failure | 500 |

---

## Rate Limiting

API requests are rate-limited per API key:

| Plan | Requests/Hour | Bulk Limit | Concurrent Jobs |
|------|---------------|-----------|-----------------|
| Free | 100 | 100 emails | 1 |
| Pro | 10,000 | 100,000 emails | 5 |
| Enterprise | Unlimited | Unlimited | 20+ |

**Rate Limit Headers**:
```
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9950
X-RateLimit-Reset: 1710750300
```

When rate limit is exceeded, the API returns `429 Too Many Requests`.

---

## Examples

### Example 1: Single Email Validation (cURL)

```bash
curl -X POST {{MAILVETTER_BASE_URL}}/v1/emails/validate \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "verify_smtp": true,
    "full_details": true
  }'
```

### Example 2: Bulk Email Validation (Python + Requests)

```python
import requests
import json

API_KEY = "YOUR_API_KEY"
BASE_URL = "{{MAILVETTER_BASE_URL}}/v1"

# Submit bulk validation job
emails = [
    "user1@example.com",
    "user2@gmail.com",
    "user3@company.org",
    "invalid-email@"
]

response = requests.post(
    f"{BASE_URL}/emails/validate-bulk",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "emails": emails,
        "verify_smtp": True,
        "check_disposable": True,
        "callback_url": "https://your-domain.com/webhook"
    }
)

job_data = response.json()
job_id = job_data['job_id']
print(f"Job ID: {job_id}")
print(f"Status: {job_data['status']}")
print(f"Progress: {job_data['progress']['percentage']}%")
```

### Example 3: Check Job Status & Results (Python)

```python
import requests
import time

API_KEY = "YOUR_API_KEY"
BASE_URL = "{{MAILVETTER_BASE_URL}}/v1"
JOB_ID = "job_550e8400e29b41d4a716446655440000"

# Poll job status
while True:
    status_response = requests.get(
        f"{BASE_URL}/jobs/{JOB_ID}",
        headers={"Authorization": f"Bearer {API_KEY}"}
    )
    
    status_data = status_response.json()
    print(f"Status: {status_data['status']}")
    print(f"Progress: {status_data['progress']['percentage']}%")
    print(f"Valid: {status_data['progress']['valid']}")
    print(f"Invalid: {status_data['progress']['invalid']}")
    
    if status_data['status'] == 'completed':
        break
    
    time.sleep(5)  # Check every 5 seconds

# Get results
results_response = requests.get(
    f"{BASE_URL}/jobs/{JOB_ID}/results?format=json&limit=100",
    headers={"Authorization": f"Bearer {API_KEY}"}
)

results = results_response.json()
print(f"\nSummary:")
print(f"Valid: {results['summary']['valid_percentage']}%")
print(f"Invalid: {results['summary']['invalid_percentage']}%")

for result in results['results']:
    print(f"\n{result['email']}: {'✓ Valid' if result['is_valid'] else '✗ Invalid'}")
    print(f"  Confidence: {result['confidence_score']}")
```

### Example 4: Get Results as CSV (cURL)

```bash
curl -X GET "{{MAILVETTER_BASE_URL}}/v1/jobs/job_550e8400e29b41d4a716446655440000/results?format=csv&filter=all" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -o results.csv
```

### Example 5: Webhook Callback Example

When a bulk job completes, the API sends a POST request to your `callback_url`:

**Request to your webhook**:
```json
{
  "event": "completed",
  "job_id": "job_550e8400e29b41d4a716446655440000",
  "status": "completed",
  "summary": {
    "total_emails": 3,
    "valid": 2,
    "invalid": 1,
    "valid_percentage": 66.67
  },
  "timestamp": "2026-03-18T10:10:00Z"
}
```

**Your webhook handler** (Flask example):
```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    data = request.json
    job_id = data['job_id']
    status = data['status']
    
    print(f"Job {job_id} completed")
    print(f"Valid: {data['summary']['valid_percentage']}%")
    
    # Fetch results
    results = get_results(job_id)  # Your function
    process_results(results)  # Your function
    
    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    app.run()
```

---

## Webhook Security

All webhook requests include an `X-Webhook-Signature` header for verification.

**Verification** (Python):
```python
import hmac
import hashlib

def verify_webhook(request_body, signature, secret_key):
    expected_signature = hmac.new(
        secret_key.encode(),
        request_body,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(signature, expected_signature)
```

---

## Response Time & Timeout

- **Single email validation**: 500ms - 2s (depends on SMTP verification)
- **Bulk validation**: 5s - 5min (depends on email count and SMTP checks)
- **Request timeout**: 30s
- **Maximum job retention**: 30 days

---

## Support & Resources

- **Documentation**: Contact360 internal docs — `docs/backend/apis/` (Email module), `docs/codebases/mailvetter-codebase-analysis.md`
- **Runtime**: `backend(dev)/mailvetter/app/mailvetter-bak/`

---

## Change Log

### Version 1.0.0 (March 18, 2026)
- Initial API release
- Single email validation endpoint
- Bulk email validation endpoint
- Job status tracking
- CSV/JSON result exports
- Webhook callbacks
- Rate limiting per plan tier

## 2026 contract note

- Canonical API contract for new integrations is `/v1/*`.
- Legacy endpoints may remain for compatibility but are deprecated for net-new consumers.
- Preferred lifecycle vocabulary: `pending`, `processing`, `completed`, `failed`.