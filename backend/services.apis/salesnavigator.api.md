# Sales Navigator API Documentation

Complete API reference for the Lambda Sales Navigator API Service deployed on AWS API Gateway.

**Go / EC2 target:** `EC2/extension.server/` — module `contact360.io/extension` implements `POST /v1/save-profiles` (dedup, chunk, Connectra upsert). **HTML scrape remains in the Chrome extension** — server returns `501` for scrape-only routes.

## Documentation map

| Doc | Purpose |
| --- | --- |
| [SERVICE_TOPOLOGY.md](../endpoints/SERVICE_TOPOLOGY.md) | SN channel in the delegation map |
| [salesnavigator_endpoint_era_matrix.md](../endpoints/salesnavigator_endpoint_era_matrix.md) | Era and gaps |
| [salesnavigator_data_lineage.md](../database/salesnavigator_data_lineage.md) | Ingest and provenance |
| [connectra.api.md](connectra.api.md) | Where saved profiles land (bulk upsert / VQL) |
| [index.md](../endpoints/index.md) | e.g. `graphql/SaveSalesNavigatorProfiles`, `graphql/SearchLinkedIn`, `graphql/UpsertByLinkedInUrl` |
| [ENDPOINT_DATABASE_LINKS.md](../endpoints/ENDPOINT_DATABASE_LINKS.md) | Naming + Connectra table notes on delegated ops |

### Also in `docs/backend/endpoints/`

- **[README.md](../endpoints/README.md)** — includes `salesnavigator` ↔ extension codebase mapping.
- **[endpoints_index.md](../endpoints/endpoints_index.md)** — [salesnavigator_endpoint_era_matrix.md](../endpoints/salesnavigator_endpoint_era_matrix.md); all GraphQL SN / LinkedIn ops: [index.md](../endpoints/index.md) → individual `*_graphql.md` files.

## Base URL

```
Production: (Update after deployment)
Local Development: http://localhost:8080
```

## Authentication

All endpoints (except health check and root) require API key authentication via the `X-API-Key` header.

```http
X-API-Key: your-api-key-here
```

### Authentication Error Response

```json
{
  "detail": "missing API key header"
}
```

or

```json
{
  "detail": "invalid API key"
}
```

**Status Code:** `401 Unauthorized`

---

## Endpoints

### Health Check

#### `GET /health`

Check service health status. **No authentication required.**

**Response:**

```json
{
  "status": "ok",
  "service": "Sales Navigator API Service",
  "version": "1.0.0"
}
```

**Status Codes:**
- `200 OK` - Service is healthy

---

### Root Endpoint

#### `GET /`

Get service information. **No authentication required.**

**Response:**

```json
{
  "service": "Sales Navigator API Service",
  "version": "1.0.0",
  "status": "running"
}
```

**Status Codes:**
- `200 OK` - Service information

---

### Scrape Sales Navigator HTML

#### `POST /v1/scrape`

Scrape Sales Navigator HTML content and extract profile data. Optionally save profiles to Connectra.

**Headers:**
```http
Content-Type: application/json
X-API-Key: your-api-key-here
```

**Request Body:**

```json
{
  "html": "<html>...</html>",
  "save": false,
  "include_metadata": true
}
```

**Request Schema:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `html` | string | Yes | Sales Navigator HTML content (max 10MB) |
| `save` | boolean | No | Save profiles to Connectra via bulk upsert (default: `false`) |
| `include_metadata` | boolean | No | Include page metadata in response (default: `true`) |

**HTML Validation:**
- Cannot be empty
- Must contain valid HTML tags
- Maximum size: 10MB (10485760 bytes)

**Response (Scraping Only, `save: false`):**

```json
{
  "extraction_metadata": {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "version": "2.0",
    "source_file": "api_request"
  },
  "page_metadata": {
    "search_context": {
      "search_type": "LEAD",
      "query": "software engineer",
      "filters": {}
    },
    "pagination": {
      "current_page": 1,
      "total_results": 150,
      "results_per_page": 25,
      "has_next_page": true,
      "next_page_url": null
    },
    "application_info": {
      "user_name": "John Doe",
      "user_urn": "urn:li:fs_salesMember:123456"
    }
  },
  "profiles": [
    {
      "name": "Jane Smith",
      "title": "Senior Software Engineer",
      "company": "Tech Corp",
      "location": "San Francisco, CA",
      "profile_url": "https://www.linkedin.com/in/janesmith",
      "image_url": "https://media.licdn.com/dms/image/...",
      "connection_degree": "2nd",
      "about": "Experienced software engineer...",
      "time_in_role": "2 years",
      "time_in_company": "3 years",
      "lead_id": "ACwAA...",
      "lead_urn": "urn:li:fs_salesLead:123456",
      "search_type": "LEAD",
      "search_id": "search-123",
      "company_id": "company-123",
      "company_url": "https://www.linkedin.com/sales/company/123",
      "is_premium_member": false,
      "is_reachable": true,
      "last_active": "2024-01-10",
      "is_viewed": false,
      "mutual_connections_count": 5,
      "mutual_connections": [],
      "is_recently_hired": false,
      "recent_posts_count": 0,
      "shared_groups_details": [],
      "data_quality_score": 0.85,
      "missing_fields": []
    }
  ],
  "saved_contacts": null,
  "saved_companies": null,
  "save_summary": null
}
```

