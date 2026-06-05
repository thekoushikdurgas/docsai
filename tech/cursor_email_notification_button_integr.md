# Email notification button integration
**User**

so i thick that when user chick DOM Path: aside.c360-.aved-.earche.-panel > div.c360-.aved-.earche.-panel__body > ul.c360-.aved-.earche.-panel__li.t > li.c360-.aved-.earche.-panel__item > div.c360-icon.-container > button.c360-btn c360-btn--gho.t c360-btn--icon c360-.aved-.earche.-panel__item-notify
Position: top=121px, left=1202px, width=40px, height=40px
React Component: motion.aside
HTML Element: <button type="button" class="c360-btn c360-btn--ghost c360-btn--icon c360-saved-searches-panel__item-notify" aria-label="Enable daily email for fgnfgn" aria-pressed="false" data-cursor-element-id="cursor-el-3608"></button>  and open a popup model to give two options , one that imediately send a mall so you only send a email imediately , and another daily  email sent , Learn, understand, and analyze deeply, breaking tasks into smaller steps 

---

**Cursor**

Analyzing the current bell behavior and what exists for immediate vs daily email sends.


Your intuition is right about **what should happen in the product**, but **what the bell does today** is simpler: one click toggles **daily** subscription only—there is **no modal** and **no “send now”** path.

---

## What happens today when the user clicks the bell

**DOM:** `button.c360-saved-searches-panel__item-notify` in [`SavedSearchesMenu.tsx`](contact360.io/app/src/components/feature/saved-searches/SavedSearchesMenu.tsx).

**Click handler (current):**

```570:573:contact360.io/app/src/components/feature/saved-searches/SavedSearchesMenu.tsx
                    onClick={(e) => {
                      e.stopPropagation();
                      void handleToggleJobEmailNotification(s.id, s.name);
                    }}
```

That calls GraphQL `toggleJobEmailNotification(savedSearchId)` → API → email.server `POST/PUT /client-configs/` with:

- `email` = logged-in user (from auth, not typed in UI)
- `is_active` = toggled or set `true`
- `template_id` = `daily-jobs-v1.html`
- `filter` = copy of that saved search’s `filters` JSON

**No popup.** Bell state = daily subscription on/off for **one** saved search per email (unique email row on email.server).

---

## What you want (product flow)

```mermaid
flowchart TD
    BellClick[User clicks bell on saved search row]
    Modal[Modal: Email options]
    BellClick --> Modal
    Modal --> SendNow[Send email now]
    Modal --> Daily[Daily email]
    SendNow --> Once[One SES send with current filter snapshot]
    Daily --> Config[Upsert client-config is_active true]
    Config --> Cron[Existing 10:00 IST cron]
```

| Option | User expectation | Fits current backend? |
|--------|------------------|------------------------|
| **Send email now** | One immediate digest for **this** saved search’s filters | **No dedicated API** — only bulk cron logic |
| **Daily email** | Subscribe; same digest every day at cron time | **Yes** — existing `toggleJobEmailNotification` + cron |

---

## Step-by-step: “Daily email” (mostly done)

### 1. UI (today)
- Bell toggles directly (you’d change to: modal → user picks “Daily” → call existing mutation).

### 2. App
- `emailService.toggleJobEmailNotification(savedSearchId)` — already wired.

### 3. API
- Validates hire_signal + ownership, writes `client-configs` ([`job_email_notification.py`](contact360.io/api/app/graphql/modules/email/job_email_notification.py)).

### 4. email.server
- Stores config; [`ProcessDailyEmails`](EC2/email.server/internal/tasks/cron_manager.go) runs daily for `is_active = true`.

### 5. Caveats (unchanged)
- One config per email; picking daily on another search **replaces** the filter.
- Cron OpenSearch query uses only **part** of `listFilters` (titles, employment types, company industries)—not full UI parity.
- `signalTimePreset: "new_7d"` is not applied in cron like the app.

