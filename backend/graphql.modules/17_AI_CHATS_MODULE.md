# AI Chats Module

## Overview

The AI Chats module exposes GraphQL operations for AI chat threads and for utility AI calls (email risk, company summary, natural language filter parsing). Resolvers use **`LambdaAIClient`** (`app/clients/lambda_ai_client.py`) to call the **Contact AI** REST microservice — codebase **`backend(dev)/contact.ai`** (FastAPI on AWS Lambda). That service persists chats in PostgreSQL table **`ai_chats`** (same database cluster as the Contact360 gateway app) and runs inference through **Hugging Face Inference Providers** (OpenAI-compatible chat completions and JSON tasks), not Google Gemini.

**Location (GraphQL):** `app/graphql/modules/ai_chats/`

**Backend service (REST):** `backend(dev)/contact.ai` — see `app/api/v1/endpoints/ai_chats.py`, `app/api/v1/endpoints/ai.py`, `app/services/hf_service.py`. Postman: `docs/media/postman/Contact AI Service.postman_collection.json`.

**Contract note:** The Contact AI API uses routes under `/api/v1/ai-chats/…` and `/api/v1/ai/…`. Ensure `LambdaAIClient` base URL and paths match the deployed service (utility endpoints were historically documented as `/gemini/…`; the canonical service uses `/api/v1/ai/…`).

GraphQL paths: `query { aiChats { aiChats(filters: { ... }) { ... } aiChat(chatId: "...") { ... } } }`, `mutation { aiChats { createAIChat(...) sendMessage(...) } }`.

## Queries and mutations – parameters and variable types

| Operation | Parameter(s) | Variable type (GraphQL) | Return type |
|-----------|---------------|-------------------------|-------------|
| **Queries** (under `aiChats { ... }`) | | | |
| `aiChats` | `filters` | `AIChatFilterInput` (optional; `limit`, `offset`, `title`, `search`, `createdAtAfter`, `createdAtBefore`, `ordering`, …) | `AIChatConnection` |
| `aiChat` | `chatId` | `String!` | `AIChat` |
| **Mutations** (under `aiChats { ... }`) | | | |
| `createAIChat` | `input` | `CreateAIChatInput!` | `AIChat` |
| `updateAIChat` | `chatId`, `input` | `String!`, `UpdateAIChatInput!` | `AIChat` |
| `deleteAIChat` | `chatId` | `String!` | `Boolean` |
| `sendMessage` | `input` | `SendMessageInput!` | message / chat result (see schema) |
| `analyzeEmailRisk` | `input` | `AnalyzeEmailRiskInput!` | analysis result |
| `generateCompanySummary` | `input` | `GenerateCompanySummaryInput!` | summary result |
| `parseContactFilters` | `input` | `ParseContactFiltersInput!` | parsed filters |

Use camelCase in variables (`chatId`, `createdAtAfter`, …). Chat and message operations call the Contact AI service via `LambdaAIClient`. See Input Types for each input's fields.

## Types

### AIChat

Full AI chat response.

```graphql
type AIChat {
  uuid: String!
  userId: String!
  title: String!
  messages: [Message!]!
  createdAt: DateTime!
  updatedAt: DateTime
}
```

### AIChatListItem

AI chat in list responses.

```graphql
type AIChatListItem {
  uuid: String!
  title: String!
  createdAt: DateTime!
  updatedAt: DateTime
}
```

### Message

Message in a chat conversation.

```graphql
type Message {
  sender: String!
  text: String!
  contacts: [ContactInMessage!]
}
```

**Sender values:** `user`, `ai`

### ContactInMessage

Contact object included in AI message responses.

```graphql
type ContactInMessage {
  uuid: String
  firstName: String
  lastName: String
  title: String
  company: String
  email: String
  city: String
  state: String
  country: String
}
```

### AIChatConnection

Paginated connection of AI chats.

```graphql
type AIChatConnection {
  items: [AIChatListItem!]!
  pageInfo: PageInfo!
}
```

### ModelSelection

Optional override for `sendMessage` / streaming (when exposed). GraphQL enum **`ModelSelection`** is defined in `app/graphql/modules/ai_chats/types.py` and maps to string values sent to the Contact AI REST API in the `model` field.

The **Contact AI** service (`backend(dev)/contact.ai/app/schemas/ai_chat.py`) defines its own `ModelSelection` with **Hugging Face** model ids (e.g. `Qwen/Qwen2.5-7B-Instruct-1M:fastest`, `HuggingFaceH4/zephyr-7b-beta:fastest`, …). **GraphQL enum values must stay aligned** with whatever the deployed Contact AI API accepts; if the GraphQL layer still maps to legacy Gemini-style strings, update the enum and client to match the HF ids or add a mapping layer.

