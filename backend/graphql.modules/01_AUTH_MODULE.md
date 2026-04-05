# Auth Module

## Overview

The Auth module provides authentication and session management for the **Contact360 GraphQL gateway**. It handles user registration, login, logout, token refresh, and session information retrieval.

**Location:** `app/graphql/modules/auth/`

GraphQL paths: `query { auth { me { ... } session { ... } } }`, `mutation { auth { login(input: ...) { ... } } }`.

## Queries and mutations – parameters and variable types

| Operation | Parameter(s) | Variable type (GraphQL) | Return type |
|-----------|---------------|-------------------------|-------------|
| **Queries** | | | |
| `me` | — | — | `User` \| `null` |
| `session` | — | — | `SessionInfo` |
| **Mutations** | | | |
| `login` | `input`, `pageType` | `LoginInput!`, `String` | `AuthPayload` |
| `register` | `input`, `pageType` | `RegisterInput!`, `String` | `AuthPayload` |
| `logout` | — | — | `Boolean` |
| `refreshToken` | `input`, `pageType` | `RefreshTokenInput!`, `String` | `AuthPayload` |

**Input type fields (for variables):** `LoginInput`: `email: String!`, `password: String!`, `geolocation: GeolocationInput`; `RegisterInput`: `name: String!`, `email: String!`, `password: String!`, `geolocation: GeolocationInput`; `RefreshTokenInput`: `refreshToken: String!`. Use camelCase in the `variables` JSON (e.g. `refreshToken`).

## Canonical SDL (gateway schema)

Regenerate the full schema from `contact360.io/api` with:

`python -c "from app.graphql.schema import schema; print(schema.as_str())"`

**Auth namespace and inputs (excerpt):**

```graphql
type AuthQuery {
  me: User
  session: SessionInfo!
}

type AuthMutation {
  login(input: LoginInput!, pageType: String = null): AuthPayload!
  register(input: RegisterInput!, pageType: String = null): AuthPayload!
  logout: Boolean!
  refreshToken(input: RefreshTokenInput!, pageType: String = null): AuthPayload!
}

type AuthPayload {
  accessToken: String!
  refreshToken: String!
  user: UserInfo!
  pages: [PageSummary!]
}

type UserInfo {
  uuid: ID!
  email: String!
  name: String
  role: String
  userType: String
}

type SessionInfo {
  userUuid: ID!
  email: String!
  isAuthenticated: Boolean!
  lastSignInAt: DateTime
}

input LoginInput {
  email: String!
  password: String!
  geolocation: GeolocationInput = null
}

input RegisterInput {
  name: String!
  email: String!
  password: String!
  geolocation: GeolocationInput = null
}

input RefreshTokenInput {
  refreshToken: String!
}

input GeolocationInput {
  ip: String = null
  continent: String = null
  continentCode: String = null
  country: String = null
  countryCode: String = null
  region: String = null
  regionName: String = null
  city: String = null
  district: String = null
  zip: String = null
  lat: Float = null
  lon: Float = null
  timezone: String = null
  offset: Int = null
  currency: String = null
  isp: String = null
  org: String = null
  asname: String = null
  reverse: String = null
  device: String = null
  proxy: Boolean = null
  hosting: Boolean = null
}
```

`User` on `me` is the shared Users module type; see [02_USERS_MODULE.md](02_USERS_MODULE.md) for fields.

## POST `/graphql` — full request and response

Headers: `Content-Type: application/json`. Optional: `Authorization: Bearer <access_token>` for `me`, `session`, `logout`.

### Login (mutation)

**Request body:**

```json
{
  "query": "mutation Login($input: LoginInput!, $pageType: String) { auth { login(input: $input, pageType: $pageType) { accessToken refreshToken user { uuid email name role userType } pages { pageId title pageType route status } } } }",
  "variables": {
    "input": {
      "email": "user@example.com",
      "password": "string",
      "geolocation": null
    },
    "pageType": null
  }
}
```

**Success response:**

```json
{
  "data": {
    "auth": {
      "login": {
        "accessToken": "<jwt>",
        "refreshToken": "<jwt>",
        "user": {
          "uuid": "550e8400-e29b-41d4-a716-446655440000",
          "email": "user@example.com",
          "name": "Jane",
          "role": "Member",
          "userType": "guest"
        },
        "pages": []
      }
    }
  }
}
```

