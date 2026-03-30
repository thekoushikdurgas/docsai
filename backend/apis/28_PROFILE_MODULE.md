# Profile Module

## Overview

The Profile module provides functionality for managing API keys, active sessions, and team members. It allows users to create and manage API keys for programmatic access, view and manage active sessions, and invite/manage team members for collaborative work.
**Location:** `app/graphql/modules/profile/`

## Queries and mutations – parameters and variable types

| Operation | Parameter(s) | Variable type (GraphQL) | Return type |
|-----------|---------------|-------------------------|-------------|
| **Queries** | | | |
| `listAPIKeys` | — | — | `APIKeyList` |
| `listSessions` | — | — | `SessionList` |
| `listTeamMembers` | — | — | team member list |
| **Mutations** | | | |
| `createAPIKey` | `input` | CreateAPIKeyInput! | `APIKey` (with `key` once) |
| `deleteAPIKey` | `id` | ID! | result |
| `revokeSession` | `id` | ID! | result |
| `revokeAllOtherSessions` | — | — | result |
| `inviteTeamMember` | `input` | InviteTeamMemberInput! | result |
| `updateTeamMemberRole` | `input` | UpdateTeamMemberRoleInput! | result |
| `removeTeamMember` | `input` | RemoveTeamMemberInput! | result |

Use camelCase in variables. Tables: api_keys, sessions, team_members. User isolation for all operations.

## Types

### APIKey

Represents an API key for programmatic access.

```graphql
type APIKey {
  id: ID!
  name: String!
  prefix: String!  # First 12 characters of key for display
  created_at: DateTime!
  last_used_at: DateTime
  key: String  # Only returned when creating a new key (shown once)
  read_access: Boolean!
  write_access: Boolean!
  expires_at: DateTime
}
```

**Fields:**
- `id` (ID!): Unique API key identifier
- `name` (String!): API key name (max 255 characters)
- `prefix` (String!): First 12 characters of the key for display purposes
- `created_at` (DateTime!): Creation timestamp
- `last_used_at` (DateTime): Timestamp of last usage
- `key` (String): Full API key (only returned when creating a new key - shown once, store securely)
- `read_access` (Boolean!): Whether key has read permissions
- `write_access` (Boolean!): Whether key has write permissions
- `expires_at` (DateTime): Optional expiration timestamp

### APIKeyList

List of API keys with total count.

```graphql
type APIKeyList {
  keys: [APIKey!]!
  total: Int!
}
```

**Fields:**
- `keys` ([APIKey!]!): List of API keys
- `total` (Int!): Total count of API keys

### Session

Represents an active user session.

```graphql
type Session {
  id: ID!
  user_agent: String
  ip_address: String
  created_at: DateTime!
  last_activity: DateTime!
  is_current: Boolean!  # Whether this is the current session
}
```

**Fields:**
- `id` (ID!): Unique session identifier
- `user_agent` (String): User agent string from browser/client
- `ip_address` (String): IP address of the session
- `created_at` (DateTime!): Session creation timestamp
- `last_activity` (DateTime!): Last activity timestamp
- `is_current` (Boolean!): Whether this is the current active session

### SessionList

List of sessions with total count.

```graphql
type SessionList {
  sessions: [Session!]!
  total: Int!
}
```

**Fields:**
- `sessions` ([Session!]!): List of sessions
- `total` (Int!): Total count of sessions

### TeamMember

Represents a team member.

```graphql
type TeamMember {
  id: ID!
  email: String!
  name: String  # From user profile if member_user_id exists
  role: String!  # "Owner", "Admin", "Member", etc. (max 50 characters)
  invited_at: DateTime!
  joined_at: DateTime
  status: String!  # "pending", "active", or "inactive"
}
```

**Fields:**
- `id` (ID!): Unique team member identifier
- `email` (String!): Team member email address
- `name` (String): Team member name (from user profile if user has joined)
- `role` (String!): Team member role (max 50 characters)
- `invited_at` (DateTime!): Invitation timestamp
- `joined_at` (DateTime): Timestamp when member joined (if status is "active")
- `status` (String!): Member status - "pending", "active", or "inactive"

### TeamList

List of team members with total count.

```graphql
type TeamList {
  members: [TeamMember!]!
  total: Int!
}
```

**Fields:**
- `members` ([TeamMember!]!): List of team members
- `total` (Int!): Total count of team members

