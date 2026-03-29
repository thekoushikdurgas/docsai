Postman collection for Lambda Documentation API Service deployed on AWS API Gateway.

**Base URL**: {{base_url}}
**Production URL**: https://94hucnirj2.execute-api.us-east-1.amazonaws.com

**Authentication**:
- Public endpoints: No authentication required (most endpoints are public)
- Access control handled at data model level via access_control fields

## API Structure

### REST API v1
- **Health Check**: Service health and info endpoints (2 endpoints)
- **Pages API** (`/api/v1/pages/`): 30+ endpoints - Full CRUD, category filtering (by type, by user type), format/import/analyse, statistics
- **Endpoints API** (`/api/v1/endpoints/`): 28+ endpoints - Full CRUD, category filtering, format/import/analyse
- **Relationships API** (`/api/v1/relationships/`): 30+ endpoints - Full CRUD, category filtering, format/import/analyse, statistics
- **Postman API** (`/api/v1/postman/`): 8+ endpoints - Configuration CRUD, format/import/analyse, statistics
- **Index Management API** (`/api/v1/index/`): 12 endpoints - Read/rebuild/validate indexes for all resources

**Total**: 100+ endpoints

## Features
- **JSON Ingestion**: `/format/` endpoints return copy/paste examples, `/import/` accepts JSON payloads for upsert operations
- **Analysis Integration**: `/analyse/` endpoints ingest analysis JSON from frontend/backend tools and sync into S3
- **Index Management**: Read, rebuild, and validate index.json files for fast INDEX-ONLY responses
- **S3 JSON storage**: All data (metadata and content) stored in JSON files
- **Content included directly**: No presigned URLs needed - content in JSON responses
- **Category filtering**: By type, user type (access control), version, method, usage type, usage context, state
- **Statistics endpoints**: Index-based aggregated statistics for fast responses
- **Partial updates (PATCH)**: Recursive merge for nested objects
- **Graceful error handling**: Statistics endpoints return empty defaults on errors

## New Endpoints (v2)

### Format Endpoints
- `GET /api/v1/{resource}/format/` - Returns JSON examples, S3 key conventions, and analysis payload formats

### Import Endpoints
- `POST /api/v1/{resource}/import/?mode=upsert|create_only|update_only` - Accepts JSON payloads (single item, list, or wrapper object) and upserts to S3 with index updates

### Analyse Endpoints
- `POST /api/v1/{resource}/analyse/` - Ingests analysis JSON from tools and syncs into S3 using existing sync_from_analysis methods

### Index Management
- `GET /api/v1/index/{resource}/` - Read index.json
- `POST /api/v1/index/{resource}/rebuild/` - Rebuild index from S3 files
- `GET /api/v1/index/{resource}/validate/` - Validate index consistency

## Route Ordering Note

The API is built with FastAPI. Specific routes (like `/format/`, `/import/`, `/statistics/`) are defined BEFORE parameterized routes (`/{id}/`) to prevent route conflicts.