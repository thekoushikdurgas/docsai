# LinkedIn Module

## Overview

The LinkedIn module provides LinkedIn URL search and export functionality. It allows users to search for contacts and companies by LinkedIn URLs and export results to CSV.
**Location:** `app/graphql/modules/linkedin/`

## Mutations – parameters and variable types

| Mutation | Parameter(s) | Variable type (GraphQL) | Return type |
|----------|---------------|-------------------------|-------------|
| `search` | `input` | LinkedInSearchInput! | `LinkedInSearchResponse` |
| `upsertByLinkedInUrl` | `input` | LinkedInUpsertInput! | upsert result |

No queries under root `linkedin` (search/export are mutations). Use camelCase in variables. 1 credit per URL for FreeUser/ProUser; validate_linkedin_url. See Input Types for LinkedInSearchInput and LinkedInUpsertInput fields.

## Types

### LinkedInSearchResponse

Response from LinkedIn URL search.

```graphql
type LinkedInSearchResponse {
  contacts: [ContactWithRelations!]!
  companies: [CompanyWithRelations!]!
  totalContacts: Int!
  totalCompanies: Int!
}
```

### LinkedInExportResponse

Response from LinkedIn export with separate contact and company exports.

```graphql
type LinkedInExportResponse {
  contactExport: ExportResponse
  companyExport: ExportResponse
  totalUrls: Int!
  contactUrlsCount: Int!
  companyUrlsCount: Int!
  unmatchedUrlsCount: Int!
}
```

**Fields:**

- `contactExport` (ExportResponse): Export response for contacts matching LinkedIn URLs (null if no contacts matched)
- `companyExport` (ExportResponse): Export response for companies matching LinkedIn URLs (null if no companies matched)
- `totalUrls` (Int!): Total number of LinkedIn URLs processed
- `contactUrlsCount` (Int!): Number of URLs that matched contacts (currently returns 0, will be calculated in future)
- `companyUrlsCount` (Int!): Number of URLs that matched companies (currently returns 0, will be calculated in future)
- `unmatchedUrlsCount` (Int!): Number of URLs that matched neither contacts nor companies (currently returns 0, will be calculated in future)

### ContactWithRelations

Contact with its metadata and related company data.

```graphql
type ContactWithRelations {
  contact: ContactBasic!
  metadata: ContactMetadataBasic
  company: CompanyBasic
  companyMetadata: CompanyMetadataBasic
}
```

### CompanyWithRelations

Company with its metadata and related contacts.

```graphql
type CompanyWithRelations {
  company: CompanyBasic!
  metadata: CompanyMetadataBasic
  contacts: [ContactWithRelations!]!
}
```

### ContactBasic

Basic contact information.

```graphql
type ContactBasic {
  uuid: ID!
  firstName: String
  lastName: String
  email: String
  title: String
  companyId: ID
  seniority: String
  departments: [String!]
  mobilePhone: String
  emailStatus: String
  createdAt: DateTime
  updatedAt: DateTime
}
```

### ContactMetadataBasic

Contact metadata information.

```graphql
type ContactMetadataBasic {
  uuid: ID!
  linkedinUrl: String
  linkedinSalesUrl: String
  facebookUrl: String
  twitterUrl: String
  website: String
  workDirectPhone: String
  homePhone: String
  otherPhone: String
  city: String
  state: String
  country: String
  stage: String
}
```

### CompanyBasic

Basic company information.

```graphql
type CompanyBasic {
  uuid: ID!
  name: String
  employeesCount: Int
  industries: [String!]
  keywords: [String!]
  address: String
  annualRevenue: Int
  totalFunding: Int
  technologies: [String!]
  createdAt: DateTime
  updatedAt: DateTime
}
```

### CompanyMetadataBasic

Company metadata information.

```graphql
type CompanyMetadataBasic {
  uuid: ID!
  linkedinUrl: String
  linkedinSalesUrl: String
  facebookUrl: String
  twitterUrl: String
  website: String
  companyNameForEmails: String
  phoneNumber: String
  latestFunding: String
  latestFundingAmount: Int
  lastRaisedAt: DateTime
  city: String
  state: String
  country: String
}
```

