# Endpoints JSON Models (DocsAI)

This document describes the JSON models used for **API endpoint documentation** in the Contact360 DocsAI codebase. Endpoint documents are stored under `media/endpoints/` and validated with Pydantic schemas ported from the Lambda documentation API.

---

## 1. Overview

- **Storage**: `media/endpoints/*.json` (one file per endpoint, e.g. `query_get_user_stats_graphql.json`).
- **Canonical schema**: Pydantic models in `apps/documentation/schemas/pydantic/models.py`.
- **Validation**: `apps/documentation/schemas/lambda_models.py` (`validate_endpoint_data`) and `apps/documentation/utils/dict_schema_validators.py` (`EndpointSchemaValidator`).
- **Repositories**: `apps/documentation/repositories/endpoints_repository.py`, unified storage (local → S3).

---

## 2. Root Model: EndpointDocumentation

The top-level JSON object for a single endpoint.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `_id` | string | Yes | Unique identifier (e.g. `{endpoint_id}-001`). |
| `endpoint_id` | string | Yes | Endpoint identifier (e.g. `query_get_user_stats_graphql`). |
| `endpoint_path` | string | Yes | Path (e.g. `graphql/GetUserStats`). |
| `method` | string | Yes | One of: `QUERY`, `MUTATION`, `GET`, `POST`, `PUT`, `DELETE`, `PATCH`. |
| `api_version` | string | Yes | e.g. `graphql`. |
| `description` | string | Yes | Endpoint description. |
| `created_at` | string | Yes | ISO 8601 timestamp. |
| `updated_at` | string | Yes | ISO 8601 timestamp. |
| `endpoint_state` | string | No | One of: `coming_soon`, `published`, `draft`, `development`, `test`. Default `development`. |
| `service_file` | string \| null | No* | Service file path. *At least one of `service_file` or `router_file` required. |
| `router_file` | string \| null | No* | Router file path. |
| `service_methods` | array | No | List of service method names. Default `[]`. |
| `repository_methods` | array | No | List of repository method names. Default `[]`. |
| `used_by_pages` | array | No | List of [EndpointPageUsage](#3-page-usage-in-endpoint-endpointpageusage). Default `[]`. |
| `rate_limit` | string \| null | No | Rate limit description. |
| `graphql_operation` | string \| null | No | GraphQL operation string. |
| `sql_file` | string \| null | No | SQL file reference. |
| `page_count` | integer | No | Must equal `used_by_pages.length` (auto-calculated). |
| `access_control` | object \| null | No | [EndpointAccessControl](#4-endpoint-access-control-endpointaccesscontrol). |
| `lambda_services` | object \| null | No | [LambdaServices](#5-lambda-services-lambdaservices). |
| `files` | object \| null | No | [EndpointFiles](#6-endpoint-files-endpointfiles). |
| `methods` | object \| null | No | [EndpointMethods](#7-endpoint-methods-endpointmethods). |

---

## 3. Page Usage in Endpoint: EndpointPageUsage

Each item in `used_by_pages`.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `page_path` | string | Yes | Page route (e.g. `/dashboard`). |
| `page_title` | string | Yes | Page title. |
| `via_service` | string | Yes | Service name. |
| `via_hook` | string \| null | No | React hook name. |
| `usage_type` | string | Yes | One of: `primary`, `secondary`, `conditional`, `lazy`, `prefetch`. |
| `usage_context` | string | Yes | One of: `data_fetching`, `data_mutation`, `authentication`, `analytics`, `realtime`, `background`. |
| `updated_at` | string \| null | No | ISO 8601 timestamp. |

---

## 4. Endpoint Access Control: EndpointAccessControl

Optional; applies to endpoint-level `access_control`. Each role is an **EndpointRoleAccess** object.

| Role | Description |
|------|-------------|
| `super_admin` | Full access and execute. |
| `admin` | Access and execute. |
| `pro_user` | Access and execute (e.g. rate_limit `100/hour`). |
| `free_user` | Access and execute (e.g. rate_limit `20/hour`). |
| `guest` | No access or execute. |

**EndpointRoleAccess** fields:

| Field | Type | Description |
|-------|------|-------------|
| `can_access` | boolean | Can access the endpoint. |
| `can_execute` | boolean | Can execute the endpoint. |
| `rate_limit` | string \| null | Rate limit for this role. |
| `restricted_fields` | array of string | Fields this role cannot access. |

---

## 5. Lambda Services: LambdaServices

Optional; backend Lambda configuration.

| Field | Type | Description |
|-------|------|-------------|
| `primary` | object \| null | [PrimaryLambdaService]: `service_name`, `function_name`, `runtime`, `memory_mb`, `timeout_seconds`. |
| `dependencies` | array | List of [DependencyLambdaService]: `service_name`, `function_name`, `invocation_type`, `purpose`. |
| `environment` | object | Environment variables (key-value). |

---

## 6. Endpoint Files: EndpointFiles

Optional; file references for the endpoint.

| Field | Type | Description |
|-------|------|-------------|
| `service_file` | string \| null | Service file path. |
| `router_file` | string \| null | Router file path. |
| `repository_file` | string \| null | Repository file path. |
| `schema_file` | string \| null | Schema file path. |
| `test_file` | string \| null | Test file path. |
| `graphql_file` | string \| null | GraphQL file path. |
| `sql_file` | string \| null | SQL file path. |

---

## 7. Endpoint Methods: EndpointMethods

Optional; method references.

| Field | Type | Description |
|-------|------|-------------|
| `service_methods` | array | Service method names. |
| `repository_methods` | array | Repository method names. |
| `validation_methods` | array | Validation method names. |
| `middleware_methods` | array | Middleware method names. |

---

## 8. Example (minimal)

```json
{
  "_id": "query_get_user_stats_graphql-001",
  "endpoint_id": "query_get_user_stats_graphql",
  "endpoint_path": "graphql/GetUserStats",
  "method": "QUERY",
  "api_version": "graphql",
  "description": "Get aggregated user statistics.",
  "created_at": "2026-01-20T00:00:00.000000+00:00",
  "updated_at": "2026-01-21T00:00:00.000000+00:00",
  "endpoint_state": "development",
  "service_file": "appointment360/app/graphql/modules/users/queries.py",
  "router_file": "contact360/dashboard/src/services/graphql/adminService.ts",
  "service_methods": ["userStats"],
  "repository_methods": ["get_user_statistics"],
  "used_by_pages": [],
  "rate_limit": null,
  "graphql_operation": "query GetUserStats { ... }",
  "sql_file": null,
  "page_count": 0,
  "access_control": null,
  "lambda_services": null,
  "files": null,
  "methods": null
}
```

---

## 9. Validation and Code References

- **Pydantic**: `EndpointDocumentation`, `EndpointPageUsage`, `EndpointAccessControl`, `EndpointFiles`, `EndpointMethods`, `LambdaServices` in `apps/documentation/schemas/pydantic/models.py`.
- **Validate before persist**: `validate_endpoint_data()` in `apps/documentation/schemas/lambda_models.py`.
- **Dict validator**: `EndpointSchemaValidator` in `apps/documentation/utils/dict_schema_validators.py`.
- **Paths**: `apps/documentation/utils/paths.py` → `get_endpoints_dir()`.
