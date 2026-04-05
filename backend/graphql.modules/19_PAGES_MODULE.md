# Pages Module

## Overview

The Pages module provides a unified interface for accessing documentation, marketing, and dashboard pages. It replaces the separate Dashboard Pages, Documentation, and Marketing modules with a single, streamlined API. Pages are returned in authentication responses based on user role. Most Pages queries are public (no access token). The `myPages` query requires authentication (current user’s pages).
**Location:** `app/graphql/modules/pages/`

GraphQL path: `query { pages { page(pageId: "...") { ... } pages { ... } dashboardPages { ... } ... } }` — all operations are fields on the root **`pages`** resolver type.

**Replaces:**
- `app/graphql/modules/dashboard_pages/` (deleted)
- `app/graphql/modules/documentation/` (deleted)
- `app/graphql/modules/marketing/` (deleted)

## Queries – parameters and variable types

| Query | Parameter(s) | Variable type (GraphQL) | Return type |
|-------|---------------|-------------------------|-------------|
| `page` | `pageId` | String! | PageDetail |
| `pages` | (filters) | — | page list |
| `pageContent` | `pageId` | String! | content |
| `pagesByType` | `pageType` | String! | pages |
| `pageTypes` | — | — | types |
| `pageStatistics` | `pageType` | String! | stats |
| `pagesByState` / `pagesByStateCount` | `state` | String! | pages / count |
| `pagesByUserType` / `pagesByDocsaiUserType` | `userType` | String! | pages |
| `myPages` | — | — | pages (auth) |
| `pageAccessControl`, `pageSections`, `pageComponents`, `pageEndpoints`, `pageVersions` | `pageId` | String! | various |
| `dashboardPages`, `marketingPages` | — | — | pages |

No mutations in this API (create/update/delete may be via DocsAI). Data is sourced from DocsAI when enabled. Use camelCase in variables.

## Canonical SDL (gateway schema)

Regenerate the full schema from `contact360.io/api` with:

`python -c "from app.graphql.schema import schema; print(schema.as_str())"`

```graphql
type PagesQuery {
  page(pageId: String!, pageType: String = null): PageDetail!
  pages(pageType: String = null, includeDrafts: Boolean! = true, includeDeleted: Boolean! = false, status: String = null, limit: Int! = 100, offset: Int! = 0): PageList!
  pageContent(pageId: String!): PageContent!
  pagesByType(pageType: String!, includeDrafts: Boolean! = true, includeDeleted: Boolean! = false, status: String = null): PageList!
  pageTypes: PageTypeList!
  pageStatistics(pageType: String!): TypeStatistics!
  pagesByState(state: String!): PageList!
  pagesByStateCount(state: String!): Int!
  pagesByUserType(userType: String!): PageList!
  pagesByDocsaiUserType(userType: String!, pageType: String = null): PageList!
  myPages(pageType: String = null): PageList!
  pageAccessControl(pageId: String!): JSON!
  pageSections(pageId: String!): JSON!
  pageComponents(pageId: String!): JSON!
  pageEndpoints(pageId: String!): JSON!
  pageVersions(pageId: String!): JSON!
  dashboardPages(page: Int! = 1, pageSize: Int! = 20, pageType: String = null, status: String = null, search: String = null): DashboardPageList!
  marketingPages(page: Int! = 1, pageSize: Int! = 20, status: String = null, search: String = null): DashboardPageList!
}
```

## POST `/graphql` — full request and response

Most queries are public (no `Authorization` header). `myPages` requires authentication.

```json
{
  "query": "query ($pageId: String!) { pages { page(pageId: $pageId) { pageId title pageType route status version } } }",
  "variables": { "pageId": "docs-getting-started" }
}
```

## Types

### PageSummary

Lightweight page information returned in authentication responses and lists.

```graphql
type PageSummary {
  pageId: String!
  title: String!
  pageType: String!
  route: String
  status: String!
}
```

**Fields:**

- `pageId` (String!): Unique page identifier
- `title` (String!): Page title
- `pageType` (String!): Page type (`docs`, `marketing`, or `dashboard`)
- `route` (String): Page route/URL path (optional)
- `status` (String!): Page status (`draft`, `published`, or `deleted`)

### PageDetail

Full page details including content URL and metadata.