**Modal change for daily:**  
- If already subscribed to **this** search → could show “Turn off daily” or keep toggle in modal.  
- If subscribed to **another** search → “Daily” should warn that it will switch subscription.

---

## Step-by-step: “Send email now” (needs new work)

Today there is **no** HTTP route like `POST /client-configs/send-now`. Sending is only inside `ProcessDailyEmails()`, which:

1. Loads **all** active configs  
2. For each: `FetchTopJobs(filter)` → render template → SES  

Manual test exists: [`EC2/email.server/scripts/test_cron/main.go`](EC2/email.server/scripts/test_cron/main.go) calls `ProcessDailyEmails()` for the whole DB—not per user from the app.

`POST /transactional/send` on email.server is **generic** (to, subject, html_body, text_body)—the **gateway** would have to build the digest HTML itself or duplicate cron logic. That’s the wrong layer unless you only send a simple text email.

### Recommended architecture for “send now”

**A. email.server (best place for digest logic)**

1. Extract from cron something like:  
   `SendDailyDigestForFilter(ctx, email, filter map, templateID) error`  
   (same steps as one loop iteration in `ProcessDailyEmails`).

2. New authenticated route, e.g.:  
   `POST /client-configs/send-now`  
   Body: `{ "email", "filter", "template_id" }`  
   - Does **not** require `is_active`  
   - Does **not** have to create/update `client_email_configs` (unless you want audit history)

**B. contact360.io/api**

3. New GraphQL mutation, e.g. `sendJobEmailNotificationNow(savedSearchId: ID!)`  
   - Same checks as `toggleJobEmailNotification` (auth, hire_signal, owner, filters)  
   - Load `saved_search.filters`  
   - Call `EmailServerClient.send_job_digest_now(...)`  

**C. contact360.io/app**

4. New modal component (pattern like [`HiringSignalsExportModal`](contact360.io/app/src/components/feature/hiring-signals/HiringSignalsExportModal.tsx) or existing [`SaveSearchNameModal`](contact360.io/app/src/components/feature/saved-searches/SavedSearchesMenu.tsx) in the same file).

5. Bell click → `setEmailNotifyModalSearch({ id, name })` instead of `handleToggleJobEmailNotification`.

6. Modal actions:  
   - **Send now** → `sendJobEmailNotificationNow` → toast “Email sent” / error from SES/OpenSearch  
   - **Daily email** → `toggleJobEmailNotification` (enable path; optional third row “Turn off daily” if already active)

7. Loading/disabled per action; keep `trapFocus` on drawer like save modal.

---

## UI / UX details to decide

1. **Bell when daily is already on for this row**  
   - Open modal with: “Send now” + “Turn off daily” (instead of “Enable daily”)?  
   - Or keep bell as off-toggle and use modal only when not subscribed?

2. **Send now without subscribing**  
   - Should not flip `is_active` or change bell unless user also chose daily.

3. **Empty results**  
   - Cron skips send if 0 jobs; “send now” should toast “No matching jobs” instead of silent skip.

4. **Rate limits**  
   - Consider cooldown per user (e.g. one “send now” per 5 minutes) to avoid SES abuse.

5. **Popover saved searches**  
   - Still panel-only for bell; modal would follow same rule.

---

## Implementation task list (ordered)

| # | Layer | Task |
|---|--------|------|
| 1 | email.server | Refactor `ProcessDailyEmails` → shared `sendDigest(email, filter, templateID)` |
| 2 | email.server | Add `POST /client-configs/send-now` (or `/digests/send`) |
| 3 | api | `EmailServerClient.send_job_digest_now()` |
| 4 | api | GraphQL `sendJobEmailNotificationNow` mutation |
| 5 | app | `emailService.sendJobEmailNotificationNow()` |
| 6 | app | `SavedSearchEmailNotifyModal` + wire bell → open modal |
| 7 | app | Wire “Daily” to existing toggle; update bell/`jobEmailNotificationConfig` after |
| 8 | qa | Verify SES, OpenSearch, filter with real saved search “fgnfgn” |
| 9 | docs | Note filter parity limits for both paths |

