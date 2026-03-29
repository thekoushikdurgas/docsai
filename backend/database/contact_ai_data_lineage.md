# Contact AI Data Lineage

**Service:** `backend(dev)/contact.ai`  
**Era relevance:** `0.x`–`10.x`  
**Primary store:** PostgreSQL (`ai_chats` table, shared with appointment360)  
**Secondary stores:** Hugging Face Inference (stateless, external); Gemini API (fallback, external)

---

## Table: `ai_chats`

| Column | Type | Notes |
| --- | --- | --- |
| `uuid` | UUID (PK) | Generated on insert; primary chat identifier |
| `user_id` | VARCHAR / UUID | FK → `users.uuid`; enforces per-user isolation |
| `title` | VARCHAR(255) | Chat display name; mutable via PUT |
| `messages` | JSONB | Ordered array of `{sender, text, contacts[]}` messages |
| `created_at` | TIMESTAMP | Auto-set by DB default; immutable |
| `updated_at` | TIMESTAMP | Auto-updated via ORM on PUT |

**DDL source:** `docs/backend/tables/ai_chats.sql`  
**Additive migration:** `docs/backend/migrations/add_ai_chats.sql`

---

## JSONB message element schema

```json
{
  "sender": "user | ai",
  "text": "<string, max 10 000 characters>",
  "contacts": [
    {
      "uuid": "<contact uuid optional>",
      "firstName": "", "lastName": "", "title": "",
      "company": "", "email": "",
      "city": "", "state": "", "country": ""
    }
  ]
}
```

**Constraints:**
- Max 100 messages per chat (enforced in `AIChatService`).
- `sender` must be `"user"` or `"ai"` (application-level check).
- `contacts` array is nullable / may be absent for user-turn messages.
- No DB-level JSON schema constraint — strict validation is application-only.

---

## Data flow: chat message lifecycle

```
Dashboard UI
  │
  ▼ GraphQL mutation: sendMessage
Appointment360 (contact360.io/api)
  │ LambdaAIClient → POST /api/v1/ai-chats/{chat_id}/message
  ▼
contact.ai (FastAPI Lambda)
  ├── AIChatRepository.get(chat_id, user_id)   → READ ai_chats
  ├── Validate ownership (user_id match)
  ├── Append user message to messages[]
  ├── HFService.chat_completion(messages, model) → Hugging Face API
  │     └── Fallback → Gemini API (on HF failure)
  ├── Append AI reply to messages[]
  ├── AIChatRepository.update(chat_id, messages) → WRITE ai_chats
  └── Return updated AIChat → Appointment360 → GraphQL → UI
```

---

## Data flow: utility AI calls (stateless)

```
Dashboard UI
  │
  ▼ GraphQL mutation: analyzeEmailRisk | generateCompanySummary | parseContactFilters
Appointment360
  │ LambdaAIClient → POST /api/v1/ai/{email/analyze | company/summary | parse-filters}
  ▼
contact.ai (FastAPI Lambda)
  ├── HFService.json_task(prompt, schema) → Hugging Face API (JSON mode)
  └── Return structured response (no DB write)
```

**Note:** Utility AI calls are fully stateless — no `ai_chats` rows are created or modified.

---

## Cross-service data lineage

| Source | Data | Destination | Notes |
| --- | --- | --- | --- |
| appointment360 | `user_id` (from JWT context) | contact.ai | Passed via `X-User-ID` header |
| contact.ai | Chat messages | PostgreSQL `ai_chats` | Persisted on every send/update |
| contact.ai | Inference prompt | Hugging Face | Stateless; no PII stored at HF |
| contact.ai | Fallback prompt | Gemini API | Stateless; PII considerations apply |
| contact.ai | `contacts[]` in messages | PostgreSQL `ai_chats` | Contact data embedded in JSONB |
| Connectra | Contact search results | contact.ai (future) | Potential: AI-driven contact search |

---

## Era lineage concerns