```graphql
type PageDetail {
  pageId: String!
  title: String!
  pageType: String!
  description: String
  contentUrl: String
  route: String
  status: String!
  version: Int!
  category: String
  createdAt: DateTime
  updatedAt: DateTime
}
```

**Fields:**

- `pageId` (String!): Unique page identifier
- `title` (String!): Page title
- `pageType` (String!): Page type (`docs`, `marketing`, or `dashboard`)
- `description` (String): Page description (optional)
- `contentUrl` (String): S3 presigned URL for content (optional)
- `route` (String): Page route/URL path (optional)
- `status` (String!): Page status (`draft`, `published`, or `deleted`)
- `version` (Int!): Page version number (default: 1)
- `category` (String): Page category (optional)
- `createdAt` (DateTime): Creation timestamp (optional)
- `updatedAt` (DateTime): Last update timestamp (optional)

### PageList

Paginated list of pages.

```graphql
type PageList {
  pages: [PageSummary!]!
  total: Int!
}
```

**Fields:**

- `pages` ([PageSummary!]!): List of page summaries
- `total` (Int!): Total count of pages matching criteria

### PageContent

Page markdown content.

```graphql
type PageContent {
  pageId: String!
  content: String!
}
```

**Fields:**

- `pageId` (String!): Page identifier
- `content` (String!): Raw markdown content

### PageTypeInfo

Page type information with count.

```graphql
type PageTypeInfo {
  type: String!
  count: Int!
}
```

**Fields:**

- `type` (String!): Page type name
- `count` (Int!): Number of pages of this type

### PageTypeList

List of page types with counts.

```graphql
type PageTypeList {
  types: [PageTypeInfo!]!
  total: Int!
}
```

**Fields:**

- `types` ([PageTypeInfo!]!): List of page type info
- `total` (Int!): Total pages across all types

### TypeStatistics

Statistics for a specific page type.

```graphql
type TypeStatistics {
  pageType: String!
  total: Int!
  published: Int!
  draft: Int!
  deleted: Int!
  lastUpdated: String
}
```

**Fields:**

- `pageType` (String!): Page type name
- `total` (Int!): Total pages of this type
- `published` (Int!): Published page count
- `draft` (Int!): Draft page count
- `deleted` (Int!): Deleted page count
- `lastUpdated` (String): ISO timestamp of last update (optional)

### DashboardPageList

Paginated dashboard pages (Dashboard API).

```graphql
type DashboardPageList {
  pages: [PageSummary!]!
  total: Int!
  page: Int!
  pageSize: Int!
  totalPages: Int!
  hasNext: Boolean!
  hasPrevious: Boolean!
}
```

**Fields:**

- `pages` ([PageSummary!]!): List of page summaries
- `total` (Int!): Total count
- `page` (Int!): Current page (1-based)
- `pageSize` (Int!): Items per page
- `totalPages` (Int!): Total pages
- `hasNext` (Boolean!): Whether there is a next page
- `hasPrevious` (Boolean!): Whether there is a previous page

## Queries

### page

Get a page by page_id.

**Parameters:**

| Name     | Type   | Required | Description                                      |
|----------|--------|----------|--------------------------------------------------|
| pageId   | String!| Yes      | Page ID (max 255 chars)                          |
| pageType | String | No       | Optional filter: docs, marketing, or dashboard   |

```graphql
query GetPage($pageId: String!, $pageType: String) {
  pages {
    page(pageId: $pageId, pageType: $pageType) {
      pageId
      title
      pageType
      description
      contentUrl
      route
      status
      version
      category
      updatedAt
    }
  }
}
```

**Arguments:**

- `pageId` (String!): Page ID (required, non-empty string, max 255 characters)
- `pageType` (String): Optional page type filter (`docs`, `marketing`, or `dashboard`)

**Returns:** `PageDetail`

**Authentication:** Not required (public endpoint)

**Validation:**

- `pageId`: Required, non-empty string, max 255 characters
- `pageType`: If provided, must be one of `docs`, `marketing`, or `dashboard`

**Example Response:**

```json
{
  "data": {
    "pages": {
      "page": {
        "pageId": "getting-started",
        "title": "Getting Started Guide",
        "pageType": "docs",
        "description": "Quick start guide for new users",
        "contentUrl": "https://s3.amazonaws.com/bucket/pages/getting-started.md?...",
        "route": "/docs/getting-started",
        "status": "published",
        "version": 3,
        "category": "guides",
        "updatedAt": "2024-01-15T10:30:00Z"
      }
    }
  }
}
```

