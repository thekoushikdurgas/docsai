# Contact AI Service - API Reference

Complete API reference for the Lambda Contact AI Service deployed on AWS API Gateway.

**Go / EC2 target:** `EC2/ai.server/` — module `contact360.io/ai` (HF router `/v1/chat/completions`, `/v1/embeddings`, RAG helpers, Asynq workers for heavy tasks). Gateway may delegate to this satellite when wired.

## Documentation map

| Doc | Purpose |
| --- | --- |
| [SERVICE_TOPOLOGY.md](../endpoints/SERVICE_TOPOLOGY.md) | Contact AI in the delegation map |
| [contact_ai_endpoint_era_matrix.md](../endpoints/contact_ai_endpoint_era_matrix.md) | HTTP + era alignment |
| [contact_ai_data_lineage.md](../database/contact_ai_data_lineage.md) | `ai_chats` and related storage |
| [ENDPOINT_DATABASE_LINKS.md](../endpoints/ENDPOINT_DATABASE_LINKS.md) | Gateway GraphQL ops that call AI utilities |
| [index.md](../endpoints/index.md) | e.g. `graphql/CreateAIChat`, `graphql/AnalyzeEmailRisk`, parse filters |

Dashboard calls **appointment360** GraphQL; resolvers invoke this Lambda’s REST/SSE contracts where configured.

### Also in `docs/backend/endpoints/`

- **[README.md](../endpoints/README.md)** — matrix registry includes `contact_ai`.
- **[endpoints_index.md](../endpoints/endpoints_index.md)** — [contact_ai_endpoint_era_matrix.md](../endpoints/contact_ai_endpoint_era_matrix.md) in supplemental indexes; pair with [index.md](../endpoints/index.md) for GraphQL ops that list **Contact AI** / `contact.ai` under **`lambda_services`** or AI module fields in `*_graphql.md`.

## Base URL

**Production:**
```
https://aziwa531nl.execute-api.us-east-1.amazonaws.com
```

**Local Development:**
```
http://localhost:8080
```

All endpoints are prefixed with `/api/v1/`.

## Authentication

All endpoints (except health check) require API key authentication via the `X-API-Key` header. Chat endpoints also require the `X-User-ID` header.

### Required Headers

```http
X-API-Key: your-api-key-here
X-User-ID: user-uuid-here  # Required for chat endpoints
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

### Missing User ID Error Response

```json
{
  "detail": "X-User-ID header is required"
}
```

**Status Code:** `400 Bad Request`

---

## Response Format

All responses are JSON unless otherwise specified. Streaming endpoints return Server-Sent Events (SSE).

### Success Response

```json
{
  "uuid": "chat-uuid",
  "user_id": "user-uuid",
  "title": "Chat Title",
  "messages": [...],
  "created_at": "2026-01-06T00:00:00Z",
  "updated_at": "2026-01-06T00:00:00Z"
}
```

### Error Response

```json
{
  "detail": "Error message describing what went wrong"
}
```

---

## Health Check Endpoints

### `GET /api/v1/health`

Check service health status. **No authentication required.**

**Response:**

```json
{
  "status": "ok",
  "service": "Contact AI API",
  "version": "1.0.0"
}
```

**Status Codes:**
- `200 OK` - Service is healthy

**Example:**

```bash
curl https://aziwa531nl.execute-api.us-east-1.amazonaws.com/api/v1/health
```

---

## AI Chat Endpoints

### List Chats

#### `GET /api/v1/ai-chats/`

Get a paginated list of all AI chat conversations for a user.

**Headers:**
```http
X-API-Key: your-api-key-here
X-User-ID: user-uuid-here
```

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `limit` | integer | No | 25 | Number of results per page (1-100) |
| `offset` | integer | No | 0 | Offset for pagination |
| `ordering` | string | No | `-created_at` | Order by field. Prepend `-` for descending. Valid: `created_at`, `updated_at`, `-created_at`, `-updated_at` |
| `title` | string | No | - | Case-insensitive substring match against chat title |
| `search` | string | No | - | General-purpose search term applied across chat text columns |
| `created_at_after` | string | No | - | Filter chats created after ISO timestamp (inclusive) |
| `created_at_before` | string | No | - | Filter chats created before ISO timestamp (inclusive) |
| `updated_at_after` | string | No | - | Filter chats updated after ISO timestamp (inclusive) |
| `updated_at_before` | string | No | - | Filter chats updated before ISO timestamp (inclusive) |
| `page` | integer | No | - | 1-indexed page number (alternative to offset) |
| `page_size` | integer | No | - | Explicit page size override |

**Response:**

```json
{
  "count": 10,
  "next": "https://api.example.com/api/v1/ai-chats/?limit=25&offset=25",
  "previous": null,
  "results": [
    {
      "uuid": "chat-uuid-1",
      "title": "Chat Title 1",
      "created_at": "2026-01-06T00:00:00Z",
      "updated_at": "2026-01-06T01:00:00Z"
    },
    {
      "uuid": "chat-uuid-2",
      "title": "Chat Title 2",
      "created_at": "2026-01-05T00:00:00Z",
      "updated_at": null
    }
  ]
}
```

**Status Codes:**
- `200 OK` - Success
- `400 Bad Request` - Invalid query parameters
- `401 Unauthorized` - Missing or invalid API key

**Example:**

```bash
curl -X GET "https://aziwa531nl.execute-api.us-east-1.amazonaws.com/api/v1/ai-chats/?limit=10&ordering=-created_at" \
  -H "X-API-Key: your-api-key" \
  -H "X-User-ID: user-uuid"
