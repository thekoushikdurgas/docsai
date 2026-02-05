# Postman JSON Models (DocsAI)

This document describes the JSON models used for **Postman configurations** in the Contact360 DocsAI codebase. Configurations include Postman Collection v2.1.0, environments, endpoint mappings, and test suites. They are stored under `media/postman/` and validated with Pydantic schemas.

---

## 1. Overview

- **Storage**: `media/postman/*.json`.
- **Canonical schema**: `apps/documentation/schemas/pydantic/postman_models.py`.
- **Validation**: `apps/documentation/schemas/lambda_models.py` (`validate_postman_configuration_data`) and management command `normalize_media_postman_n8n`.
- **Repositories**: `apps/documentation/repositories/postman_repository.py`, `apps/durgasman/services/durgasman_storage_service.py` (CollectionStorageService).

---

## 2. Root Model: PostmanConfiguration

The top-level JSON object for a Postman configuration (collection + environments + mappings + test suites).

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `_id` | string | Yes | Unique configuration ID (alias for API). |
| `config_id` | string | Yes | Configuration identifier. |
| `name` | string | Yes | Configuration name. |
| `description` | string \| null | No | Description. |
| `state` | string | No | One of: `coming_soon`, `published`, `draft`, `development`, `test`. Default `development`. |
| `collection` | object | Yes | [PostmanCollection](#3-postman-collection-postmancollection) (Collection v2.1.0). |
| `environments` | array | No | List of [PostmanEnvironment](#4-postman-environment-postmanenvironment). Default `[]`. |
| `endpoint_mappings` | array | No | List of [EndpointMapping](#5-endpoint-mapping-endpointmapping). Default `[]`. |
| `test_suites` | array | No | List of [TestSuite](#6-test-suite-testsuite). Default `[]`. |
| `access_control` | object \| null | No | [PostmanAccessControl](#7-postman-access-control-postmanaccesscontrol). |
| `metadata` | object | Yes | [PostmanConfigurationMetadata](#8-postman-configuration-metadata-postmanconfigurationmetadata). |

---

## 3. Postman Collection: PostmanCollection

Postman Collection v2.1.0 structure. Schema URL: `https://schema.getpostman.com/json/collection/v2.1.0/collection.json`.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `info` | object | Yes | [PostmanCollectionInfo](#postman-collection-info): `name`, `description`, `schema`, `version`. |
| `item` | array | Yes | List of [PostmanItem](#postman-item-postmanitem) (requests and folders). |
| `auth` | object \| null | No | Collection-level [PostmanAuth](#postman-auth-postmanauth). |
| `event` | array \| null | No | Collection-level [PostmanEvent](#postman-event-postmanevent) (e.g. pre-request, test). |
| `variable` | array \| null | No | Collection variables (same shape as [PostmanEnvironmentValue](#postman-environment-value)). |

**PostmanCollectionInfo**:

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Collection name. |
| `description` | string \| null | Collection description. |
| `schema` | string | Schema URL (alias `schema_url`). Default `https://schema.getpostman.com/json/collection/v2.1.0/collection.json`. |
| `version` | string \| null | Collection version. |

**PostmanItem** (request or folder):

| Field | Type | Description |
|-------|------|-------------|
| `id` | string \| null | Item ID. |
| `name` | string | Item name. |
| `description` | string \| null | Description. |
| `request` | object \| null | [PostmanRequest](#postman-request-postmanrequest) (if this is a request). |
| `response` | array \| null | Saved [PostmanResponse](#postman-response-postmanresponse) examples. |
| `event` | array \| null | Item-level events. |
| `item` | array \| null | Nested items (if this is a folder). |

**PostmanRequest**:

| Field | Type | Description |
|-------|------|-------------|
| `method` | string | HTTP method. |
| `header` | array \| null | List of [PostmanHeader](#postman-header): `key`, `value`, `description`, `disabled`. |
| `body` | object \| null | [PostmanBody](#postman-body-postmanbody): `mode`, `raw`, `urlencoded`, `formdata`, `graphql`, `options`. |
| `url` | string \| object | Raw URL string or [PostmanUrl](#postman-url-postmanurl): `raw`, `protocol`, `host`, `path`, `query`, `variable`. |
| `auth` | object \| null | [PostmanAuth](#postman-auth-postmanauth). |
| `description` | string \| null | Request description. |

**PostmanAuth**:

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | e.g. `noauth`, `bearer`, `apikey`, `basic`, `oauth2`. |
| `apikey` | array \| null | [PostmanAuthParam]: `key`, `value`, `type`. |
| `bearer` | array \| null | Bearer params. |
| `basic` | array \| null | Basic auth params. |
| `oauth2` | array \| null | OAuth2 params. |

**PostmanBody** (mode: raw \| urlencoded \| formdata \| file \| graphql):

| Field | Type | Description |
|-------|------|-------------|
| `mode` | string | Body mode. |
| `raw` | string \| null | Raw body. |
| `urlencoded` | array \| null | URL-encoded form items. |
| `formdata` | array \| null | Form data items. |
| `graphql` | object \| null | [PostmanGraphQL]: `query`, `variables` (JSON string). |
| `options` | object \| null | Body options. |

**PostmanResponse**:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string \| null | Response ID. |
| `name` | string | Response name. |
| `originalRequest` | object \| null | Original request. |
| `status` | string \| null | Status text. |
| `code` | integer \| null | HTTP status code. |
| `header` | array \| null | Response headers. |
| `body` | string \| null | Response body. |

**PostmanEvent** (e.g. prerequest, test):

| Field | Type | Description |
|-------|------|-------------|
| `listen` | string | Event type: `prerequest` or `test`. |
| `script` | object | [PostmanScript]: `id`, `type` (e.g. `text/javascript`), `exec` (array of script lines). |

---

## 4. Postman Environment: PostmanEnvironment

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string \| null | Environment ID. |
| `name` | string | Yes | Environment name. |
| `values` | array | Yes | List of [PostmanEnvironmentValue](#postman-environment-value-postmanenvironmentvalue). |
| `timestamp` | integer \| null | No | Last modified timestamp. |
| `is_active` | boolean | No | Is this the active environment. Default `false`. |

**PostmanEnvironmentValue**:

| Field | Type | Description |
|-------|------|-------------|
| `key` | string | Variable name. |
| `value` | string | Variable value. |
| `enabled` | boolean | Default `true`. |
| `type` | string | `default` or `secret`. |
| `description` | string \| null | Optional. |

---

## 5. Endpoint Mapping: EndpointMapping

Maps a Postman request to a documentation endpoint.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `mapping_id` | string | Yes | Unique mapping ID. |
| `endpoint_id` | string | Yes | Documentation endpoint ID. |
| `postman_request_id` | string | Yes | Postman request ID. |
| `postman_folder_path` | array | No | Folder path in collection. Default `[]`. |
| `sync_status` | string | No | One of: `synced`, `pending`, `error`. Default `synced`. |
| `last_synced_at` | string \| null | No | Last sync timestamp. |
| `config_overrides` | object \| null | No | Configuration overrides. |
| `test_config` | object \| null | No | Test configuration. |

---

## 6. Test Suite: TestSuite

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `suite_id` | string | Yes | Unique suite ID. |
| `name` | string | Yes | Suite name. |
| `description` | string \| null | No | Description. |
| `endpoint_mapping_ids` | array | No | Endpoint mapping IDs to test. Default `[]`. |
| `environment_name` | string \| null | No | Environment to use. |
| `schedule` | object \| null | No | Execution schedule. |
| `created_at` | string \| null | No | Creation timestamp. |
| `updated_at` | string \| null | No | Last update timestamp. |

---

## 7. Postman Access Control: PostmanAccessControl

Optional; per-role permissions for the configuration. Each role is **PostmanRoleAccess**.

| Role | Description |
|------|-------------|
| `super_admin` | View, run, edit, delete, export. |
| `admin` | View, run, edit, export (no delete). |
| `pro_user` | View, run (no edit, delete, export). |
| `free_user` | View only. |
| `guest` | No permissions. |

**PostmanRoleAccess** (alias `can_run_tests` for `can_run`):

| Field | Type | Description |
|-------|------|-------------|
| `can_view` | boolean | Can view the configuration. |
| `can_run` | boolean | Can run test suites. |
| `can_edit` | boolean | Can edit. |
| `can_delete` | boolean | Can delete. |
| `can_export` | boolean | Can export/download. |

---

## 8. Postman Configuration Metadata: PostmanConfigurationMetadata

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `created_at` | string | Yes | Creation timestamp. |
| `updated_at` | string | Yes | Last update timestamp. |
| `created_by` | string \| null | No | Creator. |
| `last_updated_by` | string \| null | No | Last updater. |
| `last_synced_at` | string \| null | No | Last sync timestamp. |
| `sync_source` | string \| null | No | e.g. manual, ci, import. |
| `version` | string | No | Configuration version. Default `1.0.0`. |
| `tags` | array | No | Tags. Default `[]`. |
| `notes` | string \| null | No | Notes. |

---

## 9. Example (minimal)

```json
{
  "_id": "main-api-config",
  "config_id": "main-api-config",
  "name": "Main API Collection",
  "description": null,
  "state": "development",
  "collection": {
    "info": {
      "name": "Main API",
      "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
    },
    "item": []
  },
  "environments": [],
  "endpoint_mappings": [],
  "test_suites": [],
  "access_control": null,
  "metadata": {
    "created_at": "2026-01-20T00:00:00.000000+00:00",
    "updated_at": "2026-01-20T00:00:00.000000+00:00",
    "version": "1.0.0",
    "tags": []
  }
}
```

---

## 10. Validation and Code References

- **Pydantic**: All Postman models in `apps/documentation/schemas/pydantic/postman_models.py`.
- **Validate**: `validate_postman_configuration_data()` in `apps/documentation/schemas/lambda_models.py`.
- **Normalize**: `normalize_media_postman_n8n` in `apps/documentation/management/commands/normalize_media_postman_n8n.py` (Postman configs; n8n is separate).
- **Paths**: `apps/documentation/utils/paths.py` → `get_postman_dir()`.