### 0.x — Foundation
- Schema baseline: `ai_chats` DDL created and version-controlled.
- Migration file available for environments upgrading from appointment360 without `ai_chats`.
- No runtime lineage until `5.x`.

### 1.x — User/Billing
- `user_id` FK integrity: ensure `ai_chats.user_id` references valid `users.uuid`.
- If a user account is deleted, cascade strategy must be defined (delete chats or archive).
- No new columns; lineage concern is referential integrity only.

### 2.x — Email System
- `analyzeEmailRisk` utility call: email string passed to HF API.
- Email addresses are PII — confirm HF API data retention policy.
- No `ai_chats` rows created for utility calls.
- Risk score response stored transiently in GraphQL resolver; not persisted.

### 3.x — Contact/Company Data
- `parseContactFilters` output maps to Connectra VQL filter fields.
- Parsed filter output is transient; not stored in `ai_chats`.
- `contacts[]` in message JSONB must align with Connectra contact index fields.
- `generateCompanySummary`: company name + industry passed to HF; no storage.

### 4.x — Extension / Sales Navigator
- SN contact objects may populate `messages.contacts[]` JSONB.
- SN contact provenance (source = `sales_navigator`) should be a field in JSONB contacts if lineage traceability is needed.

### 5.x — AI Workflows (primary)
- Full `ai_chats` table in production.
- Message history lineage: messages ordered chronologically; max 100 enforced.
- `ModelSelection` enum maps to specific HF model versions — model version must be recorded in message metadata for reproducibility.
- Model version drift: if HF model is retrained/replaced, historical chat responses are no longer reproducible.

### 6.x — Reliability and Scaling
- Chat TTL / archival policy: define max chat retention period.
- Idempotency: concurrent `POST /message` calls on the same `chat_id` may cause duplicate messages — needs optimistic locking or version check.
- Stale chat detection: last `updated_at` threshold for cleanup.

### 7.x — Deployment / Governance
- Audit trail: all `ai_chats` create/delete events should emit to `logs.api`.
- Retention policy: GDPR/CCPA right-to-erasure must cascade to `ai_chats`.
- Role-based access: which plans/roles can create chats vs. only use utility endpoints.

### 8.x — Public/Private APIs
- API usage counters per user/key for AI endpoints.
- Rate limit metadata (`Retry-After`, `X-RateLimit-Remaining`) must align with token bucket state.
- No new columns in `ai_chats`; usage counts in separate `api_usage` table or metadata.

### 9.x — Ecosystem Integrations
- Webhook delivery records for AI results should reference source `chat_id`.
- Integration audit entries may reference `ai_chats.uuid` for traceable AI-assisted actions.

### 10.x — Email Campaign
- AI-generated email content should be stored with campaign records (not only in `ai_chats`).
- Compliance evidence: log which AI model, which prompt template, and which output was used for each campaign email.
- If AI generation is audited, `ai_chats.uuid` or a separate `campaign_ai_log` table provides the audit anchor.

---

## Known lineage risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| JSONB `messages` schema drift | Silent data corruption | Add JSON schema validation in `5.x` |
| No model version in message metadata | Loss of reproducibility | Add `model_version` to message JSONB |
| PII in HF/Gemini API calls | Data privacy exposure | Review HF/Gemini data retention policies |
| No cascade delete for user accounts | Orphaned chat rows | Define cascade strategy in `7.x` |
| Concurrent message appends | Duplicate messages | Add optimistic lock (version column) in `6.x` |
| No chat archival TTL | Unbounded storage growth | Implement TTL cleanup job in `6.x` |

---

## References

- `docs/codebases/contact-ai-codebase-analysis.md`
- `docs/backend/apis/17_AI_CHATS_MODULE.md`
- `docs/backend/tables/ai_chats.sql`
- `docs/backend/migrations/add_ai_chats.sql`
- `docs/backend/apis/CONTACT_AI_ERA_TASK_PACKS.md`
- `backend(dev)/contact.ai/app/models/ai_chat.py`
- `backend(dev)/contact.ai/app/repositories/ai_chat.py`