```

---

### Create Chat

#### `POST /api/v1/ai-chats/`

Create a new AI chat conversation.

**Headers:**
```http
Content-Type: application/json
X-API-Key: your-api-key-here
X-User-ID: user-uuid-here
```

**Request Body:**

```json
{
  "title": "My Chat Title",
  "messages": []
}
```

**Request Schema:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | No | Chat title (max 255 characters, default: empty string) |
| `messages` | array | No | Initial messages array (default: empty array) |

**Response:**

```json
{
  "uuid": "new-chat-uuid",
  "user_id": "user-uuid",
  "title": "My Chat Title",
  "messages": [],
  "created_at": "2026-01-06T00:00:00Z",
  "updated_at": null
}
```

**Status Codes:**
- `201 Created` - Chat created successfully
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Missing or invalid API key

**Example:**

```bash
curl -X POST "https://aziwa531nl.execute-api.us-east-1.amazonaws.com/api/v1/ai-chats/" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -H "X-User-ID: user-uuid" \
  -d '{
    "title": "My Chat Title",
    "messages": []
  }'
```

---

### Get Chat

#### `GET /api/v1/ai-chats/{chat_id}/`

Get detailed information about a specific AI chat conversation, including all messages.

**Headers:**
```http
X-API-Key: your-api-key-here
X-User-ID: user-uuid-here
```

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chat_id` | string | Yes | Chat UUID |

**Response:**

```json
{
  "uuid": "chat-uuid",
  "user_id": "user-uuid",
  "title": "Chat Title",
  "messages": [
    {
      "sender": "user",
      "text": "Hello, how are you?",
      "contacts": null
    },
    {
      "sender": "ai",
      "text": "I'm doing well, thank you! How can I help you today?",
      "contacts": null
    }
  ],
  "created_at": "2026-01-06T00:00:00Z",
  "updated_at": "2026-01-06T01:00:00Z"
}
```

**Status Codes:**
- `200 OK` - Success
- `404 Not Found` - Chat not found or user doesn't have access
- `401 Unauthorized` - Missing or invalid API key

**Example:**

```bash
curl -X GET "https://aziwa531nl.execute-api.us-east-1.amazonaws.com/api/v1/ai-chats/chat-uuid/" \
  -H "X-API-Key: your-api-key" \
  -H "X-User-ID: user-uuid"
```

---

### Update Chat

#### `PUT /api/v1/ai-chats/{chat_id}/`

Update an existing AI chat conversation (typically to add new messages or update the title).