### Refresh token (mutation)

**Variables:**

```json
{
  "input": { "refreshToken": "<jwt>" },
  "pageType": null
}
```

### Session (query, requires auth)

**Request body:**

```json
{
  "query": "query { auth { session { userUuid email isAuthenticated lastSignInAt } } }"
}
```

## Types

### UserInfo

Basic user information returned in authentication responses (login, register, refreshToken).

```graphql
type UserInfo {
  uuid: ID!
  email: String!
  name: String
  role: String
  userType: String
}
```

**Fields:**

- `uuid` (ID!): Unique user identifier
- `email` (String!): User email address
- `name` (String): User's display name (optional)
- `role` (String): User role (e.g. SuperAdmin, Admin, ProUser, FreeUser, Member); optional
- `userType` (String): DocsAI user type derived from role (`super_admin`, `admin`, `pro_user`, `free_user`, `guest`); optional

### AuthPayload

Authentication response containing tokens, user information (including role and userType), and accessible pages.

```graphql
type AuthPayload {
  accessToken: String!
  refreshToken: String!
  user: UserInfo!
  pages: [PageSummary]
}
```

**Fields:**

- `accessToken` (String!): JWT access token for API authentication (expires in 30 minutes by default)
- `refreshToken` (String!): JWT refresh token for obtaining new access tokens (expires in 7 days by default)
- `user` (UserInfo!): Authenticated user information (includes `role` and `userType`; see UserInfo)
- `pages` ([PageSummary]): List of pages accessible to the user (fetched from DocsAI by user type, optionally filtered by `pageType` when provided in the mutation); optional, may be null if pages fetch fails

**Token Expiration:**

- Access tokens expire after 30 minutes (configurable via `ACCESS_TOKEN_EXPIRE_MINUTES`)
- Refresh tokens expire after 7 days (configurable via `REFRESH_TOKEN_EXPIRE_DAYS`)
- Expired access tokens can be refreshed using the refresh token
- Blacklisted tokens (from logout) cannot be used even if not expired

**Role-Based Page Access:**

Pages are fetched from DocsAI using the mapped **user type** (see below). When an optional `page_type` is passed to login/register/refreshToken, only pages of that type are returned.

| Role       | DocsAI user_type | Pages returned (when no page_type filter) |
|-----------|-------------------|-------------------------------------------|
| SuperAdmin | `super_admin`    | All pages (including drafts)              |
| Admin      | `admin`          | All pages (including drafts)              |
| ProUser    | `pro_user`       | Docs + Marketing (published)             |
| FreeUser   | `free_user`      | Published docs                            |
| Member     | `guest`          | Published docs                            |

See [Pages Module](19_PAGES_MODULE.md) for `pagesByDocsaiUserType`, `myPages`, and page types.

### SessionInfo

Current session information for authenticated users.

```graphql
type SessionInfo {
  userUuid: ID!
  email: String!
  isAuthenticated: Boolean!
  lastSignInAt: DateTime
}
```

**Fields:**

- `userUuid` (ID!): User's unique identifier
- `email` (String!): User's email address
- `isAuthenticated` (Boolean!): Always true when returned
- `lastSignInAt` (DateTime): Timestamp of last sign-in (optional)

## Queries

### me

Get current authenticated user information.

**Parameters:** None. The resolver uses the request context (Bearer token) to identify the user.

```graphql
query {
  auth {
    me {
      uuid
      email
      name
      profile {
        jobTitle
        bio
        role
        credits
      }
    }
  }
}
```

**Returns:** `User` or `null` if not authenticated

**Authentication:** Optional (returns null if not authenticated)

**Example Response:**

```json
{
  "data": {
    "auth": {
      "me": {
        "uuid": "123e4567-e89b-12d3-a456-426614174000",
        "email": "user@example.com",
        "name": "John Doe",
        "profile": {
          "jobTitle": "Software Engineer",
          "bio": "Developer",
          "role": "User",
          "credits": 1000
        }
      }
    }
  }
}
```

### session

Get current session information.

**Parameters:** None. The resolver uses the request context (Bearer token) to identify the session.

```graphql
query {
  auth {
    session {
      userUuid
      email
      isAuthenticated
      lastSignInAt
    }
  }
}
```