### pages

List all pages with optional filtering.

**Parameters:**

| Name           | Type    | Required | Description                          |
|----------------|---------|----------|--------------------------------------|
| pageType       | String  | No       | docs, marketing, or dashboard         |
| includeDrafts  | Boolean | No       | Include draft pages (default true)   |
| includeDeleted | Boolean | No       | Include deleted (default false)      |
| status         | String  | No       | draft, published, or deleted         |
| limit          | Int     | No       | Max results (default 100)            |
| offset         | Int     | No       | Skip (default 0)                     |

```graphql
query ListPages(
  $pageType: String
  $includeDrafts: Boolean
  $includeDeleted: Boolean
  $status: String
  $limit: Int
  $offset: Int
) {
  pages {
    pages(
      pageType: $pageType
      includeDrafts: $includeDrafts
      includeDeleted: $includeDeleted
      status: $status
      limit: $limit
      offset: $offset
    ) {
      pages {
        pageId
        title
        pageType
        route
        status
      }
      total
    }
  }
}
```

**Arguments:**

- `pageType` (String): Filter by page type (`docs`, `marketing`, or `dashboard`)
- `includeDrafts` (Boolean): Include draft pages (default: true)
- `includeDeleted` (Boolean): Include deleted pages (default: false)
- `status` (String): Filter by status (`draft`, `published`, or `deleted`)
- `limit` (Int): Maximum results (default: 100)
- `offset` (Int): Skip results (default: 0)

**Returns:** `PageList`

**Authentication:** Not required (public endpoint)

**Example Response:**

```json
{
  "data": {
    "pages": {
      "pages": {
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
        ],
        "total": 42
      }
    }
  }
}
```

### pageContent

Get page markdown content directly.

**Parameters:**

| Name   | Type    | Required | Description  |
|--------|---------|----------|--------------|
| pageId | String! | Yes      | Page ID      |

```graphql
query GetPageContent($pageId: String!) {
  pages {
    pageContent(pageId: $pageId) {
      pageId
      content
    }
  }
}
```

**Arguments:**

- `pageId` (String!): Page ID (required, non-empty string, max 255 characters)

**Returns:** `PageContent`

**Authentication:** Not required (public endpoint)

**Example Response:**

```json
{
  "data": {
    "pages": {
      "pageContent": {
        "pageId": "getting-started",
        "content": "# Getting Started\n\nWelcome to our documentation..."
      }
    }
  }
}
```

### pagesByType

List pages filtered by page type.

**Parameters:**

| Name           | Type    | Required | Description                        |
|----------------|---------|----------|------------------------------------|
| pageType       | String! | Yes      | docs, marketing, or dashboard      |
| includeDrafts  | Boolean | No       | Include drafts (default true)     |
| includeDeleted | Boolean | No       | Include deleted (default false)   |
| status         | String  | No       | draft, published, or deleted      |

```graphql
query GetPagesByType(
  $pageType: String!
  $includeDrafts: Boolean
  $includeDeleted: Boolean
  $status: String
) {
  pages {
    pagesByType(
      pageType: $pageType
      includeDrafts: $includeDrafts
      includeDeleted: $includeDeleted
      status: $status
    ) {
      pages {
        pageId
        title
        route
        status
      }
      total
    }
  }
}
```

**Arguments:**

- `pageType` (String!): Page type (`docs`, `marketing`, or `dashboard`) - required
- `includeDrafts` (Boolean): Include draft pages (default: true)
- `includeDeleted` (Boolean): Include deleted pages (default: false)
- `status` (String): Filter by status (`draft`, `published`, or `deleted`)

**Returns:** `PageList`

**Authentication:** Not required (public endpoint)

**Validation:**

- `pageType`: Required, must be one of `docs`, `marketing`, or `dashboard`

### pageTypes

List all page types with counts.

**Parameters:** None.

```graphql
query GetPageTypes {
  pages {
    pageTypes {
      types {
        type
        count
      }
      total
    }
  }
}
```

**Returns:** `PageTypeList`

**Authentication:** Not required (public endpoint)

