# Notifications Module

## Overview

The Notifications module provides notification management functionality including listing notifications, marking as read, deleting notifications, and managing notification preferences.
**Location:** `app/graphql/modules/notifications/`

## Queries and mutations – parameters and variable types

| Operation | Parameter(s) | Variable type (GraphQL) | Return type |
|-----------|---------------|-------------------------|-------------|
| **Queries** (under `notifications { ... }`) | | | |
| `notifications` | `filters` | `NotificationFilterInput` | `NotificationConnection` |
| `notification` | `notificationId` | `ID!` | `Notification` |
| `unreadCount` | — | — | `UnreadCountResponse` |
| `notificationPreferences` | — | — | `NotificationPreferences` |
| **Mutations** (under `notifications { ... }`) | | | |
| `markNotificationAsRead` | `notificationId` | `ID!` | `Notification` |
| `markNotificationsAsRead` | `input` | `MarkReadInput!` | `MarkReadResponse` |
| `deleteNotifications` | `input` | `DeleteNotificationsInput!` | `DeleteNotificationsResponse` |
| `updateNotificationPreferences` | `input` | `UpdateNotificationPreferencesInput!` | `NotificationPreferences` |

Use camelCase in variables. Enum `GraphQLNotificationType`: SYSTEM, SECURITY, ACTIVITY, MARKETING, BILLING. Enum `GraphQLNotificationPriority`: LOW, MEDIUM, HIGH, URGENT.

## Canonical SDL (gateway schema)

Regenerate the full schema from `contact360.io/api` with:

`python -c "from app.graphql.schema import schema; print(schema.as_str())"`

```graphql
type NotificationQuery {
  notifications(filters: NotificationFilterInput = null): NotificationConnection!
  notification(notificationId: ID!): Notification!
  unreadCount: UnreadCountResponse!
  notificationPreferences: NotificationPreferences!
}

type NotificationMutation {
  markNotificationAsRead(notificationId: ID!): Notification!
  markNotificationsAsRead(input: MarkReadInput!): MarkReadResponse!
  deleteNotifications(input: DeleteNotificationsInput!): DeleteNotificationsResponse!
  updateNotificationPreferences(input: UpdateNotificationPreferencesInput!): NotificationPreferences!
}

input NotificationFilterInput {
  limit: Int = 100
  offset: Int = 0
  unreadOnly: Boolean! = false
  type: GraphQLNotificationType = null
}

input MarkReadInput {
  notificationIds: [ID!]!
}

input DeleteNotificationsInput {
  notificationIds: [ID!]!
}

input UpdateNotificationPreferencesInput {
  emailDigest: Boolean = null
  newLeads: Boolean = null
  securityAlerts: Boolean = null
  marketing: Boolean = null
  billingUpdates: Boolean = null
  pushEnabled: Boolean = null
  emailEnabled: Boolean = null
}
```

## POST `/graphql` — full request and response

Headers: `Content-Type: application/json`, `Authorization: Bearer <access_token>`.

### `notifications.notifications` (query)

```json
{
  "query": "query ($filters: NotificationFilterInput) { notifications { notifications(filters: $filters) { items { id title read } pageInfo { total limit offset hasNext hasPrevious } } } }",
  "variables": {
    "filters": {
      "limit": 20,
      "offset": 0,
      "unreadOnly": false,
      "type": null
    }
  }
}
```

### `notifications.markNotificationAsRead` (mutation)

```json
{
  "query": "mutation ($notificationId: ID!) { notifications { markNotificationAsRead(notificationId: $notificationId) { id read } } }",
  "variables": { "notificationId": "0194a1c0-0000-7000-8000-000000000001" }
}
```

## Types

### Notification

Represents a single notification.

```graphql
type Notification {
  id: ID!
  userId: ID!
  type: NotificationType!
  priority: NotificationPriority!
  title: String!
  message: String!
  actionUrl: String
  actionLabel: String
  read: Boolean!
  createdAt: DateTime!
  readAt: DateTime
  metadata: JSON
}
```