**Response (With Save, `save: true`):**

```json
{
  "extraction_metadata": {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "version": "2.0",
    "source_file": "api_request"
  },
  "page_metadata": {
    "search_context": {},
    "pagination": {},
    "application_info": {}
  },
  "profiles": [
    {
      "name": "Jane Smith",
      "title": "Senior Software Engineer",
      "company": "Tech Corp",
      "location": "San Francisco, CA",
      "profile_url": "https://www.linkedin.com/in/janesmith",
      "data_quality_score": 0.85,
      "missing_fields": []
    }
  ],
  "saved_contacts": [
    {
      "name": "Jane Smith",
      "title": "Senior Software Engineer",
      "company": "Tech Corp"
    }
  ],
  "saved_companies": [
    {
      "name": "Tech Corp",
      "linkedin_url": "https://www.linkedin.com/sales/company/123"
    }
  ],
  "save_summary": {
    "total_profiles": 1,
    "contacts_created": 1,
    "contacts_updated": 0,
    "companies_created": 1,
    "companies_updated": 0,
    "errors": []
  }
}
```

**Profile Data Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Full name |
| `title` | string | Job title |
| `company` | string | Company name |
| `location` | string | Location string |
| `profile_url` | string | LinkedIn profile URL |
| `image_url` | string | Profile image URL |
| `connection_degree` | string | Connection degree (1st, 2nd, 3rd+) |
| `about` | string | Profile about section |
| `time_in_role` | string | Time in current role |
| `time_in_company` | string | Time at company |
| `lead_id` | string | Sales Navigator lead ID |
| `lead_urn` | string | Lead URN |
| `search_type` | string | Search type (LEAD, COMPANY, etc.) |
| `search_id` | string | Search identifier |
| `company_id` | string | Company ID |
| `company_url` | string | Company LinkedIn URL |
| `is_premium_member` | boolean | Premium member status |
| `is_reachable` | boolean | Whether user is reachable |
| `last_active` | string | Last active date |
| `is_viewed` | boolean | Whether profile was viewed |
| `mutual_connections_count` | number | Number of mutual connections |
| `mutual_connections` | array | List of mutual connections |
| `is_recently_hired` | boolean | Recently hired indicator |
| `recently_hired_company_logo` | string | Recently hired company logo URL |
| `recent_posts_count` | number | Recent posts count |
| `shared_groups_details` | array | Shared groups information |
| `data_quality_score` | number | Data quality score (0-1) |
| `missing_fields` | array | List of missing field names |

**Save Summary Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `total_profiles` | number | Total number of profiles processed |
| `contacts_created` | number | Number of contacts created |
| `contacts_updated` | number | Number of contacts updated |
| `companies_created` | number | Number of companies created |
| `companies_updated` | number | Number of companies updated |
| `errors` | array | List of error messages (if any) |

**Status Codes:**
- `200 OK` - Successful scraping
- `400 Bad Request` - Invalid HTML or validation error
- `401 Unauthorized` - Missing or invalid API key
- `500 Internal Server Error` - Server error during scraping
- `502 Bad Gateway` | `503 Service Unavailable` | `504 Gateway Timeout` - Connectra API errors (when `save: true`)

---

### Scrape HTML with Fetch

#### `POST /v1/scrape-html-with-fetch`

Scrape Sales Navigator HTML, save to Connectra, get UUIDs, query Connectra VQL, and return fetched data.

This endpoint performs a complete dual scraping flow:
1. Scrapes HTML content to extract profiles
2. Saves profiles to Connectra (if `save: true`)
3. Extracts contact UUIDs from save result
4. Queries Connectra VQL API to fetch saved contacts (if `fetch_after_save: true`)
5. Returns fetched contact data from Connectra

**Headers:**
```http
Content-Type: application/json
X-API-Key: your-api-key-here
```

**Request Body:**

```json
{
  "html": "<html>...</html>",
  "save": true,
  "fetch_after_save": true,
  "include_metadata": true
}
```

