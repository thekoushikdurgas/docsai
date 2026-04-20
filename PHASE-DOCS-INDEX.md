# Phase documentation index (`0.x`–`11.x`)

Each numbered folder under `docs/` holds a phase **`index.json`** (machine-readable section list: `id`, `title`, `file`, `status`, `flow_refs`, `schema_refs`) and optional markdown stubs referenced by that JSON.

**Authoritative cross-cutting decisions:** [`DECISIONS.md`](DECISIONS.md) — keep phase docs aligned with this file; do not fork alternate patterns without updating it.

---

## Phase folders (product roadmap)

| Phase | Folder | Primary concern |
| ----- | ------ | ----------------- |
| 0 | [`0.Foundation and pre-product stabilization and codebase setup`](0.Foundation%20and%20pre-product%20stabilization%20and%20codebase%20setup/) | Vision, monorepo, CI, docs governance, foundational flows |
| 1 | [`1.Contact360 user and billing and credit system`](1.Contact360%20user%20and%20billing%20and%20credit%20system/) | Auth, orgs, credits, billing |
| 2 | [`2.Contact360 phone number and email system`](2.Contact360%20phone%20number%20and%20email%20system/) | Email / phone satellites |
| 3 | [`3.Contact360 contact and company data system`](3.Contact360%20contact%20and%20company%20data%20system/) | Connectra (sync.server), CRM entities, VQL, search |
| 4 | [`4.Contact360 Extension and Sales Navigator maturity`](4.Contact360%20Extension%20and%20Sales%20Navigator%20maturity/) | MV3 extension, LinkedIn / Sales Navigator capture |
| 5 | [`5.Contact360 AI workflows`](5.Contact360%20AI%20workflows/) | AI server, tools, RAG |
| 6 | [`6.Contact360 Reliability and Scaling`](6.Contact360%20Reliability%20and%20Scaling/) | SLOs, queues, resilience |
| 7 | [`7.Contact360 deployment`](7.Contact360%20deployment/) | ECS, env, release |
| 8 | [`8.Contact360 public and private apis and endpoints`](8.Contact360%20public%20and%20private%20apis%20and%20endpoints/) | REST/OpenAPI vs GraphQL policy, gateway |
| 9 | [`9.Contact360 Ecosystem integrations and Platform productization`](9.Contact360%20Ecosystem%20integrations%20and%20Platform%20productization/) | Integrations, platform |
| 10 | [`10.Contact360 campaign and sequence and template and builder system`](10.Contact360%20campaign%20and%20sequence%20and%20template%20and%20builder%20system/) | Campaign server, sequences |
| 11 | [`11.Lead generation and user recommendation engine`](11.Lead%20generation%20and%20user%20recommendation%20engine/) | Lead scoring, recommendations |

---

## Supporting doc hubs (not phase-numbered)

| Area | Path | Role |
| ---- | ---- | ---- |
| **Backend (satellites + gateway)** | [`backend/`](backend/) | Per-service `endpoints/*/AUTH-ENV.md`, `ROUTES.md`, `EVENTS-BOUNDARY.md`, `GATEWAY-PARITY.md`; [`backend/database/`](backend/database/) schemas |
| **Gateway package** | [`backend/endpoints/contact360.io/`](backend/endpoints/contact360.io/) | `GRAPHQL-SCHEMA.md`, `ROUTES.md`, `GATEWAY-BOUNDARY.md`, `PIPELINE.md` |
| **Codebases** | [`codebases/`](codebases/) | High-level repo/stack notes |
| **Frontend** | [`frontend/`](frontend/) | Dashboard patterns, extension design eras under [`frontend/extension/eras/`](frontend/extension/eras/) |
| **Tech** | [`tech/`](tech/) | e.g. `dashboard-graphql-vql.md`, `extension-git.md` |
| **Flowcharts** | [`flowchart/`](flowchart/) | Visual flows (e.g. extension capture, contacts VQL) |
| **PRD / product** | [`prd/`](prd/) | Architecture and requirements snapshots (large; use search) |
| **Scripts** | [`scripts/`](scripts/) | Tooling (e.g. Apollo table helpers) |
| **Nested `docs/docs/`** | [`docs/docs/`](docs/docs/) | Long-form UI backlogs (e.g. contacts filter / VQL) |

---

## Cross-links (frequently used)

