# Users Module

## Overview

The Users module provides user management functionality including user queries, profile updates, avatar uploads, and user statistics. It supports both regular user operations and admin operations.

**Location:** `app/graphql/modules/users/`

GraphQL paths: `query { users { user(uuid: ...) { ... } } }`, `mutation { users { updateProfile(...) { ... } } }`.

## Queries and mutations – parameters and variable types

| Operation | Parameter(s) | Variable type (GraphQL) | Return type |
|-----------|---------------|-------------------------|-------------|
| **Queries** (under `users { ... }`) | | | |
| `user` | `uuid` | `ID!` | `User` |
| `users` | `limit`, `offset` | `Int`, `Int` | `[User!]!` |
| `userStats` | — | — | `UserStats` (Admin/SuperAdmin) |
| **Mutations** (under `users { ... }`) | | | |
| `updateProfile` | `input` | `UpdateProfileInput!` | `UserProfile` |
| `uploadAvatar` | `input` | `UploadAvatarInput!` | `UserProfile` |
| `updateUser` | `input` | `UpdateUserInput!` | `User` |
| `promoteToAdmin` | `input` | `PromoteToAdminInput!` | `User` (SuperAdmin) |
| `promoteToSuperAdmin` | `input` | `PromoteToSuperAdminInput!` | `User` (SuperAdmin) |

Use camelCase in the `variables` JSON (e.g. `uuid` for `user(uuid:)`, `jobTitle` in profile inputs). See Input Types section for field-level types.

## Canonical SDL (gateway schema)

Regenerate the full schema from `contact360.io/api` with:

`python -c "from app.graphql.schema import schema; print(schema.as_str())"`

```graphql
type UserQuery {
  user(uuid: ID!): User!
  users(limit: Int = 100, offset: Int = 0): [User!]!
  userStats: UserStats!
}

type UserMutation {
  updateProfile(input: UpdateProfileInput!): UserProfile!
  uploadAvatar(input: UploadAvatarInput!): UserProfile!
  updateUser(input: UpdateUserInput!): User!
  promoteToAdmin(input: PromoteToAdminInput!): User!
  promoteToSuperAdmin(input: PromoteToSuperAdminInput!): User!
}

input UpdateProfileInput {
  jobTitle: String = null
  bio: String = null
  timezone: String = null
  notifications: JSON = null
}

input UploadAvatarInput {
  fileData: String = null
  filePath: String = null
}

input UpdateUserInput {
  name: String = null
  email: String = null
}
```

`PromoteToAdminInput` / `PromoteToSuperAdminInput` are defined in the Admin inputs section of the schema (`userId: ID!`).

## POST `/graphql` — full request and response

Headers: `Content-Type: application/json`, `Authorization: Bearer <access_token>` (required for all operations below except where noted).

### `users.user` (query)

**Request body:**

```json
{
  "query": "query User($uuid: ID!) { users { user(uuid: $uuid) { uuid email name isActive profile { userId jobTitle credits role } } } }",
  "variables": { "uuid": "550e8400-e29b-41d4-a716-446655440000" }
}
```

**Success response (shape):**

```json
{
  "data": {
    "users": {
      "user": {
        "uuid": "550e8400-e29b-41d4-a716-446655440000",
        "email": "user@example.com",
        "name": "Jane",
        "isActive": true,
        "profile": null
      }
    }
  }
}
```

### `users.updateProfile` (mutation)

**Variables:**

```json
{
  "input": {
    "jobTitle": "Engineer",
    "bio": null,
    "timezone": "UTC",
    "notifications": null
  }
}
```

**Minimal query string:**

```graphql
mutation ($input: UpdateProfileInput!) {
  users {
    updateProfile(input: $input) {
      userId
      jobTitle
      bio
      avatarUrl
    }
  }
}
```

## Types

### User

User information with profile data.

```graphql
type User {
  uuid: ID!
  email: String!
  name: String
  isActive: Boolean!
  lastSignInAt: DateTime
  createdAt: DateTime!
  updatedAt: DateTime
  profile: UserProfile
}
```

