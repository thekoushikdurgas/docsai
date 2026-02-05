# n8n JSON Models (DocsAI)

This document describes the **n8n workflow** JSON structures used in the Contact360 DocsAI codebase. n8n workflow files are stored under `media/n8n/` in a folder hierarchy (e.g. `workflows/`, `Database Cleaning/`, `P2PMigration/`). DocsAI does **not** enforce a full Pydantic schema for n8n JSON; it performs a lightweight structural sanity check and optionally adds a `workflow_id` field.

---

## 1. Overview

- **Storage**: `media/n8n/**/*.json` (e.g. `media/n8n/workflows/data_search.json`, `media/n8n/Database Cleaning/Worker.json`).
- **Schema**: **No** canonical Pydantic schema in DocsAI. Structure follows the **n8n workflow export format** (n8n-native).
- **Normalization**: `apps/documentation/management/commands/normalize_media_postman_n8n.py` (`_normalize_n8n`):
  - Ensures each file is valid JSON and is an object (or wraps non-dict payloads in `{"workflow": ...}`).
  - If `workflow_id` is missing, sets it to the filename stem (e.g. `data_search`).
- **Paths**: `apps/documentation/utils/paths.py` → `get_n8n_dir()` returns `get_media_root() / "n8n"`.
- **Media Manager**: n8n is one of the resource types; subfolders (e.g. `workflows`, `Database Cleaning`, `P2PMigration`, `Sales Navigator Workflows`, `Email Pattern`) are listed in `media_file_manager.py`.

---

## 2. Top-Level Workflow Object (n8n Export Format)

Based on workflow JSON under `media/n8n/workflows/` and other folders.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Workflow name (e.g. `Data Search`). |
| `nodes` | array | Yes | List of [Node](#3-node-object) objects. |
| `connections` | object | Yes | Map of node name → connection definitions. See [Connections](#4-connections). |
| `settings` | object | No | Workflow settings (e.g. `executionOrder`: `v1`). |
| `triggerCount` | integer | No | Number of triggers. |
| `workflow_id` | string | No | Stable ID; added by DocsAI normalize if missing (from filename stem). |

---

## 3. Node Object

Each item in `nodes`.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique node ID (e.g. `webhook-trigger-1`). |
| `name` | string | Yes | Display name (e.g. `Webhook Trigger`). |
| `type` | string | Yes | n8n node type (e.g. `n8n-nodes-base.webhook`, `@n8n/n8n-nodes-langchain.embeddingsOpenAi`). |
| `typeVersion` | number | Yes | Node type version. |
| `position` | array | Yes | `[x, y]` on canvas. |
| `parameters` | object | Yes | Node-specific parameters (e.g. `httpMethod`, `path`, `model`, `options`). |
| `credentials` | object | No | Credential references by name (e.g. `openAiApi`: `{ "id": "...", "name": "..." }`). |

**Examples of node types** (from codebase):

- `n8n-nodes-base.stickyNote` – sticky note (e.g. `content`, `height`, `width`, `color`).
- `n8n-nodes-base.webhook` – webhook trigger (`httpMethod`, `path`, `responseMode`, `options`).
- `@n8n/n8n-nodes-langchain.embeddingsOpenAi` – OpenAI embeddings (`model`, `options`).
- `@n8n/n8n-nodes-langchain.vectorStorePinecone` – Pinecone vector store.
- `n8n-nodes-base.postgres` – PostgreSQL (`operation`, `query`, `schema`, `table`, `columns`, etc.).
- `n8n-nodes-base.code` – Code node (`jsCode`).
- `n8n-nodes-base.respondToWebhook` – Respond to webhook (`respondWith`, `responseBody`, `options`).

---

## 4. Connections

`connections` is an object keyed by **source node name**. Each value is an object keyed by **output type** (e.g. `main`, `ai_embedding`, `ai_vectorStore`). Each output type maps to an array of “sockets”; each socket is an array of connection targets.

**Structure**:

```json
{
  "Source Node Name": {
    "outputType": [
      [
        { "node": "Target Node Name", "type": "inputType", "index": 0 }
      ]
    ]
  }
}
```

**Example** (from `data_search.json`):

```json
{
  "Webhook Trigger": {
    "main": [[{ "node": "Generate Embeddings", "type": "main", "index": 0 }]]
  },
  "Generate Embeddings": {
    "ai_embedding": [[{ "node": "Query Vector DB", "type": "ai_embedding", "index": 0 }]]
  }
}
```

---

## 5. DocsAI-Added Field: workflow_id

- **When**: Applied by `normalize_media_postman_n8n` when `workflow_id` is missing.
- **Value**: File stem (e.g. `data_search` for `data_search.json`).
- **Purpose**: Stable identifier for the workflow in DocsAI media/S3 context; does not change n8n execution behavior.

---

## 6. Folder Layout (media/n8n)

| Folder / File | Description |
|---------------|-------------|
| `workflows/*.json` | Workflows (e.g. `data_search.json`, `key_ingestion_workflow.json`). |
| `Database Cleaning/*.json` | Database cleaning workflows (Worker, Work Distributor, etc.). |
| `P2PMigration/*.json` | P2P migration workflows. |
| `Sales Navigator Workflows/*.json` | Sales Navigator-related workflows. |
| `Email Pattern/*.json` | Email pattern workflows (e.g. Web_search Tool). |
| `index.json` | May be empty or a simple index; not part of n8n export. |

---

## 7. No Full Schema in DocsAI

- **Pydantic**: DocsAI does **not** define Pydantic models for n8n workflow JSON.
- **Validation**: Only:
  - Valid JSON.
  - Root is an object (or wrapped as `{"workflow": ...}`).
  - Optional `workflow_id` injection.
- **Consumption**: Workflows are primarily consumed by n8n or by Durgasflow’s n8n parser (`apps/durgasflow/services/n8n_parser.py`) if imported; DocsAI treats them as opaque JSON for storage and listing.

---

## 8. Code References

- **Paths**: `get_n8n_dir()` in `apps/documentation/utils/paths.py`.
- **Normalize**: `_normalize_n8n()` in `apps/documentation/management/commands/normalize_media_postman_n8n.py` (skip with `--skip-n8n`).
- **Media Manager**: `resource_type === "n8n"`; subdirs in `media_file_manager.py` (e.g. `workflows`, `Database Cleaning`, `P2PMigration`, `Sales Navigator Workflows`, `Email Pattern`).