```graphql
enum ModelSelection {
  FLASH
  PRO
  FLASH_2_0
  PRO_2_5
}
```

### EmailRiskAnalysisResponse

Response from email risk analysis.

```graphql
type EmailRiskAnalysisResponse {
  riskScore: Int!
  analysis: String!
  isRoleBased: Boolean!
  isDisposable: Boolean!
}
```

**Fields:**
- `riskScore` (Int!): Risk score from 0-100 (higher = higher risk)
- `analysis` (String!): Detailed text analysis of risk factors
- `isRoleBased` (Boolean!): Whether email is role-based (info@, support@, admin@)
- `isDisposable` (Boolean!): Whether email is from a disposable email service

### CompanySummaryResponse

Response from company summary generation.

```graphql
type CompanySummaryResponse {
  summary: String!
}
```

**Fields:**
- `summary` (String!): AI-generated company summary with insights and context

### ParseFiltersResponse

Response from parsing natural language filters.

```graphql
type ParseFiltersResponse {
  jobTitles: [String!]
  companyNames: [String!]
  industry: [String!]
  location: [String!]
  employees: [Int!]
  seniority: [String!]
}
```

**Fields:**
- `jobTitles` ([String!]): Extracted job titles (e.g., "VP", "CEO", "Director")
- `companyNames` ([String!]): Extracted company names
- `industry` ([String!]): Extracted industry sectors
- `location` ([String!]): Extracted locations (city, state, country)
- `employees` ([Int!]): Employee count range as [min, max] (null if no range)
- `seniority` ([String!]): Extracted seniority levels (e.g., "CXO", "VP", "Director")

## Queries

### aiChats

List all AI chat conversations for the current user with pagination.

**Parameters:**

| Name    | Type                | Required | Description                    |
|---------|---------------------|----------|--------------------------------|
| filters | AIChatFilterInput   | No       | title, search, limit, offset, ordering |

```graphql
query ListAIChats($filters: AIChatFilterInput) {
  aiChats {
    aiChats(filters: $filters) {
      items {
        uuid
        title
        createdAt
        updatedAt
      }
      pageInfo {
        total
        limit
        offset
      }
    }
  }
}
```

**Variables:**
```json
{
  "filters": {
    "title": "contact search",
    "search": "VP",
    "limit": 20,
    "offset": 0,
    "ordering": "-created_at"
  }
}
```

**Arguments:**
- `filters` (AIChatFilterInput): Optional filter criteria

**Returns:** `AIChatConnection`

**Authentication:** Required

**Validation:**
- Pagination is validated via `validate_pagination` utility
- `title`: Optional, max 255 characters if provided
- `search`: Optional, max 500 characters if provided
- `limit` and `offset`: Validated via `validate_pagination` utility

