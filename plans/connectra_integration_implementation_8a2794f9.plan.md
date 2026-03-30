---
name: Connectra Integration Implementation
overview: Complete integration of Connectra API into Appointment360 GraphQL backend, fixing endpoint paths, implementing VQL query conversion, enabling full CRUD operations via batch-upsert, and adding common API features.
todos:
  - id: vql-converter-create
    content: Create VQL converter utility module (appointment360/app/utils/vql_converter.py) with field type mappings, operator conversion, and nested filter support
    status: pending
  - id: fix-client-endpoints
    content: "Fix ConnectraClient endpoint paths: /vql/contacts → /contacts, /vql/companies → /companies, and their count variants"
    status: pending
  - id: fix-response-parsing
    content: "Fix ConnectraClient response parsing to extract data/count from {success: true, data: [...]} format and handle error responses"
    status: pending
    dependencies:
      - fix-client-endpoints
  - id: update-contact-queries
    content: Update contact query resolvers (contact, contacts, contactCount, contactQuery) to use VQL converter and remove deprecated _convert_filter_input method
    status: pending
    dependencies:
      - vql-converter-create
      - fix-response-parsing
  - id: update-company-queries
    content: Update company query resolvers (company, companies, companyQuery, companyContacts) to use VQL converter and remove deprecated _convert_filter_input method
    status: pending
    dependencies:
      - vql-converter-create
      - fix-response-parsing
  - id: add-batch-upsert-methods
    content: Add batch_upsert_contacts, batch_upsert_companies, and batch_upsert_common methods to ConnectraClient with batch size validation
    status: pending
    dependencies:
      - fix-response-parsing
  - id: create-data-mappers
    content: Create connectra_mappers.py utility with functions to map GraphQL input types (CreateContactInput, UpdateContactInput, etc.) to Connectra format
    status: pending
  - id: implement-contact-mutations
    content: Implement createContact, updateContact, batchCreateContacts mutations using batch upsert methods and data mappers
    status: pending
    dependencies:
      - add-batch-upsert-methods
      - create-data-mappers
  - id: implement-company-mutations
    content: Implement createCompany and updateCompany mutations using batch upsert methods and data mappers
    status: pending
    dependencies:
      - add-batch-upsert-methods
      - create-data-mappers
  - id: add-filter-metadata
    content: Add get_filters and get_filter_data methods to ConnectraClient and create common GraphQL module with filters and filterData queries
    status: pending
    dependencies:
      - fix-response-parsing
  - id: add-job-management
    content: Add create_job and list_jobs methods to ConnectraClient and create GraphQL mutations/queries for job management
    status: pending
    dependencies:
      - fix-response-parsing
  - id: enhance-vql-features
    content: Enhance VQL converter to support advanced text matching (fuzzy, slop), range queries, denormalized company fields, and cursor pagination
    status: pending
    dependencies:
      - vql-converter-create
  - id: add-error-handling
    content: Create connectra_errors.py utility to map Connectra error codes to GraphQL errors and create custom exceptions
    status: pending
  - id: add-validation
    content: Create connectra_validators.py utility to validate VQL queries, batch sizes, pagination, and mutation inputs
    status: pending
  - id: add-retry-logic
    content: Add retry logic to ConnectraClient using tenacity for transient failures and rate limiting with exponential backoff
    status: pending
    dependencies:
      - add-error-handling
  - id: unit-tests
    content: Create unit tests for VQL converter, ConnectraClient methods, and data mappers with >80% coverage
    status: pending
    dependencies:
      - vql-converter-create
      - add-batch-upsert-methods
      - create-data-mappers
  - id: integration-tests
    content: Create integration tests for GraphQL resolvers and end-to-end flows (create→read, update→read, filter→count)
    status: pending
    dependencies:
      - implement-contact-mutations
      - implement-company-mutations
  - id: documentation
    content: Update GraphQL API documentation, create Connectra integration guide, and update README with examples and troubleshooting
    status: pending
    dependencies:
      - enhance-vql-features
---

# Connectra Integration Implementation Plan

## Current State Analysis

**Critical Issues Identified:**

1. **Endpoint Mismatch**: Client uses `/vql/contacts` and `/vql/companies` but Connectra expects `/contacts` and `/companies`
2. **Query Format Mismatch**: GraphQL filters use custom format `{"filters": {"and": [...]}} `but Connectra requires VQL format `{"where": {"keyword_match": {...}}}`
3. **Response Format Mismatch**: Client expects `data` and `total` directly, but Connectra wraps in `{"success": true, "data": [...]}`
4. **Mutations Not Implemented**: All write operations raise `NotImplementedError`
5. **Missing Common APIs**: Filter metadata, job management, upload URLs not integrated

## Architecture Overview

```
GraphQL Request → Resolver → VQL Converter → ConnectraClient → Connectra API
                                    ↓
                            Data Mapper (for mutations)
```

## Implementation Phases

### Phase 1: Foundation - VQL Converter & Client Fixes (Critical)