**Returns:** `SessionInfo`

**Authentication:** Required (raises `UnauthorizedError` if not authenticated)

**Example Response:**

```json
{
  "data": {
    "auth": {
      "session": {
        "userUuid": "123e4567-e89b-12d3-a456-426614174000",
        "email": "user@example.com",
        "isAuthenticated": true,
        "lastSignInAt": "2024-01-15T10:30:00Z"
      }
    }
  }
}
```

## Mutations

### login

Authenticate user with email and password. Optionally request pages filtered by `page_type`; response includes `role`, `userType` (DocsAI user type), and `pages`.

```graphql
mutation Login($input: LoginInput!, $pageType: String) {
  auth {
    login(input: $input, pageType: $pageType) {
      accessToken
      refreshToken
      user { uuid email name role userType }
      pages { pageId title pageType route status }
    }
  }
}
```

**Parameters:**

| Name     | Type          | Required | Description |
|----------|---------------|----------|-------------|
| `input`  | LoginInput!   | Yes      | Email, password, and optional geolocation (IP/location data for audit). |
| `pageType` | String      | No       | When provided, `pages` in the response are filtered by this type: `docs`, `marketing`, or `dashboard`. Fetched from DocsAI by user type. |

**Variables:**

```json
{
  "input": {
    "email": "user@example.com",
    "password": "password123",
    "geolocation": { "ip": "192.168.1.1", "country": "United States", "city": "New York" }
  },
  "pageType": "docs"
}
```

**Input:** `LoginInput!`; optional `pageType`

**Returns:** `AuthPayload` (includes `userType` and `pages` filtered by `pageType` when provided)

**Authentication:** Not required

**Example Response:**

```json
{
  "data": {
    "auth": {
      "login": {
        "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "user": {
          "uuid": "123e4567-e89b-12d3-a456-426614174000",
          "email": "user@example.com",
          "name": "John Doe",
          "role": "ProUser",
          "userType": "pro_user"
        },
        "pages": [
          {
            "pageId": "getting-started",
            "title": "Getting Started",
            "pageType": "docs",
            "route": "/docs/getting-started",
            "status": "published"
          },
          {
            "pageId": "api-reference",
            "title": "API Reference",
            "pageType": "docs",
            "route": "/docs/api",
            "status": "published"
          }
        ]
      }
    }
  }
}
```

### register

Register a new user account. Optionally request pages filtered by `page_type`; response includes `role`, `userType`, and `pages`.

```graphql
mutation Register($input: RegisterInput!, $pageType: String) {
  auth {
    register(input: $input, pageType: $pageType) {
      accessToken
      refreshToken
      user { uuid email name role userType }
      pages { pageId title pageType route status }
    }
  }
}
```

**Parameters:**

| Name     | Type            | Required | Description |
|----------|-----------------|----------|-------------|
| `input`  | RegisterInput!  | Yes      | Name, email, password, and optional geolocation (IP/location data for audit). |
| `pageType` | String        | No       | When provided, `pages` in the response are filtered by this type: `docs`, `marketing`, or `dashboard`. |

**Variables:**

```json
{
  "input": {
    "name": "John Doe",
    "email": "user@example.com",
    "password": "securePassword123",
    "geolocation": { "ip": "192.168.1.1", "country": "United States" }
  },
  "pageType": "marketing"
}
```

**Input:** `RegisterInput!`; optional `pageType`

**Returns:** `AuthPayload`

**Authentication:** Not required

**Example Response:**

```json
{
  "data": {
    "auth": {
      "register": {
        "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "user": {
          "uuid": "123e4567-e89b-12d3-a456-426614174000",
          "email": "user@example.com",
          "name": "John Doe",
          "role": "Member",
          "userType": "guest"
        },
        "pages": [
          {
            "pageId": "getting-started",
            "title": "Getting Started",
            "pageType": "docs",
            "route": "/docs/getting-started",
            "status": "published"
          }
        ]
      }
    }
  }
}
```

### logout

Logout current user and blacklist the current access token.

**Parameters:** None. The resolver uses the `Authorization: Bearer <token>` header to identify the token to blacklist.

```graphql
mutation Logout {
  auth {
    logout
  }
}
```

**Returns:** `Boolean` (true on success)

**Authentication:** Required

**Example Response:**