- **Contacts list / VQL UI backlog:** [`docs/docs/contacts-filter-vql-ui.md`](docs/contacts-filter-vql-ui.md) · Phase 3 pointer: [`3.Contact360 contact and company data system/52-app-contacts-vql-filters.md`](3.Contact360%20contact%20and%20company%20data%20system/52-app-contacts-vql-filters.md)
- **Extension UX eras (preview, auth, side panel):** [`frontend/extension/eras/`](frontend/extension/eras/) · Flow: [`flowchart/extension-capture.md`](flowchart/extension-capture.md)
- **GraphQL schema (generated reference):** [`backend/endpoints/contact360.io/GRAPHQL-SCHEMA.md`](backend/endpoints/contact360.io/GRAPHQL-SCHEMA.md)

---

## How to work with phase `index.json`

1. Open `docs/<phase folder>/index.json`.
2. Sections list **`file`** paths (often relative stubs like `60-extension/...` or `../backend/...`).
3. **`status`:** `stub` vs `populated` indicates whether the markdown exists and is filled vs placeholder.
4. **`flow_refs`:** ties to foundation flow docs under phase `0` (e.g. `flow5` = extension capture).
5. When adding a new concern, prefer **a new section** in `index.json` + one markdown file rather than duplicating content across phases.

---

## Documentation maintenance backlog (small tasks)

Work items below are **independent**; batch them by theme (gateway, Connectra, extension) in a single PR when possible.

### Governance & index hygiene

1. For each phase `0`–`11`, verify `index.json` **`file`** paths resolve (no broken relative links).
2. Mark sections **`populated`** only after a real outline + owner + last-reviewed date in the markdown front matter or first paragraph.
3. Keep [`DECISIONS.md`](DECISIONS.md) in sync when changing satellite HTTP contracts or gateway GraphQL fields.

### Phase 0 – Foundation

4. List CI entrypoints and doc update gates in one short `README`-style file under phase 0 (if missing).
5. Cross-link phase 0 flows to [`flowchart/`](flowchart/) diagrams where duplicates exist; avoid three sources of truth.

### Phase 3 – Contact & company data

6. Confirm [`backend/database/sync.server-schema.md`](backend/database/sync.server-schema.md) mentions batch-upsert response fields (`contact_uuids`, `company_uuids`) and error semantics.
7. Add or update a **single** Postman note for `POST /contacts/batch-upsert` / `POST /companies/batch-upsert` response shape (align with `EC2/sync.server/docs/postman/`).

### Phase 4 – Extension & Sales Navigator

8. Replace stub `63-sales-navigator/*` sections progressively: start with **capture → gateway → extension.server → Connectra** sequence (mirror [`DECISIONS.md`](DECISIONS.md) § Sales Navigator / extension satellite).
9. Document **chrome.storage** keys for `c360_last_capture_preview` and preview merge behavior (see [`frontend/extension/eras/era-04-scrape-preview.md`](frontend/extension/eras/era-04-scrape-preview.md)).
10. Align [`flowchart/extension-capture.md`](flowchart/extension-capture.md) with current GraphQL mutation fields (`contactUuids`, `savedContacts`, etc.).

### Phase 8 – APIs

11. Refresh [`backend/endpoints/contact360.io/public-private.md`](backend/endpoints/contact360.io/public-private.md) if GraphQL vs REST split changes.
12. Regenerate or diff [`GRAPHQL-SCHEMA.md`](backend/endpoints/contact360.io/GRAPHQL-SCHEMA.md) when Strawberry types change (automate in `commands.txt` or CI if not already).

### `docs/backend`, `docs/tech`, `docs/frontend`

13. **Satellite parity:** For each EC2 service, ensure `SATELLITE-PARITY.md` / `GATEWAY-PARITY.md` matches [`DECISIONS.md`](DECISIONS.md).
14. **Tech:** Keep [`tech/dashboard-graphql-vql.md`](tech/dashboard-graphql-vql.md) aligned with `vql_converter.py` and Connectra filter docs.
15. **Frontend:** Component standards and tokens under [`frontend/docs/`](frontend/docs/) — link from phase 4 popup/side panel stubs when those sections graduate from stub.

### `docs/prd` & `docs/codebases`

16. Treat **`prd/`** as historical / narrative; **do not** duplicate satellite route tables here — link to `backend/endpoints/*` instead.
17. **`codebases/`** — one-page-per-repo overview; update only when default branch or deploy URL changes.

### `docs/scripts` & tooling

18. Document any doc generation command in [`scripts/`](scripts/) README (e.g. schema dump, Postman export).

### Verification checklist (periodic)

19. Run link check on `docs/**/*.md` (or spot-check critical paths quarterly).
20. After major features, update **this file’s** cross-links and **DECISIONS** in the same release cycle.

---

*Index file last updated: 2026-04-19 (master-plan vertical slices: Phase 0 README, deployment matrix, flows reconciled, satellite parity, observability baseline, slice READMEs + runbooks).*