**1.1 Create VQL Query Converter** (`appointment360/app/utils/vql_converter.py`)

- Convert GraphQL `VQLQueryInput` to Connectra VQL format
- Map operators: `eq/in` → `keyword_match`, `contains` → `text_matches`, `gte/lte` → `range_query`
- Support nested AND/OR logic from `VQLFilterInput`
- Handle field type detection (text, keyword, range, denormalized company fields)
- Support pagination (`page`, `limit`, `cursor`), sorting (`order_by`), and column selection (`select_columns`)
- Support `company_config` for contact queries with company population

**1.2 Fix ConnectraClient Endpoints** (`appointment360/app/clients/connectra_client.py`)

- Change `query_contacts()`: `/vql/contacts` → `/contacts`
- Change `query_companies()`: `/vql/companies` → `/companies`
- Change `count_contacts()`: `/vql/contacts/count` → `/contacts/count`
- Change `count_companies()`: `/vql/companies/count` → `/companies/count`
- Update `search_by_linkedin_url()` to use VQL format

**1.3 Fix Response Parsing** (`appointment360/app/clients/connectra_client.py`)

- Create `_parse_response()` helper to extract `data`/`count` from `{"success": true, "data": [...]}`
- Handle error responses: `{"success": false, "error": "ERR_CODE: message"}`
- Create custom exceptions: `ConnectraAPIError`, `ConnectraValidationError`, `ConnectraRateLimitError`
- Update all query methods to use parser

**1.4 Update Contact Query Resolvers** (`appointment360/app/graphql/modules/contacts/queries.py`)

- Import and use `convert_to_vql()` in all resolvers
- Update `contact()`, `contacts()`, `contactCount()`, `contactQuery()` to use VQL format
- Remove deprecated `_convert_filter_input()` method

**1.5 Update Company Query Resolvers** (`appointment360/app/graphql/modules/companies/queries.py`)

- Import and use `convert_to_vql()` in all resolvers
- Update `company()`, `companies()`, `companyQuery()`, `companyContacts()` to use VQL format
- Remove deprecated `_convert_filter_input()` method

### Phase 2: Write Operations - Mutations Implementation (High Priority)

**2.1 Add Batch Upsert Methods** (`appointment360/app/clients/connectra_client.py`)

- `batch_upsert_contacts(data: List[Dict]) `→ `POST /contacts/batch-upsert`
- `batch_upsert_companies(data: List[Dict]) `→ `POST /companies/batch-upsert`
- `batch_upsert_common(data: List[Dict]) `→ `POST /common/batch-upsert`
- Validate batch size (max 100), parse responses, handle errors

**2.2 Create Data Mapper Utilities** (`appointment360/app/utils/connectra_mappers.py` - new file)

- `map_create_contact_input()`: Convert `CreateContactInput` → Connectra format
- `map_update_contact_input()`: Convert `UpdateContactInput` with UUID
- `map_create_company_input()`: Convert `CreateCompanyInput` → Connectra format
- `map_update_company_input()`: Convert `UpdateCompanyInput` with UUID
- Handle field transformations: lowercase strings, `company_uuid` → `company_id`, array fields

**2.3 Implement Contact Mutations** (`appointment360/app/graphql/modules/contacts/mutations.py`)

- `createContact()`: Map input → batch upsert → fetch created contact
- `updateContact()`: Map input with UUID → batch upsert → fetch updated contact
- `batchCreateContacts()`: Map list → chunk (100 per batch) → batch upsert → fetch all
- `deleteContact()`: Document that Connectra doesn't support DELETE (return error or remove)

**2.4 Implement Company Mutations** (`appointment360/app/graphql/modules/companies/mutations.py`)

- `createCompany()`: Map input → batch upsert → fetch created company
- `updateCompany()`: Map input with UUID → batch upsert → fetch updated company
- `deleteCompany()`: Document that Connectra doesn't support DELETE (return error or remove)

### Phase 3: Common API Features (Medium Priority)

**3.1 Add Filter Metadata Methods** (`appointment360/app/clients/connectra_client.py`)

- `get_filters(service: str)` → `GET /common/:service/filters`
- `get_filter_data(service: str, filter_key: str, ...)` → `POST /common/:service/filters/data`

**3.2 Create Common GraphQL Module** (`appointment360/app/graphql/modules/common/` - new directory)

- Types: `Filter`, `FilterData`, `FilterConnection`
- Inputs: `FilterDataInput`
- Queries: `filters(service)`, `filterData(service, filterKey, ...)`
- Register in main schema

**3.3 Add Job Management Methods** (`appointment360/app/clients/connectra_client.py`)

- `create_job(job_type, job_data, retry_count)` → `POST /common/jobs/create`
- `list_jobs(filters)` → `POST /common/jobs`

**3.4 Create Job GraphQL Module** (`appointment360/app/graphql/modules/common/`)