**Fields:**
- `id` (ID!): Unique notification identifier
- `userId` (ID!): User who owns the notification
- `type` (NotificationType!): Notification type
- `priority` (NotificationPriority!): Notification priority level
- `title` (String!): Notification title
- `message` (String!): Notification message
- `actionUrl` (String): Optional action URL
- `actionLabel` (String): Optional action button label
- `read` (Boolean!): Whether notification has been read
- `createdAt` (DateTime!): Creation timestamp
- `readAt` (DateTime): Timestamp when marked as read
- `metadata` (JSON): Additional metadata

### NotificationType

Enum for notification types.

```graphql
enum NotificationType {
  SYSTEM
  SECURITY
  ACTIVITY
  MARKETING
  BILLING
}
```

### NotificationPriority

Enum for notification priorities.

```graphql
enum NotificationPriority {
  LOW
  MEDIUM
  HIGH
  URGENT
}
```

### NotificationConnection

Paginated notification connection.

```graphql
type NotificationConnection {
  items: [Notification!]!
  pageInfo: PageInfo!
}
```

### UnreadCountResponse

Response for unread notification count.

```graphql
type UnreadCountResponse {
  count: Int!
}
```

### NotificationPreferences

Notification preferences for a user.

```graphql
type NotificationPreferences {
  emailDigest: Boolean!
  newLeads: Boolean!
  securityAlerts: Boolean!
  marketing: Boolean!
  billingUpdates: Boolean!
  pushEnabled: Boolean!
  emailEnabled: Boolean!
}
```

### MarkReadResponse

Response for marking notifications as read.

```graphql
type MarkReadResponse {
  count: Int!
}
```

### DeleteNotificationsResponse

Response for deleting notifications.

```graphql
type DeleteNotificationsResponse {
  count: Int!
}
```

## Queries

### notifications

List notifications for the current user with pagination and filters.

**Parameters:**

| Name     | Type                     | Required | Description |
|----------|--------------------------|----------|-------------|
| `filters` | NotificationFilterInput | No       | Optional: limit, offset, type (NotificationType), unreadOnly. |

```graphql
query ListNotifications($filters: NotificationFilterInput) {
  notifications {
    notifications(filters: $filters) {
      items {
        id
        type
        priority
        title
        message
        read
        createdAt
      }
      pageInfo {
        total
        limit
        offset
        hasNext
        hasPrevious
      }
    }
  }
}
```

**Variables:**

```json
{
  "filters": {
    "unreadOnly": true,
    "type": "SYSTEM",
    "limit": 20,
    "offset": 0
  }
}
```

**Arguments:**
- `filters` (NotificationFilterInput): Optional filter criteria

**Returns:** `NotificationConnection`

**Authentication:** Required

**Validation:**
- Pagination is validated via `validate_pagination` utility (limit, offset)
- `type`: Optional, must be valid NotificationType enum value if provided
- `unread_only`: Optional boolean filter

**Implementation Details:**
- Uses `NotificationRepository.list_by_user` to retrieve user's notifications
- User isolation enforced - users can only view their own notifications
- Pagination is normalized for backward compatibility
- Notification type is converted from enum to NotificationType model
- Response structure is validated before conversion to GraphQL types

**Example Response:**

```json
{
  "data": {
    "notifications": {
      "notifications": {
        "items": [
          {
            "id": "1",
            "type": "SYSTEM",
            "priority": "HIGH",
            "title": "Welcome!",
            "message": "Welcome to the platform",
            "read": false,
            "createdAt": "2024-01-15T10:30:00Z"
          }
        ],
        "pageInfo": {
          "total": 1,
          "limit": 20,
          "offset": 0,
          "hasNext": false,
          "hasPrevious": false
        }
      }
    }
  }
}
```

### notification

Get a notification by ID.

**Parameters:**

| Name             | Type | Required | Description |
|------------------|------|----------|-------------|
| `notificationId` | ID!  | Yes      | Notification ID (positive integer). |

```graphql
query GetNotification($notificationId: ID!) {
  notifications {
    notification(notificationId: $notificationId) {
      id
      type
      priority
      title
      message
      read
      createdAt
    }
  }
}
```

**Arguments:**
- `notificationId` (ID!): Notification ID (must be a positive integer)

**Returns:** `Notification`

**Authentication:** Required

**Validation:**
- `notificationId`: Required, must be a positive integer

**Implementation Details:**
- Uses `NotificationService.get_notification` to retrieve notification
- User isolation enforced - users can only view their own notifications
- Raises NotFoundError if notification doesn't exist or doesn't belong to user
- Response structure is validated before conversion to GraphQL type