**Implementation Details:**
- Users can only view their own chats (filtered by user_id)
- Uses `LambdaAIClient.list_chats` → `GET /api/v1/ai-chats/` with `X-User-ID`
- Activity logging is non-blocking (errors are logged but don't affect the operation)

**Example Response:**
```json
{
  "data": {
    "aiChats": {
      "aiChats": {
        "items": [
          {
            "uuid": "chat_123456",
            "title": "Find VPs in Tech",
            "createdAt": "2024-01-15T10:30:00Z",
            "updatedAt": "2024-01-15T11:00:00Z"
          }
        ],
        "pageInfo": {
          "total": 1,
          "limit": 20,
          "offset": 0
        }
      }
    }
  }
}
```

### aiChat

Get detailed information about a specific AI chat conversation, including all messages.

**Parameters:**

| Name   | Type    | Required | Description  |
|--------|---------|----------|--------------|
| chatId | String! | Yes      | Chat UUID    |

```graphql
query GetAIChat($chatId: String!) {
  aiChats {
    aiChat(chatId: $chatId) {
      uuid
      title
      messages {
        sender
        text
        contacts {
          firstName
          lastName
          email
          title
          company
        }
      }
      createdAt
      updatedAt
    }
  }
}
```

**Arguments:**
- `chatId` (String!): Chat UUID (must be valid UUID format if it looks like a UUID)

**Returns:** `AIChat`

**Authentication:** Required

**Validation:**
- `chatId`: Required, non-empty string
- If chatId looks like a UUID (36 characters with dashes), it must be valid UUID format

**Implementation Details:**
- Users can only view their own chats (ownership verified via user_id)
- Uses `LambdaAIClient.get_chat` → `GET /api/v1/ai-chats/{chat_id}/`
- Activity logging is non-blocking (errors are logged but don't affect the operation)

**Example Response:**
```json
{
  "data": {
    "aiChats": {
      "aiChat": {
        "uuid": "chat_123456",
        "title": "Find VPs in Tech",
        "messages": [
          {
            "sender": "user",
            "text": "Find VPs at tech companies in San Francisco",
            "contacts": null
          },
          {
            "sender": "ai",
            "text": "I found 25 VPs at tech companies in San Francisco. Here are the top results:",
            "contacts": [
              {
                "firstName": "John",
                "lastName": "Doe",
                "email": "john.doe@example.com",
                "title": "VP Engineering",
                "company": "Acme Corp"
              }
            ]
          }
        ],
        "createdAt": "2024-01-15T10:30:00Z",
        "updatedAt": "2024-01-15T11:00:00Z"
      }
    }
  }
}
```

## Mutations

### createAIChat

Create a new AI chat conversation.

**Parameters:**

| Name  | Type                 | Required | Description        |
|-------|----------------------|----------|--------------------|
| input | CreateAIChatInput!   | Yes      | title, messages    |

```graphql
mutation CreateAIChat($input: CreateAIChatInput!) {
  aiChats {
    createAIChat(input: $input) {
      uuid
      title
      messages {
        sender
        text
      }
      createdAt
    }
  }
}
```

**Variables:**
```json
{
  "input": {
    "title": "Find VPs in Tech",
    "messages": [
      {
        "sender": "user",
        "text": "Find VPs at tech companies"
      }
    ]
  }
}
```

**Input:** `CreateAIChatInput!`

**Returns:** `AIChat`

**Authentication:** Required

**Validation:**
- `title`: Optional, max 255 characters if provided
- `messages`: Optional, max 100 messages per chat
- Each message `text`: Max 10,000 characters
- Input validation is performed via `input.validate()` method

**Implementation Details:**
- Uses `LambdaAIClient.create_chat` → `POST /api/v1/ai-chats/`
- Messages are converted to dict format before sending to Contact AI
- Activity logging is non-blocking (errors are logged but don't affect the operation)

### updateAIChat

Update an existing AI chat conversation.

**Parameters:**

| Name   | Type                 | Required | Description     |
|--------|----------------------|----------|----------------|
| chatId | String!              | Yes      | Chat UUID      |
| input  | UpdateAIChatInput!   | Yes      | title, messages |

```graphql
mutation UpdateAIChat($chatId: String!, $input: UpdateAIChatInput!) {
  aiChats {
    updateAIChat(chatId: $chatId, input: $input) {
      uuid
      title
      messages {
        sender
        text
      }
    }
  }
}
```

**Variables:**
```json
{
  "chatId": "chat_123456",
  "input": {
    "title": "Updated Title",
    "messages": [
      {
        "sender": "user",
        "text": "Updated message"
      }
    ]
  }
}
```

**Arguments:**
- `chatId` (String!): Chat UUID (must be valid UUID format if it looks like a UUID)
- `input` (UpdateAIChatInput!): Update data

**Returns:** `AIChat`

**Authentication:** Required

**Validation:**
- `chatId`: Required, non-empty string
- `title`: Optional, max 255 characters if provided
- `messages`: Optional, max 100 messages per chat
- Each message `text`: Max 10,000 characters

**Implementation Details:**
- Users can only update their own chats (ownership verified via user_id)
- Uses `LambdaAIClient.update_chat` → `PUT /api/v1/ai-chats/{chat_id}/`
- Activity logging is non-blocking (errors are logged but don't affect the operation)

### deleteAIChat

Delete an AI chat conversation.

**Parameters:**

| Name   | Type   | Required | Description |
|--------|--------|----------|-------------|
| chatId | String!| Yes      | Chat UUID   |

```graphql
mutation DeleteAIChat($chatId: String!) {
  aiChats {
    deleteAIChat(chatId: $chatId)
  }
}
```

**Arguments:**
- `chatId` (String!): Chat UUID (must be valid UUID format if it looks like a UUID)

**Returns:** `Boolean`

**Authentication:** Required

**Validation:**
- `chatId`: Required, non-empty string

**Implementation Details:**
- Users can only delete their own chats (ownership verified before deletion)
- Uses `LambdaAIClient.delete_chat` → `DELETE /api/v1/ai-chats/{chat_id}/`
- Activity logging is non-blocking (errors are logged but don't affect the operation)

### sendMessage

Send a message in a chat and get AI response.

**Parameters:**

| Name   | Type               | Required | Description   |
|--------|--------------------|----------|---------------|
| chatId | String!            | Yes      | Chat UUID     |
| input  | SendMessageInput!  | Yes      | message, model |

```graphql
mutation SendMessage($chatId: String!, $input: SendMessageInput!) {
  aiChats {
    sendMessage(chatId: $chatId, input: $input) {
      uuid
      title
      messages {
        sender
        text
        contacts {
          firstName
          lastName
          email
          title
          company
        }
      }
    }
  }
}
```

**Variables:**
```json
{
  "chatId": "chat_123456",
  "input": {
    "message": "Find more contacts in New York",
    "model": "PRO"
  }
}
```

**Arguments:**
- `chatId` (String!): Chat UUID (must be valid UUID format if it looks like a UUID)
- `input` (SendMessageInput!): Message data

**Returns:** `AIChat`

**Authentication:** Required

**Validation:**
- `chatId`: Required, non-empty string
- `message`: Required, non-empty string, min 1 character, max 10,000 characters
- `model`: Optional, must be one of: `FLASH`, `PRO`, `FLASH_2_0`, `PRO_2_5`

**Implementation Details:**
- Users can only send messages in their own chats (ownership verified via user_id)
- Uses `LambdaAIClient.send_message` → `POST /api/v1/ai-chats/{chat_id}/message` (Contact AI + Hugging Face chat completions)
- Model selection: GraphQL `ModelSelection` values must match strings accepted by Contact AI (see **ModelSelection** above)
- Activity logging is non-blocking (errors are logged but don't affect the operation)

### analyzeEmailRisk

Analyze an email address for potential risk factors via Contact AI (`HFService` / LLM JSON).

**Parameters:**

| Name  | Type                     | Required | Description  |
|-------|--------------------------|----------|--------------|
| input | AnalyzeEmailRiskInput!   | Yes      | email        |

```graphql
mutation AnalyzeEmailRisk($input: AnalyzeEmailRiskInput!) {
  aiChats {
    analyzeEmailRisk(input: $input) {
      riskScore
      analysis
      isRoleBased
      isDisposable
    }
  }
}
```

**Variables:**
```json
{
  "input": {
    "email": "info@example.com"
  }
}
```

**Input:** `AnalyzeEmailRiskInput!`

**Returns:** `EmailRiskAnalysisResponse`

**Authentication:** Required

**Validation:**
- `email`: Required, must be valid email format, max 255 characters

**Implementation Details:**
- Uses `LambdaAIClient.analyze_email_risk` → `POST /api/v1/ai/email/analyze` (see Contact AI; client path must match deployment)
- Analyzes email for risk factors: role-based emails, disposable email addresses
- Returns risk score (0–100 in prompts/schema), detailed analysis, and boolean flags
- Activity logging is non-blocking (errors are logged but don't affect the operation)

### generateCompanySummary

Generate an AI-powered company summary via Contact AI.

**Parameters:**

| Name  | Type                           | Required | Description          |
|-------|--------------------------------|----------|----------------------|
| input | GenerateCompanySummaryInput!   | Yes      | companyName, industry |

```graphql
mutation GenerateCompanySummary($input: GenerateCompanySummaryInput!) {
  aiChats {
    generateCompanySummary(input: $input) {
      summary
    }
  }
}
```

**Variables:**
```json
{
  "input": {
    "companyName": "Acme Corporation",
    "industry": "Technology"
  }
}
```

**Input:** `GenerateCompanySummaryInput!`

**Returns:** `CompanySummaryResponse`

**Authentication:** Required

**Validation:**
- `companyName`: Required, max 255 characters
- `industry`: Required, max 255 characters

**Implementation Details:**
- Uses `LambdaAIClient.generate_company_summary` → `POST /api/v1/ai/company/summary`
- Generates comprehensive summary with insights and context
- Activity logging is non-blocking (errors are logged but don't affect the operation)

### parseContactFilters

Parse a natural language query into structured contact filter parameters via Contact AI.

**Parameters:**

| Name  | Type               | Required | Description  |
|-------|--------------------|----------|--------------|
| input | ParseFiltersInput! | Yes      | query (natural language) |

```graphql
mutation ParseFilters($input: ParseFiltersInput!) {
  aiChats {
    parseContactFilters(input: $input) {
      jobTitles
      companyNames
      industry
      location
      employees
      seniority
    }
  }
}
```

**Variables:**
```json
{
  "input": {
    "query": "Find VPs and Directors at tech companies in San Francisco with 100-500 employees"
  }
}
```

**Input:** `ParseFiltersInput!`

**Returns:** `ParseFiltersResponse`

**Authentication:** Required

**Validation:**
- `query`: Required, non-empty string, max 1000 characters

**Implementation Details:**
- Uses `LambdaAIClient.parse_contact_filters` → `POST /api/v1/ai/parse-filters`
- Extracts structured filter parameters: job titles, company names, industries, locations, employee counts, seniority levels
- Parsed filters can be used in contact queries
- Activity logging is non-blocking (errors are logged but don't affect the operation)

## Input Types

### CreateAIChatInput

Input for creating a new AI chat.

```graphql
input CreateAIChatInput {
  title: String
  messages: [MessageInput!]
}
```

**Fields:**
- `title` (String): Chat title (max 255 characters, default: "")
- `messages` ([MessageInput!]): List of initial messages

### UpdateAIChatInput

Input for updating an AI chat.

```graphql
input UpdateAIChatInput {
  title: String
  messages: [MessageInput!]
}
```

**Fields:**
- `title` (String): New chat title (max 255 characters)
- `messages` ([MessageInput!]): Complete list of messages (replaces existing)

### SendMessageInput

Input for sending a message in a chat.

```graphql
input SendMessageInput {
  message: String!
  model: ModelSelection
}
```

**Fields:**
- `message` (String!): User message text (min length: 1)
- `model` (ModelSelection): Optional model selection override

### MessageInput

Input for a message in a chat.

```graphql
input MessageInput {
  sender: String!
  text: String!
  contacts: [ContactInMessageInput!]
}
```

**Validation:**
- Sender must be "user" or "ai"
- Text is required and cannot be empty

### ContactInMessageInput

Input for contact object in messages.

```graphql
input ContactInMessageInput {
  uuid: String
  firstName: String
  lastName: String
  title: String
  company: String
  email: String
  city: String
  state: String
  country: String
}
```

### AIChatFilterInput

Input for filtering AI chats.

```graphql
input AIChatFilterInput {
  title: String
  search: String
  createdAtAfter: DateTime
  createdAtBefore: DateTime
  ordering: String
  limit: Int
  offset: Int
}
```

**Ordering values:** `created_at`, `updated_at`, `-created_at`, `-updated_at` (default: `-created_at`)

### AnalyzeEmailRiskInput

Input for analyzing email risk.

```graphql
input AnalyzeEmailRiskInput {
  email: String!
}
```

**Validation:**
- Email is required and cannot be empty
- Email must be a valid email address format

### GenerateCompanySummaryInput

Input for generating company summary.

```graphql
input GenerateCompanySummaryInput {
  companyName: String!
  industry: String!
}
```

**Validation:**
- `companyName` is required and cannot be empty
- `industry` is required and cannot be empty

### ParseFiltersInput

Input for parsing natural language filters.

```graphql
input ParseFiltersInput {
  query: String!
}
```

**Fields:**
- `query` (String!): Natural language query describing the contact filters to extract - max 1000 characters

**Validation:**
- `query`: Required, non-empty, max 1000 characters
- Input validation is performed via `input.validate()` method

## Error Handling

The AI Chats module implements comprehensive error handling with input validation, database error handling, external service error handling, and response validation.

### Error Types

The AI Chats module may raise the following errors:

- **NotFoundError** (404): Chat not found
  - Code: `NOT_FOUND`
  - Extensions: `resourceType: "AIChat"`, `identifier: <chat_id>`
  - Occurs when: Requested chat ID does not exist or belongs to another user
- **ForbiddenError** (403): User doesn't own the chat
  - Code: `FORBIDDEN`
  - Extensions: `requiredRole: <role>` (if applicable)
  - Occurs when: User attempts to access or modify a chat they don't own
- **ValidationError** (422): Input validation failed
  - Code: `VALIDATION_ERROR`
  - Extensions: `fieldErrors` (field-specific errors)
  - Occurs when: Invalid chat ID format, invalid message format, invalid model selection, invalid title length (max 255), or missing required fields
- **BadRequestError** (400): Invalid request data
  - Code: `BAD_REQUEST`
  - Occurs when: Request format is invalid, message is empty, or invalid message sender value
- **ServiceUnavailableError** (503): Contact AI / upstream inference unavailable
  - Code: `SERVICE_UNAVAILABLE`
  - Extensions: `serviceName: "lambda_ai"` (and optionally upstream Hugging Face errors surfaced by the service)
  - Occurs when: Contact AI API is down, Hugging Face Inference is unavailable, timeout occurs, or connection fails
- **RateLimitError** (429): Rate limit exceeded
  - Code: `RATE_LIMIT_EXCEEDED`
  - Extensions: `retryAfter: <seconds>`
  - Occurs when: Too many requests to AI service within time window

### Error Response Examples

**Example: Chat Not Found**
```json
{
  "errors": [
    {
      "message": "AIChat with identifier 'chat_123456' not found",
      "extensions": {
        "code": "NOT_FOUND",
        "statusCode": 404,
        "resourceType": "AIChat",
        "identifier": "chat_123456"
      }
    }
  ]
}
```

**Example: Validation Error**
```json
{
  "errors": [
    {
      "message": "Invalid message format",
      "extensions": {
        "code": "VALIDATION_ERROR",
        "statusCode": 422,
        "fieldErrors": {
          "message": ["Message is required", "Message cannot be empty"],
          "title": ["Title cannot exceed 255 characters"],
          "model": ["Model must be one of: FLASH, PRO, FLASH_2_0, PRO_2_5"]
        }
      }
    }
  ]
}
```

**Example: Service Unavailable**
```json
{
  "errors": [
    {
      "message": "AI service temporarily unavailable. Please try again later.",
      "extensions": {
        "code": "SERVICE_UNAVAILABLE",
        "statusCode": 503,
        "serviceName": "lambda_ai"
      }
    }
  ]
}
```

**Example: Rate Limit Error**
```json
{
  "errors": [
    {
      "message": "Rate limit exceeded. Please try again later.",
      "extensions": {
        "code": "RATE_LIMIT_EXCEEDED",
        "statusCode": 429,
        "retryAfter": 60
      }
    }
  ]
}
```

### Error Handling Patterns

- **Input Validation**: Chat IDs, messages, titles, models, and filter parameters are validated before processing
- **Database Errors**: All database operations include transaction rollback on failure
- **External Service Errors**: Contact AI (`LambdaAIClient`) and upstream inference errors are caught and converted to appropriate GraphQL errors
- **User Isolation**: Users can only access their own chats
- **Message Validation**: Messages are validated for sender type ("user" or "ai") and content
- **Response Validation**: AI responses are validated before returning to clients
- **Error Logging**: Comprehensive error logging with context for debugging

## Usage Examples

### Complete AI Chat Flow

```graphql
# 1. Create a new chat
mutation CreateChat {
  aiChats {
    createAIChat(input: {
      title: "Find VPs in Tech"
      messages: [
        {
          sender: "user"
          text: "Find VPs at tech companies in San Francisco"
        }
      ]
    }) {
      uuid
      title
      messages {
        sender
        text
      }
    }
  }
}

# 2. Send a message
mutation SendMessage {
  aiChats {
    sendMessage(
      chatId: "chat_123456"
      input: {
        message: "Find more contacts in New York"
        model: PRO
      }
    ) {
      uuid
      messages {
        sender
        text
        contacts {
          firstName
          lastName
          email
          title
        }
      }
    }
  }
}

# 3. List all chats
query ListChats {
  aiChats {
    aiChats(filters: {
      limit: 20
      ordering: "-updated_at"
    }) {
      items {
        uuid
        title
        createdAt
        updatedAt
      }
      pageInfo {
        total
      }
    }
  }
}

# 4. Get specific chat
query GetChat {
  aiChats {
    aiChat(chatId: "chat_123456") {
      uuid
      title
      messages {
        sender
        text
        contacts {
          firstName
          lastName
          email
        }
      }
    }
  }
}

# 5. Update chat title
mutation UpdateChat {
  aiChats {
    updateAIChat(
      chatId: "chat_123456"
      input: {
        title: "Updated Title"
      }
    ) {
      uuid
      title
    }
  }
}

# 6. Delete chat
mutation DeleteChat {
  aiChats {
    deleteAIChat(chatId: "chat_123456")
  }
}
```

## Implementation Details

### External Service Integration

- **LambdaAIClient**: All AI operations (chat and analysis) are handled via `LambdaAIClient` → Contact AI REST API (`LAMBDA_AI_API_URL`, `LAMBDA_AI_API_KEY`; headers `X-API-Key`, and `X-User-ID` for chat routes)
  - Connection errors are converted to ServiceUnavailableError
  - API errors are parsed and converted to appropriate GraphQL errors
  - Rate limit handling with retry_after information
  - Timeout handling with retry logic
- **Contact AI / Hugging Face**: Chat completions and JSON tasks use Hugging Face Inference Providers (see `backend(dev)/contact.ai`)
  - Default chat model is configured server-side (`HF_CHAT_MODEL`); optional per-message override via `SendMessageInput.model` when values match the deployed API

### Chat Management

- **User Isolation**: Users can only access their own chats (filtered by user_id)
  - Ownership is verified before any operation (create, read, update, delete, send message)
  - ForbiddenError is raised if user tries to access another user's chat
- **Message History**: All messages are stored and maintained in the chat
  - Messages are ordered chronologically
  - Maximum 100 messages per chat
  - Each message text: max 10,000 characters
- **Chat operations**: All chat operations go through `LambdaAIClient` to Contact AI
  - Create, update, delete, list, get, send message
  - **Persistence:** Chats are stored in PostgreSQL table **`ai_chats`** by the Contact AI service (same database as the Contact360 gateway; `user_id` references `users.uuid`)

### AI analysis operations (stateless REST)

- **Email risk analysis**: LLM JSON scoring via Contact AI `HFService`
  - Returns risk score, detailed analysis, role-based flag, disposable flag
  - Email validation: max 255 characters, must be valid email format
- **Company summary generation**: LLM-generated summary from company name + industry
  - Input: company name (max 255 chars), industry (max 255 chars)
- **Natural language filter parsing**: Parses NL into structured filters for contact search
  - Extracts: job titles, company names, industries, locations, employee counts, seniority levels
  - Parsed filters can be used in contact queries

### Validation

- **Input Validation**: All inputs are validated before processing
  - `title`: Optional, max 255 characters
  - `search`: Optional, max 500 characters
  - `message`: Required, min 1 character, max 10,000 characters
  - `email`: Required, max 255 characters, must be valid email format
  - `companyName`/`industry`: Required, max 255 characters each
  - `chatId`: Required, non-empty string (UUID format validated if it looks like UUID)
  - Messages limit: max 100 messages per chat
  - Pagination: validated via `validate_pagination` utility
- **Validation Methods**: Input validation is performed via `input.validate()` method
  - Raises ValueError with descriptive messages
  - Converted to ValidationError for GraphQL responses

### Activity Logging

- **Non-Blocking**: Activity logging is non-blocking - if logging fails, the operation still succeeds
  - Activity logging errors are caught and logged but don't affect the primary operation
  - Logs include: operation type, user UUID, chat ID, model used, metadata
  - Both success and failure activities are logged (non-blocking)

### Error Handling

- **Input Validation**: All inputs are validated before processing
  - String length validation (title, search, message, email, company_name, industry)
  - UUID format validation for chat IDs
  - Email format validation
  - Message count and length limits
- **External Service Error Handling**: Lambda AI API errors are handled centrally via `handle_lambda_ai_error`
  - Rate limit errors are converted to RateLimitError with retry_after
  - Validation errors from Lambda AI are converted to ValidationError
  - Connection/timeout errors are converted to ServiceUnavailableError
  - 404 errors are converted to NotFoundError
- **Response Validation**: All API responses are validated before returning
  - Chat data structure validation
  - AI analysis response validation
  - Required fields validation
- **Ownership Verification**: User ownership is verified for all chat operations
  - ForbiddenError is raised if user doesn't own the chat
  - Ownership check happens before any modification operation

## Task breakdown (for maintainers)

1. **aiChats/aiChat:** Resolver → `LambdaAIClient` → Contact AI REST; user isolation (`userId` from context); pagination for list; messages loaded with chat from API response.
2. **createAIChat/updateAIChat/deleteAIChat:** CRUD via Contact AI; validate title and input; persistence is **`ai_chats`** in Postgres (service-side); activity logging (AI_CHATS, CREATE/UPDATE/DELETE).
3. **sendMessage:** `SendMessageInput` (chatId, message, model); Contact AI Hugging Face chat completion; map `ModelSelection` enum strings to deployed HF model ids if needed.
4. **analyzeEmailRisk/generateCompanySummary/parseContactFilters:** Map inputs to `POST /api/v1/ai/...` responses; ensure `LambdaAIClient` paths match Contact AI (`/api/v1/ai/`, not legacy `/gemini/`); non-blocking activity log where documented.
5. **Error handling:** `handle_lambda_ai_error` / external errors; validate response shape; document rate limits and timeout; keep [README External Services](README.md#module-dependencies) in sync.

## Related Modules

- **Contacts Module**: AI can search and return contacts; parsed filters can be used in contact queries
- **Companies Module**: AI can search and return companies; company summaries provide insights
- **Email Module**: Email risk analysis complements email verification
- **Activities Module**: All AI Chats operations are tracked in user activities

## Direct Contact AI REST contract (source service)

The GraphQL module proxies all AI operations through `LambdaAIClient` → Contact AI (`backend(dev)/contact.ai`). The canonical REST endpoints are:

### Chat endpoints

| Method | Path | Auth | Description |
| --- | --- | --- | --- |
| `GET` | `/api/v1/ai-chats/` | `X-API-Key` + `X-User-ID` | List user chats |
| `POST` | `/api/v1/ai-chats/` | `X-API-Key` + `X-User-ID` | Create chat |
| `GET` | `/api/v1/ai-chats/{id}/` | `X-API-Key` + `X-User-ID` | Get chat |
| `PUT` | `/api/v1/ai-chats/{id}/` | `X-API-Key` + `X-User-ID` | Update chat |
| `DELETE` | `/api/v1/ai-chats/{id}/` | `X-API-Key` + `X-User-ID` | Delete chat |
| `POST` | `/api/v1/ai-chats/{id}/message` | `X-API-Key` + `X-User-ID` | Send message (sync) |
| `POST` | `/api/v1/ai-chats/{id}/message/stream` | `X-API-Key` + `X-User-ID` | Send message (SSE stream) |

### Utility AI endpoints (stateless — no DB write)

| Method | Path | Auth | Description |
| --- | --- | --- | --- |
| `POST` | `/api/v1/ai/email/analyze` | `X-API-Key` | Email risk analysis |
| `POST` | `/api/v1/ai/company/summary` | `X-API-Key` | Company summary generation |
| `POST` | `/api/v1/ai/parse-filters` | `X-API-Key` | NL → structured contact filters |

> **Legacy path note:** Some older docs referenced `/gemini/…` paths. The canonical service uses `/api/v1/ai/…`. `LambdaAIClient` paths must match the deployed service.

### ModelSelection enum — canonical HF model IDs

| GraphQL enum | HF model ID |
| --- | --- |
| `FLASH` | `Qwen/Qwen2.5-7B-Instruct-1M:fastest` |
| `PRO` | `HuggingFaceH4/zephyr-7b-beta:fastest` |
| `FLASH_2_0` | `meta-llama/Llama-3.1-8B-Instruct:fastest` |
| `PRO_2_5` | `mistralai/Mistral-7B-Instruct-v0.3:fastest` |

`LambdaAIClient` must map GraphQL enum string values to these HF model IDs before sending to Contact AI.

### Known gaps

- `ModelSelection` enum in GraphQL uses legacy names; mapping shim required in `LambdaAIClient`.
- Single global `API_KEY` in `0.x`–`7.x`; per-tenant scoped keys target: `8.x`.
- `messages` JSONB schema is application-only validated; no DB-level JSON schema constraint.
- SSE streaming endpoint requires client reconnect logic for Lambda timeout handling.

## Era binding

- This module is operationally relevant from `5.x` through `10.x` (primary era: `5.x`).
- Utility endpoints (`analyzeEmailRisk`, `generateCompanySummary`, `parseContactFilters`) are available as stubs from `2.x`/`3.x`.
- `email/generate` endpoint (campaign AI) planned for `10.x`.

## Maintenance references

- Era index: `docs/backend/apis/CONTACT_AI_ERA_TASK_PACKS.md`
- Data lineage: `docs/backend/database/contact_ai_data_lineage.md`
- UI bindings: `docs/frontend/contact-ai-ui-bindings.md`
- Endpoint matrix: `docs/backend/endpoints/contact_ai_endpoint_era_matrix.json`
- Codebase analysis: `docs/codebases/contact-ai-codebase-analysis.md`

## Documentation metadata

- Era: `5.x`–`10.x`
- Introduced in: `5.x` (chat + streaming + all utility endpoints live)
- Frontend bindings: `docs/frontend/contact-ai-ui-bindings.md`
- Data stores touched: PostgreSQL `ai_chats` (chat CRUD); stateless for utility endpoints

## Endpoint/version binding checklist

- Add operation list with `introduced_in` / `deprecated_in` tags.
- Map each operation to frontend page bindings and hook/service usage.
- Record DB tables read/write for each operation.
- Keep `LambdaAIClient` paths aligned with actual deployed Contact AI route paths.

## 2026 route-contract correction

- Canonical routes are `/api/v1/ai/*` (chat) and `/api/v1/ai-*` utility paths.
- Stale `/api/v2` and `/gemini` path references are deprecated documentation drift and not canonical API contracts.