## Queries

### listAPIKeys

List all API keys for the current user.

**Parameters:** None.

```graphql
query ListAPIKeys {
  profile {
    listAPIKeys {
      keys {
        id
        name
        prefix
        created_at
        last_used_at
        read_access
        write_access
        expires_at
      }
      total
    }
  }
}
```

**Returns:** `APIKeyList`

**Authentication:** Required

**Implementation Details:**
- Uses `APIKeyRepository.list_by_user` to retrieve user's API keys
- User isolation enforced - users can only view their own API keys
- Full keys are never returned (only prefix for display)
- Results are ordered by creation date (newest first)

**Example Response:**

```json
{
  "data": {
    "profile": {
      "listAPIKeys": {
        "keys": [
          {
            "id": "1",
            "name": "Production API Key",
            "prefix": "ck_ABC123DEF4",
            "created_at": "2024-01-15T10:30:00Z",
            "last_used_at": "2024-01-20T09:15:00Z",
            "read_access": true,
            "write_access": false,
            "expires_at": null
          }
        ],
        "total": 1
      }
    }
  }
}
```

### listSessions

List all active sessions for the current user.

**Parameters:** None.

```graphql
query ListSessions {
  profile {
    listSessions {
      sessions {
        id
        user_agent
        ip_address
        created_at
        last_activity
        is_current
      }
      total
    }
  }
}
```

**Returns:** `SessionList`

**Authentication:** Required

**Implementation Details:**
- Uses `SessionRepository.list_by_user` to retrieve user's active sessions
- User isolation enforced - users can only view their own sessions
- Only active sessions are returned (not revoked sessions)
- `is_current` is determined by matching session ID with current session
- Results are ordered by last activity (most recent first)

**Example Response:**

```json
{
  "data": {
    "profile": {
      "listSessions": {
        "sessions": [
          {
            "id": "1",
            "user_agent": "Mozilla/5.0...",
            "ip_address": "192.168.1.1",
            "created_at": "2024-01-15T10:30:00Z",
            "last_activity": "2024-01-20T09:15:00Z",
            "is_current": true
          }
        ],
        "total": 1
      }
    }
  }
}
```

### listTeamMembers

List all team members for the current user's team.

**Parameters:** None.

```graphql
query ListTeamMembers {
  profile {
    listTeamMembers {
      members {
        id
        email
        name
        role
        invited_at
        joined_at
        status
      }
      total
    }
  }
}
```

**Returns:** `TeamList`

**Authentication:** Required

**Authorization:** Only team owners can view their team members

**Implementation Details:**
- Uses `TeamMemberRepository.list_by_owner` to retrieve team members
- Only team owners can view their team members
- Eagerly loads `member_user` and `member_user.profile` relationships for performance
- Email and name are derived from `member_user` if user has joined, otherwise from `member_email`
- Results are ordered by invitation date (newest first)

**Example Response:**

```json
{
  "data": {
    "profile": {
      "listTeamMembers": {
        "members": [
          {
            "id": "1",
            "email": "member@example.com",
            "name": "John Doe",
            "role": "Member",
            "invited_at": "2024-01-15T10:30:00Z",
            "joined_at": "2024-01-16T14:20:00Z",
            "status": "active"
          }
        ],
        "total": 1
      }
    }
  }
}
```

## Mutations

### createAPIKey

Create a new API key for the current user.

**Parameters:**

| Name  | Type                 | Required | Description        |
|-------|----------------------|----------|--------------------|
| input | CreateAPIKeyInput!   | Yes      | name, read_access, write_access, expires_at |

```graphql
mutation CreateAPIKey($input: CreateAPIKeyInput!) {
  profile {
    createAPIKey(input: $input) {
      id
      name
      prefix
      key
      read_access
      write_access
      expires_at
      created_at
    }
  }
}
```

**Variables:**

```json
{
  "input": {
    "name": "Production API Key",
    "read_access": true,
    "write_access": false,
    "expires_at": "2025-01-15T10:30:00Z"
  }
}
```

**Arguments:**
- `input` (CreateAPIKeyInput!): API key data

**Returns:** `APIKey` (with `key` field populated - shown only once)

**Authentication:** Required

**Validation:**
- `name`: Required, must be a string with max length 255 characters
- `read_access`: Optional boolean (default: true)
- `write_access`: Optional boolean (default: false)
- `expires_at`: Optional ISO 8601 datetime string