**Example Response:**

```json
{
  "data": {
    "pages": {
      "pageTypes": {
        "types": [
          { "type": "docs", "count": 25 },
          { "type": "marketing", "count": 10 },
          { "type": "dashboard", "count": 7 }
        ],
        "total": 42
      }
    }
  }
}
```

### pageStatistics

Get statistics for a specific page type.

**Parameters:**

| Name     | Type   | Required | Description  |
|----------|--------|----------|--------------|
| pageType | String!| Yes      | docs, marketing, or dashboard |

```graphql
query GetPageStatistics($pageType: String!) {
  pages {
    pageStatistics(pageType: $pageType) {
      pageType
      total
      published
      draft
      deleted
      lastUpdated
    }
  }
}
```

**Arguments:**

- `pageType` (String!): Page type (`docs`, `marketing`, or `dashboard`) - required

**Returns:** `TypeStatistics`

**Authentication:** Not required (public endpoint)

**Example Response:**

```json
{
  "data": {
    "pages": {
      "pageStatistics": {
        "pageType": "docs",
        "total": 25,
        "published": 20,
        "draft": 4,
        "deleted": 1,
        "lastUpdated": "2024-01-15T10:30:00Z"
      }
    }
  }
}
```

### pagesByState

List pages filtered by state (draft, published, deleted).

**Parameters:**

| Name  | Type   | Required | Description                    |
|-------|--------|----------|--------------------------------|
| state | String!| Yes      | One of draft, published, deleted |

```graphql
query PagesByState($state: String!) {
  pages {
    pagesByState(state: $state) {
      pages { pageId title pageType route status }
      total
    }
  }
}
```

**Arguments:** `state` (String!): One of `draft`, `published`, `deleted`

**Returns:** `PageList` · **Auth:** Not required

### pagesByStateCount

Count pages by state.

**Parameters:**

| Name  | Type   | Required | Description                    |
|-------|--------|----------|--------------------------------|
| state | String!| Yes      | One of draft, published, deleted |

```graphql
query PagesByStateCount($state: String!) {
  pages {
    pagesByStateCount(state: $state)
  }
}
```

**Arguments:** `state` (String!): One of `draft`, `published`, `deleted`

**Returns:** `Int` · **Auth:** Not required

### pagesByUserType

List pages accessible by user type (e.g. developer, admin).

**Parameters:**

| Name     | Type   | Required | Description  |
|----------|--------|----------|--------------|
| userType | String!| Yes      | User type    |

```graphql
query PagesByUserType($userType: String!) {
  pages {
    pagesByUserType(userType: $userType) {
      pages { pageId title pageType route status }
      total
    }
  }
}
```

**Arguments:** `userType` (String!): User type

**Returns:** `PageList` · **Auth:** Not required

### pagesByDocsaiUserType

List pages by DocsAI user type, optionally filtered by page type. Maps to DocsAI `GET /api/v1/pages/{user_type}/?page_type=...`.

**Parameters:**

| Name     | Type   | Required | Description                                      |
|----------|--------|----------|--------------------------------------------------|
| userType | String!| Yes      | super_admin, admin, pro_user, free_user, guest  |
| pageType | String | No       | docs, marketing, or dashboard                    |

```graphql
query PagesByDocsaiUserType($userType: String!, $pageType: String) {
  pages {
    pagesByDocsaiUserType(userType: $userType, pageType: $pageType) {
      pages { pageId title pageType route status }
      total
    }
  }
}
```

**Arguments:**

- `userType` (String!): DocsAI user type — one of `super_admin`, `admin`, `pro_user`, `free_user`, `guest`
- `pageType` (String): Optional filter — one of `docs`, `marketing`, or `dashboard`

**Returns:** `PageList`

**Authentication:** Not required (public endpoint)

**Validation:**

- `userType`: Required, must be one of `super_admin`, `admin`, `pro_user`, `free_user`, `guest`
- `pageType`: If provided, must be one of `docs`, `marketing`, or `dashboard`

### myPages

Pages for the current authenticated user, mapped to DocsAI user type from profile role, optionally filtered by page type. Requires authentication.

**Parameters:**

| Name     | Type   | Required | Description  |
|----------|--------|----------|--------------|
| pageType | String | No       | docs, marketing, or dashboard |