---

## Summary

- **Today:** Bell = direct **daily** subscribe/unsubscribe via `client-configs`; no modal, no immediate send.  
- **Your design:** Bell → **modal** with **Send now** (new backend path) and **Daily email** (reuse current mutation + cron).  
- **Daily** is ~80% built; **Send now** needs a new email.server endpoint plus one GraphQL mutation and the modal in the app.

I'm in **Ask mode**, so I can’t implement this. If you want it built, switch to **Agent mode** and say whether “Send now” should work without creating a `client-config` row and whether the bell should still show daily on/off state after using only “Send now.”

---

**User**

@EC2/scraper.server read this codebase and implement @EC2/email.server  in @EC2/scraper.server  and also create a worker to check in postgress database ClientEmailConfig table , all new job coloumn data if activated , this active saved filtes according new job we receied that job imediated send to user email , so add another option for new jobs to send new job imediately . Learn, understand, and analyze deeply, breaking tasks into smaller steps

---

**Cursor**

Exploring scraper.server and how it relates to email.server and job ingestion so we can plan immediate "new job" notifications.


You are asking for a **third notification mode**: when **new jobs** land in OpenSearch (from `scraper.server`), immediately email users whose **active** saved-search filters match those jobs. That is different from today’s **daily cron** and the planned **“send now”** one-shot.

Below is a structured read of the codebases and a practical build plan. (Ask mode — no edits.)

---

## 1. What exists today

### scraper.server (Python, Celery, OpenSearch)

| Piece | Role |
|--------|------|
| [`queueing/tasks.py`](EC2/scraper.server/queueing/tasks.py) | Celery task `scrape.process_job` runs scrapes |
| [`scraper/scrape_runner.py`](EC2/scraper.server/scraper/scrape_runner.py) | Skips jobs already in OS via `is_job_duplicate` → `job_exists(linkedin_job_id)` |
| [`storage/scrape_job_store.py`](EC2/scraper.server/storage/scrape_job_store.py) `append_results` | Indexes **new** jobs with `bulk_index_jobs` → index `linkedin_jobs` (config) |
| [`storage/opensearch_client.py`](EC2/scraper.server/storage/opensearch_client.py) | Job mapping: `title`, `company_name`, `employment_type`, `industries`, `posted_at`, `linkedin_job_id`, etc. |

**Important:** Only jobs that were **not** already in the jobs index are scraped and appended. Those are the right candidates for “new job” alerts.

### email.server (Go, PostgreSQL, OpenSearch, SES)

| Piece | Role |
|--------|------|
| [`ClientEmailConfig`](EC2/email.server/internal/models/client_email_config.go) | `email`, `is_active`, `template_id`, `filter` (JSONB) — **one row per email** |
| [`router.go`](EC2/email.server/internal/api/router.go) | CRUD `POST/GET/PUT /client-configs/` |
| [`cron_manager.go`](EC2/email.server/internal/tasks/cron_manager.go) | Daily 10:00 IST: active configs → `FetchTopJobs(filter)` → SES |
| OpenSearch URL | Uses `linkedin_jobs_index` (may differ from scraper’s `linkedin_jobs` in `.env` — **must be aligned in prod**) |

### contact360.io app + API

- Bell → `toggleJobEmailNotification` → writes `client-configs` with full hire-signal `filters` JSON.
- No modal yet for “send now” / “instant on new jobs”.
- `is_active` today effectively means **daily digest** only.

---

## 2. What you want (three notification behaviors)

```mermaid
flowchart LR
    subgraph modes [User choices per saved search]
        A[Send email now]
        B[Daily digest]
        C[Email me on new matching jobs]
    end
    A --> Once[One SES send snapshot]
    B --> Cron[email.server cron 10:00 IST]
    C --> Worker[scraper worker after index]
```

| Mode | Trigger | Storage |
|------|---------|---------|
| **Send now** | User clicks in modal | No schedule; optional one-off API |
| **Daily** | Cron | `is_active` + `filter` (today) |
| **New jobs** | Each new doc in OS after scrape | Needs **new flag** on config (see below) |