## Mutations

### search

Search for contacts and companies by LinkedIn URL.

**Parameters:**

| Name  | Type                 | Required | Description        |
|-------|----------------------|----------|--------------------|
| input | LinkedInSearchInput! | Yes      | url (LinkedIn URL)  |

```graphql
mutation SearchLinkedIn($input: LinkedInSearchInput!) {
  linkedin {
    search(input: $input) {
      contacts {
        contact {
          uuid
          firstName
          lastName
          email
          title
        }
        metadata {
          linkedinUrl
          city
          country
        }
        company {
          name
          employeesCount
        }
      }
      companies {
        company {
          uuid
          name
          employeesCount
        }
        metadata {
          linkedinUrl
          website
        }
      }
      totalContacts
      totalCompanies
    }
  }
}
```

**Variables:**
```json
{
  "input": {
    "url": "https://www.linkedin.com/in/johndoe"
  }
}
```

**Input:** `LinkedInSearchInput!`

**Returns:** `LinkedInSearchResponse`

**Authentication:** Required

**Credits:** 1 credit per search (FreeUser/ProUser only)

**Example Response:**
```json
{
  "data": {
    "linkedin": {
      "search": {
        "contacts": [
          {
            "contact": {
              "uuid": "123e4567-e89b-12d3-a456-426614174000",
              "firstName": "John",
              "lastName": "Doe",
              "email": "john.doe@example.com",
              "title": "VP Engineering"
            },
            "metadata": {
              "linkedinUrl": "https://www.linkedin.com/in/johndoe",
              "city": "San Francisco",
              "country": "United States"
            },
            "company": {
              "name": "Acme Corporation",
              "employeesCount": 500
            }
          }
        ],
        "companies": [],
        "totalContacts": 1,
        "totalCompanies": 0
      }
    }
  }
}
```

### upsertByLinkedInUrl

Create or update a contact and/or company by LinkedIn URL.

This mutation allows for creating new contacts/companies or updating existing ones based on a LinkedIn URL. It supports providing partial data for both contact and company.

**Parameters:**

| Name  | Type                   | Required | Description                          |
|-------|------------------------|----------|--------------------------------------|
| input | LinkedInUpsertInput!   | Yes      | url, contactData, companyData, etc.  |

```graphql
mutation UpsertByLinkedInUrl($input: LinkedInUpsertInput!) {
  linkedin {
    upsertByLinkedInUrl(input: $input) {
      success
      created
      contact {
        uuid
        firstName
        lastName
        email
        title
      }
      company {
        uuid
        name
        employeesCount
      }
      errors
    }
  }
}
```

**Variables:**
```json
{
  "input": {
    "url": "https://www.linkedin.com/in/johndoe",
    "contactData": {
      "firstName": "John",
      "lastName": "Doe",
      "email": "john.doe@example.com"
    },
    "contactMetadata": {
      "city": "San Francisco",
      "state": "CA",
      "country": "United States"
    },
    "companyData": {
      "name": "Acme Corporation"
    }
  }
}
```

**Input:** `LinkedInUpsertInput!`

**Returns:** `LinkedInUpsertResponse`

**Authentication:** Required

**Credits:** 1 credit per upsert operation (FreeUser/ProUser only)

**Example Response:**
```json
{
  "data": {
    "linkedin": {
      "upsertByLinkedInUrl": {
        "success": true,
        "created": true,
        "contact": {
          "uuid": "123e4567-e89b-12d3-a456-426614174000",
          "firstName": "John",
          "lastName": "Doe",
          "email": "john.doe@example.com",
          "title": "VP Engineering"
        },
        "company": {
          "uuid": "456e7890-e89b-12d3-a456-426614174001",
          "name": "Acme Corporation",
          "employeesCount": 500
        },
        "errors": []
      }
    }
  }
}
```