- Types: `Job`, `JobConnection`
- Inputs: `CreateJobInput`, `JobFilterInput`
- Mutation: `createJob(input)`
- Query: `jobs(filters)`

**3.5 Add Upload URL Method** (`appointment360/app/clients/connectra_client.py`)

- `get_upload_url(filename)` → `GET /common/upload-url?filename=...`

### Phase 4: Advanced VQL Features (Medium Priority)

**4.1 Enhance Text Matching** (`appointment360/app/utils/vql_converter.py`)

- Support `exact`, `shuffle`, `substring` search types
- Auto-detect search type from operator (`contains` → `shuffle`, `exact` → `exact`)
- Support fuzzy matching for text searches
- Support `slop` parameter for phrase matching

**4.2 Enhance Range Queries** (`appointment360/app/utils/vql_converter.py`)

- Support all range operators: `gte`, `lte`, `gt`, `lt`
- Handle numeric and date ranges (ISO 8601 format)
- Support multiple range conditions on same field

**4.3 Support Denormalized Company Fields** (`appointment360/app/utils/vql_converter.py`)

- Detect `company_*` prefix fields in contact queries
- Map to correct VQL structure for denormalized fields
- Support text, keyword, and range denormalized fields

**4.4 Support Cursor Pagination** (`appointment360/app/utils/vql_converter.py` & resolvers)

- Add `cursor` parameter to converter
- Extract cursor from Connectra response
- Return cursor in `ContactConnection` and `CompanyConnection`

**4.5 Support Company Population** (`appointment360/app/graphql/modules/contacts/queries.py`)

- Accept `company_config` parameter in `contactQuery()` and `contacts()`
- Pass to VQL converter and include in Connectra query
- Update `Contact` type to include optional `company` field
- Test company data population

### Phase 5: Error Handling & Validation (Medium Priority)

**5.1 Create Error Mapping Utility** (`appointment360/app/utils/connectra_errors.py` - new file)

- Map Connectra error codes (`ERR_PAGE_SIZE_EXCEEDED`, `ERR_BATCH_TOO_LARGE`, etc.) to GraphQL errors
- Parse error format: `"ERR_CODE: message"`
- Handle HTTP status codes (400, 401, 429, 500)
- Create custom exceptions

**5.2 Add Request Validation** (`appointment360/app/utils/connectra_validators.py` - new file)

- Validate VQL query structure
- Validate batch size (max 100)
- Validate pagination (page max 10, limit max 100)
- Validate mutation inputs (required fields, types, formats)
- Integrate into resolvers

**5.3 Add Retry Logic** (`appointment360/app/clients/connectra_client.py`)

- Use existing `tenacity` retry decorator from base client
- Configure retry attempts and delay from settings
- Retry on transient failures only (skip validation errors)
- Handle rate limiting (429) with exponential backoff

### Phase 6: Testing & Documentation (Low Priority)

**6.1 Unit Tests**

- `tests/utils/test_vql_converter.py`: Test filter conversion, field detection, operator mapping
- `tests/clients/test_connectra_client.py`: Mock HTTP responses, test all methods, error handling
- `tests/integration/test_connectra_integration.py`: Test against Connectra API, GraphQL resolvers, end-to-end flows

**6.2 Documentation**

- Update GraphQL API docs with VQL format examples
- Create Connectra integration guide
- Update README with integration section
- Document error codes and troubleshooting

## Key Files to Modify

**Core Files:**

- `appointment360/app/clients/connectra_client.py` - Fix endpoints, add batch upsert, common APIs
- `appointment360/app/utils/vql_converter.py` - New file for VQL conversion
- `appointment360/app/utils/connectra_mappers.py` - New file for data mapping
- `appointment360/app/utils/connectra_errors.py` - New file for error handling
- `appointment360/app/utils/connectra_validators.py` - New file for validation

**GraphQL Resolvers:**

- `appointment360/app/graphql/modules/contacts/queries.py` - Update to use VQL converter
- `appointment360/app/graphql/modules/contacts/mutations.py` - Implement all mutations
- `appointment360/app/graphql/modules/companies/queries.py` - Update to use VQL converter
- `appointment360/app/graphql/modules/companies/mutations.py` - Implement all mutations
- `appointment360/app/graphql/modules/common/` - New module for common APIs

## Critical Path

1. **Task 1.1** (VQL Converter) - Blocks all query fixes
2. **Task 1.2** (Fix Endpoints) - Blocks all API calls
3. **Task 1.3** (Fix Response Parsing) - Blocks data extraction
4. **Task 2.1** (Batch Upsert Methods) - Blocks all mutations
5. **Task 2.2** (Data Mappers) - Blocks mutation implementation

## Success Criteria

- All read operations use correct VQL format and endpoints
- All mutations functional via batch-upsert
- Common API features available in GraphQL
- Advanced VQL features supported (text matching, ranges, denormalized fields)
- Comprehensive error handling and validation
- Unit tests with >80% coverage
- Integration tests passing
- Documentation complete