### unreadCount

Get count of unread notifications for the current user.

**Parameters:** None.

```graphql
query GetUnreadCount {
  notifications {
    unreadCount {
      count
    }
  }
}
```

**Returns:** `UnreadCountResponse`

**Authentication:** Required

**Implementation Details:**
- Uses `NotificationRepository.get_unread_count` to count unread notifications
- User isolation enforced - counts only user's own notifications
- Returns 0 if count is invalid or negative
- Database errors are handled centrally via `handle_database_exception`

**Example Response:**

```json
{
  "data": {
    "notifications": {
      "unreadCount": {
        "count": 5
      }
    }
  }
}
```

### notificationPreferences

Get notification preferences for the current user.

**Parameters:** None.

```graphql
query GetPreferences {
  notifications {
    notificationPreferences {
      emailDigest
      newLeads
      securityAlerts
      marketing
      billingUpdates
      pushEnabled
      emailEnabled
    }
  }
}
```

**Returns:** `NotificationPreferences`

**Authentication:** Required

**Implementation Details:**
- Uses `UserProfileRepository.get_by_user_id` to retrieve user profile
- Returns default preferences (all false) if profile or notifications field is missing
- Preferences are stored as JSON in user profile
- Response structure is validated before conversion to GraphQL type

## Mutations

### markNotificationAsRead

Mark a notification as read.

**Parameters:**

| Name             | Type | Required | Description |
|------------------|------|----------|-------------|
| `notificationId` | ID!  | Yes      | Notification ID (positive integer) to mark as read. |

```graphql
mutation MarkAsRead($notificationId: ID!) {
  notifications {
    markNotificationAsRead(notificationId: $notificationId) {
      id
      read
      readAt
    }
  }
}
```

**Arguments:**
- `notificationId` (ID!): Notification ID (must be a positive integer)

**Returns:** `Notification`

**Authentication:** Required

**Validation:**
- `notificationId`: Required, must be a positive integer

**Implementation Details:**
- Uses `NotificationService.mark_as_read` to mark notification as read
- User isolation enforced - users can only mark their own notifications as read
- Updates read status and readAt timestamp
- Raises NotFoundError if notification doesn't exist or doesn't belong to user
- Transaction rollback on failure
- Response structure is validated before conversion to GraphQL type

### markNotificationsAsRead

Mark multiple notifications as read.

**Parameters:**

| Name    | Type           | Required | Description |
|---------|----------------|----------|-------------|
| `input` | MarkReadInput! | Yes      | `notificationIds`: list of notification IDs (positive integers). |

```graphql
mutation MarkMultipleAsRead($input: MarkReadInput!) {
  notifications {
    markNotificationsAsRead(input: $input) {
      count
    }
  }
}
```

**Variables:**

```json
{
  "input": {
    "notificationIds": ["1", "2", "3"]
  }
}
```

**Input:** `MarkReadInput!`

**Returns:** `MarkReadResponse`

**Authentication:** Required

**Validation:**
- `notification_ids`: Required, non-empty list, max 1000 notifications
- Each notification_id must be a positive integer

**Implementation Details:**
- Uses `NotificationService.mark_multiple_as_read` to mark multiple notifications as read
- User isolation enforced - users can only mark their own notifications as read
- Batch processing for efficiency
- Returns count of notifications marked as read
- Transaction rollback on failure
- Returns 0 if count is invalid or negative

### markAllNotificationsAsRead

Mark all notifications as read (if available).

**Parameters:** None.

```graphql
mutation MarkAllAsRead {
  notifications {
    markAllNotificationsAsRead {
      count
    }
  }
}
```

### deleteNotification

Delete a notification.

**Parameters:**

| Name             | Type | Required | Description |
|------------------|------|----------|-------------|
| `notificationId` | ID!  | Yes      | Notification ID (positive integer) to delete. |

```graphql
mutation DeleteNotification($notificationId: ID!) {
  notifications {
    deleteNotification(notificationId: $notificationId)
  }
}
```

### deleteNotifications

Delete multiple notifications.

**Parameters:**

| Name    | Type                        | Required | Description |
|---------|-----------------------------|----------|-------------|
| `input` | DeleteNotificationsInput!  | Yes      | `notificationIds`: list of notification IDs to delete. |