`ClientEmailConfig` cannot express “instant on new jobs” with only `is_active` — that flag is already used for **daily** cron.

---

## 3. Core design decision: where should the worker live?

You asked to “implement email.server in scraper.server”. Realistically:

| Approach | Pros | Cons |
|----------|------|------|
| **A. Logic in scraper, call email.server HTTP** | New jobs detected at source; no polling all jobs | Need new email.server endpoints; network coupling |
| **B. Logic in email.server, scraper only enqueues job IDs** | Single place for SES + templates | email.server must consume a queue; scraper still publishes events |
| **C. Shared Postgres read in scraper + SES in Python** | Fast to wire in scraper worker | Duplicates Go digest/SES/template logic |

**Recommended: A + B hybrid**

1. **scraper.server** — after indexing, enqueue Celery task with **list of newly indexed job docs** (or `linkedin_job_id`s).
2. **email.server** — owns matching, templating, SES (refactor `ProcessDailyEmails` into reusable `SendDigest(...)` + new `POST /notifications/match-and-send` or internal queue consumer).
3. **Same PostgreSQL** — scraper gets read-only `DATABASE_URL` to `client_email_configs` **or** only calls email.server API (cleaner boundary).

Prefer **scraper → HTTP → email.server** so you do not reimplement `buildOSQuery`, S3 templates, and SES in Python.

---

## 4. Schema change (required)

Extend [`ClientEmailConfig`](EC2/email.server/internal/models/client_email_config.go) (and API/app):

```text
daily_enabled          bool   // cron includes this config
instant_on_new_job     bool   // scraper-triggered path includes this config
# optional: last_notified_at, dedupe window, saved_search_id for UI
```

Or a single enum: `notification_mode: daily | instant | both | off`.

**UI (bell modal)** — three actions:

1. Send email now → `POST .../send-now` with `filter` from saved search  
2. Enable daily emails → existing `toggle` / `daily_enabled = true`  
3. Notify on new jobs → `instant_on_new_job = true` (+ store `filter`)

Still **one row per email**: enabling “new jobs” on search B while daily is on search A **replaces** `filter` unless you later allow multiple configs per user.

---

## 5. Step-by-step implementation plan

### Phase 1 — email.server: reusable send + config flags

1. **Refactor** `ProcessDailyEmails` loop body → `SendDigestForConfig(ctx, cfg)` (filter → OS top N → template → SES).
2. **Add routes**
   - `POST /client-configs/send-now` — body `{ email, filter, template_id }` (no `is_active` required).
   - `POST /notifications/new-jobs` — body `{ jobs: [{ linkedin_job_id, ... }] }` or `{ linkedin_job_ids: [] }`; server loads configs where `instant_on_new_job = true`, matches each job to each filter, sends **one email per user per batch** (or per job — see rate limits).
3. **Extend** `CreateClientEmailConfigRequest` / `UpdateClientEmailConfigRequest` with `daily_enabled`, `instant_on_new_job`.
4. **Cron** uses `daily_enabled` instead of only `is_active` (migrate: `daily_enabled = is_active`).

### Phase 2 — contact360.io/api

5. GraphQL mutations:
   - `sendJobEmailNotificationNow(savedSearchId)`
   - `setJobEmailNotificationPreferences(savedSearchId, daily: Boolean, instantNewJobs: Boolean)` (replaces naive toggle for modal)
6. Update `toggleJobEmailNotification` or deprecate in favor of explicit prefs.

### Phase 3 — contact360.io/app

7. Bell opens modal (not direct toggle): **Send now** | **Daily** | **New jobs** (checkboxes or three buttons).
8. Query returns `dailyEnabled`, `instantNewJobsEnabled`, `savedSearchId` for bell state.

### Phase 4 — scraper.server integration