**Implementation Details:**
- Generates secure random API key with prefix `ck_` (Contact360 key)
- Hashes the full key using SHA-256 before storage
- Stores only the key prefix (first 12 characters) for display
- Full key is returned only once - user must store it securely
- Database errors are handled centrally via `handle_database_exception`

**Security Notes:**
- API keys are hashed before storage (cannot be retrieved)
- Full key is shown only once during creation
- Key prefix is stored for display purposes only
- Expired keys should be rejected by authentication middleware

**Example Response:**

```json
{
  "data": {
    "profile": {
      "createAPIKey": {
        "id": "1",
        "name": "Production API Key",
        "prefix": "ck_ABC123DEF4",
        "key": "ck_ABC123DEF456GHI789JKL012MNO345PQR678STU901VWX234YZ",
        "read_access": true,
        "write_access": false,
        "expires_at": "2025-01-15T10:30:00Z",
        "created_at": "2024-01-15T10:30:00Z"
      }
    }
  }
}
```

### deleteAPIKey

Delete an API key.

**Parameters:**

| Name | Type | Required | Description  |
|------|------|----------|--------------|
| id   | ID!  | Yes      | API key ID   |

```graphql
mutation DeleteAPIKey($id: ID!) {
  profile {
    deleteAPIKey(id: $id)
  }
}
```

**Arguments:**
- `id` (ID!): API key ID (must be a positive integer)

**Returns:** `Boolean` (true if successful)

**Authentication:** Required

**Validation:**
- `id`: Required, must be a positive integer

**Implementation Details:**
- Uses `APIKeyRepository.get_by_id` to retrieve API key
- User isolation enforced - users can only delete their own API keys
- Raises NotFoundError if API key doesn't exist
- Raises ForbiddenError if API key doesn't belong to user
- Uses `APIKeyRepository.delete` to remove API key
- Database errors are handled centrally via `handle_database_exception`

**Example Response:**

```json
{
  "data": {
    "profile": {
      "deleteAPIKey": true
    }
  }
}
```

### revokeSession

Revoke (logout) a specific session.

**Parameters:**

| Name | Type | Required | Description  |
|------|------|----------|--------------|
| id   | ID!  | Yes      | Session ID   |

```graphql
mutation RevokeSession($id: ID!) {
  profile {
    revokeSession(id: $id)
  }
}
```

**Arguments:**
- `id` (ID!): Session ID (must be a positive integer)

**Returns:** `Boolean` (true if successful)

**Authentication:** Required

**Validation:**
- `id`: Required, must be a positive integer

**Implementation Details:**
- Uses `SessionRepository.get_by_id` to retrieve session
- User isolation enforced - users can only revoke their own sessions
- Raises NotFoundError if session doesn't exist
- Raises ForbiddenError if session doesn't belong to user
- Uses `SessionRepository.revoke` to mark session as revoked
- Database errors are handled centrally via `handle_database_exception`

**Example Response:**

```json
{
  "data": {
    "profile": {
      "revokeSession": true
    }
  }
}
```

### revokeAllOtherSessions

Revoke all sessions except the current one.

**Parameters:** None.

```graphql
mutation RevokeAllOtherSessions {
  profile {
    revokeAllOtherSessions
  }
}
```

**Returns:** `Boolean` (true if successful)

**Authentication:** Required

**Implementation Details:**
- Uses `SessionRepository.revoke_all_except` to revoke all sessions except current
- User isolation enforced - users can only revoke their own sessions
- Current session ID is determined from context
- Useful for security when user suspects account compromise
- Database errors are handled centrally via `handle_database_exception`

**Example Response:**

```json
{
  "data": {
    "profile": {
      "revokeAllOtherSessions": true
    }
  }
}
```

### inviteTeamMember

Invite a new team member.

**Parameters:**

| Name  | Type                     | Required | Description    |
|-------|--------------------------|----------|----------------|
| input | InviteTeamMemberInput!   | Yes      | email, role    |

```graphql
mutation InviteTeamMember($input: InviteTeamMemberInput!) {
  profile {
    inviteTeamMember(input: $input) {
      id
      email
      name
      role
      invited_at
      status
    }
  }
}
```

**Variables:**

```json
{
  "input": {
    "email": "member@example.com",
    "role": "Member"
  }
}
```

