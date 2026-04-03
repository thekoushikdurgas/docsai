# Extension Telemetry Schema (`telemetryClient.js`)

Describes the log event payload emitted by `contact360.extension/utils/telemetryClient.js` to the Logs API.

## Overview

The telemetry client is a best-effort, fire-and-forget emitter. If no `LOGS_API_BASE_URL` is configured, all calls are no-ops — no errors are thrown and no retry is attempted.

The client is loaded as a plain IIFE and exposes a single function on `window.Contact360Telemetry`.

---

## Configuration

Configuration is resolved at call time from `window.Contact360Constants.LAMBDA_API_CONFIG`:

| Config key | Type | Default | Description |
|---|---|---|---|
| `LOGS_API_BASE_URL` | `string` | `""` (disabled) | Base URL of the Logs API server (e.g. `https://logs.api` or `http://54.x.x.x:8090`) |
| `LOGS_API_ENDPOINT` | `string` | `"/api/v1/logs"` | Path suffix for the log ingest endpoint |
| `LOGS_API_KEY` | `string` | `""` (omitted) | Optional API key sent as `X-API-Key` header |

Runtime values can be overridden by the extension popup's Settings tab and written to `chrome.storage.local` (keys `c360_logs_api_base_url`, `c360_logs_api_key`).

---

## Emitter API

```js
// Exposed on window.Contact360Telemetry
window.Contact360Telemetry.emit(eventType, payload?)
```

| Parameter | Type | Description |
|---|---|---|
| `eventType` | `string` | A namespaced event label (see Event catalog below) |
| `payload` | `Record<string, unknown>` (optional) | Arbitrary key-value metadata merged into `metadata` |

---

## HTTP Request Shape

**Method:** `POST`

**URL:** `${LOGS_API_BASE_URL}${LOGS_API_ENDPOINT}` (trailing slash stripped)

**Headers:**

```
Content-Type: application/json
X-API-Key: <LOGS_API_KEY>         # omitted when key is empty
```

**Body:**

```json
{
  "logs": [
    {
      "level": "info",
      "service_type": "extension",
      "action_type": "<eventType>",
      "metadata": {
        "<...caller payload fields...>",
        "telemetry_schema_version": "<TELEMETRY_SCHEMA_VERSION>"
      }
    }
  ]
}
```

### Fixed fields

| Field | Value |
|---|---|
| `level` | Always `"info"` |
| `service_type` | Always `"extension"` |
| `metadata.telemetry_schema_version` | Read from `window.Contact360Constants.TELEMETRY_SCHEMA_VERSION` or `"unknown"` |

---

## Event Catalog

| `action_type` | Emitted by | Key payload fields |
|---|---|---|
| `extension.capture.start` | `background.js` capture handler | `tab_url`, `profile_count` |
| `extension.capture.complete` | `background.js` capture success | `saved_count`, `retry_count`, `failed_count` |
| `extension.capture.error` | `background.js` capture failure | `error_message` |
| `extension.page.load` | `content.js` init | `tab_url`, `detected_platform` |
| `extension.auth.refresh` | `background.js` token refresh | `outcome: "ok" \| "failed"` |
| `extension.settings.save` | `popup.js` save action | (no extra payload) |
| `extension.gateway.reachable` | `popup.js` health check | `gateway_url` |
| `extension.gateway.unreachable` | `popup.js` health check | `gateway_url`, `error_message` |

---

## Logs API Server

Events are ingested by `EC2/log.server` — a Go service (`contact360.io/logsapi`). Visibility:

- **admin.contact360.io** — searchable via the admin log viewer (Logs page)
- **GraphQL** — `queryLogs` / `searchLogs` queries (see [query_query_logs_graphql.md](../endpoints/query_query_logs_graphql.md), [query_search_logs_graphql.md](../endpoints/query_search_logs_graphql.md))

---

## Related documentation

| Doc | Purpose |
|---|---|
| [extension-graphql-session.md](extension-graphql-session.md) | JWT refresh contract |
| [logsapi.api.md](logsapi.api.md) | Logs API service contract |
| [salesnavigator.api.md](salesnavigator.api.md) | Extension server flows |
| [mutation_create_log_graphql.md](../endpoints/mutation_create_log_graphql.md) | Single log mutation |
| [mutation_create_logs_batch_graphql.md](../endpoints/mutation_create_logs_batch_graphql.md) | Batch log mutation |
| [logsapi_endpoint_era_matrix.md](../endpoints/logsapi_endpoint_era_matrix.md) | Logs API route inventory |

---

## Era traceability

| Era | Milestone |
|---|---|
| 0.x | `telemetryClient.js` loaded in content + background; `LOGS_API_BASE_URL` wired via constants |
| 4.x | Logs URL + key configurable via popup Settings tab; written to `chrome.storage.local` |
| 6.x | Event catalog expanded for capture, auth, gateway events; schema version token added |
| 7.x | `EC2/log.server` (Go) becomes primary ingest endpoint; Python lambda deprecated |
