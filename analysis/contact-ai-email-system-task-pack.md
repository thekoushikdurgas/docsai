# Contact AI — 2.x Email System Task Pack

**Service:** `backend(dev)/contact.ai`  
**Era:** `2.x` — Email system  
**Status:** `analyzeEmailRisk` contract locked; stub live; HF JSON task validated

## Codebase file map (high-value)

Grounded in [`docs/codebases/contact-ai-codebase-analysis.md`](../codebases/contact-ai-codebase-analysis.md).

| Area | Paths (start here) | Notes |
| --- | --- | --- |
| Entrypoint | `backend(dev)/contact.ai/app/main.py` | FastAPI + Mangum wiring, middleware |
| AI utility endpoints | `backend(dev)/contact.ai/app/api/v1/endpoints/ai.py` | `POST /api/v1/ai/email/analyze` lives here |
| Model routing + JSON tasks | `backend(dev)/contact.ai/app/services/hf_service.py` | HF inference + Gemini fallback; JSON task mode |
| Schemas | `backend(dev)/contact.ai/app/schemas/ai_chat.py` | `ModelSelection` enum + response models |

---

## Contract track

- [ ] Lock `POST /api/v1/ai/email/analyze` request/response schema:
  - Request: `{"email": "<string, valid email>"}`
  - Response: `{"risk_score": <0-100>, "analysis": "<string>", "is_role_based": <bool>, "is_disposable": <bool>}`
- [ ] Align `AnalyzeEmailRiskInput` in GraphQL schema (`17_AI_CHATS_MODULE.md`) with REST schema.
- [ ] Confirm `LambdaAIClient.analyze_email_risk()` path is `/api/v1/ai/email/analyze` (not legacy `/gemini/email`).
- [ ] Document rate limit for email risk analysis endpoint (token bucket parameters).

### ModelSelection mapping risk (GraphQL ↔ REST)

The codebase analysis flags a mismatch risk: GraphQL uses legacy-style enum names, while REST maps to actual HF model IDs.

- [ ] Add/verify a mapping shim at the gateway boundary so `AnalyzeEmailRiskInput.model` invokes the intended HF model.

## Service track

- [ ] Implement `POST /api/v1/ai/email/analyze` in `app/api/v1/endpoints/ai.py`.
- [ ] Write `HFService.json_task()` prompt for email risk scoring (role-based check, disposable domain check).
- [ ] Validate HF API response against `EmailRiskAnalysisResponse` schema; handle malformed JSON from LLM.
- [ ] Add fallback to Gemini if HF JSON task fails for email risk analysis.
- [ ] Confirm email addresses are not logged or persisted in any table (privacy compliance).

## Surface track

- [ ] Design `EmailRiskBadge` component spec: shows risk score as colored badge (green/yellow/red) on contact email field.
- [ ] Define loading state (spinner on badge while fetching) and error state (tooltip on error).
- [ ] Add `useEmailRisk(email)` hook stub to dashboard (disabled until `5.x` full rollout).

### UI binding references

- `docs/frontend/contact-ai-ui-bindings.md`
- `docs/frontend/components.md` (for `EmailRiskBadge` inventory)

## Data track

- [ ] Confirm no `ai_chats` rows created by utility calls (stateless path).
- [ ] Document in `contact_ai_data_lineage.md`: email PII is passed to HF API; review HF data retention policy.
- [ ] Risk analysis result is transient (not persisted); document this in data lineage.

## Ops track

- [ ] Load test `POST /api/v1/ai/email/analyze` with p95 target < 2s.
- [ ] Confirm Lambda timeout is sufficient for HF JSON task (recommend 10–15s timeout).
- [ ] Add email risk endpoint to contact.ai Postman collection (`docs/media/postman/Contact AI Service.postman_collection.json`).

---

**References:**  
`docs/codebases/contact-ai-codebase-analysis.md` · `docs/backend/apis/17_AI_CHATS_MODULE.md` · `docs/frontend/contact-ai-ui-bindings.md`
