# Pages JSON Models (DocsAI)

This document describes the JSON models used for **documentation pages** in the Contact360 DocsAI codebase. Page documents are stored under `media/pages/` (and optionally synced to S3) and validated with Pydantic schemas ported from the Lambda documentation API.

---

## 1. Overview

- **Storage**: `media/pages/*.json` (one file per page, e.g. `dashboard_page.json`).
- **Canonical schema**: Pydantic models in `apps/documentation/schemas/pydantic/models.py`.
- **Validation**: `apps/documentation/schemas/lambda_models.py` (`validate_page_data`) and `apps/documentation/utils/dict_schema_validators.py` (`PageSchemaValidator`).
- **Repositories**: `apps/documentation/repositories/pages_repository.py`, unified storage (local → S3).

---

## 2. Root Model: PageDocumentation

The top-level JSON object for a single page.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `_id` | string | Yes | Unique identifier (e.g. `{page_id}-001`). Serialized from Pydantic alias. |
| `page_id` | string | Yes | Page identifier (e.g. `dashboard_page`). Alphanumeric with underscores/hyphens. |
| `page_type` | string | Yes | One of: `dashboard`, `marketing`, `docs`. |
| `metadata` | object | Yes | See [PageMetadata](#3-metadata-model-pagemetadata). |
| `content` | string \| null | No | Markdown content for the page (optional). |
| `created_at` | string | Yes | ISO 8601 timestamp. |
| `access_control` | object \| null | No | See [AccessControl](#4-access-control-accesscontrol). |
| `sections` | object \| null | No | See [PageSections](#5-sections-pagesections). |
| `fallback_data` | array | No | List of [DataReference](#6-data-references-datareference). Default `[]`. |
| `mock_data` | array | No | List of [DataReference](#6-data-references-datareference). Default `[]`. |
| `demo_data` | array | No | List of [DataReference](#6-data-references-datareference). Default `[]`. |

---

## 3. Metadata Model: PageMetadata

Nested under `metadata`.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `route` | string | Yes | Page route (e.g. `/dashboard`). Must start with `/`. |
| `file_path` | string | Yes | Source file path (e.g. dashboard app page component). |
| `purpose` | string | Yes | Short description of the page purpose. |
| `s3_key` | string | Yes | S3 key for this page JSON (e.g. `data/pages/{page_id}.json`). |
| `status` | string | Yes | One of: `draft`, `published`, `archived`, `deleted`. |
| `authentication` | string | No | Default `"Not required"`. |
| `authorization` | string \| null | No | Authorization notes. |
| `page_state` | string | No | One of: `coming_soon`, `published`, `draft`, `development`, `test`. Default `development`. |
| `last_updated` | string | Yes | ISO 8601 timestamp. |
| `uses_endpoints` | array | No | List of [PageEndpointUsage](#7-endpoint-usage-in-page-pageendpointusage). Default `[]`. |
| `ui_components` | array | No | List of [UIComponent](#8-ui-component-uicomponent). Default `[]`. |
| `versions` | array | No | Page version history (strings). Default `[]`. |
| `endpoint_count` | integer | No | Must equal `uses_endpoints.length` (auto-calculated). |
| `api_versions` | array | No | Derived from `uses_endpoints` (e.g. `["graphql"]`). |
| `content_sections` | object \| null | No | Optional content sections structure. |

---

## 4. Access Control: AccessControl

Optional; applies to page-level `access_control`. Each role is a **UserRoleAccess** object.

| Role | Description |
|------|-------------|
| `super_admin` | Full view, edit, delete. |
| `admin` | View, edit; no delete. |
| `pro_user` | View only. |
| `free_user` | View only. |
| `guest` | No view, edit, or delete. |

**UserRoleAccess** fields:

| Field | Type | Description |
|-------|------|-------------|
| `can_view` | boolean | Can view the resource. |
| `can_edit` | boolean | Can edit the resource. |
| `can_delete` | boolean | Can delete the resource. |
| `restricted_components` | array of string | Component IDs this role cannot access. |

---

## 5. Sections: PageSections

Optional; used for structured page content (headings, tabs, buttons, components, endpoints, etc.).

| Field | Type | Description |
|-------|------|-------------|
| `headings` | array | [HeadingElement](#headingelement): `id`, `text`, `level` (1–6). |
| `subheadings` | array | Same shape as headings. |
| `tabs` | array | [TabElement]: `id`, `label`, `content_ref`. |
| `buttons` | array | [ButtonElement]: `id`, `label`, `action`, `variant`. |
| `input_boxes` | array | [InputBoxElement]: `id`, `label`, `input_type`, `placeholder`, `required`. |
| `text_blocks` | array | [TextBlockElement]: `id`, `content`, `format`. |
| `components` | array | [ComponentReference]: `name`, `file_path`, `props`. |
| `utilities` | array | [UtilityReference]: `name`, `file_path`, `functions`. |
| `services` | array | [ServiceReference]: `name`, `file_path`, `methods`. |
| `hooks` | array | [HookReference]: `name`, `file_path`, `dependencies`. |
| `contexts` | array | [ContextReference]: `name`, `file_path`, `provider`. |
| `ui_components` | array | [ComponentReference]. |
| `endpoints` | array | [EndpointReferenceInSection]: `endpoint_id`, `endpoint_path`, `method`, `file_path`. |

---

## 6. Data References: DataReference

Used in `fallback_data`, `mock_data`, `demo_data`.

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Data name. |
| `file_path` | string | Data file path. |
| `description` | string \| null | Optional description. |

---

## 7. Endpoint Usage in Page: PageEndpointUsage

Each item in `metadata.uses_endpoints`.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `endpoint_path` | string | Yes | e.g. `graphql/GetUserStats`. |
| `method` | string | Yes | One of: `QUERY`, `MUTATION`, `GET`, `POST`, `PUT`, `DELETE`, `PATCH`. |
| `api_version` | string | Yes | e.g. `graphql`. |
| `via_service` | string | Yes | Service that uses this endpoint. |
| `via_hook` | string \| null | No | React hook name. |
| `usage_type` | string | Yes | One of: `primary`, `secondary`, `conditional`, `lazy`, `prefetch`. |
| `usage_context` | string | Yes | One of: `data_fetching`, `data_mutation`, `authentication`, `analytics`, `realtime`, `background`. |
| `description` | string \| null | No | How the endpoint is used. |

---

## 8. UI Component: UIComponent

Each item in `metadata.ui_components`.

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Component name. |
| `file_path` | string | Component file path. |

---

## 9. Example (minimal)

```json
{
  "_id": "dashboard_page-001",
  "page_id": "dashboard_page",
  "page_type": "dashboard",
  "metadata": {
    "route": "/dashboard",
    "file_path": "contact360/dashboard/app/(dashboard)/dashboard/page.tsx",
    "purpose": "Main dashboard page.",
    "s3_key": "data/pages/dashboard_page.json",
    "status": "published",
    "authentication": "Required",
    "page_state": "development",
    "last_updated": "2026-01-20T00:00:00.000000+00:00",
    "uses_endpoints": [],
    "ui_components": [],
    "versions": [],
    "endpoint_count": 0,
    "api_versions": []
  },
  "content": null,
  "created_at": "2026-01-20T00:00:00.000000+00:00",
  "access_control": null,
  "sections": null,
  "fallback_data": [],
  "mock_data": [],
  "demo_data": []
}
```

---

## 10. Validation and Code References

- **Pydantic**: `PageDocumentation`, `PageMetadata`, `PageSections`, `PageEndpointUsage`, `UIComponent`, `DataReference`, `AccessControl` in `apps/documentation/schemas/pydantic/models.py`.
- **Validate before persist**: `validate_page_data()` in `apps/documentation/schemas/lambda_models.py` (uses Pydantic after legacy normalization).
- **Dict validator**: `PageSchemaValidator` in `apps/documentation/utils/dict_schema_validators.py` (required fields, types, enums).
- **Paths**: `apps/documentation/utils/paths.py` → `get_pages_dir()`.