9. **Env:** `EMAIL_SERVER_URL`, `EMAIL_SERVER_API_KEY`, optional `NOTIFICATIONS_ENABLED`.
10. **Hook** in [`append_results`](EC2/scraper.server/storage/scrape_job_store.py) (or `bulk_index_jobs` return path):
    - Track which jobs in the batch were **new** (already know: only non-duplicates reach batch; still filter with `job_exists` **before** index in runner — safest: in `append_results`, call `job_exists` per id before bulk, split `new_jobs` vs updates).
11. **New Celery task** `notifications.process_new_jobs(new_job_docs)`:
    - POST to email.server `/notifications/new-jobs` with slim payload (title, company, location, linkedin_job_id, industries, employment_type, posted_at).
    - Retry / log failures; do not block scrape completion.
12. **Optional second worker** `notification_worker.py` consuming queue `job_notifications` so scrape workers stay fast.

### Phase 5 — Matching logic for “does this new job match this filter?”

Today [`buildOSQuery`](EC2/email.server/internal/tasks/cron_manager.go) only uses:

- `listFilters.titles`, `employmentTypes`, `companyIndustries`, `excludedCompanyIndustries`
- Ignores `signalTimePreset`, locations, salary, most firmographics

For **instant** alerts you need either:

- **Short term:** Reuse `buildOSQuery` + OpenSearch: query `_search` with filter bool **and** `ids: [linkedin_job_id]` — if hit, match.
- **Long term:** Port full hire-signal filter → OS query (same as job.server) so panel count ≈ email match.

Also align index name: scraper `OPENSEARCH_JOBS_INDEX` vs email `linkedin_jobs_index` — **one alias in OpenSearch** or shared env var.

### Phase 6 — Operational safeguards

13. **Dedup:** Table `client_email_notification_sent(job_id, config_id, sent_at)` or Redis SET per user per 24h to avoid re-alerting same job.
14. **Rate limit:** Max N instant emails per user per hour; batch multiple new jobs into one email (“3 new jobs match your saved search”).
15. **Empty match:** No email if zero new jobs match.
16. **SES / template:** Reuse `daily-jobs-v1.html` with 1–N jobs; subject e.g. “New job match: {title}”.

---

## 6. Worker flow (target architecture)

```mermaid
sequenceDiagram
    participant Scrape as scraper Celery scrape.process_job
    participant OS as OpenSearch linkedin_jobs
    participant NQ as Celery notifications.process_new_jobs
    participant Email as email.server
    participant PG as Postgres client_email_configs
    participant SES as AWS SES

    Scrape->>OS: bulk_index_jobs new docs only
    Scrape->>NQ: enqueue new_job_docs
    NQ->>Email: POST /notifications/new-jobs
    Email->>PG: SELECT instant_on_new_job = true
    loop each config
        Email->>OS: job matches filter?
        Email->>SES: send if matches
    end
```

**Postgres check:** Worker does **not** need to poll all jobs in PG. It should:

1. Read **configs** from `client_email_configs` where `instant_on_new_job` (and maybe `is_active` if you reuse flag).
2. Receive **only the new job batch** from scraper.
3. Match batch ↔ filters in email.server (OpenSearch or in-process).

“All new job column data if activated” = when `instant_on_new_job` is true for a config, any **newly indexed** job document that matches that config’s `filter` triggers send.

---

## 7. What *not* to do

- **Do not** put full email.server (Go) inside scraper as a subprocess.
- **Do not** poll OpenSearch every minute for all new jobs without scraper events — expensive and duplicate of scrape path.
- **Do not** use only `is_active` for both daily and instant without splitting flags — users cannot get daily without instant or vice versa cleanly.

---

## 8. Suggested task order (for Agent mode)

1. email.server: config columns + migration + `send-now` + `new-jobs` endpoints + refactor send helper  
2. api: GraphQL prefs + send-now  
3. app: 3-option modal + bell state  
4. scraper: detect new jobs in `append_results` + Celery notify task + HTTP client  
5. Index name alignment + integration test with one `ClientEmailConfig` + one scrape batch  
6. Dedup + batched instant email copy  

---

## 9. Open questions for you