```graphql
query MyPages($pageType: String) {
  pages {
    myPages(pageType: $pageType) {
      pages { pageId title pageType route status }
      total
    }
  }
}
```

**Arguments:**

- `pageType` (String): Optional filter — one of `docs`, `marketing`, or `dashboard`

**Returns:** `PageList`

**Authentication:** Required. Uses current user's role mapped to DocsAI user type (e.g. SuperAdmin → `super_admin`, Admin → `admin`, ProUser → `pro_user`, FreeUser → `free_user`, Member → `guest`).

**Validation:**

- `pageType`: If provided, must be one of `docs`, `marketing`, or `dashboard`

### pageAccessControl

Get page access control. Returns raw JSON from DocsAI API.

**Parameters:**

| Name   | Type   | Required | Description  |
|--------|--------|----------|--------------|
| pageId | String!| Yes      | Page ID      |

```graphql
query PageAccessControl($pageId: String!) {
  pages {
    pageAccessControl(pageId: $pageId)
  }
}
```

**Arguments:** `pageId` (String!) · **Returns:** `JSON` · **Auth:** Not required

### pageSections

Get page sections. Returns raw JSON.

**Parameters:**

| Name   | Type   | Required | Description  |
|--------|--------|----------|--------------|
| pageId | String!| Yes      | Page ID      |

```graphql
query PageSections($pageId: String!) {
  pages {
    pageSections(pageId: $pageId)
  }
}
```

**Arguments:** `pageId` (String!) · **Returns:** `JSON` · **Auth:** Not required

### pageComponents

Get page components. Returns raw JSON.

**Parameters:**

| Name   | Type   | Required | Description  |
|--------|--------|----------|--------------|
| pageId | String!| Yes      | Page ID      |

```graphql
query PageComponents($pageId: String!) {
  pages {
    pageComponents(pageId: $pageId)
  }
}
```

**Arguments:** `pageId` (String!) · **Returns:** `JSON` · **Auth:** Not required

### pageEndpoints

Get endpoints used by page. Returns raw JSON.

**Parameters:**

| Name   | Type   | Required | Description  |
|--------|--------|----------|--------------|
| pageId | String!| Yes      | Page ID      |

```graphql
query PageEndpoints($pageId: String!) {
  pages {
    pageEndpoints(pageId: $pageId)
  }
}
```

**Arguments:** `pageId` (String!) · **Returns:** `JSON` · **Auth:** Not required

### pageVersions

Get page versions. Returns raw JSON.

**Parameters:**

| Name   | Type   | Required | Description  |
|--------|--------|----------|--------------|
| pageId | String!| Yes      | Page ID      |

```graphql
query PageVersions($pageId: String!) {
  pages {
    pageVersions(pageId: $pageId)
  }
}
```

**Arguments:** `pageId` (String!) · **Returns:** `JSON` · **Auth:** Not required

### dashboardPages

Get dashboard pages (paginated). Uses DocsAI Dashboard API.

**Parameters:**

| Name     | Type   | Required | Description        |
|----------|--------|----------|--------------------|
| page     | Int    | No       | Page number (default 1) |
| pageSize | Int    | No       | Page size (default 20) |
| pageType | String | No       | Filter by type     |
| status   | String | No       | Filter by status   |
| search   | String | No       | Search term        |

```graphql
query DashboardPages($page: Int, $pageSize: Int, $pageType: String, $status: String, $search: String) {
  pages {
    dashboardPages(page: $page, pageSize: $pageSize, pageType: $pageType, status: $status, search: $search) {
      pages { pageId title pageType route status }
      total
      page
      pageSize
      totalPages
      hasNext
      hasPrevious
    }
  }
}
```

**Arguments:** `page` (default 1), `pageSize` (default 20), `pageType`, `status`, `search`

**Returns:** `DashboardPageList` · **Auth:** Not required

### marketingPages

Get marketing pages (paginated). Like `dashboardPages` but scoped to `page_type=marketing`. Uses DocsAI Dashboard API.

**Parameters:**

| Name     | Type   | Required | Description        |
|----------|--------|----------|--------------------|
| page     | Int    | No       | Page number (default 1) |
| pageSize | Int    | No       | Page size (default 20) |
| status   | String | No       | Filter by status   |
| search   | String | No       | Search term        |