**Arguments:**
- `input` (InviteTeamMemberInput!): Team member invitation data

**Returns:** `TeamMember`

**Authentication:** Required

**Authorization:** Only team owners can invite members

**Validation:**
- `email`: Required, must be a valid email format
- `role`: Optional string (default: "Member"), max length 50 characters

**Implementation Details:**
- Validates email format using `validate_email_format`
- Checks if user exists by email using `UserRepository.get_by_email`
- Creates team member record with:
  - `member_user_id`: Set if user exists, otherwise null
  - `member_email`: Set if user doesn't exist, otherwise null
  - `status`: Set to "pending"
- Eagerly loads relationships for response
- **Note:** Email notifications for invitations are not yet implemented
- Database errors are handled centrally via `handle_database_exception`

**Example Response:**

```json
{
  "data": {
    "profile": {
      "inviteTeamMember": {
        "id": "1",
        "email": "member@example.com",
        "name": null,
        "role": "Member",
        "invited_at": "2024-01-15T10:30:00Z",
        "status": "pending"
      }
    }
  }
}
```

### updateTeamMemberRole

Update a team member's role.

**Parameters:**

| Name | Type   | Required | Description      |
|------|--------|----------|------------------|
| id   | ID!    | Yes      | Team member ID   |
| role | String!| Yes      | New role         |

```graphql
mutation UpdateTeamMemberRole($id: ID!, $role: String!) {
  profile {
    updateTeamMemberRole(id: $id, role: $role) {
      id
      email
      name
      role
      status
    }
  }
}
```

**Arguments:**
- `id` (ID!): Team member ID (must be a positive integer)
- `role` (String!): New role (max 50 characters)

**Returns:** `TeamMember`

**Authentication:** Required

**Authorization:** Only team owners can update member roles

**Validation:**
- `id`: Required, must be a positive integer
- `role`: Required, must be a string with max length 50 characters

**Implementation Details:**
- Uses `TeamMemberRepository.get_by_id` to retrieve team member
- Only team owners can update member roles
- Raises NotFoundError if team member doesn't exist
- Raises ForbiddenError if team member doesn't belong to user's team
- Uses `TeamMemberRepository.update_role` to update role
- Eagerly loads relationships for response
- Database errors are handled centrally via `handle_database_exception`

**Example Response:**

```json
{
  "data": {
    "profile": {
      "updateTeamMemberRole": {
        "id": "1",
        "email": "member@example.com",
        "name": "John Doe",
        "role": "Admin",
        "status": "active"
      }
    }
  }
}
```

### removeTeamMember

Remove a team member from the team.

**Parameters:**

| Name | Type | Required | Description    |
|------|------|----------|----------------|
| id   | ID!  | Yes      | Team member ID |

```graphql
mutation RemoveTeamMember($id: ID!) {
  profile {
    removeTeamMember(id: $id)
  }
}
```

**Arguments:**
- `id` (ID!): Team member ID (must be a positive integer)

**Returns:** `Boolean` (true if successful)

**Authentication:** Required

**Authorization:** Only team owners can remove members

**Validation:**
- `id`: Required, must be a positive integer

**Implementation Details:**
- Uses `TeamMemberRepository.get_by_id` to retrieve team member
- Only team owners can remove members
- Raises NotFoundError if team member doesn't exist
- Raises ForbiddenError if team member doesn't belong to user's team
- Uses `TeamMemberRepository.delete` to remove team member
- Database errors are handled centrally via `handle_database_exception`

**Example Response:**

```json
{
  "data": {
    "profile": {
      "removeTeamMember": true
    }
  }
}
```

## Input Types

### CreateAPIKeyInput

Input for creating an API key.

```graphql
input CreateAPIKeyInput {
  name: String!
  read_access: Boolean = true
  write_access: Boolean = false
  expires_at: String  # ISO 8601 datetime string
}
```

**Fields:**
- `name` (String!): API key name (required, max 255 characters)
- `read_access` (Boolean): Whether key has read permissions (default: true)
- `write_access` (Boolean): Whether key has write permissions (default: false)
- `expires_at` (String): Optional expiration date as ISO 8601 datetime string

### InviteTeamMemberInput

Input for inviting a team member.

```graphql
input InviteTeamMemberInput {
  email: String!
  role: String = "Member"
}
```

**Fields:**
- `email` (String!): Team member email address (required, must be valid email format)
- `role` (String): Team member role (default: "Member", max 50 characters)

