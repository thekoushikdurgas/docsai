# Saved Searches Module

## Overview

The Saved Searches module provides functionality for saving and managing search queries including search terms, filters, sorting, and pagination settings. Users can save frequently used searches for quick access and track usage statistics.
**Location:** `app/graphql/modules/saved_searches/`

> **Integration:** Saved searches can be used as the source for Contact360 exports. When exporting contacts or companies via `contacts.exportContacts` / `companies.exportCompanies`, an optional `savedSearchId` can be passed to `createContact360Export`, and is stored on the corresponding `scheduler_jobs` record for auditability.

## Queries and mutations – parameters and variable types

| Operation | Parameter(s) | Variable type (GraphQL) | Return type |
|-----------|---------------|-------------------------|-------------|
| **Queries** | | | |
| `listSavedSearches` | `type`, `limit`, `offset` | String, Int, Int | `SavedSearchList` |
| `getSavedSearch` | `id` | ID! | `SavedSearch` |
| **Mutations** | | | |
| `createSavedSearch` | `input` | CreateSavedSearchInput! | `SavedSearch` |
| `updateSavedSearch` | `id`, `input` | ID!, UpdateSavedSearchInput! | `SavedSearch` |
| `deleteSavedSearch` | `id` | ID! | result |
| `updateSavedSearchUsage` | `id` | ID! | result |

Use camelCase in variables. Type filter: "contact", "company", or "all". saved_searches table; user isolation by user_id.

## Types

### SavedSearch

Represents a saved search query.

```graphql
type SavedSearch {
  id: ID!
  name: String!
  description: String
  type: String!  # "contact", "company", or "all"
  search_term: String
  filters: JSON
  sort_field: String
  sort_direction: String
  page_size: Int
  created_at: DateTime!
  updated_at: DateTime
  last_used_at: DateTime
  use_count: Int!
}
```

**Fields:**

- `id` (ID!): Unique saved search identifier
- `name` (String!): Search name (max 255 characters)
- `description` (String): Optional description (max 1000 characters)
- `type` (String!): Search type - "contact", "company", or "all"
- `search_term` (String): Optional search term
- `filters` (JSON): Optional filters as JSON object
- `sort_field` (String): Optional sort field name
- `sort_direction` (String): Optional sort direction ("asc" or "desc")
- `page_size` (Int): Optional page size for pagination
- `created_at` (DateTime!): Creation timestamp
- `updated_at` (DateTime): Last update timestamp
- `last_used_at` (DateTime): Timestamp of last usage
- `use_count` (Int!): Number of times this search has been used

### SavedSearchList

Paginated list of saved searches.

```graphql
type SavedSearchList {
  searches: [SavedSearch!]!
  total: Int!
}
```

**Fields:**

- `searches` ([SavedSearch!]!): List of saved searches
- `total` (Int!): Total count of saved searches

## Queries

### listSavedSearches

List saved searches for the current user with optional type filter and pagination.

**Parameters:**

| Name   | Type   | Required | Description                                      |
|--------|--------|----------|--------------------------------------------------|
| type   | String | No       | Filter by type: "contact", "company", or "all"   |
| limit  | Int    | No       | Max results (default 100, max 1000)              |
| offset | Int    | No       | Skip (default 0)                                 |

```graphql
query ListSavedSearches($type: String, $limit: Int, $offset: Int) {
  savedSearches {
    listSavedSearches(type: $type, limit: $limit, offset: $offset) {
      searches {
        id
        name
        description
        type
        search_term
        filters
        sort_field
        sort_direction
        page_size
        created_at
        updated_at
        last_used_at
        use_count
      }
      total
    }
  }
}
```

**Variables:**

```json
{
  "type": "contact",
  "limit": 50,
  "offset": 0
}
```

**Arguments:**

- `type` (String): Optional filter by search type ("contact", "company", or "all")
- `limit` (Int): Maximum number of results (default: 100, max: 1000)
- `offset` (Int): Number of results to skip (default: 0)

**Returns:** `SavedSearchList`

**Authentication:** Required

**Validation:**

- Pagination is validated via `validate_pagination` utility (limit: 1-1000, offset: non-negative)
- `type`: Optional, must be "contact", "company", or "all" if provided (case-insensitive)

**Implementation Details:**

- Uses `SavedSearchRepository.list_by_user` to retrieve user's saved searches
- User isolation enforced - users can only view their own saved searches
- Type filter is converted to enum value before querying
- Results are ordered by most recently used first, then by creation date

**Example Response:**