```graphql
query MarketingPages($page: Int, $pageSize: Int, $status: String, $search: String) {
  pages {
    marketingPages(page: $page, pageSize: $pageSize, status: $status, search: $search) {
      pages { pageId title pageType route status }
      total
      page
      pageSize
      totalPages
      hasNext
      hasPrevious
    }
  }
}
```

**Arguments:** `page` (default 1), `pageSize` (default 20), `status`, `search`

**Returns:** `DashboardPageList` · **Auth:** Not required

## Integration with Authentication

Pages are automatically included in the authentication response based on user role. When users login, register, or refresh their token, the accessible pages are returned in the `pages` field of `AuthPayload`.

### Role-Based Page Access

| Role | Pages Accessible |
|------|-----------------|
| Admin/Owner/SuperAdmin | All pages (including drafts) |
| Member/Pro/ProUser | Docs + Marketing pages (published only) |
| Free/Guest | Published docs only |

### Login with Pages Example

```graphql
mutation Login($input: LoginInput!) {
  auth {
    login(input: $input) {
      accessToken
      refreshToken
      user {
        uuid
        email
        name
      }
      pages {
        pageId
        title
        pageType
        route
        status
      }
    }
  }
}
```

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
          "name": "John Doe"
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
          },
          {
            "pageId": "pricing",
            "title": "Pricing",
            "pageType": "marketing",
            "route": "/pricing",
            "status": "published"
          }
        ]
      }
    }
  }
}
```

## Error Handling

The Pages module implements comprehensive error handling with input validation, service error handling, and response validation.

### Error Types

The Pages module may raise the following errors:

- **NotFoundError** (404): Page not found
  - Code: `NOT_FOUND`
  - Extensions: `resourceType: "Page"`, `identifier: <page_id>`
  - Occurs when: Requested page ID does not exist
- **ValidationError** (422): Input validation failed
  - Code: `VALIDATION_ERROR`
  - Extensions: `fieldErrors` (field-specific errors)
  - Occurs when: Invalid page ID, invalid page type, or invalid status
- **BadRequestError** (400): Invalid request data
  - Code: `BAD_REQUEST`
  - Occurs when: Response format is invalid
- **ServiceUnavailableError** (503): Pages service unavailable
  - Code: `SERVICE_UNAVAILABLE`
  - Extensions: `serviceName: "Pages"`
  - Occurs when: DocsAI API is unavailable

### Error Response Examples

**Example: Page Not Found**

```json
{
  "errors": [
    {
      "message": "Page with identifier 'nonexistent-page' not found",
      "extensions": {
        "code": "NOT_FOUND",
        "statusCode": 404,
        "resourceType": "Page",
        "identifier": "nonexistent-page"
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
      "message": "page_type must be one of 'docs', 'marketing', or 'dashboard'",
      "extensions": {
        "code": "VALIDATION_ERROR",
        "statusCode": 422
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
      "message": "Pages service error. Please try again later.",
      "extensions": {
        "code": "SERVICE_UNAVAILABLE",
        "statusCode": 503,
        "serviceName": "Pages"
      }
    }
  ]
}
```

## Usage Examples

### Complete Pages Flow

```graphql
# 1. List all published docs pages
query ListDocsPages {
  pages {
    pagesByType(pageType: "docs", status: "published") {
      pages {
        pageId
        title
        route
      }
      total
    }
  }
}

# 2. Get specific page details
query GetPageDetails {
  pages {
    page(pageId: "getting-started") {
      pageId
      title
      description
      contentUrl
      status
      version
    }
  }
}

# 3. Get page content
query GetContent {
  pages {
    pageContent(pageId: "getting-started") {
      pageId
      content
    }
  }
}

# 4. Get page types with counts
query GetTypes {
  pages {
    pageTypes {
      types {
        type
        count
      }
      total
    }
  }
}

# 5. Get statistics for docs pages
query GetDocsStats {
  pages {
    pageStatistics(pageType: "docs") {
      pageType
      total
      published
      draft
    }
  }
}
```

### Filter Pages by Status

```graphql
# Get only published pages
query PublishedPages {
  pages {
    pages(status: "published", includeDrafts: false) {
      pages { pageId title pageType }
      total
    }
  }
}

# Get only draft pages (requires higher privileges)
query DraftPages {
  pages {
    pages(status: "draft") {
      pages { pageId title pageType }
      total
    }
  }
}
```

## Implementation Details

### PagesService Integration

- **PagesService**: All page operations are handled via `PagesService`
  - `get_page_by_id`, `list_pages`, `get_page_content`, `get_pages_by_type`, `count_pages_by_type`, `get_type_statistics`, `get_pages_for_user`
  - **By state:** `list_pages_by_state`, `count_pages_by_state`
  - **By user type:** `list_pages_by_user_type`
  - **Sub-resources:** `get_page_access_control`, `get_page_sections`, `get_page_components`, `get_page_endpoints`, `get_page_versions`
  - **Dashboard:** `get_dashboard_pages` (paginated)
  - **Marketing:** `marketingPages` GraphQL query reuses `get_dashboard_pages` with `page_type="marketing"`

### DocsAIPagesRepository Integration

- **DocsAIPagesRepository**: Data access layer for pages
  - Connects to DocsAI (Django) API via **DocsAIClient**
  - Handles page list, get, by-type, by-state, by user-type (with optional page_type), sub-resources, and dashboard
  - Response validation and error handling
  - Methods: `get_by_page_id`, `list_all`, `list_pages_by_user_type(user_type, page_type)`, etc.

### DocsAIClient Integration

- **DocsAIClient**: HTTP client for DocsAI API
  - Configurable base URL, API key, and timeout
  - **Pages:** list, get, by user_type (with optional page_type), dashboard
  - **By state:** list/count by state
  - **Sub-resources:** access control, sections, components, endpoints, versions
  - **Dashboard:** paginated dashboard/marketing pages

### Validation

- **Input Validation**: All inputs are validated before processing
  - `pageId`: Required, non-empty string, max 255 characters
  - `pageType`: Must be one of `docs`, `marketing`, or `dashboard`
  - `status`: Must be one of `draft`, `published`, or `deleted`
- **Response Validation**: All service responses are validated before conversion
  - Checks response structure matches expected format
  - Logs conversion errors but continues processing

### Error Handling

- **Input Validation**: All inputs validated with specific error messages
- **Service Errors**: Wrapped with ServiceUnavailableError for external failures
- **Response Validation**: Invalid responses logged and converted to BadRequestError
- **Non-Blocking Conversion**: Individual page conversion errors are logged but don't fail lists

### Page Structure

- **Page Types**: Three supported types
  - `docs`: Documentation pages
  - `marketing`: Marketing/promotional pages
  - `dashboard`: Dashboard/app pages
- **Page Status**: Three statuses
  - `draft`: Work in progress, not publicly visible
  - `published`: Live and publicly accessible
  - `deleted`: Soft-deleted, not visible

## Task breakdown (for maintainers)

1. **Data source:** All page data from DocsAI (PagesService); no local pages table; get_pages_for_docsai_user_type, get_page_by_id, etc.
2. **page/pages/pageContent:** DocsAI client calls; pageType = docs | marketing | dashboard; state = draft | published | deleted; document which queries require auth (myPages) vs public.
3. **pagesByDocsaiUserType:** Used by Auth module to return pages in login/register/refreshToken; user_type = super_admin | admin | pro_user | free_user | guest; include_drafts for admin/super_admin.
4. **dashboardPages/marketingPages:** Convenience queries for published pages by type; public.
5. **pageSections/pageComponents/pageEndpoints/pageVersions:** DocsAI-specific fields; document response shape and when null.

## Related Modules

- **Auth Module**: Pages are included in `AuthPayload` after login/register
- **Admin Module**: Admin-level page management operations
- **Users Module**: User roles determine page access
- **AI Chats Module** ([17_AI_CHATS_MODULE.md](17_AI_CHATS_MODULE.md)): product/docs pages (DocsAI) are separate from the Contact AI REST microservice

## Documentation metadata

- Era: `9.x`
- Introduced in: `TBD` (fill with exact minor)
- Frontend bindings: list page files from `docs/frontend/pages/*.json`
- Data stores touched: PostgreSQL/Elasticsearch/MongoDB/S3 as applicable

## Endpoint/version binding checklist

- Add operation list with `introduced_in` / `deprecated_in` tags.
- Map each operation to frontend page bindings and hook/service usage.
- Record DB tables read/write for each operation.