```graphql
mutation DeleteNotifications($input: DeleteNotificationsInput!) {
  notifications {
    deleteNotifications(input: $input) {
      count
    }
  }
}
```

**Variables:**

```json
{
  "input": {
    "notificationIds": ["1", "2", "3"]
  }
}
```

**Input:** `DeleteNotificationsInput!`

**Returns:** `DeleteNotificationsResponse`

**Authentication:** Required

**Validation:**
- `notification_ids`: Required, non-empty list, max 1000 notifications
- Each notification_id must be a positive integer

**Implementation Details:**
- Uses `NotificationService.delete_notifications` to delete multiple notifications
- User isolation enforced - users can only delete their own notifications
- Batch processing for efficiency
- Returns count of notifications deleted
- Transaction rollback on failure
- Returns 0 if count is invalid or negative

### updateNotificationPreferences

Update notification preferences for the current user.

**Parameters:**

| Name    | Type                                  | Required | Description |
|---------|---------------------------------------|----------|-------------|
| `input` | UpdateNotificationPreferencesInput!  | Yes      | emailDigest, newLeads, securityAlerts, marketing, billingUpdates, pushEnabled, emailEnabled (all Boolean). |

```graphql
mutation UpdatePreferences($input: UpdateNotificationPreferencesInput!) {
  notifications {
    updateNotificationPreferences(input: $input) {
      emailDigest
      newLeads
      securityAlerts
      marketing
      billingUpdates
      pushEnabled
      emailEnabled
    }
  }
}
```

**Variables:**

```json
{
  "input": {
    "emailDigest": true,
    "newLeads": true,
    "securityAlerts": true,
    "marketing": false,
    "billingUpdates": true,
    "pushEnabled": false,
    "emailEnabled": true
  }
}
```

**Input:** `UpdateNotificationPreferencesInput!`

**Returns:** `NotificationPreferences`

**Authentication:** Required

**Validation:**
- All preference fields are optional booleans
- Each field must be a boolean if provided (validated before update)

**Implementation Details:**
- Uses `UserProfileRepository.get_by_user_id` to retrieve user profile
- Raises NotFoundError if profile doesn't exist
- Updates preferences by merging with existing preferences (partial update)
- Stores preferences as JSON in user profile
- Transaction rollback on failure
- Response structure is validated before conversion to GraphQL type

## Input Types

### NotificationFilterInput

Filter input for notifications.

```graphql
input NotificationFilterInput {
  unreadOnly: Boolean
  type: NotificationType
  priority: NotificationPriority
  limit: Int
  offset: Int
}
```

### MarkReadInput

Input for marking notifications as read.

```graphql
input MarkReadInput {
  notificationIds: [ID!]!
}
```

### DeleteNotificationsInput

Input for deleting notifications.

```graphql
input DeleteNotificationsInput {
  notificationIds: [ID!]!
}
```

### UpdateNotificationPreferencesInput

Input for updating notification preferences.

```graphql
input UpdateNotificationPreferencesInput {
  emailDigest: Boolean
  newLeads: Boolean
  securityAlerts: Boolean
  marketing: Boolean
  billingUpdates: Boolean
  pushEnabled: Boolean
  emailEnabled: Boolean
}
```

### CreateNotificationInput

Input for creating a notification (admin only).

```graphql
input CreateNotificationInput {
  userId: ID!
  type: NotificationType!
  priority: NotificationPriority!
  title: String!
  message: String!
  actionUrl: String
  actionLabel: String
  metadata: JSON
}
```

## Error Handling

The Notifications module implements comprehensive error handling with input validation, database error handling, and response validation.

### Error Types

The Notifications module may raise the following errors:

- **NotFoundError** (404): Notification not found
  - Code: `NOT_FOUND`
  - Extensions: `resourceType: "Notification"`, `identifier: <notification_id>`
  - Occurs when: Requested notification ID does not exist or belongs to another user
- **ForbiddenError** (403): Insufficient permissions
  - Code: `FORBIDDEN`
  - Extensions: `requiredRole: <role>` (if applicable)
  - Occurs when: User lacks required permissions for the operation
- **ValidationError** (422): Input validation failed
  - Code: `VALIDATION_ERROR`
  - Extensions: `fieldErrors` (field-specific errors)
  - Occurs when: Invalid notification ID format, invalid filter parameters, invalid pagination values, or invalid notification type/priority

