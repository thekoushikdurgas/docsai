# Contact AI — 4.x Extension / Sales Navigator Task Pack

**Service:** `backend(dev)/contact.ai`  
**Era:** `4.x` — Extension and Sales Navigator maturity  
**Status:** No new contact.ai endpoints; SN contact objects tested in `messages.contacts` JSONB

---

## Contract track

- [ ] Confirm no new Contact AI endpoints are introduced in `4.x`.
- [ ] Validate `messages.contacts[]` JSONB `ContactInMessage` schema is compatible with SN profile objects.
- [ ] Document SN contact provenance: if needed, add `source` field to `ContactInMessage` (e.g. `"source": "sales_navigator"`).
- [ ] Confirm extension CSP (Content Security Policy) allows requests to `LAMBDA_AI_API_URL` domain.

## Service track

- [ ] Test SN contact object fields against `ContactInMessage` schema:
  - `uuid`, `firstName`, `lastName`, `title`, `company`, `email`, `city`, `state`, `country`
- [ ] Confirm SN contacts stored via `ai_chats.messages` JSONB round-trip without field loss.
- [ ] Optional: surface AI context panel in extension popup if SN contact is selected and `ENABLE_AI_CHAT=true`.

## Surface track

- [ ] Optional: add AI context action in extension SN contact flyout: "Open in AI Chat".
- [ ] If implemented: extension popup sends SN contact data as initial message context to new chat.
- [ ] Define UX: extension AI panel is optional; main AI chat page (`/app/ai-chat`) remains canonical.

## Data track

- [ ] Confirm SN contact fields are not PII-leaked to HF/Gemini unless explicitly included in chat message prompt.
- [ ] Review prompt construction: only include SN contact fields that are explicitly referenced in user query.
- [ ] Document in `contact_ai_data_lineage.md`: SN contact provenance in `messages.contacts[]` JSONB.

## Ops track

- [ ] CSP review for extension: add `LAMBDA_AI_API_URL` to allowed `connect-src` origins.
- [ ] Test extension flow (optional): SN contact → extension popup → AI chat context → message sent → response received.
- [ ] No new Lambda timeout or memory changes expected in `4.x`.

---

**References:**  
`docs/codebases/contact-ai-codebase-analysis.md` · `docs/frontend/contact-ai-ui-bindings.md`