## Error Handling

### Error Types

- **UnauthorizedError** (401): Authentication required
- **ForbiddenError** (403): User doesn't own the resource or insufficient permissions
- **NotFoundError** (404): Resource not found
- **BadRequestError** (400): Invalid input data (e.g., invalid email, string length exceeded)
- **ValidationError** (422): Input validation failed
- **InternalServerError** (500): Internal server error

### Error Response Examples

**Not Found:**

```json
{
  "errors": [{
    "message": "Resource with identifier '999' not found",
    "extensions": {
      "code": "NOT_FOUND",
      "statusCode": 404,
      "resourceType": "APIKey",
      "identifier": "999"
    }
  }]
}
```

**Forbidden:**

```json
{
  "errors": [{
    "message": "You can only delete your own API keys",
    "extensions": {
      "code": "FORBIDDEN",
      "statusCode": 403
    }
  }]
}
```

**Validation Error:**

```json
{
  "errors": [{
    "message": "Invalid email format: Email must contain @ symbol",
    "extensions": {
      "code": "BAD_REQUEST",
      "statusCode": 400
    }
  }]
}
```

**Invalid Expiration Date:**

```json
{
  "errors": [{
    "message": "Invalid expires_at format: Invalid isoformat string",
    "extensions": {
      "code": "BAD_REQUEST",
      "statusCode": 400
    }
  }]
}
```

## Usage Examples

### Complete Flow: API Key Management

```graphql
# 1. Create an API key
mutation CreateKey {
  profile {
    createAPIKey(input: {
      name: "Production API Key"
      read_access: true
      write_access: false
      expires_at: "2025-01-15T10:30:00Z"
    }) {
      id
      name
      key
      prefix
      created_at
    }
  }
}

# 2. List all API keys
query ListKeys {
  profile {
    listAPIKeys {
      keys {
        id
        name
        prefix
        last_used_at
        expires_at
      }
      total
    }
  }
}

# 3. Delete an API key
mutation DeleteKey {
  profile {
    deleteAPIKey(id: "1")
  }
}
```

### Session Management

```graphql
# 1. List all active sessions
query ListSessions {
  profile {
    listSessions {
      sessions {
        id
        user_agent
        ip_address
        created_at
        last_activity
        is_current
      }
      total
    }
  }
}

# 2. Revoke a specific session
mutation RevokeSession {
  profile {
    revokeSession(id: "2")
  }
}

# 3. Revoke all other sessions (keep current)
mutation RevokeAllOthers {
  profile {
    revokeAllOtherSessions
  }
}
```

### Team Management

```graphql
# 1. Invite a team member
mutation InviteMember {
  profile {
    inviteTeamMember(input: {
      email: "member@example.com"
      role: "Member"
    }) {
      id
      email
      role
      status
      invited_at
    }
  }
}

# 2. List all team members
query ListMembers {
  profile {
    listTeamMembers {
      members {
        id
        email
        name
        role
        status
        invited_at
        joined_at
      }
      total
    }
  }
}

# 3. Update team member role
mutation UpdateRole {
  profile {
    updateTeamMemberRole(id: "1", role: "Admin") {
      id
      email
      role
    }
  }
}

# 4. Remove team member
mutation RemoveMember {
  profile {
    removeTeamMember(id: "1")
  }
}
```

## Implementation Details

### Repository Integration

- **APIKeyRepository**: Provides data access layer for API keys
  - `create`: Create new API key
  - `get_by_id`: Get API key by ID
  - `list_by_user`: List API keys for user
  - `update_last_used`: Update last used timestamp
  - `delete`: Delete API key

- **SessionRepository**: Provides data access layer for sessions
  - `get_by_id`: Get session by ID
  - `list_by_user`: List sessions for user
  - `revoke`: Revoke a session
  - `revoke_all_except`: Revoke all sessions except specified one
  - `update_last_activity`: Update last activity timestamp

- **TeamMemberRepository**: Provides data access layer for team members
  - `create`: Create new team member invitation
  - `get_by_id`: Get team member by ID
  - `list_by_owner`: List team members for team owner
  - `update_role`: Update team member role
  - `update_status`: Update team member status
  - `delete`: Remove team member

### Database Schema