```json
{
  "data": {
    "savedSearches": {
      "listSavedSearches": {
        "searches": [
          {
            "id": "1",
            "name": "Tech Companies in SF",
            "description": "Technology companies in San Francisco",
            "type": "company",
            "search_term": "technology",
            "filters": {
              "location": "San Francisco",
              "industry": "Technology"
            },
            "sort_field": "name",
            "sort_direction": "asc",
            "page_size": 50,
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-16T14:20:00Z",
            "last_used_at": "2024-01-20T09:15:00Z",
            "use_count": 12
          }
        ],
        "total": 1
      }
    }
  }
}
```

### getSavedSearch

Get a specific saved search by ID.

**Parameters:**

| Name | Type | Required | Description              |
|------|------|----------|--------------------------|
| id   | ID!  | Yes      | Saved search ID (positive integer) |

```graphql
query GetSavedSearch($id: ID!) {
  savedSearches {
    getSavedSearch(id: $id) {
      id
      name
      description
      type
      search_term
      filters
      sort_field
      sort_direction
      page_size
      created_at
      updated_at
      last_used_at
      use_count
    }
  }
}
```

**Arguments:**

- `id` (ID!): Saved search ID (must be a positive integer)

**Returns:** `SavedSearch`

**Authentication:** Required

**Validation:**

- `id`: Required, must be a positive integer

**Implementation Details:**

- Uses `SavedSearchRepository.get_by_id` to retrieve saved search
- User isolation enforced - users can only access their own saved searches
- Raises NotFoundError if saved search doesn't exist
- Raises ForbiddenError if saved search doesn't belong to user

## Mutations

### createSavedSearch

Create a new saved search.

**Parameters:**

| Name  | Type                      | Required | Description        |
|-------|---------------------------|----------|--------------------|
| input | CreateSavedSearchInput!   | Yes      | name, type, filters, sort_field, etc. |

```graphql
mutation CreateSavedSearch($input: CreateSavedSearchInput!) {
  savedSearches {
    createSavedSearch(input: $input) {
      id
      name
      description
      type
      search_term
      filters
      sort_field
      sort_direction
      page_size
      created_at
      use_count
    }
  }
}
```

**Variables:**

```json
{
  "input": {
    "name": "Tech Companies in SF",
    "description": "Technology companies in San Francisco",
    "type": "company",
    "search_term": "technology",
    "filters": {
      "location": "San Francisco",
      "industry": "Technology"
    },
    "sort_field": "name",
    "sort_direction": "asc",
    "page_size": 50
  }
}
```

**Arguments:**

- `input` (CreateSavedSearchInput!): Saved search data

**Returns:** `SavedSearch`

**Authentication:** Required

**Validation:**

- `name`: Required, must be a string with max length 255 characters
- `description`: Optional, must be a string with max length 1000 characters if provided
- `type`: Required, must be "contact", "company", or "all" (case-insensitive)
- `search_term`: Optional string
- `filters`: Optional JSON object
- `sort_field`: Optional string
- `sort_direction`: Optional string
- `page_size`: Optional positive integer

**Implementation Details:**

- Uses `SavedSearchRepository.create` to create saved search
- Automatically sets `user_id` from authenticated user
- Sets `use_count` to 0 and `last_used_at` to null on creation
- Type is converted to enum value before storage
- Database errors are handled centrally via `handle_database_exception`

**Example Response:**

```json
{
  "data": {
    "savedSearches": {
      "createSavedSearch": {
        "id": "1",
        "name": "Tech Companies in SF",
        "description": "Technology companies in San Francisco",
        "type": "company",
        "search_term": "technology",
        "filters": {
          "location": "San Francisco",
          "industry": "Technology"
        },
        "sort_field": "name",
        "sort_direction": "asc",
        "page_size": 50,
        "created_at": "2024-01-15T10:30:00Z",
        "use_count": 0
      }
    }
  }
}
```

### updateSavedSearch

Update an existing saved search.

**Parameters:**

| Name  | Type                      | Required | Description                          |
|-------|---------------------------|----------|--------------------------------------|
| id    | ID!                       | Yes      | Saved search ID                      |
| input | UpdateSavedSearchInput!   | Yes      | Fields to update (all optional)     |

```graphql
mutation UpdateSavedSearch($id: ID!, $input: UpdateSavedSearchInput!) {
  savedSearches {
    updateSavedSearch(id: $id, input: $input) {
      id
      name
      description
      type
      search_term
      filters
      sort_field
      sort_direction
      page_size
      updated_at
    }
  }
}
```

**Variables:**

```json
{
  "id": "1",
  "input": {
    "name": "Updated Search Name",
    "description": "Updated description",
    "page_size": 100
  }
}
```

**Arguments:**

- `id` (ID!): Saved search ID (must be a positive integer)
- `input` (UpdateSavedSearchInput!): Updated saved search data (all fields optional)

**Returns:** `SavedSearch`

**Authentication:** Required

**Validation:**