### Error Response Examples

**Example: Notification Not Found**

```json
{
  "errors": [
    {
      "message": "Notification with identifier '1' not found",
      "extensions": {
        "code": "NOT_FOUND",
        "statusCode": 404,
        "resourceType": "Notification",
        "identifier": "1"
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
      "message": "Invalid notification type",
      "extensions": {
        "code": "VALIDATION_ERROR",
        "statusCode": 422,
        "fieldErrors": {
          "type": ["Notification type must be one of: SYSTEM, SECURITY, ACTIVITY, MARKETING, BILLING"],
          "limit": ["Limit must be a positive integer between 1 and 1000"]
        }
      }
    }
  ]
}
```

### Error Handling Patterns

- **Input Validation**: Notification IDs, filters, pagination parameters, and notification types are validated before processing
- **Database Errors**: All database operations include transaction rollback on failure
- **User Isolation**: Users can only access their own notifications
- **Error Logging**: Comprehensive error logging with context for debugging

## Usage Examples

### Complete Notification Management Flow

```graphql
# 1. Get unread count
query GetUnreadCount {
  notifications {
    unreadCount {
      count
    }
  }
}

# 2. List unread notifications
query ListUnread {
  notifications {
    notifications(filters: {
      unreadOnly: true
      limit: 20
    }) {
      items {
        id
        type
        priority
        title
        message
        createdAt
      }
      pageInfo {
        total
      }
    }
  }
}

# 3. Mark notification as read
mutation MarkAsRead {
  notifications {
    markNotificationAsRead(notificationId: "1") {
      id
      read
      readAt
    }
  }
}

# 4. Mark multiple as read
mutation MarkMultiple {
  notifications {
    markNotificationsAsRead(input: {
      notificationIds: ["1", "2", "3"]
    }) {
      count
    }
  }
}

# 5. Delete notifications
mutation Delete {
  notifications {
    deleteNotifications(input: {
      notificationIds: ["1", "2"]
    }) {
      count
    }
  }
}

# 6. Update preferences
mutation UpdatePrefs {
  notifications {
    updateNotificationPreferences(input: {
      emailDigest: true
      newLeads: true
      marketing: false
    }) {
      emailDigest
      newLeads
      marketing
    }
  }
}
```

## Implementation Details

### NotificationRepository Integration

- **NotificationRepository**: Handles notification data operations
  - `list_by_user`: Lists notifications for a user with filters and pagination
  - `get_unread_count`: Counts unread notifications for a user
  - User isolation enforced at repository level
- **User Isolation**: Users can only access their own notifications
  - All queries filter by user_id
  - All mutations verify ownership before operations
  - Raises NotFoundError if notification doesn't belong to user

### NotificationService Integration

- **NotificationService**: Handles notification business logic
  - `get_notification`: Retrieves notification by ID with user ownership check
  - `mark_as_read`: Marks single notification as read
  - `mark_multiple_as_read`: Marks multiple notifications as read (batch)
  - `delete_notifications`: Deletes multiple notifications (batch)
  - All operations enforce user isolation

### UserProfileRepository Integration

- **UserProfileRepository**: Handles notification preferences
  - `get_by_user_id`: Retrieves user profile for preferences
  - Preferences stored as JSON in `profile.notifications` field
  - Default preferences returned if profile or notifications field is missing

### Validation

- **Input Validation**: All inputs are validated before processing
  - `notification_id`: Required, must be a positive integer
  - `notification_ids`: Required, non-empty list, max 1000 items, each must be positive integer
  - Pagination validation via `validate_pagination` utility (limit, offset)
  - Notification type validation (must be valid NotificationType enum)
  - Boolean validation for preference fields
- **Integer Validation**: Notification IDs are validated as positive integers
  - Converts from string/ID to integer
  - Validates positive (greater than 0)
  - Batch operations validate all IDs in list

### Error Handling

- **Input Validation**: All inputs are validated before processing
  - Notification ID format validation (positive integer)
  - List validation (non-empty, max 1000 items)
  - Boolean validation for preferences
  - Pagination validation