**Fields:**

- `uuid` (ID!): Unique user identifier
- `email` (String!): User email address
- `name` (String): User's display name
- `isActive` (Boolean!): Whether the user account is active
- `lastSignInAt` (DateTime): Timestamp of last sign-in
- `createdAt` (DateTime!): Account creation timestamp
- `updatedAt` (DateTime): Last update timestamp
- `profile` (UserProfile): User profile information

### UserProfile

Detailed user profile information.

```graphql
type UserProfile {
  userId: ID!
  jobTitle: String
  bio: String
  timezone: String
  avatarUrl: String
  role: String
  credits: Int!
  subscriptionPlan: String
  subscriptionPeriod: String
  subscriptionStatus: String
  subscriptionStartedAt: DateTime
  subscriptionEndsAt: DateTime
  createdAt: DateTime!
  updatedAt: DateTime
}
```

**Fields:**

- `userId` (ID!): Associated user ID
- `jobTitle` (String): User's job title
- `bio` (String): User biography
- `timezone` (String): User's timezone
- `avatarUrl` (String): Full URL to user's avatar image (presigned or public, depending on S3 configuration)
- `role` (String): User role (User, Admin, SuperAdmin)
- `credits` (Int!): Available credits balance
- `subscriptionPlan` (String): Current subscription plan
- `subscriptionPeriod` (String): Subscription billing period
- `subscriptionStatus` (String): Subscription status
- `subscriptionStartedAt` (DateTime): Subscription start date
- `subscriptionEndsAt` (DateTime): Subscription end date
- `createdAt` (DateTime!): Profile creation timestamp
- `updatedAt` (DateTime): Last update timestamp

### UserStats

Aggregated user statistics (admin only).

```graphql
type UserStats {
  totalUsers: Int!
  activeUsers: Int!
  inactiveUsers: Int!
  usersByRole: [UserRoleCount!]!
  usersBySubscription: [UserSubscriptionCount!]!
}
```

**Fields:**

- `totalUsers` (Int!): Total number of users
- `activeUsers` (Int!): Number of active users
- `inactiveUsers` (Int!): Number of inactive users
- `usersByRole` ([UserRoleCount!]!): User counts grouped by role
- `usersBySubscription` ([UserSubscriptionCount!]!): User counts grouped by subscription plan

### UserRoleCount

User count by role.

```graphql
type UserRoleCount {
  role: String!
  count: Int!
}
```

### UserSubscriptionCount

User count by subscription plan.

```graphql
type UserSubscriptionCount {
  subscriptionPlan: String!
  count: Int!
}
```

## Queries

### user

Get user by UUID.

**Parameters:**

| Name  | Type | Required | Description |
|-------|------|----------|-------------|
| `uuid` | ID! | Yes | The unique identifier of the user to fetch. |

```graphql
query GetUser($uuid: ID!) {
  users {
    user(uuid: $uuid) {
      uuid
      email
      name
      isActive
      profile {
        jobTitle
        bio
        role
        credits
        subscriptionPlan
      }
    }
  }
}
```

**Arguments:**

- `uuid` (ID!): User UUID

**Returns:** `User`

**Authentication:** Required

**Authorization:**

- Regular users can only access their own user data
- Admin/SuperAdmin can access any user

**Example Response:**

```json
{
  "data": {
    "users": {
      "user": {
        "uuid": "123e4567-e89b-12d3-a456-426614174000",
        "email": "user@example.com",
        "name": "John Doe",
        "isActive": true,
        "profile": {
          "jobTitle": "Software Engineer",
          "bio": "Full-stack developer",
          "role": "User",
          "credits": 1000,
          "subscriptionPlan": "pro"
        }
      }
    }
  }
}
```

### users

List all users (admin only).

**Parameters:**

