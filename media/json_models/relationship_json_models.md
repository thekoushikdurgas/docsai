# Relationship JSON Models (DocsAI)

This document describes the JSON models used for **page–endpoint relationship** documentation in the Contact360 DocsAI codebase. Relationships link dashboard/marketing/docs pages to API endpoints (e.g. which service/hook uses which endpoint on which page). They are stored under `media/retations/` (legacy name; relationships dir) in both **by-page** and **by-endpoint** forms, plus index files.

---

## 1. Overview

- **Storage**: `media/retations/by-page/*.json`, `media/retations/by-endpoint/*.json`, `media/retations/index.json`, `media/retations/relationships_index.json`.
- **Canonical schema**: Pydantic models in `apps/documentation/schemas/pydantic/models.py` (EnhancedRelationship and related).
- **Validation**: `apps/documentation/schemas/lambda_models.py` (`validate_relationship_data`) and `apps/documentation/utils/dict_schema_validators.py` (`RelationshipSchemaValidator`).
- **Repositories**: `apps/documentation/repositories/relationships_repository.py`, unified storage (local → S3).
- **Paths**: `apps/documentation/utils/paths.py` → `get_relationships_dir()` (resolves to `retations` on disk for backward compatibility).

---

## 2. Root Model: EnhancedRelationship