**Request Schema:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `html` | string | Yes | Sales Navigator HTML content (max 50MB) |
| `save` | boolean | No | Save profiles to Connectra via bulk upsert (default: `true`) |
| `fetch_after_save` | boolean | No | Fetch saved contacts via VQL after saving (default: `true`) |
| `include_metadata` | boolean | No | Include page metadata in response (default: `true`) |

**Response:**

```json
{
  "extraction_metadata": {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "version": "2.0",
    "source_file": "api_request"
  },
  "page_metadata": {
    "search_context": {
      "search_id": "search_123",
      "session_id": "session_456"
    },
    "pagination": {
      "current_page": 1,
      "total_pages": 5,
      "results_per_page": 25
    }
  },
  "profiles": [
    {
      "uuid": "c3d4e5f6-a7b8-9012-cdef-123456789012",
      "first_name": "John",
      "last_name": "Doe",
      "email": "john.doe@example.com",
      "title": "VP Engineering",
      "mobile_phone": "+1-555-123-4567",
      "linkedin_url": "https://linkedin.com/in/johndoe",
      "linkedin_sales_url": "https://linkedin.com/sales/lead/123",
      "company_id": "c0a8012e-1111-2222-3333-444455556666",
      "created_at": "2024-01-15T10:30:00.000Z",
      "company": {
        "name": "Acme Corp",
        "employees_count": 500,
        "industries": ["Technology", "Software"]
      }
    }
  ],
  "save_summary": {
    "total_profiles": 1,
    "contacts_created": 1,
    "contacts_updated": 0,
    "companies_created": 1,
    "companies_updated": 0,
    "errors": []
  },
  "fetched_count": 1,
  "contact_uuids": [
    "c3d4e5f6-a7b8-9012-cdef-123456789012"
  ]
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `extraction_metadata` | object | Extraction metadata (timestamp, version, source_file) |
| `page_metadata` | object | Page-level metadata (search_context, pagination, user_info, application_info) |
| `profiles` | array | **Fetched contacts from Connectra VQL** (includes company data if populated) |
| `save_summary` | object | Summary of save operation (contacts/companies created/updated, errors) |
| `fetched_count` | number | Number of contacts successfully fetched from Connectra VQL |
| `contact_uuids` | array | Array of contact UUIDs that were saved and fetched |

**Note:** The `profiles` field contains contact data fetched from Connectra VQL API, which includes all fields specified in the VQL query (default: uuid, first_name, last_name, email, title, mobile_phone, linkedin_url, linkedin_sales_url, company_id, created_at). Company data is populated if `company_config.populate: true` is set in the VQL query.

**Status Codes:**
- `200 OK` - Successful scraping and fetch
- `400 Bad Request` - Invalid HTML or validation error
- `401 Unauthorized` - Missing or invalid API key
- `500 Internal Server Error` - Server error during scraping
- `502 Bad Gateway` | `503 Service Unavailable` | `504 Gateway Timeout` - Connectra API errors

**Flow:**
1. HTML is scraped to extract profiles
2. If `save: true`, profiles are saved to Connectra via bulk upsert
3. Contact UUIDs are extracted from Connectra bulk upsert response (`contact_uuids` field)
4. If `fetch_after_save: true` and UUIDs exist, Connectra VQL API is queried using `POST /contacts/` with UUID filter
5. Fetched contacts are returned in `profiles` field

---

### Save Profiles

#### `POST /v1/save-profiles`

Save profiles array to Connectra database.

This endpoint saves a profiles array to Connectra via bulk upsert operations and returns a summary of the operation. It creates or updates contacts and companies based on the provided profile data.

**Headers:**
```http
Content-Type: application/json
X-API-Key: your-api-key-here
```

**Request Body:**

```json
{
  "profiles": [
    {
      "name": "Jane Smith",
      "title": "Senior Software Engineer",
      "company": "Tech Corp",
      "location": "San Francisco, CA",
      "profile_url": "https://linkedin.com/in/janesmith",
      "image_url": "https://media.licdn.com/...",
      "connection_degree": "2nd"
    }
  ]
}
```

**Request Schema:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `profiles` | array | Yes | Array of profile objects to save (max 1000 per request) |

**Profile Object Structure:**

Each profile object should contain Sales Navigator profile fields:
- `name` (string): Full name
- `title` (string, optional): Job title
- `company` (string, optional): Company name
- `location` (string, optional): Location string
- `profile_url` (string, optional): LinkedIn profile URL
- `image_url` (string, optional): Profile image URL
- `connection_degree` (string, optional): Connection degree
- Other Sales Navigator profile fields as available

**Response:**

```json
{
  "success": true,
  "total_profiles": 1,
  "saved_count": 1,
  "errors": []
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether the save operation was successful |
| `total_profiles` | number | Total number of profiles in the input array |
| `saved_count` | number | Number of profiles successfully saved (contacts created + contacts updated) |
| `errors` | array | Array of error messages (if any) |

**Status Codes:**
- `200 OK` - Save operation completed (may include errors in response)
- `400 Bad Request` - Invalid profiles array or validation error
- `401 Unauthorized` - Missing or invalid API key
- `500 Internal Server Error` - Server error during save
- `502 Bad Gateway` | `503 Service Unavailable` | `504 Gateway Timeout` - Connectra API errors

**Note:** The `saved_count` field represents the actual number of contacts successfully created or updated in Connectra (contacts_created + contacts_updated). This may differ from `total_profiles` if some profiles fail to save or are duplicates.

**Validation:**
- Profiles array is required and cannot be empty
- Profiles array cannot exceed 1000 items per request
- Each profile must be a valid JSON object

---

## Error Responses

### Validation Error

**Status Code:** `400 Bad Request`

```json
{
  "detail": "No profiles provided"
}
```

or

```json
{
  "detail": "Profiles array cannot exceed 1000 items per request"
}
```

### Connectra Client Error

**Status Code:** `502 Bad Gateway` | `503 Service Unavailable` | `504 Gateway Timeout`

```json
{
  "error": "ConnectraClientError",
  "message": "Failed to connect to Connectra API: timeout",
  "success": false
}
```

or

```json
{
  "error": "ConnectraAPIError",
  "message": "Connectra API error: 400 Bad Request",
  "success": false,
  "status_code": 400,
  "response_data": {
    "error": "Invalid request"
  }
}
```

### Internal Server Error

**Status Code:** `500 Internal Server Error`

```json
{
  "error": "InternalServerError",
  "message": "An unexpected error occurred",
  "success": false
}
```

---

## Integration with Connectra

### Save Profiles Flow (`/v1/save-profiles`)

When saving profiles array:

1. **Maps profiles** to Contact/Company data using Connectra-compatible schemas
2. **Deduplicates companies** by UUID (deterministic based on name + URL)
3. **Performs bulk upsert** via Connectra API in parallel:
   - `POST /contacts/bulk` - For all contacts
   - `POST /companies/bulk` - For all unique companies (runs in parallel with contacts)
4. **Returns response** with success status and actual saved count (contacts_created + contacts_updated)

**Note:** 
- The `saved_count` reflects the actual number of contacts saved to Connectra (contacts_created + contacts_updated), not just the input length
- Company and contact saves are performed in parallel for better performance
- Save errors are collected and returned in the response without raising exceptions

---

## Example Usage

### Save Profiles Array

```bash
curl -X POST http://localhost:8080/v1/save-profiles \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key-here" \
  -d '{
    "profiles": [
      {
        "name": "Jane Smith",
        "title": "Senior Software Engineer",
        "company": "Tech Corp",
        "location": "San Francisco, CA",
        "profile_url": "https://linkedin.com/in/janesmith"
      }
    ]
  }'
```

### Health Check

```bash
curl http://localhost:8080/health
```

---

## Rate Limits

Currently, no rate limits are enforced. Consider implementing rate limiting for production deployments.

---

## Environment Variables

The service requires the following environment variables:

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `API_KEY` | Yes | API key for service authentication | - |
| `CONNECTRA_API_URL` | Yes | Lambda Connectra base URL | - |
| `CONNECTRA_API_KEY` | Yes | Lambda Connectra API key | - |
| `CONNECTRA_TIMEOUT` | No | Connectra request timeout (seconds) | `30` |
| `LOG_LEVEL` | No | Logging level | `INFO` |

---

## Notes

- **Save Behavior**: Save errors are collected and returned in the response without raising exceptions
- **UUID Generation**: Contact and company UUIDs are deterministically generated for deduplication
- **Response Format**: Compatible with `appointment360` GraphQL mutation response format
- **Save Profiles**: The `/v1/save-profiles` endpoint saves profiles to Connectra and returns the actual saved count
- **Profiles Array Limit**: Maximum 1000 profiles per save request
- **Accurate Metrics**: The `saved_count` reflects actual contacts saved (contacts_created + contacts_updated) from Connectra
- **Parallel Processing**: Company and contact saves are performed in parallel for better performance

## 2026 contract note

- Canonical implemented routes: `/v1/scrape`, `/v1/save-profiles`, `/v1/health`.
- Any documented non-implemented routes should be marked planned/deprecated until delivered.