1. **One email per new job** vs **one digest per batch** (e.g. every 5 minutes)?  
2. Should **instant** and **daily** use the **same** saved search filter on the single email row, or do you need **multiple subscriptions per user** later?  
3. Confirm production OpenSearch index name: `linkedin_jobs` vs `linkedin_jobs_index`.

---

I'm in **Ask mode** and cannot implement this. Switch to **Agent mode** if you want this built; say whether instant alerts should be **per job** or **batched**, and whether scraper should call **email.server HTTP only** or also read **Postgres** directly.

---

**User**

alsio add another option for new jobs to send new job after n hours . Learn, understand, and analyze deeply, breaking tasks into smaller steps

---

**Cursor**

Analyzing the codebase to design a delayed "new jobs after N hours" option alongside instant and daily modes.


You are extending the notification model with a **delayed new-job** path: when a job is indexed and matches an active saved search, email the user **after N hours** (not immediately, not only at the fixed daily cron). Below is how that fits the current stack and how to break the work into steps.

---

## 1. Full notification matrix (four user-facing behaviors)

| # | User label | Trigger | Timing |
|---|------------|---------|--------|
| 1 | **Send email now** | Button in bell modal | Immediate, one-shot |
| 2 | **Daily digest** | `email.server` cron (`ProcessDailyEmails`, 10:00 IST) | Fixed schedule; top N jobs from OpenSearch for `filter` |
| 3 | **New jobs — immediately** | `scraper.server` indexes new docs | Per batch or per job (product choice) |
| 4 | **New jobs — after N hours** | Same ingest as (3) | **Debounce / batch**: collect matches, send once when window ends |

Today only **#2** exists (`is_active` on `ClientEmailConfig`). **#3** and **#4** need new fields, ingest from scraper, and different dispatch logic.

```mermaid
flowchart TB
    subgraph ingest [On new job indexed]
        S[scraper append_results]
        API[email.server POST ingest-new-jobs]
    end
    S --> API
    API --> M{Per config new_job_mode}
    M -->|instant| I[Send now or mini-digest]
    M -->|delayed| P[Write pending matches + schedule send_at]
    M -->|off| X[Skip]
    P --> W[Asynq or cron at send_at]
    W --> E[SES digest]
    CRON[Daily cron] --> E2[SES daily top-10]
```

**#4 is not “sleep N hours in scraper.”** Scraper should only report **new job payloads**; **email.server** owns delay, batching, templates, and SES (same as instant path).

---

## 2. What “after N hours” should mean (pick one product rule)

| Interpretation | Behavior | Typical UX |
|----------------|----------|------------|
| **A. Debounced digest** | First match at `t₀` → send at `t₀ + N` with **all** jobs matched before that time | “Email me a summary every N hours if there are new matches” |
| **B. Per-job delay** | Each job gets its own `t_indexed + N` | Many emails if many jobs; usually too noisy |
| **C. Rolling poll** | Cron every N hours: “jobs matching filter since `last_sent_at`” | Like a mini-daily; not tied to scrape event |

**Recommended: A (debounced digest)** — one email per user per window, same template as daily/instant, subject e.g. “3 new jobs match your saved search.”

Optional refinement (Slack-style): **reset** `send_at` to `now + N` on each new match (quiet period). That is stricter than fixed `t₀ + N`; document which you want in the modal copy.

---

## 3. Why `ClientEmailConfig` alone is not enough

Current model:

```12:21:EC2/email.server/internal/models/client_email_config.go
type ClientEmailConfig struct {
	ID         uint                   `gorm:"primaryKey" json:"id"`
	// ...
	Email      string                 `gorm:"uniqueIndex;not null" json:"email"`
	IsActive   bool                   `gorm:"not null;default:true" json:"is_active"`
	TemplateID string                 `gorm:"type:varchar(255)" json:"template_id"`
	Filter     map[string]interface{} `gorm:"type:jsonb;serializer:json;default:'{}'" json:"filter"`
```

You need to separate **daily** from **new-job** modes (one row per email today):