### exportLinkedInResults

Export contacts and companies by multiple LinkedIn URLs.

**Parameters:**

| Name  | Type                   | Required | Description        |
|-------|------------------------|----------|--------------------|
| input | LinkedInExportInput!   | Yes      | urls (list of LinkedIn URLs) |

```graphql
mutation ExportLinkedIn($input: LinkedInExportInput!) {
  linkedin {
    exportLinkedInResults(input: $input) {
      exportId
      downloadUrl
      expiresAt
      contactCount
      companyCount
      status
    }
  }
}
```

**Variables:**
```json
{
  "input": {
    "urls": [
      "https://www.linkedin.com/in/johndoe",
      "https://www.linkedin.com/in/janesmith",
      "https://www.linkedin.com/company/acme-corp"
    ]
  }
}
```

**Input:** `LinkedInExportInput!`

**Returns:** `LinkedInExportResponse`

**Authentication:** Required

**Credits:** 1 credit per LinkedIn URL (FreeUser/ProUser only)

**Example Response:**
```json
{
  "data": {
    "linkedin": {
      "exportLinkedInResults": {
        "contactExport": {
          "exportId": "exp_contact_123456",
          "downloadUrl": "https://s3.amazonaws.com/bucket/exports/exp_contact_123456.csv",
          "expiresAt": "2024-01-20T10:30:00Z",
          "contactCount": 2,
          "companyCount": 0,
          "status": "pending"
        },
        "companyExport": {
          "exportId": "exp_company_123456",
          "downloadUrl": "https://s3.amazonaws.com/bucket/exports/exp_company_123456.csv",
          "expiresAt": "2024-01-20T10:30:00Z",
          "contactCount": 0,
          "companyCount": 1,
          "status": "pending"
        },
        "totalUrls": 3,
        "contactUrlsCount": 2,
        "companyUrlsCount": 1,
        "unmatchedUrlsCount": 0
      }
    }
  }
}
```

## Input Types

### LinkedInSearchInput

Input for LinkedIn URL search.

```graphql
input LinkedInSearchInput {
  url: String!
}
```

**Validation:**
- URL is required and cannot be empty
- URL must be a valid LinkedIn URL format:
  - Must start with one of: `https://www.linkedin.com/`, `http://www.linkedin.com/`, `https://linkedin.com/`, or `http://linkedin.com/`
  - Maximum length: 2048 characters (validated in LinkedInService)
  - Note: ConnectraClient validates max 500 characters, but LinkedInService allows up to 2048 characters

### LinkedInUpsertInput

Input for LinkedIn URL upsert (create or update).

```graphql
input LinkedInUpsertInput {
  url: String!
  contactData: JSON
  contactMetadata: JSON
  companyData: JSON
  companyMetadata: JSON
}
```

**Validation:**
- URL is required and cannot be empty
- URL must be a valid LinkedIn URL (must contain "linkedin.com")
- At least one of `contactData`, `contactMetadata`, `companyData`, or `companyMetadata` must be provided
- `contactData` and `contactMetadata` must be dictionaries if provided
- `companyData` and `companyMetadata` must be dictionaries if provided

**Fields:**
- `url` (String!): LinkedIn URL (required)
- `contactData` (JSON, optional): Contact data to merge/create
- `contactMetadata` (JSON, optional): Contact metadata to merge/create
- `companyData` (JSON, optional): Company data to merge/create
- `companyMetadata` (JSON, optional): Company metadata to merge/create

### LinkedInUpsertResponse

Response from LinkedIn URL upsert operation.

```graphql
type LinkedInUpsertResponse {
  success: Boolean!
  created: Boolean!
  contact: Contact
  company: Company
  errors: [String!]!
}
```

**Fields:**
- `success` (Boolean!): Whether the operation was successful
- `created` (Boolean!): Whether a new record was created (true) or existing record was updated (false)
- `contact` (Contact, optional): Created/updated contact (if contact data was provided)
- `company` (Company, optional): Created/updated company (if company data was provided)
- `errors` ([String!]!): Array of error messages (if any)