- `id`: Required, must be a positive integer
- `name`: Optional, must be a string with max length 255 characters if provided
- `description`: Optional, must be a string with max length 1000 characters if provided
- `type`: Optional, must be "contact", "company", or "all" if provided (case-insensitive)
- Other fields: Optional, no validation beyond type checking

**Implementation Details:**

- Uses `SavedSearchRepository.get_by_id` to retrieve existing saved search
- User isolation enforced - users can only update their own saved searches
- Raises NotFoundError if saved search doesn't exist
- Raises ForbiddenError if saved search doesn't belong to user
- Only provided fields are updated (partial update)
- Type is converted to enum value before storage if provided
- `updated_at` is automatically set to current timestamp

### deleteSavedSearch

Delete a saved search.

**Parameters:**

| Name | Type | Required | Description        |
|------|------|----------|--------------------|
| id   | ID!  | Yes      | Saved search ID    |

```graphql
mutation DeleteSavedSearch($id: ID!) {
  savedSearches {
    deleteSavedSearch(id: $id)
  }
}
```

**Arguments:**

- `id` (ID!): Saved search ID (must be a positive integer)

**Returns:** `Boolean` (true if successful)

**Authentication:** Required

**Validation:**

- `id`: Required, must be a positive integer

**Implementation Details:**

- Uses `SavedSearchRepository.get_by_id` to retrieve saved search
- User isolation enforced - users can only delete their own saved searches
- Raises NotFoundError if saved search doesn't exist
- Raises ForbiddenError if saved search doesn't belong to user
- Uses `SavedSearchRepository.delete` to remove saved search
- Database errors are handled centrally via `handle_database_exception`

**Example Response:**

```json
{
  "data": {
    "savedSearches": {
      "deleteSavedSearch": true
    }
  }
}
```

### updateSavedSearchUsage

Update the last used timestamp and increment use count for a saved search.

**Parameters:**

| Name | Type | Required | Description        |
|------|------|----------|--------------------|
| id   | ID!  | Yes      | Saved search ID    |

```graphql
mutation UpdateSavedSearchUsage($id: ID!) {
  savedSearches {
    updateSavedSearchUsage(id: $id)
  }
}
```

**Arguments:**

- `id` (ID!): Saved search ID (must be a positive integer)

**Returns:** `Boolean` (true if successful)

**Authentication:** Required

**Validation:**

- `id`: Required, must be a positive integer

**Implementation Details:**

- Uses `SavedSearchRepository.update_usage` to update usage tracking
- User isolation enforced - users can only update usage for their own saved searches
- Raises NotFoundError if saved search doesn't exist
- Raises ForbiddenError if saved search doesn't belong to user
- Automatically sets `last_used_at` to current UTC timestamp
- Increments `use_count` by 1
- Database errors are handled centrally via `handle_database_exception`

**Example Response:**

```json
{
  "data": {
    "savedSearches": {
      "updateSavedSearchUsage": true
    }
  }
}
```

## Input Types

### CreateSavedSearchInput

Input for creating a saved search.

```graphql
input CreateSavedSearchInput {
  name: String!
  description: String
  type: String!  # "contact", "company", or "all"
  search_term: String
  filters: JSON
  sort_field: String
  sort_direction: String
  page_size: Int
}
```

**Fields:**

- `name` (String!): Search name (required, max 255 characters)
- `description` (String): Optional description (max 1000 characters)
- `type` (String!): Search type - "contact", "company", or "all" (required, case-insensitive)
- `search_term` (String): Optional search term
- `filters` (JSON): Optional filters as JSON object
- `sort_field` (String): Optional sort field name
- `sort_direction` (String): Optional sort direction ("asc" or "desc")
- `page_size` (Int): Optional page size for pagination

### UpdateSavedSearchInput

Input for updating a saved search.

```graphql
input UpdateSavedSearchInput {
  name: String
  description: String
  type: String  # "contact", "company", or "all"
  search_term: String
  filters: JSON
  sort_field: String
  sort_direction: String
  page_size: Int
}
```

**Fields:**

- All fields are optional
- Same validation rules as `CreateSavedSearchInput` for provided fields

## Error Handling

### Error Types

