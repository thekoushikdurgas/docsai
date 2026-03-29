# Resume AI Service (REST)

## Overview

The **resumeai** microservice is a **FastAPI** application that exposes **REST** endpoints under **`/v1`** for:

- **Health** — liveness and version metadata (no API key).
- **Resume** — CRUD metadata in the shared Postgres database; resume JSON is stored in **s3storage** under the user’s logical bucket at **`resume_data_key`** (see [Database — resume_documents](../database/tables/resume_documents.sql)).
- **AI** — parse uploads, section enhancement, ATS scoring, LaTeX, photo enhancement, LinkedIn import (requires upstream AI keys on the service).

**Codebase:** `backend(dev)/resumeai/`  
**Deployment:** AWS SAM (`template.yaml`, `sam deploy`), HTTP API (API Gateway v2).  
**Contact360 integration:** The main GraphQL API proxies resume operations via `ResumeAIClient` and the `resume` module; clients may use GraphQL instead of calling resumeai directly.

**Postman:** `backend(dev)/resumeai/postman/Resume_AI_Service.postman_collection.json` — see `postman/README.md`.

**Related (other FastAPI microservice):** [Contact AI / AI Chats GraphQL](17_AI_CHATS_MODULE.md) — `backend(dev)/contact.ai`, shared Postgres; Postman: `docs/media/postman/Contact AI Service.postman_collection.json`.

**OpenAPI:** When the service is running, **`GET {baseUrl}/docs`** (Swagger UI).

---

## Authentication

| Header        | Value                          |
|---------------|--------------------------------|
| `X-API-Key`   | Shared secret (`API_KEY` / SAM **ApiKey**) |

Endpoints that require the key return **422** if the header is missing (FastAPI validation). Invalid key returns **401** with body `{"detail": "invalid or missing API key"}`.

**Public (no key):** `GET /`, `GET /v1/health`, `GET /v1/health/info`.

---

## Base URL

- **Local:** `http://127.0.0.1:8080` (or `PORT` from `.env`).
- **Lambda:** API Gateway URL from `sam deploy` output (e.g. `ResumeAiUrl` / `Outputs.ResumeAiUrl`).

All routes below are relative to that origin. The app mounts the API under **`/v1`** (see `app/main.py`).

---

## Environment (service)

| Variable | Purpose |
|----------|---------|
| `API_KEY` | Service-to-service auth (must match callers e.g. `RESUME_AI_API_KEY` on Contact360). |
| `DATABASE_URL` | Async SQLAlchemy URL (`sqlite+aiosqlite` dev; `postgresql+asyncpg` production). |
| `LAMBDA_S3STORAGE_API_URL` | s3storage API base URL (no trailing slash). |
| `LAMBDA_S3STORAGE_API_KEY` | Optional `X-API-Key` for s3storage API Gateway. |
| `HF_API_KEY` | Hugging Face token for Inference API (text generation and embeddings). |
| `HF_TEXT_MODEL` | Hugging Face model id for text/JSON tasks (default `mistralai/Mistral-7B-Instruct-v0.2`). |
| `HF_EMBED_MODEL` | Hugging Face model id for RAG ATS embeddings (default `sentence-transformers/all-MiniLM-L6-v2`). |

See `backend(dev)/resumeai/.env.example` and `template.yaml` for the full list.

---