**Headers:**
```http
Content-Type: application/json
X-API-Key: your-api-key-here
X-User-ID: user-uuid-here
```

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chat_id` | string | Yes | Chat UUID |

**Request Body:**

```json
{
  "title": "Updated Chat Title",
  "messages": [
    {
      "sender": "user",
      "text": "Hello",
      "contacts": null
    }
  ]
}
```

**Request Schema:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | No | Chat title (max 255 characters) |
| `messages` | array | No | Complete messages array (replaces existing messages) |

**Note:** All fields are optional - only provided fields will be updated (partial update). When updating messages, provide the complete messages array (it replaces existing messages).

**Response:**

```json
{
  "uuid": "chat-uuid",
  "user_id": "user-uuid",
  "title": "Updated Chat Title",
  "messages": [...],
  "created_at": "2026-01-06T00:00:00Z",
  "updated_at": "2026-01-06T02:00:00Z"
}
```

**Status Codes:**
- `200 OK` - Chat updated successfully
- `400 Bad Request` - Invalid request data
- `404 Not Found` - Chat not found or user doesn't have access
- `401 Unauthorized` - Missing or invalid API key

**Example:**

```bash
curl -X PUT "https://aziwa531nl.execute-api.us-east-1.amazonaws.com/api/v1/ai-chats/chat-uuid/" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -H "X-User-ID: user-uuid" \
  -d '{
    "title": "Updated Chat Title"
  }'
```

---

### Send Message

#### `POST /api/v1/ai-chats/{chat_id}/message`

Send a message in a chat and get AI response.

**Headers:**
```http
Content-Type: application/json
X-API-Key: your-api-key-here
X-User-ID: user-uuid-here
```

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chat_id` | string | Yes | Chat UUID |

**Request Body:**

```json
{
  "message": "Hello, how are you?",
  "model": "gemini-1.5-flash"
}
```

**Request Schema:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `message` | string | Yes | User message text (min 1 character) |
| `model` | string | No | Optional model selection override. Valid: `gemini-1.5-flash`, `gemini-1.5-pro`, `gemini-2.0-flash-exp`, `gemini-2.5-pro` |

**Response:**

```json
{
  "uuid": "chat-uuid",
  "user_id": "user-uuid",
  "title": "Chat Title",
  "messages": [
    {
      "sender": "user",
      "text": "Hello, how are you?",
      "contacts": null
    },
    {
      "sender": "ai",
      "text": "I'm doing well, thank you! How can I help you today?",
      "contacts": null
    }
  ],
  "created_at": "2026-01-06T00:00:00Z",
  "updated_at": "2026-01-06T03:00:00Z"
}
```

**Status Codes:**
- `200 OK` - Message sent and AI response generated
- `400 Bad Request` - Invalid request data
- `404 Not Found` - Chat not found or user doesn't have access
- `401 Unauthorized` - Missing or invalid API key
- `500 Internal Server Error` - Error generating AI response

**Example:**

```bash
curl -X POST "https://aziwa531nl.execute-api.us-east-1.amazonaws.com/api/v1/ai-chats/chat-uuid/message" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -H "X-User-ID: user-uuid" \
  -d '{
    "message": "Hello, how are you?",
    "model": "gemini-1.5-flash"
  }'
```

---

### Stream Message

#### `POST /api/v1/ai-chats/{chat_id}/message/stream`

Send a message in a chat and stream AI response using Server-Sent Events (SSE).

**Headers:**
```http
Content-Type: application/json
X-API-Key: your-api-key-here
X-User-ID: user-uuid-here
```

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chat_id` | string | Yes | Chat UUID |

**Request Body:**

```json
{
  "message": "Tell me about artificial intelligence",
  "model": "gemini-1.5-flash"
}
```

**Request Schema:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `message` | string | Yes | User message text (min 1 character) |
| `model` | string | No | Optional model selection override |

**Response:**

Content-Type: `text/event-stream`

```
data: Artificial
data:  intelligence
data:  (AI)
data:  is
data:  a
data:  branch
data:  of
data:  computer
data:  science
...
data: [DONE]
```

**Status Codes:**
- `200 OK` - Stream started successfully
- `400 Bad Request` - Invalid request data
- `404 Not Found` - Chat not found or user doesn't have access
- `401 Unauthorized` - Missing or invalid API key
- `500 Internal Server Error` - Error generating AI response

**Example:**

```bash
curl -X POST "https://aziwa531nl.execute-api.us-east-1.amazonaws.com/api/v1/ai-chats/chat-uuid/message/stream" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -H "X-User-ID: user-uuid" \
  -d '{
    "message": "Tell me about artificial intelligence"
  }' \
  --no-buffer