- **UnauthorizedError** (401): Authentication required
- **ForbiddenError** (403): User doesn't own the saved search
- **NotFoundError** (404): Saved search not found
- **BadRequestError** (400): Invalid input data (e.g., invalid type, string length exceeded)
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
      "resourceType": "SavedSearch",
      "identifier": "999"
    }
  }]
}
```

**Forbidden:**

```json
{
  "errors": [{
    "message": "You can only access your own saved searches",
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
    "message": "Invalid name: name must be at most 255 characters",
    "extensions": {
      "code": "BAD_REQUEST",
      "statusCode": 400
    }
  }]
}
```

**Invalid Type:**

```json
{
  "errors": [{
    "message": "Invalid type: 'invalid_type'. Valid options are: contact, company, all",
    "extensions": {
      "code": "BAD_REQUEST",
      "statusCode": 400
    }
  }]
}
```

## Usage Examples

### Complete Flow: Create, Use, and Update Saved Search

```graphql
# 1. Create a saved search
mutation CreateSearch {
  savedSearches {
    createSavedSearch(input: {
      name: "Tech Companies"
      type: "company"
      search_term: "technology"
      filters: { industry: "Technology" }
      page_size: 50
    }) {
      id
      name
      type
      created_at
    }
  }
}

# 2. Use the saved search (update usage)
mutation UseSearch {
  savedSearches {
    updateSavedSearchUsage(id: "1")
  }
}

# 3. List all saved searches
query ListSearches {
  savedSearches {
    listSavedSearches(limit: 10) {
      searches {
        id
        name
        type
        last_used_at
        use_count
      }
      total
    }
  }
}

# 4. Update the saved search
mutation UpdateSearch {
  savedSearches {
    updateSavedSearch(id: "1", input: {
      name: "Updated Tech Companies"
      page_size: 100
    }) {
      id
      name
      page_size
      updated_at
    }
  }
}
```

### Filter by Type

```graphql
query ListContactSearches {
  savedSearches {
    listSavedSearches(type: "contact", limit: 20) {
      searches {
        id
        name
        type
        use_count
      }
      total
    }
  }
}
```

## Implementation Details

### Repository Integration

- **SavedSearchRepository**: Provides data access layer
  - `create`: Create new saved search
  - `get_by_id`: Get saved search by ID
  - `list_by_user`: List saved searches for user with optional type filter
  - `update`: Update saved search fields
  - `update_usage`: Update last_used_at and increment use_count
  - `delete`: Delete saved search

### Database Schema

- **Table**: `saved_searches`
- **Key Fields**: `id`, `user_id`, `name`, `type`, `search_term`, `filters`, `sort_field`, `sort_direction`, `page_size`, `description`, `created_at`, `updated_at`, `last_used_at`, `use_count`
- **Indexes**: `user_id`, `type`, `user_id + type` (composite)
- **Foreign Keys**: `user_id` references `users.uuid`

### User Isolation

All operations enforce user isolation:

- Queries filter by `user_id` at repository level
- Mutations verify ownership before allowing updates/deletes
- Raises ForbiddenError if user tries to access another user's saved searches

### Timezone Handling

All timestamps use UTC timezone:

- `created_at`, `updated_at`, `last_used_at` are stored as timezone-aware datetimes
- Repository uses `datetime.now(UTC)` for timestamp updates

### Validation

- String length validation: `name` (max 255), `description` (max 1000)
- Type validation: Must be "contact", "company", or "all" (case-insensitive)
- Pagination validation: Uses `validate_pagination` utility
- ID validation: Must be positive integer

## Task breakdown (for maintainers)

1. **listSavedSearches/getSavedSearch:** SavedSearchRepository; user_id from context; optional type filter ("contact", "company", "all"); validate_pagination for list; return SavedSearchList/SavedSearch.
2. **createSavedSearch/updateSavedSearch:** Validate name (max 255), description (max 1000), type (contact|company|all), filters (JSON), sort_field, sort_direction, page_size; user_id stored; update last_used_at/use_count when used in export.
3. **updateSavedSearchUsage:** Increment use_count and set last_used_at when a saved search is used (e.g. in createContact360Export with savedSearchId); confirm Jobs module stores saved_search_id in request_payload.
4. **deleteSavedSearch:** Ownership check; delete from saved_searches; cascade or orphan handling if referenced by scheduler_jobs (audit only, no FK).
5. **Export integration:** Document how savedSearchId in CreateContact360ExportInput links to saved_searches.id and is stored in scheduler_jobs.request_payload.

## Related Modules

- **Contacts Module**: Saved searches can be used with contact queries
- **Companies Module**: Saved searches can be used with company queries
- **Users Module**: User profile and authentication
- **AI Chats Module** ([17_AI_CHATS_MODULE.md](17_AI_CHATS_MODULE.md)): `parseContactFilters` can help build filter JSON for saved searches

## Documentation metadata

- Era: `9.x`
- Introduced in: `TBD` (fill with exact minor)
- Frontend bindings: list page files from `docs/frontend/pages/*.json`
- Data stores touched: PostgreSQL/Elasticsearch/MongoDB/S3 as applicable

## Endpoint/version binding checklist

- Add operation list with `introduced_in` / `deprecated_in` tags.
- Map each operation to frontend page bindings and hook/service usage.
- Record DB tables read/write for each operation.

