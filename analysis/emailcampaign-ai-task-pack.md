# Email Campaign Service — Era 5.x Task Pack
## Contact360 AI Workflows

### Context
Era `5.x` integrates AI-assisted content generation into Contact360. For the email campaign service this means AI-generated template bodies, AI subject-line suggestions, optimal send-time prediction, and recipient personalization beyond name/email.

---

## Track A — Contract

| Task | Description | Owner |
| --- | --- | --- |
| A-5.1 | Define AI template generation API contract: prompt-in → HTML-out with variable placeholders | Backend + AI |
| A-5.2 | Specify subject-line suggestion API: campaign context → N ranked subjects | Backend + AI |
| A-5.3 | Document personalization variable schema beyond `{FirstName}`, `{LastName}` | Backend + Product |

## Track B — Service

| Task | Description | Owner |
| --- | --- | --- |
| B-5.1 | Add `POST /templates/generate` endpoint: accepts prompt, calls AI service, stores output as template | Backend |
| B-5.2 | Add `POST /templates/:id/suggest-subject` endpoint: calls AI with template content | Backend |
| B-5.3 | Extend `TemplateData` struct with AI-personalization fields: `{Company}`, `{Title}`, `{Industry}` | Backend |
| B-5.4 | Inject personalization fields from Connectra `Contact` fields at render time | Backend |
| B-5.5 | Optimal send-time: expose `suggested_send_at TIMESTAMP` field on campaign, computed by AI model | Backend |

## Track C — Surface

| Task | Description | Owner |
| --- | --- | --- |
| C-5.1 | Template builder: "Generate with AI" button with prompt textarea; streams AI response into editor | Frontend |
| C-5.2 | Subject line input: "Suggest" button shows a dropdown of N AI-proposed subjects | Frontend |
| C-5.3 | Campaign wizard: "AI-optimized send time" checkbox with suggested timestamp | Frontend |
| C-5.4 | AI confidence badge on auto-generated templates ("AI draft — review before send") | Frontend |

## Track D — Data

| Task | Description | Owner |
| --- | --- | --- |
| D-5.1 | Add `is_ai_generated BOOLEAN`, `ai_prompt TEXT`, `ai_model TEXT` to `templates` table | Backend |
| D-5.2 | Store `personalization_fields JSONB` on `campaigns` for extended variable resolution | Backend |

## Track E — Ops

| Task | Description | Owner |
| --- | --- | --- |
| E-5.1 | AI service base URL env var (`AI_SERVICE_URL`) in campaign service | DevOps |
| E-5.2 | Rate-limit AI generation calls; add timeout and graceful fallback | Backend |

---

## Completion gate
- [ ] "Generate with AI" produces a valid HTML template stored in S3.
- [ ] Personalization variables from Connectra contact fields render correctly in preview.
- [ ] Subject suggestions appear within 3 seconds in UI.