```

**Note:** The `--no-buffer` flag is important for streaming responses. The stream ends with `data: [DONE]`.

---

### Delete Chat

#### `DELETE /api/v1/ai-chats/{chat_id}/`

Delete an AI chat conversation.

**Headers:**
```http
X-API-Key: your-api-key-here
X-User-ID: user-uuid-here
```

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chat_id` | string | Yes | Chat UUID |

**Response:**

No content (204 No Content)

**Status Codes:**
- `204 No Content` - Chat deleted successfully
- `404 Not Found` - Chat not found or user doesn't have access
- `401 Unauthorized` - Missing or invalid API key
- `500 Internal Server Error` - Error deleting chat

**Example:**

```bash
curl -X DELETE "https://aziwa531nl.execute-api.us-east-1.amazonaws.com/api/v1/ai-chats/chat-uuid/" \
  -H "X-API-Key: your-api-key" \
  -H "X-User-ID: user-uuid"
```

**Note:** Deletion is permanent and cannot be undone.

---

## Gemini AI Endpoints

### Email Risk Analysis

#### `POST /api/v1/gemini/email/analyze`

Analyze email address for potential risk factors using Gemini AI.

**Headers:**
```http
Content-Type: application/json
X-API-Key: your-api-key-here
```

**Request Body:**

```json
{
  "email": "test@example.com"
}
```

**Request Schema:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `email` | string | Yes | Email address to analyze (must be valid email format) |

**Response:**

```json
{
  "riskScore": 5,
  "analysis": "This email appears to be a standard business email address. No significant risk factors detected.",
  "isRoleBased": false,
  "isDisposable": false
}
```

**Response Schema:**

| Field | Type | Description |
|-------|------|-------------|
| `riskScore` | integer | Risk score from 0-10 (0 = low risk, 10 = high risk) |
| `analysis` | string | Detailed analysis text |
| `isRoleBased` | boolean | Whether the email is role-based (e.g., info@, support@) |
| `isDisposable` | boolean | Whether the email is from a disposable email service |

**Status Codes:**
- `200 OK` - Analysis completed successfully
- `400 Bad Request` - Invalid email format
- `401 Unauthorized` - Missing or invalid API key
- `500 Internal Server Error` - Error analyzing email

**Example:**

```bash
curl -X POST "https://aziwa531nl.execute-api.us-east-1.amazonaws.com/api/v1/gemini/email/analyze" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "email": "test@example.com"
  }'
```

---

### Company Summary

#### `POST /api/v1/gemini/company/summary`

Generate AI-powered company summary using Gemini AI.

**Headers:**
```http
Content-Type: application/json
X-API-Key: your-api-key-here
```

**Request Body:**

```json
{
  "company_name": "Google",
  "industry": "Technology"
}
```

**Request Schema:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `company_name` | string | Yes | Company name |
| `industry` | string | Yes | Industry sector |

**Response:**

```json
{
  "summary": "Google is a multinational technology company specializing in Internet-related services and products. Founded in 1998, Google has become one of the world's most valuable companies, known for its search engine, cloud computing services, and innovative technologies like artificial intelligence and machine learning."
}
```

**Response Schema:**

| Field | Type | Description |
|-------|------|-------------|
| `summary` | string | Generated company summary text |

**Status Codes:**
- `200 OK` - Summary generated successfully
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Missing or invalid API key
- `500 Internal Server Error` - Error generating summary

**Example:**

```bash
curl -X POST "https://aziwa531nl.execute-api.us-east-1.amazonaws.com/api/v1/gemini/company/summary" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "company_name": "Google",
    "industry": "Technology"
  }'
```

---

### Parse Filters

#### `POST /api/v1/gemini/parse-filters`

Parse natural language query into structured contact filter parameters using Gemini AI.

**Headers:**
```http
Content-Type: application/json
X-API-Key: your-api-key-here
```

**Request Body:**

```json
{
  "query": "Find software engineers in San Francisco with 5-10 years of experience"
}
```