```json
{
  "data": {
    "auth": {
      "logout": true
    }
  }
}
```

### refreshToken

Refresh access token using refresh token. Optionally request pages filtered by `pageType`; response includes `role`, `userType`, and `pages`.

```graphql
mutation RefreshToken($input: RefreshTokenInput!, $pageType: String) {
  auth {
    refreshToken(input: $input, pageType: $pageType) {
      accessToken
      refreshToken
      user { uuid email name role userType }
      pages { pageId title pageType route status }
    }
  }
}
```

**Parameters:**

| Name       | Type                | Required | Description |
|------------|---------------------|----------|-------------|
| `input`    | RefreshTokenInput!  | Yes      | The current refresh token string. |
| `pageType` | String              | No       | When provided, `pages` in the response are filtered by this type: `docs`, `marketing`, or `dashboard`. |

**Variables:**

```json
{
  "input": { "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." },
  "pageType": "docs"
}
```

**Input:** `RefreshTokenInput!`; optional `pageType`

**Returns:** `AuthPayload`

**Authentication:** Not required (uses refresh token)

**Example Response:**

```json
{
  "data": {
    "auth": {
      "refreshToken": {
        "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "user": {
          "uuid": "123e4567-e89b-12d3-a456-426614174000",
          "email": "user@example.com",
          "name": "John Doe",
          "role": "ProUser",
          "userType": "pro_user"
        },
        "pages": [
          {
            "pageId": "getting-started",
            "title": "Getting Started",
            "pageType": "docs",
            "route": "/docs/getting-started",
            "status": "published"
          }
        ]
      }
    }
  }
}
```

## Input Types

### LoginInput

Input for user login.

```graphql
input LoginInput {
  email: String!
  password: String!
  geolocation: GeolocationInput
}
```

**Fields:**

- `email` (String!): User email address (must be valid email format)
- `password` (String!): User password (minimum 8 characters)
- `geolocation` (GeolocationInput): Optional IP geolocation data

**Validation:**

- `email`: Must be a valid email address format
- `password`: Must be at least 8 characters long

### RegisterInput

Input for user registration.

```graphql
input RegisterInput {
  name: String!
  email: String!
  password: String!
  geolocation: GeolocationInput
}
```

**Fields:**

- `name` (String!): User's display name (1-255 characters)
- `email` (String!): User email address (must be valid email format, must be unique)
- `password` (String!): User password (minimum 8 characters)
- `geolocation` (GeolocationInput): Optional IP geolocation data

**Validation:**

- `name`: Must be between 1 and 255 characters
- `email`: Must be a valid email address format and must not already exist in the system
- `password`: Must be at least 8 characters long

### RefreshTokenInput

Input for token refresh.

```graphql
input RefreshTokenInput {
  refreshToken: String!
}
```

**Fields:**

- `refreshToken` (String!): Current refresh token

### GeolocationInput

IP geolocation data (optional).

```graphql
input GeolocationInput {
  ip: String
  continent: String
  continentCode: String
  country: String
  countryCode: String
  region: String
  regionName: String
  city: String
  district: String
  zip: String
  lat: Float
  lon: Float
  timezone: String
  offset: Int
  currency: String
  isp: String
  org: String
  asname: String
  reverse: String
  device: String
  proxy: Boolean
  hosting: Boolean
}
```

All fields are optional. Used for tracking user login locations.

## Error Handling

The Auth module implements comprehensive error handling with input validation, database error handling, and specific error types.

### Error Types

The Auth module may raise the following errors:

- **UnauthorizedError** (401): Authentication required or invalid credentials
  - Code: `UNAUTHORIZED`
  - Occurs when: User is not authenticated, token is invalid, or credentials are incorrect
- **BadRequestError** (400): Invalid input data or request format
  - Code: `BAD_REQUEST`
  - Occurs when: Request body is malformed or contains invalid data
- **ValidationError** (422): Input validation failed
  - Code: `VALIDATION_ERROR`
  - Occurs when: Required fields are missing, field formats are invalid, or validation rules are violated
  - Includes field-level errors in `extensions.fieldErrors`
- **ServiceUnavailableError** (503): Database or external service unavailable
  - Code: `SERVICE_UNAVAILABLE`
  - Occurs when: Database connection fails or external authentication service is down