| Field | Purpose |
|--------|---------|
| `daily_enabled` | Include in `ProcessDailyEmails` (migrate from `is_active`) |
| `new_job_mode` | `off` \| `instant` \| `delayed` |
| `new_job_delay_hours` | Required when `delayed`; e.g. 1, 3, 6, 12, 24 |
| `last_new_job_digest_sent_at` | Optional; for dedup / “since last send” in mode C |

**Do not** overload `is_active` for all four behaviors.

---

## 4. Pending matches store (required for delayed mode)

Postgres table (name example: `client_email_pending_job_matches`):

| Column | Notes |
|--------|--------|
| `client_email_config_id` | FK |
| `linkedin_job_id` | Unique with config_id — idempotent ingest |
| `job_snapshot` | JSONB slim fields for template (title, company, location, link) |
| `matched_at` | When ingest matched |
| `batch_id` or `scheduled_send_at` | Tie rows to one outgoing send |

Optional: `client_email_notification_batches`

| Column | Notes |
|--------|--------|
| `config_id` | One open batch per config |
| `scheduled_send_at` | `first_match_at + N` or debounced `now + N` |
| `asynq_task_id` | Cancel/reschedule when user changes N or filter |

At send time: load pending for batch → build HTML → SES → delete pending / close batch.

**Re-match at send time:** If the user changed `filter` before send, re-run match against stored snapshot or OpenSearch so stale rows are dropped.

---

## 5. Where delay runs: use email.server Asynq (already there)

`email.server` already has **Redis + Asynq** (`router.go`, `cmd/worker/main.go`). Pattern:

1. Ingest endpoint receives jobs from scraper.
2. For each `delayed` config with matches → insert pending rows.
3. If no open batch for config → create batch with `scheduled_send_at = now + N hours` and enqueue:
   - `asynq.NewTask("job_notify:send_delayed_digest", payload, asynq.ProcessIn(time.Duration(N)*time.Hour))`
4. Task handler: send digest, clear pending, clear batch.

**Backup sweeper:** Cron every 5–15 minutes: `WHERE scheduled_send_at <= now() AND status = open` — covers lost Asynq tasks.

Scraper **Celery** should not implement N-hour delay; only call ingest HTTP (or a thin enqueue to email.server).

---

## 6. Instant vs delayed on same ingest path

Single entry point keeps scraper simple:

```
POST /notifications/ingest-new-jobs
Body: { jobs: [ { linkedin_job_id, title, ... } ] }
```

Server loop:

1. Load configs where `new_job_mode IN ('instant', 'delayed')` (and optionally `daily_enabled` unrelated).
2. For each config × job: `MatchesFilter(filter, job)` (OpenSearch `ids` query or shared matcher).
3. **instant** → accumulate into `instant_batch[config_id]`; after loop, one email per config per ingest (recommended).
4. **delayed** → `UPSERT pending`; ensure batch scheduled at `send_at`.

Instant and delayed should be **mutually exclusive** per config in the UI (radio: “Immediately” vs “After … hours”).

---

## 7. UI / API (bell modal)

Extend planned modal beyond daily + send now:

| Control | Maps to |
|---------|---------|
| Send email now | `POST /client-configs/send-now` |
| Daily digest (toggle) | `daily_enabled` |
| New job alerts (off / instant / delayed) | `new_job_mode` |
| Delay (hours) | `new_job_delay_hours` — show only when `delayed`; preset dropdown + maybe custom |

GraphQL `JobEmailNotificationConfig` today only has `is_active`:

```303:309:contact360.io/api/app/graphql/modules/email/types.py
class JobEmailNotificationConfig:
    id: int
    is_active: bool
    template_id: str | None = None
    saved_search_id: strawberry.ID | None = None
```

Add: `dailyEnabled`, `newJobMode`, `newJobDelayHours`, and mutation `setJobEmailNotificationPreferences(...)` instead of a single toggle.

Validation: `new_job_delay_hours` in allowed set (e.g. 1–72), max one open batch per config.