- **Database Error Handling**: Database errors are handled centrally via `handle_database_exception`
  - NotificationRepository errors are caught and converted to appropriate GraphQL errors
  - NotificationService errors are caught and converted to appropriate GraphQL errors
  - Transaction rollback on failure
  - Transaction commit after successful operations
- **User Isolation**: User ownership is verified before operations
  - Raises NotFoundError if notification doesn't exist or doesn't belong to user
  - Prevents unauthorized access to other users' notifications
- **Response Validation**: Service responses are validated before conversion
  - Checks for required structure
  - Validates count values (non-negative)
  - Conversion errors are caught and logged

### Pagination

- **Pagination Support**: List queries support pagination
  - `limit`: Maximum number of items to return
  - `offset`: Number of items to skip
  - Pagination is normalized for backward compatibility
  - Total count is included in response
- **Pagination Validation**: Pagination parameters are validated
  - Uses `validate_pagination` utility
  - Normalizes limit and offset values

### Notification Types and Priorities

- **Notification Types**: Five notification types supported
  - `SYSTEM`: System notifications
  - `SECURITY`: Security alerts
  - `ACTIVITY`: Activity notifications
  - `MARKETING`: Marketing notifications
  - `BILLING`: Billing notifications
- **Notification Priorities**: Four priority levels supported
  - `LOW`: Low priority
  - `MEDIUM`: Medium priority
  - `HIGH`: High priority
  - `URGENT`: Urgent priority

### Read Tracking

- **Read Status**: Read status and read timestamp are tracked separately
  - `read`: Boolean flag indicating if notification has been read
  - `readAt`: Timestamp when notification was marked as read
  - Updated when notification is marked as read
  - Used for filtering unread notifications

### Preferences Management

- **Preferences Storage**: Notification preferences are stored in the user profile
  - Stored as JSON in `profile.notifications` field
  - Supports partial updates (only provided fields are updated)
  - Default preferences returned if not set
- **Preference Fields**: Seven preference fields supported
  - `emailDigest`: Email digest notifications
  - `newLeads`: New leads notifications
  - `securityAlerts`: Security alerts
  - `marketing`: Marketing notifications
  - `billingUpdates`: Billing update notifications
  - `pushEnabled`: Push notifications enabled
  - `emailEnabled`: Email notifications enabled

### Batch Operations

- **Batch Limits**: Batch operations have limits
  - Max 1000 notifications per batch operation
  - Prevents excessive resource usage
  - Validated before processing
- **Batch Processing**: Multiple notifications processed efficiently
  - `mark_multiple_as_read`: Marks multiple notifications as read
  - `delete_notifications`: Deletes multiple notifications
  - Returns count of affected notifications

### Metadata

- **JSON Metadata**: Notifications support JSON metadata for additional data
  - Stored in `metadata` field
  - Flexible structure for custom data
  - Can include any JSON-serializable data

## Task breakdown (for maintainers)

1. **Trace notifications list:** NotificationQuery.notifications → NotificationRepository with user_id from context; validate_pagination(limit, offset); filter by read/type.
2. **markNotificationAsRead:** Verify ownership (notification.user_id == context.user); update read/readAt; return updated Notification.
3. **Batch operations:** markNotificationsAsRead and deleteNotifications accept [ID!]!; confirm max batch size (e.g. 1000) and user isolation in repository.
4. **notificationPreferences:** Stored on user_profiles or separate table; verify updateNotificationPreferences input validation and that all preference fields are documented.
5. **Admin-created notifications:** If admin module creates notifications for users, ensure NotificationRepository or NotificationService is used and userId is set correctly.

## Related Modules

- **Users Module**: User profile contains notification preferences
- **Admin Module**: Admin can create notifications for users
- **AI Chats Module** ([17_AI_CHATS_MODULE.md](17_AI_CHATS_MODULE.md)): in-app AI features are separate from this notification system unless product explicitly ties them (e.g. marketing emails)

## Documentation metadata

- Era: `9.x`
- Introduced in: `TBD` (fill with exact minor)
- Frontend bindings: list page files from `docs/frontend/pages/*.json`
- Data stores touched: PostgreSQL/Elasticsearch/MongoDB/S3 as applicable

## Endpoint/version binding checklist

- Add operation list with `introduced_in` / `deprecated_in` tags.
- Map each operation to frontend page bindings and hook/service usage.
- Record DB tables read/write for each operation.