**Request Schema:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `query` | string | Yes | Natural language query to parse |

**Response:**

```json
{
  "job_titles": ["Software Engineer", "Senior Software Engineer"],
  "company_names": null,
  "industry": null,
  "location": ["San Francisco"],
  "employees": [5, 10],
  "seniority": ["Mid-level", "Senior"]
}
```

**Response Schema:**

| Field | Type | Description |
|-------|------|-------------|
| `job_titles` | array of strings | Extracted job titles (nullable) |
| `company_names` | array of strings | Extracted company names (nullable) |
| `industry` | array of strings | Extracted industries (nullable) |
| `location` | array of strings | Extracted locations (nullable) |
| `employees` | tuple of integers | Employee count range [min, max] (nullable) |
| `seniority` | array of strings | Extracted seniority levels (nullable) |

**Status Codes:**
- `200 OK` - Filters parsed successfully
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Missing or invalid API key
- `500 Internal Server Error` - Error parsing filters

**Example:**

```bash
curl -X POST "https://aziwa531nl.execute-api.us-east-1.amazonaws.com/api/v1/gemini/parse-filters" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "query": "Find software engineers in San Francisco with 5-10 years of experience"
  }'
```

---

## Error Handling

### Common Error Responses

#### 400 Bad Request

```json
{
  "detail": "X-User-ID header is required"
}
```

#### 401 Unauthorized

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

#### 404 Not Found

```json
{
  "detail": "Chat not found"
}
```

#### 500 Internal Server Error

```json
{
  "detail": "An error occurred while processing the request."
}
```

---

## Example Usage

### Complete Chat Flow

```bash
# 1. Create a new chat
CHAT_UUID=$(curl -X POST "https://aziwa531nl.execute-api.us-east-1.amazonaws.com/api/v1/ai-chats/" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -H "X-User-ID: user-uuid" \
  -d '{"title": "My Chat"}' | jq -r '.uuid')

# 2. Send a message
curl -X POST "https://aziwa531nl.execute-api.us-east-1.amazonaws.com/api/v1/ai-chats/$CHAT_UUID/message" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -H "X-User-ID: user-uuid" \
  -d '{"message": "Hello, how are you?"}'

# 3. Get chat details
curl -X GET "https://aziwa531nl.execute-api.us-east-1.amazonaws.com/api/v1/ai-chats/$CHAT_UUID/" \
  -H "X-API-Key: your-api-key" \
  -H "X-User-ID: user-uuid"

# 4. List all chats
curl -X GET "https://aziwa531nl.execute-api.us-east-1.amazonaws.com/api/v1/ai-chats/?limit=10" \
  -H "X-API-Key: your-api-key" \
  -H "X-User-ID: user-uuid"
```

---

## Rate Limiting

The service implements rate limiting to prevent abuse:
- Default: 20 requests per 60 seconds per user
- Configurable via environment variables: `AI_RATE_LIMIT_REQUESTS` and `AI_RATE_LIMIT_WINDOW`

When rate limit is exceeded, the service returns:

**Status Code:** `429 Too Many Requests`

```json
{
  "detail": "Rate limit exceeded"
}
```

---

## Best Practices

1. **Always include required headers**: `X-API-Key` for all endpoints, `X-User-ID` for chat endpoints
2. **Handle errors gracefully**: Check status codes and error messages
3. **Use pagination**: For list endpoints, use `limit` and `offset` or `page` and `page_size`
4. **Stream for long responses**: Use the streaming endpoint for better UX with long AI responses
5. **Cache when appropriate**: Chat data doesn't change frequently, consider caching
6. **Monitor rate limits**: Be aware of rate limiting and implement retry logic with exponential backoff

---

## Support

For issues or questions:
- Check CloudWatch Logs: `/aws/lambda/contact-ai`
- Review [DEPLOYMENT.md](../DEPLOYMENT.md) for deployment information
- See [INTEGRATION_TESTING.md](../INTEGRATION_TESTING.md) for testing guide

## 2026 route-contract note

- Canonical route families are `/api/v1/ai/*` and `/api/v1/ai-*`.
- Any `/api/v2` or `/gemini` direct-route references should be treated as legacy documentation drift unless explicitly reintroduced.