## REST endpoints summary

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/` | No | Service banner (`status`, `version`, endpoint hints). |
| GET | `/v1/health` | No | Liveness: `status`, `service`. |
| GET | `/v1/health/info` | No | `version`, `service`, `status`. |
| POST | `/v1/resume` | Yes | Create resume; body: `userId`, `resume`, optional `bucketId`. |
| GET | `/v1/resume/user/{user_id}` | Yes | List resumes for user (newest first). |
| GET | `/v1/resume/{resume_id}` | Yes | Get one resume (loads JSON from s3storage). |
| PUT | `/v1/resume/{resume_id}` | Yes | Update resume JSON (overwrites object in storage). |
| DELETE | `/v1/resume/{resume_id}` | Yes | Delete DB row; best-effort delete in s3storage. |
| POST | `/v1/ai/parse` | Yes | Multipart `file` — parse resume file to `Resume` JSON (PDF, DOCX, plain text). Image-only uploads are not supported. |
| POST | `/v1/ai/enhance` | Yes | JSON: `content`, `enhancement_type`. |
| POST | `/v1/ai/skills` | Yes | JSON: `title`, `experienceText`. |
| POST | `/v1/ai/ats-score` | Yes | JSON: `resume`, optional `jobDescription`, optional `atsMode` (`full` or `rag`). RAG requires `jobDescription`. |
| POST | `/v1/ai/ats-improve` | Yes | JSON: `resume`, optional `jobDescription`, optional `atsResult`, optional `atsStyle`. |
| POST | `/v1/ai/insights` | Yes | JSON: `resume`, optional `jobDescription` — deterministic skill match, flags, interview prompts. |
| POST | `/v1/ai/generate-ats-text` | Yes | JSON: `rawNotes`, optional `style`, optional `jobDescription` — plain ATS-oriented text. |
| POST | `/v1/ai/critique` | Yes | JSON: `resume`, optional `tone` (`professional` or `roast`). |
| POST | `/v1/ai/latex` | Yes | JSON: `resume`, optional `template`. |
| POST | `/v1/ai/photo` | Yes | Multipart `file` — image enhancement. |
| POST | `/v1/ai/linkedin` | Yes | JSON: `url` (LinkedIn profile URL). |

---

## Resume CRUD — JSON shapes

### Create — `POST /v1/resume`

Request body (camelCase aliases supported):

```json
{
  "userId": "uuid-of-user",
  "bucketId": "optional-logical-bucket-id",
  "resume": { }
}
```

- **`bucketId`:** Logical s3storage bucket (typically `users.bucket` from Contact360). If omitted, the service uses **`userId`** as the bucket id.
- **`resume`:** Full `Resume` object (`personalDetails`, `objective`, `experience`, etc.) — see `app/models/resume.py`.

Response **201** — `ResumeRecordResponse`:

```json
{
  "id": "uuid",
  "userId": "uuid-of-user",
  "resume": { },
  "createdAt": "2026-03-22T00:00:00+00:00",
  "updatedAt": "2026-03-22T00:00:00+00:00"
}
```

### Update — `PUT /v1/resume/{resume_id}`

```json
{
  "resume": { }
}
```

### List / Get

- **GET** `/v1/resume/user/{user_id}` → array of `ResumeRecordResponse`.
- **GET** `/v1/resume/{resume_id}` → single `ResumeRecordResponse`.

### Delete — `DELETE /v1/resume/{resume_id}`

**204** No Content on success.

---

## Storage and database

- Rows in **`resume_documents`** store **`storage_bucket_id`** and **`resume_data_key`** (not inline JSON). JSON is read/written via s3storage (`LAMBDA_S3STORAGE_API_URL`).
- Failures talking to storage surface as **502** with a clear message where applicable (`ResumeStorageError`).

---

## AI endpoints — notes

- **`/v1/ai/parse`:** `multipart/form-data` with field name **`file`**. Max size: `MAX_UPLOAD_SIZE_MB` (default 10 MB). Accepts **PDF, DOCX, or plain text**; text is extracted locally then structured via **Hugging Face** text generation.
- **`/v1/ai/photo`:** `multipart/form-data` with field name **`file`**. Applies **local PIL** sharpening/contrast only (no generative image API).
- **`/v1/ai/enhance`:** `enhancement_type` is one of: `objective`, `description`, `hobbies`, `education_description`.
- **`/v1/ai/ats-score`:** `atsMode` defaults to `full`; use `rag` with a non-empty `jobDescription` to score using **HF embeddings** (`HF_EMBED_MODEL`) + retrieved resume chunks + HF text model.
- **`/v1/ai/ats-improve`:** `atsStyle` is one of `standard`, `tech`, `executive`, `creative`, `entry` (default `standard`).
- **`/v1/ai/insights`:** No generative model; pure Python heuristics over resume text (and optional JD for skill overlap).
- **`/v1/ai/linkedin`:** Best-effort JSON from the URL string via HF; there is **no live web search**. For best results, paste profile content elsewhere or expect limited accuracy.
- Upstream AI failures typically return **502**.

---

## Error handling

| HTTP | Typical cause |
|------|----------------|
| 401 | Invalid or missing `X-API-Key` (when required). |
| 404 | Resume id not found (`ResumeNotFoundError`). |
| 422 | Missing required header/body fields. |
| 502 | AI provider or s3storage failure. |
| 500 | Database or unhandled server error (`DatabaseError`, etc.). |

Error bodies for domain exceptions may use `{ "error", "message", "success" }` via `ResumeAIException` handler (see `app/main.py`).

---

## Related modules and docs

- **GraphQL (Contact360):** `contact360.io/api/app/graphql/modules/resume/` — `saveResume` passes `userId`, `bucketId` (from `user.bucket` or `user.uuid`), and `resumeData`. When resumeai returns **502/503/504**, the GraphQL layer maps these to **`ServiceUnavailableError`** (HTTP **503**, code `SERVICE_UNAVAILABLE`) instead of a generic bad request.
- **Database:** [resume_documents.sql](../database/tables/resume_documents.sql) — table definition and keys.
- **s3storage:** [07_S3_MODULE.md](07_S3_MODULE.md), [lambda/s3storage](../../../lambda/s3storage/) — logical buckets and `resume/` uploads.

---

## Task breakdown (for maintainers)

1. **Import Postman** — Set `baseUrl` and `apiKey`; run **Health**, then **Resume → Create**, copy `id` into `resumeId`, run **Get** and **Delete**.
2. **Trace one resume request** — `app/api/v1/endpoints/resume.py` → `ResumeService` → `S3StorageClient` + `ResumeRepository`; confirm `bucketId` defaults and storage keys under `resume/`.
3. **Align with GraphQL** — In `contact360.io/api`, open `app/clients/resume_ai_client.py` and `graphql/modules/resume/mutations.py`; verify paths are relative to `RESUME_AI_BASE_URL` including `/v1` if configured.
4. **Contract check** — Compare request/response models in `app/schemas/` with this doc and with `frontend(dev)/resume` types if the UI calls resumeai directly.
5. **Deploy parity** — After `sam deploy`, confirm `LAMBDA_S3STORAGE_API_URL` / `LAMBDA_S3STORAGE_API_KEY` on the Lambda match a deployed s3storage stack that exposes **`POST /api/v1/uploads/resume`**.

## Documentation metadata

- Era: `9.x`
- Introduced in: `TBD` (fill with exact minor)
- Frontend bindings: list page files from `docs/frontend/pages/*.json`
- Data stores touched: PostgreSQL/Elasticsearch/MongoDB/S3 as applicable

## Endpoint/version binding checklist

- Add operation list with `introduced_in` / `deprecated_in` tags.
- Map each operation to frontend page bindings and hook/service usage.
- Record DB tables read/write for each operation.

