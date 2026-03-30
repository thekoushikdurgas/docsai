# Documentation content summary and maintenance status
_Exported on 3/24/2026 at 20:12:59 GMT+5:30 from Cursor (2.6.21)_

---

**User**

Read these files from d:\code\ayan\contact\docs and summarize content (first 60 lines each):

1. docs\0. Foundation and pre-product stabilization and codebase setup\0.0 — Pre-repo baseline.md
2. docs\1.  Contact360 user and billing and credit system\1.0 — User Genesis.md
3. docs\2. Contact360 email system\2.0 — Email Foundation.md
4. docs\2. Contact360 email system\2.10 — Email System Exit Gate.md  
5. docs\backend\apis\README.md
6. docs\codebases\README.md
7. docs\frontend\README.md
8. docs\media\DASHBOARD_ALIGNMENT.md
9. docs\media\ENDPOINTS_AUDIT.md
10. docs\media\TASK_BREAKDOWN.md

For each file: what does it contain, is it actively maintained spec content, is it placeholder/stub, or is it stale/orphaned content?

---

**Cursor**


Reading the first 60 lines of each listed file.




Here is a concise summary of the **first 60 lines** of each file and a **maintenance / role** judgment.

---

### 1. `docs\0. Foundation and pre-product stabilization and codebase setup\0.0 — Pre-repo baseline.md`

**What it contains:** Version **0.0** doc. Front matter says **placeholder — scope not yet approved**; explains pre-monorepo baseline and that **`0.1.0`** in `docs/versions.md` is the first real Foundation release. Scope, owners, exclusions, DoD, exit to `0.1.0`, and **Mermaid** five-track + runtime flowcharts.

**Classification:** **Placeholder / stub** — explicitly labeled; structural template more than an approved product spec.

---

### 2. `docs\1.  Contact360 user and billing and credit system\1.0 — User Genesis.md`

**What it contains:** **Version 1.0** — **Status: released**, “active MVP baseline.” Summary: signup → finder/verifier/results; auth, credits, engines, results. Roadmap pointers (`1.1`, `1.2`, etc.), owner **Product + Core Engineering**. Same five-track delivery model and runtime-focus Mermaid as other version files.

**Classification:** **Active spec / canonical version doc** for a shipped era (released baseline).

---

### 3. `docs\2. Contact360 email system\2.0 — Email Foundation.md`

**What it contains:** **Version 2.0** — **Status: planned**, target **TBD**. “Connectra intelligence”: VQL, enrichment, dedup, advanced search UX; roadmap `2.1`–`2.4`; owner Search/Data Engineering. Same execution-pack structure and diagrams.

**Classification:** **Active planned spec** — real scope text, not an empty stub; timing still TBD.

---

### 4. `docs\2. Contact360 email system\2.10 — Email System Exit Gate.md`

**What it contains:** **Version 2.10** — **Status: planned**; says scope is filled in when a stage is approved and `docs/versions.md` is updated. Flowchart node: **“2.10.x placeholder — Connectra era buffer before 3.x.”** Same boilerplate tracks/diagrams as other minors.

**Classification:** **Placeholder / buffer stub** — intentional holding pattern before 3.x, not detailed feature spec yet.

---

### 5. `docs\backend\apis\README.md`

**What it contains:** **GraphQL modules** index for the “Appointment GraphQL API”: instructions to add modules, **table of 29 module markdown files** (Auth through Resume AI), then **Module Index** sections (Core, Data, Communication…). Points to `TASK_BREAKDOWN_APIS.md` for maintenance tasks.

**Classification:** **Actively maintained navigation / index** for backend API module docs (living doc if modules change).

---

### 6. `docs\codebases\README.md`

**What it contains:** **“Codebase Deep Analyses”** — lists named deep-dive markdowns (logs.api, s3storage, Connectra, jobs, email campaign, contact.ai, appointment360, salesnavigator, mailvetter) and where **era task packs** live. **Usage guideline:** update analysis when contracts change; sync `architecture.md`, `roadmap.md`, `versions.md`, `governance.md`, `docsai-sync.md`, and `docs/backend/` as needed.

**Classification:** **Actively maintained** index + process note (stale only if those linked analyses stop being updated).

---

### 7. `docs\frontend\README.md`

**What it contains:** **Supplementary frontend** inventory (JSON page metadata, CSV, design/engineering refs). Canonical code under `contact360.io/`; pointer to **`docs/frontent.md`** (typo for `frontend`). **Era table** `0.x`–`10.x` with themes and UI surfaces. **Tri-surface** contract (`root`, `app`, `admin`). **Contents** table listing `components.md`, `design-system.md`, `pages/`, `excel/`, etc.

**Classification:** **Actively maintained** map and conventions; worth fixing the `frontent.md` link when editing is allowed.

---

### 8. `docs\media\DASHBOARD_ALIGNMENT.md`

**What it contains:** **Dashboard (`/dashboard`)** alignment across `media/pages`, `media/endpoints`, `media/postman`, `media/relationship`. Four GraphQL operations, canonical endpoint JSON files, relationship by-page file, Postman `contact360.json` **mapping_id** table (with example UUIDs), sync scripts (`sync_pages_to_relationships.py`, `normalize_media_indexes`), and spec references.

**Classification:** **Concrete, maintained alignment spec** for one page; could become **stale** if dashboard operations or Postman IDs change without updating this file.

---

### 9. `docs\media\ENDPOINTS_AUDIT.md`

**What it contains:** **Audit header**: counts from `endpoints_index.json` vs `contact360.io/api` — e.g. **156** documented endpoint files, **154** paths, **128** backend ops in audit, **128** matched, **0** missing docs. Then a long **sample** list of operation names (alphabetically).

**Classification:** **Snapshot / audit artifact** tied to a point in time — **useful but can go stale** whenever the API or generated index changes unless regenerated. Not a narrative “how to” spec; more **inventory audit**.

---

### 10. `docs\media\TASK_BREAKDOWN.md`

**What it contains:** **Media alignment** master plan: phases **0–3+** with tables (task, description, **Status**: Done / Deferred / Pending). Covers conventions, `media/endpoints`, Postman, relationship JSON, optional follow-ups (e.g. only 4 Postman mappings of 156 endpoints).

**Classification:** **Actively maintained project checklist** — shows what’s done vs pending; **stale** if statuses aren’t updated as work proceeds.

---

### Quick matrix

| File | Role |
|------|------|
| `0.0 — Pre-repo baseline.md` | Placeholder (explicit) |
| `1.0 — User Genesis.md` | Released era spec |
| `2.0 — Email Foundation.md` | Planned era spec |
| `2.10 — Email System Exit Gate.md` | Placeholder / buffer |
| `backend/apis/README.md` | Living index |
| `codebases/README.md` | Living index + sync process |
| `frontend/README.md` | Living map + conventions |
| `DASHBOARD_ALIGNMENT.md` | Focused alignment spec |
| `ENDPOINTS_AUDIT.md` | Point-in-time audit snapshot |
| `TASK_BREAKDOWN.md` | Living task tracker (if updated) |

Absolute paths used above: under `d:\code\ayan\contact\docs\` as listed in your query.

