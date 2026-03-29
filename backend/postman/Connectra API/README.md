Complete Postman collection for Connectra API with comprehensive examples from all documentation.

**Service:** `contact360.io/sync` (Connectra)  
**Auth:** `X-API-Key`  
**Middleware model:** CORS -> gzip -> token-bucket rate limiter -> API key auth

**All Endpoints Implemented**:
- **System**: Health Check
- **Companies**: Filter, Count, Batch Upsert, Filters, Filter Data
- **Contacts**: Filter, Count, Batch Upsert, Filters, Filter Data
- **Common**: Batch Upsert (CSV), Upload URL, Jobs (Create, List), Filters, Filter Data

**CRUD Operations**:

**Contacts**:
- **CREATE**: `POST /contacts/batch-upsert` (UPSERT)
- **READ**: `POST /contacts/` (VQL filter query), `POST /contacts/count`
- **UPDATE**: `POST /contacts/batch-upsert` (UPSERT by UUID)

**Companies**:
- **CREATE**: `POST /companies/batch-upsert` (UPSERT)
- **READ**: `POST /companies/` (VQL filter query), `POST /companies/count`
- **UPDATE**: `POST /companies/batch-upsert` (UPSERT by UUID)

**Features**:
- 100+ example requests covering all filter types
- Account-based filtering examples
- Real-world use cases
- Comprehensive VQL examples
- Proper organization with folders

**Documentation**: All endpoints align with documentation in `docs/`. See [API Overview](./docs/api_structures/API_OVERVIEW.md) for complete reference.

## Era alignment

For era-to-endpoint governance (`0.x`-`10.x`), use:

- `docs/backend/endpoints/connectra_endpoint_era_matrix.json`
- `docs/codebases/connectra-codebase-analysis.md`
- `docs/3. Contact360 contact and company data system/connectra-service.md`

## Connectra vs Jobs testing boundary

Use this collection for `contact360.io/sync` (Connectra) REST contracts only.

- Connectra jobs endpoints in this collection:
  - `POST /common/jobs/create`
  - `POST /common/jobs`
- TKD Job (`contact360.io/jobs`) runtime endpoints are separate and should be validated using the jobs endpoint matrix:
  - `docs/backend/endpoints/jobs_endpoint_era_matrix.json`
- Gateway-facing GraphQL jobs operations are documented under:
  - `docs/backend/apis/16_JOBS_MODULE.md`