### LinkedInExportInput

Input for LinkedIn export by multiple URLs.

```graphql
input LinkedInExportInput {
  urls: [String!]!
}
```

**Validation:**
- At least one LinkedIn URL is required (non-empty list)
- All URLs must be valid LinkedIn URLs:
  - Must start with one of: `https://www.linkedin.com/`, `http://www.linkedin.com/`, `https://linkedin.com/`, or `http://linkedin.com/`
  - Maximum length: 2048 characters per URL
  - Each URL is validated individually

## Error Handling

The LinkedIn module implements comprehensive error handling with input validation, external service error handling, and response validation.

### Error Types

The LinkedIn module may raise the following errors:

- **ValidationError** (422): Input validation failed
  - Code: `VALIDATION_ERROR`
  - Extensions: `fieldErrors` (field-specific errors)
  - Occurs when: 
    - Empty URL or empty URL list
    - Invalid LinkedIn URL format (must start with `https://www.linkedin.com/`, `http://www.linkedin.com/`, `https://linkedin.com/`, or `http://linkedin.com/`)
    - URL exceeds maximum length (2048 characters)
    - URL list is empty or contains invalid URLs
- **BadRequestError** (400): Invalid request data
  - Code: `BAD_REQUEST`
  - Occurs when: Request format is invalid or required parameters are missing
- **ServiceUnavailableError** (503): LinkedIn service unavailable
  - Code: `SERVICE_UNAVAILABLE`
  - Extensions: `serviceName: "linkedin"`
  - Occurs when: LinkedIn service is down, timeout occurs, or connection fails

### Error Response Examples

**Example: Validation Error - Invalid URL Format**
```json
{
  "errors": [
    {
      "message": "Invalid LinkedIn URL",
      "extensions": {
        "code": "VALIDATION_ERROR",
        "statusCode": 422,
        "fieldErrors": {
          "url": ["URL must start with https://www.linkedin.com/, http://www.linkedin.com/, https://linkedin.com/, or http://linkedin.com/"]
        }
      }
    }
  ]
}
```

**Example: Validation Error - Empty URL List**
```json
{
  "errors": [
    {
      "message": "Validation failed",
      "extensions": {
        "code": "VALIDATION_ERROR",
        "statusCode": 422,
        "fieldErrors": {
          "urls": ["At least one LinkedIn URL is required"]
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
      "message": "LinkedIn service temporarily unavailable. Please try again later.",
      "extensions": {
        "code": "SERVICE_UNAVAILABLE",
        "statusCode": 503,
        "serviceName": "linkedin"
      }
    }
  ]
}
```

### Error Handling Patterns

- **Input Validation**: LinkedIn URLs are validated for format and domain before processing
- **External Service Errors**: LinkedIn service errors are caught and converted to appropriate GraphQL errors
- **Export Job Errors**: Export job creation errors are handled gracefully
- **Response Validation**: Search results and export responses are validated before returning
- **Error Logging**: Comprehensive error logging with context for debugging

## Usage Examples

### Complete LinkedIn Operations Flow

```graphql
# 1. Search by LinkedIn URL
mutation Search {
  linkedin {
    search(input: {
      url: "https://www.linkedin.com/in/johndoe"
    }) {
      contacts {
        contact {
          uuid
          firstName
          lastName
          email
          title
        }
        metadata {
          linkedinUrl
          city
          country
        }
        company {
          name
          employeesCount
        }
      }
      totalContacts
    }
  }
}

# 2. Export multiple LinkedIn URLs
mutation Export {
  linkedin {
    exportLinkedInResults(input: {
      urls: [
        "https://www.linkedin.com/in/johndoe",
        "https://www.linkedin.com/in/janesmith",
        "https://www.linkedin.com/company/acme-corp"
      ]
    }) {
      contactExport {
        exportId
        downloadUrl
        expiresAt
        contactCount
        companyCount
        status
      }
      companyExport {
        exportId
        downloadUrl
        expiresAt
        contactCount
        companyCount
        status
      }
      totalUrls
      contactUrlsCount
      companyUrlsCount
      unmatchedUrlsCount
    }
  }
}

```