### Error Response Format

All errors follow the GraphQL error format with extensions:

#### Example: Unauthorized Error

```json
{
  "errors": [
    {
      "message": "Invalid email or password",
      "extensions": {
        "code": "UNAUTHORIZED",
        "statusCode": 401
      }
    }
  ]
}
```

#### Example: Validation Error with Field Errors

```json
{
  "errors": [
    {
      "message": "Email is required",
      "extensions": {
        "code": "VALIDATION_ERROR",
        "statusCode": 422,
        "fieldErrors": {
          "email": ["Email is required", "Email must be a valid email address"],
          "password": ["Password must be at least 8 characters"]
        }
      }
    }
  ]
}
```

#### Example: Service Unavailable Error

```json
{
  "errors": [
    {
      "message": "Database service temporarily unavailable. Please try again later.",
      "extensions": {
        "code": "SERVICE_UNAVAILABLE",
        "statusCode": 503,
        "serviceName": "database"
      }
    }
  ]
}
```

### Error Handling Patterns

- **Input Validation**: All inputs are validated before processing (email format, password strength, required fields)
- **Database Errors**: Database operations are wrapped with transaction rollback on failure
- **Token Validation**: JWT tokens are validated with specific error messages for expired or invalid tokens
- **Error Logging**: All errors are logged with context for debugging while maintaining user-friendly messages

## Usage Examples

### Complete Authentication Flow

```graphql
# 1. Register new user
mutation Register {
  auth {
    register(input: {
      name: "John Doe"
      email: "john@example.com"
      password: "securePassword123"
    }) {
      accessToken
      refreshToken
      user {
        uuid
        email
      }
    }
  }
}

# 2. Login
mutation Login {
  auth {
    login(input: {
      email: "john@example.com"
      password: "securePassword123"
    }) {
      accessToken
      refreshToken
      user {
        uuid
        email
      }
    }
  }
}

# 3. Get current user
query GetMe {
  auth {
    me {
      uuid
      email
      name
      profile {
        role
        credits
      }
    }
  }
}

# 4. Refresh token
mutation Refresh {
  auth {
    refreshToken(input: {
      refreshToken: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }) {
      accessToken
      refreshToken
    }
  }
}

# 5. Logout
mutation Logout {
  auth {
    logout
  }
}
```

### Error Scenario Examples

#### Invalid Credentials

```graphql
mutation Login {
  auth {
    login(input: {
      email: "wrong@example.com"
      password: "wrongpassword"
    }) {
      accessToken
      refreshToken
      user { uuid email }
    }
  }
}
```

**Response:**

```json
{
  "errors": [{
    "message": "Invalid email or password",
    "extensions": {
      "code": "UNAUTHORIZED",
      "statusCode": 401
    }
  }]
}
```

#### Validation Error - Invalid Input

```graphql
mutation Register {
  auth {
    register(input: {
      name: "John Doe"
      email: "invalid-email"
      password: "123"
    }) {
      accessToken
      user { uuid }
    }
  }
}
```

**Response:**

```json
{
  "errors": [{
    "message": "Validation failed",
    "extensions": {
      "code": "VALIDATION_ERROR",
      "statusCode": 422,
      "fieldErrors": {
        "email": ["Email must be a valid email address format"],
        "password": ["Password must be at least 8 characters"]
      }
    }
  }]
}
```

#### Validation Error - Duplicate Email

```graphql
mutation Register {
  auth {
    register(input: {
      name: "John Doe"
      email: "existing@example.com"
      password: "securePassword123"
    }) {
      accessToken
      user { uuid }
    }
  }
}
```

**Response:**

```json
{
  "errors": [{
    "message": "Validation failed",
    "extensions": {
      "code": "VALIDATION_ERROR",
      "statusCode": 422,
      "fieldErrors": {
        "email": ["Email already exists"]
      }
    }
  }]
}
```

#### Service Unavailable

```graphql
mutation Register {
  auth {
    register(input: {
      name: "John Doe"
      email: "john@example.com"
      password: "securePassword123"
    }) {
      accessToken
      user { uuid }
    }
  }
}
```

**Response (when database is unavailable):**

```json
{
  "errors": [{
    "message": "Database service temporarily unavailable. Please try again later.",
    "extensions": {
      "code": "SERVICE_UNAVAILABLE",
      "statusCode": 503,
      "serviceName": "database"
    }
  }]
}
```