The full relationship document (single page–endpoint link with context). Used in by-page and by-endpoint payloads and in the relationships index.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `_id` | string | Yes | Unique identifier (often same as `relationship_id`). |
| `relationship_id` | string | Yes | Composite ID (e.g. `{page_id}_graphql_{Operation}_{METHOD}`). |
| `state` | string | No | One of: `coming_soon`, `published`, `draft`, `development`, `test`. Default `development`. |
| `access_control` | object \| null | No | [RelationshipAccessControl](#3-relationship-access-control-relationshipaccesscontrol). |
| `page_reference` | object \| null | No | [PageReference](#4-page-reference-pagereference). |
| `endpoint_reference` | object \| null | No | [EndpointRef](#5-endpoint-reference-endpointref). |
| `connection` | object \| null | No | [RelationshipConnection](#6-connection-relationshipconnection). |
| `files` | object \| null | No | File references. |
| `data_flow` | object \| null | No | Data flow description. |
| `postman_reference` | object \| null | No | Postman reference. |
| `dependencies` | object \| null | No | Dependencies. |
| `performance` | object \| null | No | Performance metrics. |
| `metadata` | object \| null | No | [RelationshipMetadata](#7-relationship-metadata-relationshipmetadata). |
| **Flattened fields** (convenience) | | | |
| `page_path` | string \| null | No | Page route (e.g. `/dashboard`). |
| `endpoint_path` | string \| null | No | Endpoint path (e.g. `graphql/GetUserStats`). |
| `method` | string \| null | No | HTTP/GraphQL method. |
| `api_version` | string \| null | No | e.g. `graphql`. |
| `via_service` | string \| null | No | Service name. |
| `via_hook` | string \| null | No | React hook name. |
| `usage_type` | string \| null | No | One of: `primary`, `secondary`, `conditional`, etc. |
| `usage_context` | string \| null | No | One of: `data_fetching`, `data_mutation`, `authentication`, `analytics`, etc. |
| `created_at` | string \| null | No | ISO 8601 timestamp. |
| `updated_at` | string \| null | No | ISO 8601 timestamp. |

---

## 3. Relationship Access Control: RelationshipAccessControl

Optional; per-role permissions for the relationship. Each role is **RelationshipRoleAccess**.

| Role | Description |
|------|-------------|
| `super_admin` | View, edit, delete. |
| `admin` | View, edit (no delete). |
| `pro_user` | View only. |
| `free_user` | View only. |
| `guest` | No view, edit, or delete. |

**RelationshipRoleAccess**:

| Field | Type | Description |
|-------|------|-------------|
| `can_view` | boolean | Can view the relationship. |
| `can_edit` | boolean | Can edit. |
| `can_delete` | boolean | Can delete. |

---

## 4. Page Reference: PageReference

Optional; reference to the page in the relationship.

| Field | Type | Description |
|-------|------|-------------|
| `page_id` | string | Page ID. |
| `page_path` | string | Page route. |
| `page_title` | string | Page title. |
| `page_type` | string | Page type. |
| `page_state` | string | Page state. |
| `file_path` | string | Page component file path. |

---

## 5. Endpoint Reference: EndpointRef

Optional; reference to the endpoint in the relationship.

| Field | Type | Description |
|-------|------|-------------|
| `endpoint_id` | string | Endpoint ID. |
| `endpoint_path` | string | Endpoint path. |
| `method` | string | HTTP/GraphQL method. |
| `api_version` | string | API version. |
| `endpoint_state` | string | Endpoint state. |
| `description` | string \| null | Endpoint description. |
| `lambda_service` | string \| null | Lambda service name. |

---

## 6. Connection: RelationshipConnection

Optional; how the page and endpoint are connected.

| Field | Type | Description |
|-------|------|-------------|
| `via_service` | string | Service name. |
| `via_hook` | string \| null | React hook name. |
| `usage_type` | string | Default `primary`. One of: `primary`, `secondary`, `conditional`, etc. |
| `usage_context` | string | Default `data_fetching`. One of: `data_fetching`, `data_mutation`, `authentication`, `analytics`, etc. |
| `invocation_pattern` | string | e.g. `on_mount`. |
| `caching_strategy` | string \| null | Caching approach. |
| `retry_policy` | object \| null | Retry configuration. |

---

## 7. Relationship Metadata: RelationshipMetadata

Optional; metadata for the relationship.

| Field | Type | Description |
|-------|------|-------------|
| `created_at` | string | Creation timestamp. |
| `updated_at` | string | Last update timestamp. |
| `created_by` | string \| null | Creator. |
| `last_updated_by` | string \| null | Last updater. |
| `version` | string | Default `1.0.0`. |
| `tags` | array | Tags. Default `[]`. |
| `notes` | string \| null | Notes. |

---

## 8. Index and Aggregated Structures

### 8.1 Relationships Index: `index.json` (by-endpoint style)

| Field | Type | Description |
|-------|------|-------------|
| `version` | string | e.g. `2.0`. |
| `last_updated` | string | ISO 8601 timestamp. |
| `total` | integer | Total number of relationship entries. |
| `relationships` | array | List of grouped entries: `endpoint_path`, `method`, `pages` (array of [EnhancedRelationship](#2-root-model-enhancedrelationship)), `created_at`, `updated_at`. |

### 8.2 By-Page and By-Endpoint Files

- **By-page**: One file per page (e.g. `dashboard.json`). Structure is script/API-defined; typically contains `page_path` and a list of relationships or endpoints for that page.
- **By-endpoint**: One file per endpoint (e.g. `graphql_GetUserStats_QUERY.json`). Structure is script/API-defined; typically contains `endpoint_path`, `method`, and a list of pages or relationship objects.
- **Result files**: `*_result.json` files in the same folders often wrap the main file path and S3 key for sync/upload results.

---

## 9. Example (single relationship object)

```json
{
  "_id": "dashboard_graphql_GetUserStats_QUERY",
  "relationship_id": "dashboard_graphql_GetUserStats_QUERY",
  "state": "development",
  "access_control": null,
  "page_reference": null,
  "endpoint_reference": null,
  "connection": null,
  "files": null,
  "data_flow": null,
  "postman_reference": null,
  "dependencies": null,
  "performance": null,
  "metadata": null,
  "page_path": "/dashboard",
  "endpoint_path": "graphql/GetUserStats",
  "method": "QUERY",
  "api_version": "graphql",
  "via_service": "adminService",
  "via_hook": "useDashboardPage",
  "usage_type": "conditional",
  "usage_context": "analytics",
  "created_at": "2026-01-21T13:33:51.897968+00:00",
  "updated_at": "2026-01-21T13:33:51.897968+00:00"
}
```

---

## 10. Validation and Code References

- **Pydantic**: `EnhancedRelationship`, `RelationshipAccessControl`, `RelationshipRoleAccess`, `PageReference`, `EndpointRef`, `RelationshipConnection`, `RelationshipMetadata` in `apps/documentation/schemas/pydantic/models.py`.
- **Validate before persist**: `validate_relationship_data()` in `apps/documentation/schemas/lambda_models.py`.
- **Dict validator**: `RelationshipSchemaValidator` in `apps/documentation/utils/dict_schema_validators.py` (`validate_by_page`, `validate_by_endpoint`).
- **Paths**: `get_relationships_dir()` in `apps/documentation/utils/paths.py` (returns `retations` if that dir exists, else `relationships`).