## Implementation Details

### LinkedIn Service

- **LinkedInService**: LinkedIn operations are handled by `LinkedInService` which coordinates with ConnectraClient
- **URL Validation**: URLs are validated using `validate_linkedin_url` / `validate_linkedin_urls` from `app.utils.validation`
  - Validates URL format (must start with linkedin.com domain patterns)
  - Validates URL length (max 2048 characters)
  - For batch operations: `validate_linkedin_urls` validates list is non-empty (max 10000 URLs)

### Search Operations

- **URL Search**: Searches both person LinkedIn URLs (`/in/`) and company LinkedIn URLs (`/company/`)
- **VQL Query Building**: Uses ConnectraClient to construct and execute VQL queries
  - Builds queries to search contacts by `linkedin_url` field
  - Builds queries to search companies by company metadata `linkedin_url` field
  - Handles both person and company URL patterns
- **Contact Matching**: Matches LinkedIn URLs to contacts via `linkedin_url` field in contact metadata
- **Company Matching**: Matches LinkedIn URLs to companies via company metadata `linkedin_url` field
- **Search Results**: Returns contacts and companies with their related metadata and relationships

### Credit Management

- **Credit Deduction**: Credits are deducted after successful operations (FreeUser/ProUser only)
  - **Non-Blocking**: Credit deduction is non-blocking - if credit deduction fails, the operation still succeeds
  - Credit deduction errors are logged but do not affect the search/export operation
  - 1 credit per LinkedIn URL search
  - 1 credit per LinkedIn URL searched
- **Activity Logging**: LinkedIn operations are logged for activity tracking
  - **Non-Blocking**: Activity logging is non-blocking - if logging fails, the operation still succeeds
  - Activity logging errors are logged but do not affect the operation
  - Logs include: operation type, URLs processed, result counts

### Error Handling

- **Input Validation**: LinkedIn URLs are validated for format and domain before processing
- **External Service Errors**: Connectra API errors are caught and converted to appropriate GraphQL errors
- **Response Validation**: Search results are validated before returning
- **Error Logging**: Comprehensive error logging with context (user UUID, URLs, operation type) for debugging

## Task breakdown (for maintainers)

1. **search:** LinkedInSearchInput (e.g. LinkedIn URLs); validate_linkedin_url(s); call LinkedIn service; return contacts/companies; credit deduction and LINKEDIN usage tracking.
2. **upsertByLinkedInUrl:** LinkedInUpsertInput; upsert contacts/companies to Connectra (or local); validate URLs; activity logging; document response shape.
3. **Credit/usage:** Confirm 1 credit per URL and UsageService.track_usage(LINKEDIN); SuperAdmin/Admin unlimited.
4. **Error handling:** External service errors; invalid URL validation (field-level error); document LinkedIn service URL and timeout.

## Related Modules

- **Contacts Module**: Provides contact data for LinkedIn search results
- **Companies Module**: Provides company data for LinkedIn search results
- **Usage Module**: Tracks LinkedIn feature usage
- **AI Chats Module** ([17_AI_CHATS_MODULE.md](17_AI_CHATS_MODULE.md)): different flow — AI chat may return `ContactInMessage` from Connectra-backed search, not the LinkedIn URL search service

## Documentation metadata

- Era: `4.x`
- Introduced in: `TBD` (fill with exact minor)
- Frontend bindings: list page files from `docs/frontend/pages/*.json`
- Data stores touched: PostgreSQL/Elasticsearch/MongoDB/S3 as applicable

## Endpoint/version binding checklist

- Add operation list with `introduced_in` / `deprecated_in` tags.
- Map each operation to frontend page bindings and hook/service usage.
- Record DB tables read/write for each operation.