| Name    | Type | Required | Description |
|---------|------|----------|-------------|
| `limit`  | Int | No | Maximum number of users to return (default: 100). Validated via `validate_pagination` (1–1000). |
| `offset` | Int | No | Number of users to skip (default: 0). Must be non-negative. |

```graphql
query ListUsers($limit: Int, $offset: Int) {
  users {
    users(limit: $limit, offset: $offset) {
      uuid
      email
      name
      isActive
      createdAt
    }
  }
}
```

**Arguments:**

- `limit` (Int): Maximum number of users to return (default: 100, validated via `validate_pagination`)
- `offset` (Int): Number of users to skip (default: 0, validated via `validate_pagination`)

**Validation:**

- `limit`: Must be a positive integer (validated via `validate_pagination`)
- `offset`: Must be a non-negative integer (validated via `validate_pagination`)

**Returns:** `[User!]!`

**Authentication:** Required

**Authorization:** Admin/SuperAdmin only

**Example Response:**

```json
{
  "data": {
    "users": {
      "users": [
        {
          "uuid": "123e4567-e89b-12d3-a456-426614174000",
          "email": "user1@example.com",
          "name": "User One",
          "isActive": true,
          "createdAt": "2024-01-01T00:00:00Z"
        },
        {
          "uuid": "223e4567-e89b-12d3-a456-426614174001",
          "email": "user2@example.com",
          "name": "User Two",
          "isActive": true,
          "createdAt": "2024-01-02T00:00:00Z"
        }
      ]
    }
  }
}
```

### userStats

Get user statistics (admin only).

**Parameters:** None.

```graphql
query GetUserStats {
  users {
    userStats {
      totalUsers
      activeUsers
      inactiveUsers
      usersByRole {
        role
        count
      }
      usersBySubscription {
        subscriptionPlan
        count
      }
    }
  }
}
```

**Returns:** `UserStats`

**Authentication:** Required

**Authorization:** Admin/SuperAdmin only

**Example Response:**

```json
{
  "data": {
    "users": {
      "userStats": {
        "totalUsers": 150,
        "activeUsers": 142,
        "inactiveUsers": 8,
        "usersByRole": [
          {
            "role": "User",
            "count": 140
          },
          {
            "role": "Admin",
            "count": 8
          },
          {
            "role": "SuperAdmin",
            "count": 2
          }
        ],
        "usersBySubscription": [
          {
            "subscriptionPlan": "free",
            "count": 50
          },
          {
            "subscriptionPlan": "pro",
            "count": 80
          },
          {
            "subscriptionPlan": "enterprise",
            "count": 20
          }
        ]
      }
    }
  }
}
```

## Mutations

### updateProfile

Update current user's profile. All input fields are optional; only provided fields are updated.

**Parameters:**

| Name    | Type                 | Required | Description |
|---------|----------------------|----------|-------------|
| `input` | UpdateProfileInput!  | Yes      | Fields to update: jobTitle, bio, timezone, notifications (JSON). All optional. |

```graphql
mutation UpdateProfile($input: UpdateProfileInput!) {
  users {
    updateProfile(input: $input) {
      userId
      jobTitle
      bio
      timezone
      role
      credits
    }
  }
}
```

**Variables:**

```json
{
  "input": {
    "jobTitle": "Senior Software Engineer",
    "bio": "Experienced full-stack developer",
    "timezone": "America/New_York",
    "notifications": {
      "email": true,
      "push": false
    }
  }
}
```

**Input:** `UpdateProfileInput!`

**Returns:** `UserProfile`

**Authentication:** Required

**Example Response:**

```json
{
  "data": {
    "users": {
      "updateProfile": {
        "userId": "123e4567-e89b-12d3-a456-426614174000",
        "jobTitle": "Senior Software Engineer",
        "bio": "Experienced full-stack developer",
        "timezone": "America/New_York",
        "role": "User",
        "credits": 1000
      }
    }
  }
}
```

### uploadAvatar

Upload avatar image for current user. Provide exactly one of `fileData` or `filePath`. Accepted image types: JPEG, PNG, GIF, WebP (max 5MB). Filename is auto-generated as `{user_id}.jpg`.