## Implementation Details

### Authentication & Security

- **Token Storage**: Access tokens are stored in the `Authorization` header as `Bearer <token>`
- **Token Blacklisting**: Logout blacklists the access token in the database (prevents reuse even if not expired)
- **Token Expiration**:
  - Access tokens expire after 30 minutes (default, configurable)
  - Refresh tokens expire after 7 days (default, configurable)
  - Expired tokens cannot be used and must be refreshed
- **Password Security**: Passwords are hashed using bcrypt before storage (never stored in plain text)
- **JWT Validation**: Tokens are validated with specific error handling for expired or invalid tokens
- **Token Refresh**: Refresh token generates new access and refresh tokens (token rotation)

### Data Tracking

- **User History**: Login and registration events are tracked in user history
  - **Non-Blocking**: User history creation is non-blocking - if history creation fails during registration/login, the operation still succeeds (history is logged but doesn't block the request)
  - History is only created if geolocation data is provided
  - History creation errors are logged but do not affect the authentication flow
- **Geolocation**: Optional geolocation data is stored with login/registration events
  - All geolocation fields are optional
  - Used for tracking user login locations and security monitoring

### Error Handling Implementation

- **Input Validation**: All inputs (email, password, name) are validated using centralized validation utilities before processing
  - **Email Format Validation**: Email must be a valid email address format (validated via `validate_email_format`)
  - **Password Validation**: Password must be at least 8 characters long (validated via `validate_password`)
  - **Name Validation**: Name must be between 1 and 255 characters (validated via `validate_name`)
  - **Duplicate Email Check**: Registration checks if email already exists before creating user (raises ValidationError with field-level error)
  - **Required Field Validation**: All required fields are validated before processing
- **Database Error Handling**: All database operations use centralized error handlers
  - Transaction rollback on failure (automatic via FastAPI dependency)
  - Integrity errors (duplicate email) are caught and converted to user-friendly ValidationError with field-level errors
  - Database connection errors are converted to ServiceUnavailableError
  - User and profile creation are atomic - if profile creation fails, user creation is rolled back
- **Error Logging**: All errors are logged with context (user UUID, operation type, error details) for debugging while maintaining user-friendly error messages
- **Response Validation**: User data and token responses are validated before returning to clients

## Task breakdown (for maintainers)

1. **Trace login flow:** From `AuthMutation.login` in `app/graphql/modules/auth/mutations.py` → `authenticate_user` in `app/services/users/auth.py` → UserRepository/TokenBlacklistRepository; note where JWT and pages are built.
2. **Trace context auth:** In `app/graphql/context.py`, see how `Authorization: Bearer <token>` is decoded and how `context.user` is set via `UserRepository.get_by_uuid`.
3. **Verify input validation:** In auth mutations, confirm `validate_email_format`, `validate_password`, `validate_name` (and duplicate-email check) are used before DB calls.
4. **Check token blacklist:** Logout stores the access token in `token_blacklist`; ensure refresh flow rejects blacklisted refresh tokens in `app/services/users/auth.py`.
5. **DocsAI pages:** Login/register/refreshToken optionally accept `pageType` and return `pages` from PagesService; verify role → DocsAI user_type mapping in `app/core/constants.py` (role_to_docsai_user_type).

## Related Modules

- **Users Module**: Provides user profile management
- **Admin Module**: Provides admin user management operations
- **Pages Module**: Pages are returned in AuthPayload based on user role
- **AI Chats Module** ([17_AI_CHATS_MODULE.md](17_AI_CHATS_MODULE.md)): user-facing AI features use the same JWT as other GraphQL modules; the Contact AI microservice is invoked server-side with `X-API-Key` / `X-User-ID`, not with the client’s JWT directly

## Documentation metadata

- Era: `1.x`
- Introduced in: `TBD` (fill with exact minor)
- Frontend bindings: list page files from `docs/frontend/pages/*.json`
- Data stores touched: PostgreSQL/Elasticsearch/MongoDB/S3 as applicable

## Endpoint/version binding checklist

- Add operation list with `introduced_in` / `deprecated_in` tags.
- Map each operation to frontend page bindings and hook/service usage.
- Record DB tables read/write for each operation.