- **Table**: `api_keys`
  - **Key Fields**: `id`, `user_id`, `name`, `key_hash`, `key_prefix`, `read_access`, `write_access`, `expires_at`, `created_at`, `last_used_at`
  - **Indexes**: `user_id`
  - **Foreign Keys**: `user_id` references `users.uuid`

- **Table**: `sessions`
  - **Key Fields**: `id`, `user_id`, `user_agent`, `ip_address`, `created_at`, `last_activity`, `revoked_at`
  - **Indexes**: `user_id`
  - **Foreign Keys**: `user_id` references `users.uuid`

- **Table**: `team_members`
  - **Key Fields**: `id`, `team_owner_id`, `member_user_id`, `member_email`, `role`, `status`, `invited_at`, `joined_at`
  - **Indexes**: `team_owner_id`, `member_user_id`
  - **Foreign Keys**: `team_owner_id` references `users.uuid`, `member_user_id` references `users.uuid`

### User Isolation

All operations enforce user isolation:
- API keys: Users can only view/manage their own API keys
- Sessions: Users can only view/manage their own sessions
- Team members: Only team owners can view/manage their team members

### Eager Loading

Team member queries use eager loading for performance:
- `member_user` relationship is eagerly loaded
- `member_user.profile` relationship is eagerly loaded
- Prevents N+1 query issues when accessing email and name

### Timezone Handling

All timestamps use UTC timezone:
- `created_at`, `updated_at`, `last_used_at`, `last_activity`, `invited_at`, `joined_at` are stored as timezone-aware datetimes
- Repository uses `datetime.now(UTC)` for timestamp updates

### Validation

- String length validation: `name` (max 255), `role` (max 50)
- Email validation: Uses `validate_email_format` utility
- ID validation: Must be positive integer
- Date validation: ISO 8601 format for `expires_at`

### Security Considerations

1. **API Key Security**:
   - Keys are hashed using SHA-256 before storage
   - Full key is shown only once during creation
   - Key prefix is stored for display purposes only
   - Expired keys should be rejected by authentication middleware

2. **Session Security**:
   - Sessions can be revoked individually or in bulk
   - Current session can be preserved when revoking others
   - Session activity is tracked for security monitoring

3. **Team Management**:
   - Only team owners can invite/manage members
   - Email validation ensures valid invitations
   - Role-based access control for team operations

### Future Enhancements

- 📌 Planned: Email notifications for team invitations
- 📌 Planned: API key usage analytics
- 📌 Planned: Session activity monitoring and alerts
- 📌 Planned: Team member invitation acceptance flow
- 📌 Planned: Role-based permissions for team members
- 📌 Planned: API key rate limiting
- 📌 Planned: Session IP geolocation

## Task breakdown (for maintainers)

1. **listAPIKeys/createAPIKey/deleteAPIKey:** API key repository; key hashed (store key_hash, key_prefix); create returns full key once; user_id from context; validate name, read_access, write_access, expires_at.
2. **listSessions/revokeSession/revokeAllOtherSessions:** Sessions repository; list shows current session (is_current via token match); revoke by id (ownership); revokeAllOtherSessions revokes all except current.
3. **inviteTeamMember/updateTeamMemberRole/removeTeamMember:** team_members table; owner = context.user; invite by email or user; validate role and status; document role enum and status (pending, active, etc.).
4. **API key auth:** If API keys are used for GraphQL auth, document how context resolves key (e.g. separate header or Bearer with key prefix) and rate limits.
5. **Cascade:** User deletion cascades to api_keys, sessions, team_members (as owner and member); document in schema.

## Related Modules

- **Auth Module**: User authentication and session management
- **Users Module**: User profile and account management
- **Two Factor Module**: Two-factor authentication for enhanced security
- **AI Chats Module** ([17_AI_CHATS_MODULE.md](17_AI_CHATS_MODULE.md)): distinct from user API keys — Contact AI uses service-to-service `LAMBDA_AI_API_KEY` on the GraphQL server

## Documentation metadata

- Era: `9.x`
- Introduced in: `TBD` (fill with exact minor)
- Frontend bindings: list page files from `docs/frontend/pages/*.json`
- Data stores touched: PostgreSQL/Elasticsearch/MongoDB/S3 as applicable

## Endpoint/version binding checklist

- Add operation list with `introduced_in` / `deprecated_in` tags.
- Map each operation to frontend page bindings and hook/service usage.
- Record DB tables read/write for each operation.