**Parameters:**

| Name    | Type                  | Required | Description |
|---------|-----------------------|----------|-------------|
| `input` | UploadAvatarInput!    | Yes      | Either `fileData` (base64, HTTP/HTTPS URL, or file:// URL) or `filePath` (local path). |

```graphql
mutation UploadAvatar($input: UploadAvatarInput!) {
  users {
    uploadAvatar(input: $input) {
      userId
      avatarUrl
      jobTitle
      bio
      timezone
      role
      credits
      subscriptionPlan
      subscriptionStatus
      createdAt
      updatedAt
    }
  }
}
```

**Variables (Base64 method):**

```json
{
  "input": {
    "fileData": "/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCdABmX/9k="
  }
}
```

**Variables (HTTP/HTTPS URL method):**

```json
{
  "input": {
    "fileData": "https://upload.wikimedia.org/wikipedia/commons/9/99/Sample_User_Icon.png"
  }
}
```

**Variables (file:// URL method):**

```json
{
  "input": {
    "fileData": "file:///C:/Users/durga/Downloads/images.png"
  }
}
```

**Variables (Local file path method):**

```json
{
  "input": {
    "filePath": "/path/to/local/image.jpg"
  }
}
```

**Input:** `UploadAvatarInput!`

**Returns:** `UserProfile`

**Authentication:** Required

**File Requirements:**

- **Types:** JPEG, PNG, GIF, or WebP (detected automatically from file content)
- **Maximum size:** 5MB
- **Input Methods:**
  - `fileData`:
    - Base64-encoded file data (without data URI prefix like `data:image/jpeg;base64,`)
    - HTTP/HTTPS URL to an image (e.g., `https://example.com/image.png`)
    - file:// URL to a local file (e.g., `file:///C:/path/to/image.jpg` or `file:///path/to/image.jpg`)
  - `filePath`: Local file path on the server (e.g., `/path/to/image.jpg` or `C:\\path\\to\\image.jpg`)
- **Note:**
  - Either `fileData` OR `filePath` must be provided (not both)
  - Filename is auto-generated as `{user_id}.jpg` - no need to provide filename
  - File type is detected from file content (magic bytes), not from filename
  - URLs are downloaded automatically and validated for image content type

**Example Response:**

```json
{
  "data": {
    "users": {
      "uploadAvatar": {
        "userId": "123e4567-e89b-12d3-a456-426614174000",
        "avatarUrl": "https://s3.amazonaws.com/bucket/avatars/123e4567-e89b-12d3-a456-426614174000/123e4567-e89b-12d3-a456-426614174000.jpg?X-Amz-Algorithm=...",
        "jobTitle": null,
        "bio": null,
        "timezone": null,
        "role": "Member",
        "credits": 100,
        "subscriptionPlan": "free",
        "subscriptionStatus": "active",
        "createdAt": "2024-01-15T10:30:00Z",
        "updatedAt": "2024-01-15T10:35:00Z"
      }
    }
  }
}
```

**Notes:**

- The `avatarUrl` field returns a full URL that can be used directly in `<img>` tags or other frontend components
- If `S3_USE_PRESIGNED_URLS` is enabled (default), the URL will be a presigned URL with expiration (default: 1 hour)
- If `S3_USE_PRESIGNED_URLS` is disabled, the URL will be a public S3 URL (requires bucket to be public)
- The filename is auto-generated as `{user_id}.jpg`, so the S3 key format is: `avatars/{user_id}/{user_id}.jpg`
- File type is detected from file content (magic bytes), not from filename
- If URL generation fails, the system falls back to returning the S3 key
- If the user profile doesn't exist, it will be automatically created
- The `filePath` method requires the file to exist on the server's filesystem and be readable

### updateUser

Update current user's basic information (name and/or email). All input fields are optional.

**Parameters:**

| Name    | Type                | Required | Description |
|---------|---------------------|----------|-------------|
| `input` | UpdateUserInput!    | Yes      | Fields to update: name (String), email (String). Both optional. |

```graphql
mutation UpdateUser($input: UpdateUserInput!) {
  users {
    updateUser(input: $input) {
      uuid
      email
      name
    }
  }
}
```

**Variables:**

```json
{
  "input": {
    "name": "John Doe Updated"
  }
}
```

**Input:** `UpdateUserInput!`

**Returns:** `User`

**Authentication:** Required

**Example Response:**

```json
{
  "data": {
    "users": {
      "updateUser": {
        "uuid": "123e4567-e89b-12d3-a456-426614174000",
        "email": "user@example.com",
        "name": "John Doe Updated"
      }
    }
  }
}
```

### promoteToAdmin

Promote a user to Admin role. Requires the caller to have SuperAdmin role.

**Parameters:**

| Name    | Type                     | Required | Description |
|---------|--------------------------|----------|-------------|
| `input` | PromoteToAdminInput!     | Yes      | Contains `userId` (ID!): the UUID of the user to promote to Admin. |

```graphql
mutation PromoteToAdmin($input: PromoteToAdminInput!) {
  users {
    promoteToAdmin(input: $input) {
      uuid
      email
      name
      profile {
        role
      }
    }
  }
}
```

**Variables:**

```json
{
  "input": {
    "userId": "123e4567-e89b-12d3-a456-426614174000"
  }
}
```

**Input:** `PromoteToAdminInput!`

**Returns:** `User`

**Authentication:** Required

**Authorization:** SuperAdmin role required

**Example Response:**

```json
{
  "data": {
    "users": {
      "promoteToAdmin": {
        "uuid": "123e4567-e89b-12d3-a456-426614174000",
        "email": "user@example.com",
        "name": "John Doe",
        "profile": {
          "role": "Admin"
        }
      }
    }
  }
}
```

**Error Responses:**

- **ForbiddenError** (403): If user is not SuperAdmin
- **NotFoundError** (404): If target user does not exist

### promoteToSuperAdmin

Promote a user to SuperAdmin role. Requires the caller to have SuperAdmin role.

**Parameters:**

| Name    | Type                         | Required | Description |
|---------|------------------------------|----------|-------------|
| `input` | PromoteToSuperAdminInput!     | Yes      | Contains `userId` (ID!): the UUID of the user to promote to SuperAdmin. |

```graphql
mutation PromoteToSuperAdmin($input: PromoteToSuperAdminInput!) {
  users {
    promoteToSuperAdmin(input: $input) {
      uuid
      email
      name
      profile {
        role
      }
    }
  }
}
```

**Variables:**

```json
{
  "input": {
    "userId": "123e4567-e89b-12d3-a456-426614174000"
  }
}
```

**Input:** `PromoteToSuperAdminInput!`

**Returns:** `User`

**Authentication:** Required

**Authorization:** SuperAdmin role required

**Example Response:**

```json
{
  "data": {
    "users": {
      "promoteToSuperAdmin": {
        "uuid": "123e4567-e89b-12d3-a456-426614174000",
        "email": "user@example.com",
        "name": "John Doe",
        "profile": {
          "role": "SuperAdmin"
        }
      }
    }
  }
}
```

**Error Responses:**

- **ForbiddenError** (403): If user is not SuperAdmin
- **NotFoundError** (404): If target user does not exist

## Input Types

### UpdateUserInput

Input for updating user information.

```graphql
input UpdateUserInput {
  name: String
  email: String
}
```

**Fields:**

- `name` (String): New display name (optional, 1-255 characters)
- `email` (String): New email address (optional, must be valid email format)

**Validation:**

- `name`: Must be between 1 and 255 characters if provided
- `email`: Must be a valid email address format if provided (note: email updates may require additional verification)

### UpdateProfileInput

Input for updating user profile.

```graphql
input UpdateProfileInput {
  jobTitle: String
  bio: String
  timezone: String
  notifications: JSON
}
```

**Fields:**

- `jobTitle` (String): Job title (optional, max 255 characters)
- `bio` (String): Biography (optional, max 1000 characters)
- `timezone` (String): Timezone (optional, max 100 characters)
- `notifications` (JSON): Notification preferences (optional, must be valid JSON object)

**Validation:**

- `jobTitle`: Maximum length 255 characters
- `bio`: Maximum length 1000 characters
- `timezone`: Maximum length 100 characters
- `notifications`: Must be a valid JSON object (dict) if provided

### UploadAvatarInput

Input for uploading avatar.

```graphql
input UploadAvatarInput {
  fileData: String
  filePath: String
}
```

**Fields:**

- `fileData` (String, optional):
  - Base64-encoded file content (without data URI prefix like `data:image/jpeg;base64,`)
  - HTTP/HTTPS URL to an image (e.g., `https://example.com/image.png`)
  - file:// URL to a local file (e.g., `file:///C:/path/to/image.jpg`)
- `filePath` (String, optional): Local file path on the server (e.g., `/path/to/image.jpg` or `C:\\path\\to\\image.jpg`)

**Validation:**

- Exactly one of `fileData` or `filePath` must be provided (not both, not neither)
- File size must not exceed 5MB
- Supported image formats: JPEG, PNG, GIF, WebP (detected automatically from file content using magic bytes)
- Filename is auto-generated as `{user_id}.jpg` - no need to provide filename
- File type validation is performed on file content, not filename
- File paths are validated for security (prevents directory traversal attacks)
- URLs are validated to ensure they point to image content (Content-Type: image/*)

**Examples:**

Base64 method:

```json
{
  "fileData": "/9j/4AAQSkZJRgABAQEAYABgAAD..."
}
```

HTTP/HTTPS URL method:

```json
{
  "fileData": "https://upload.wikimedia.org/wikipedia/commons/9/99/Sample_User_Icon.png"
}
```

file:// URL method:

```json
{
  "fileData": "file:///C:/Users/durga/Downloads/images.png"
}
```

Local file path method:

```json
{
  "filePath": "/path/to/local/image.jpg"
}
```

**Notes:**

- The `filePath` method is useful for server-side uploads or automated processes
- The `fileData` URL method automatically downloads images from HTTP/HTTPS URLs
- file:// URLs allow accessing local files through the file:// protocol
- Base64 padding issues are automatically fixed
- The uploaded file will be stored in S3 with the key: `avatars/{user_id}/{user_id}.jpg`

**Example:**

```json
{
  "fileData": "/9j/4AAQSkZJRgABAQEAYABgAAD...",
  "filename": "my-avatar.jpg"
}
```

### PromoteToAdminInput

Input for promoting a user to admin role.

```graphql
input PromoteToAdminInput {
  userId: ID!
}
```

**Fields:**

- `userId` (ID!): UUID of the user to promote

### PromoteToSuperAdminInput

Input for promoting a user to super admin role.

```graphql
input PromoteToSuperAdminInput {
  userId: ID!
}
```

**Fields:**

- `userId` (ID!): UUID of the user to promote

## Error Handling

The Users module implements comprehensive error handling with input validation, database error handling, file validation, and role-based access control.

### Error Types

The Users module may raise the following errors:

- **ForbiddenError** (403): Insufficient permissions
  - Code: `FORBIDDEN`
  - Extensions: `requiredRole: <role>` (if applicable)
  - Occurs when: User lacks required permissions (e.g., accessing another user's data, promoting users without SuperAdmin role)
- **NotFoundError** (404): User not found
  - Code: `NOT_FOUND`
  - Extensions: `resourceType: "User"`, `identifier: <user_uuid>`
  - Occurs when: Requested user UUID does not exist
- **BadRequestError** (400): Invalid input data
  - Code: `BAD_REQUEST`
  - Occurs when: Invalid file type, file size exceeds limit (5MB), or invalid file format
- **ValidationError** (422): Input validation failed
  - Code: `VALIDATION_ERROR`
  - Extensions: `fieldErrors` (field-specific errors)
  - Occurs when: Invalid UUID format, invalid email format, missing required fields, or invalid field values
- **ServiceUnavailableError** (503): Database or S3 service unavailable
  - Code: `SERVICE_UNAVAILABLE`
  - Extensions: `serviceName: "database"` or `serviceName: "s3"`
  - Occurs when: Database connection fails or S3 service is unavailable

### Error Response Examples

**Example: File Size Error**

```json
{
  "errors": [
    {
      "message": "File size exceeds maximum of 5MB",
      "extensions": {
        "code": "BAD_REQUEST",
        "statusCode": 400
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
      "message": "Invalid email format",
      "extensions": {
        "code": "VALIDATION_ERROR",
        "statusCode": 422,
        "fieldErrors": {
          "email": ["Email must be a valid email address format"]
        }
      }
    }
  ]
}
```

**Example: Forbidden Error**

```json
{
  "errors": [
    {
      "message": "You do not have permission to perform this action",
      "extensions": {
        "code": "FORBIDDEN",
        "statusCode": 403,
        "requiredRole": "SuperAdmin"
      }
    }
  ]
}
```

**Example: User Not Found**

```json
{
  "errors": [
    {
      "message": "User with identifier '123e4567-e89b-12d3-a456-426614174000' not found",
      "extensions": {
        "code": "NOT_FOUND",
        "statusCode": 404,
        "resourceType": "User",
        "identifier": "123e4567-e89b-12d3-a456-426614174000"
      }
    }
  ]
}
```

### Error Handling Patterns

- **Input Validation**: UUIDs, emails, file data, and profile fields are validated before processing
- **File Validation**: Avatar uploads validate file type (JPEG, PNG, GIF, WebP), size (max 5MB), and content
- **Database Errors**: All database operations include transaction rollback on failure
- **Role-Based Access**: Access control checks prevent unauthorized access to user data
- **S3 Errors**: S3 upload errors are caught and converted to appropriate GraphQL errors
- **Error Logging**: Comprehensive error logging with context for debugging

## Usage Examples

### Complete User Management Flow

```graphql
# 1. Get current user
query GetMe {
  users {
    user(uuid: "123e4567-e89b-12d3-a456-426614174000") {
      uuid
      email
      name
      profile {
        jobTitle
        bio
        credits
      }
    }
  }
}

# 2. Update profile
mutation UpdateMyProfile {
  users {
    updateProfile(input: {
      jobTitle: "Senior Developer"
      bio: "Passionate about code"
      timezone: "UTC"
    }) {
      userId
      jobTitle
      bio
    }
  }
}

# 3. Upload avatar
mutation UploadMyAvatar {
  users {
    uploadAvatar(input: {
      fileData: "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
      filename: "profile.png"
    }) {
      userId
      avatarUrl
    }
  }
}

# 4. Update user name
mutation UpdateMyName {
  users {
    updateUser(input: {
      name: "John Updated"
    }) {
      uuid
      name
    }
  }
}

# 5. Admin: List all users
query ListAllUsers {
  users {
    users(limit: 50, offset: 0) {
      uuid
      email
      name
      isActive
    }
  }
}

# 6. Admin: Get user statistics
query GetStats {
  users {
    userStats {
      totalUsers
      activeUsers
      usersByRole {
        role
        count
      }
    }
  }
}

# 7. SuperAdmin: Promote user to Admin
mutation PromoteUserToAdmin {
  users {
    promoteToAdmin(input: {
      userId: "123e4567-e89b-12d3-a456-426614174000"
    }) {
      uuid
      email
      profile {
        role
      }
    }
  }
}

# 8. SuperAdmin: Promote user to SuperAdmin
mutation PromoteUserToSuperAdmin {
  users {
    promoteToSuperAdmin(input: {
      userId: "123e4567-e89b-12d3-a456-426614174000"
    }) {
      uuid
      email
      profile {
        role
      }
    }
  }
}
```

## Implementation Details

### Query Optimization

- **DataLoaders**: User queries use DataLoaders to prevent N+1 queries
  - The `user` query uses `info.context.dataloaders.user_by_uuid` to batch load users
  - This ensures that if multiple users are requested in a single query, only one database query is executed
  - Profile data is eagerly loaded using `selectinload(UserModel.profile)` in the `users` query to avoid lazy loading issues

### Avatar Upload

- **Avatar Storage**: Avatars are uploaded to S3 (or local storage if S3 not configured)
  - Filename is auto-generated as `{user_id}.jpg` (always uses .jpg extension regardless of source format)
  - S3 key format: `avatars/{user_id}/{user_id}.jpg`
  - File type is detected from file content (magic bytes), not from filename
  - Multiple input methods supported: base64, HTTP/HTTPS URL, file:// URL, local file path
  - File size limit: 5MB
  - Supported formats: JPEG, PNG, GIF, WebP
  - Database rollback on S3 upload failure to maintain consistency

### Profile Management

- **Profile Creation**: User profiles are automatically created during registration
- **Profile Updates**: Profile updates are atomic - all fields are updated in a single transaction
- **Validation**: All profile fields are validated before update (job_title max 255, bio max 1000, timezone max 100)

### Access Control

- **Role-Based Access**: Regular users can only access their own data; admins can access all users
  - `user` query: Regular users can only query their own UUID; Admin/SuperAdmin can query any user
  - `users` query: Admin/SuperAdmin only
  - `userStats` query: Admin/SuperAdmin only
  - `promoteToAdmin` and `promoteToSuperAdmin`: SuperAdmin only
- **Permission Checks**: Profile repository is used to check user roles before allowing operations

### Credit System

- **Credit Management**: Credits are managed through the profile and can be updated by admin operations
- **Credit Display**: Credits are shown in the UserProfile type and can be queried by users

### Error Handling

- **Transaction Management**: All mutations use database transactions with rollback on failure
- **S3 Error Handling**: S3 errors are caught and converted to ServiceUnavailableError with proper context
- **Database Error Handling**: Database errors are handled via centralized `handle_database_exception` function
- **Validation Errors**: Field-level validation errors are returned in `extensions.fieldErrors` for proper GraphQL error handling

## Task breakdown (for maintainers)

1. **Trace user query:** `UserQuery.user(uuid)` in `app/graphql/modules/users/queries.py` → repository; confirm ownership check (self or Admin/SuperAdmin).
2. **Trace updateProfile:** Mutation → UserProfileRepository update; verify `validate_name`, `validate_string_length` for optional fields.
3. **Avatar upload flow:** `uploadAvatar` → S3StorageClient (presigned URL or upload); confirm bucket comes from `user_profiles` / user context and URL is returned in User type.
4. **Promotion mutations:** `promoteToAdmin` / `promoteToSuperAdmin` require SuperAdmin; verify role update in UserProfileRepository and any audit logging.
5. **userStats:** Admin-only aggregation; confirm repository filters and that counts match users/user_profiles tables.

## Related Modules

- **Auth Module**: Provides authentication and user registration
- **Admin Module**: Provides admin operations for user management
- **Billing Module**: Manages subscriptions and billing information
- **AI Chats / data**: PostgreSQL `ai_chats` rows are owned by `users.uuid` and cascade on user deletion (Contact AI service); see [17_AI_CHATS_MODULE.md](17_AI_CHATS_MODULE.md), [database tables](../database/tables/README.md#user-deletion-cascade)

## Documentation metadata

- Era: `1.x`
- Introduced in: `TBD` (fill with exact minor)
- Frontend bindings: list page files from `docs/frontend/pages/*.json`
- Data stores touched: PostgreSQL/Elasticsearch/MongoDB/S3 as applicable

## Endpoint/version binding checklist

- Add operation list with `introduced_in` / `deprecated_in` tags.
- Map each operation to frontend page bindings and hook/service usage.
- Record DB tables read/write for each operation.