---

## 8. Implementation phases (small steps)

### Phase A — Schema and API contract
1. Migration: `daily_enabled`, `new_job_mode`, `new_job_delay_hours`, pending + batch tables.
2. Migrate `is_active` → `daily_enabled` for existing rows.
3. Extend create/update schemas in `client_email_config_schemas.go` and router handlers.
4. Document allowed `new_job_mode` values and delay presets.

### Phase B — Shared send pipeline
5. Refactor `ProcessDailyEmails` → `SendJobDigest(email, templateID, jobs[], meta)`.
6. Implement `MatchesFilter(config, jobDoc)` shared by daily query, instant, and delayed send.
7. Align OpenSearch index name (`linkedin_jobs` vs `linkedin_jobs_index`).

### Phase C — Ingest + instant
8. `POST /notifications/ingest-new-jobs` (API key auth like other routes).
9. Instant branch: group by config → send (with rate limit / dedup table).

### Phase D — Delayed (N hours)
10. Pending insert + batch create on first match in window.
11. Asynq task `send_delayed_digest` with `ProcessIn(N * time.Hour)`.
12. On task run: load pending, send, delete, mark batch closed.
13. Sweeper cron for missed tasks.
14. On config update (disable / change N / change filter): cancel Asynq task, delete or revalidate pending.

### Phase E — scraper.server
15. After `bulk_index_jobs` for **new** docs only → Celery `notifications.forward_new_jobs` → HTTP ingest.
16. Env: `EMAIL_SERVER_URL`, `EMAIL_SERVER_API_KEY`, feature flag.

### Phase F — contact360.io
17. Bell modal with four behaviors; GraphQL prefs mutation.
18. Bell icon state: daily on / instant on / delayed on (different visual if needed).

### Phase G — Ops and QA
19. Dedup: same `linkedin_job_id` never two emails in same window.
20. Load test: 100 jobs × 50 configs — instant rate limits; delayed single email per user per N hours.
21. Manual: scrape one new job → instant user gets mail; delayed user gets mail at T+N.

---

## 9. Edge cases to design up front

| Case | Handling |
|------|----------|
| User sets N=6, then N=3 before send | Reschedule batch: `send_at = min(existing, now+3)` or cancel and recreate |
| User disables delayed mid-window | Cancel task; optionally flush pending without send |
| Job matched at ingest but deleted from OS before send | Skip missing IDs at send |
| Daily + delayed both on | Allowed: daily at 10:00 + delayed new-job digest; cap total emails/day |
| Same job scraped twice | `job_exists` in scraper prevents re-index; ingest only sees true new docs |
| `filter` uses `signalTimePreset: new_7d` | For **new-job** paths, job is already “new”; time preset may be redundant or still applied at match |

---

## 10. How this differs from daily cron

| | Daily | Delayed new jobs |
|--|--------|------------------|
| Schedule | Fixed 10:00 IST | `first_match + N` (per user N) |
| Job source | OS query top 10 | Jobs from **scrape ingest** that matched filter |
| User expectation | “Morning roundup” | “Don’t ping me instantly; batch for N hours” |

Daily should **not** replace delayed; they are independent toggles.

---

## 11. Suggested defaults for N

Start with presets: **1, 3, 6, 12, 24** hours. Default **3** or **6** in UI. Avoid arbitrary floats; store integer hours in DB.

---

## 12. Open decisions for you

1. **Debounce rule:** fixed `t₀ + N` vs reset to `now + N` on each new match?
2. **Can daily + instant + delayed** all be on for one email address (same `filter`)?
3. **Allowed N values:** fixed list only, or any 1–48 from a number input?
4. **One email per ingest** for instant vs one email per job?

---

I'm in **Ask mode** and cannot implement this. In **Agent mode**, implement in order **A → B → D → C → E → F**, with delayed batching (interpretation **A**) unless you specify per-job delay (**B**).

If you confirm debounce vs fixed window and the preset list for N, the schema and Asynq task shape can be nailed down in one pass.

