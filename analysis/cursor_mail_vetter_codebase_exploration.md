# Mail vetter codebase exploration
_Exported on 3/24/2026 at 01:24:38 GMT+5:30 from Cursor (2.6.20)_

---

**User**

Explore the codebase at D:\code\ayan\contact\backend(dev)\mailvetter\app\mailvetter-bak with medium thoroughness. Focus on: overall architecture, key packages/modules, data flow for email validation/scoring, APIs/endpoints, worker/background jobs, storage dependencies, and any scoring heuristics/algorithms. Return: (1) concise architecture map, (2) list of files central to scoring, (3) end-to-end request->score pipeline, (4) risks/gaps you notice in scoring logic/testing.

---

**Cursor**

I’ll quickly scan the target project and map the architecture/scoring flow from source files, then summarize the pipeline and risks. I’m starting by pulling any existing project knowledge so the exploration stays consistent with prior patterns.

I couldn’t find local tool descriptor files for the Byterover server (only server metadata is present), so I’ll proceed with direct codebase exploration now and map the scoring flow from source.

I found a compact Go service layout with API + worker + validator modules. Next I’m reading the core files (router, handlers, services, validator/scoring, queue, and worker) to build the exact request-to-score path.

I’ve mapped the core API and worker paths and confirmed test coverage around scoring is mostly unit-level. I’ll now synthesize the architecture map, the exact request→score pipeline, and concrete scoring/testing risks.

## 1) Concise architecture map

- **Runtime shape:** Go monolith split into API process + worker process, sharing Redis + Postgres.  
  - API entry: `D:\code\ayan\contact\backend(dev)\mailvetter\app\mailvetter-bak\cmd\api\main.go`  
  - Worker entry: `D:\code\ayan\contact\backend(dev)\mailvetter\app\mailvetter-bak\cmd\worker\main.go`
- **HTTP layer:** Gin router + middleware + handlers.  
  - Router: `D:\code\ayan\contact\backend(dev)\mailvetter\app\mailvetter-bak\internal\api\router.go`  
  - New handlers: `...\internal\handlers\validate.go`, `...\internal\handlers\jobs.go`  
  - Legacy endpoints: `...\internal\api\legacy.go`
- **Validation engine:** orchestration in `...\internal\validator\logic.go`, scoring in `...\internal\validator\scoring.go`.
- **Signals/probes layer:** DNS/SMTP/OSINT/breach/security checks in `...\internal\lookup\*.go`.
- **Background processing:** queue client in `...\internal\queue\client.go`, worker loop in `...\internal\worker\runner.go`, optional completion webhooks in `...\internal\webhook\dispatcher.go`.
- **Persistence:** Postgres schema/migrations in `...\internal\store\db.go`, raw engine result JSON stored per email in `results.data`.
- **Infra helpers:** in-memory cache (`...\internal\cache\store.go`), proxy rotation (`...\internal\proxy\manager.go`), plan/rate limits (`...\internal\plans\plans.go`, `...\internal\middleware\ratelimit.go`).

---

## 2) Files central to scoring

Most central (direct scoring logic + signal assembly):

- `D:\code\ayan\contact\backend(dev)\mailvetter\app\mailvetter-bak\internal\validator\scoring.go`
- `D:\code\ayan\contact\backend(dev)\mailvetter\app\mailvetter-bak\internal\validator\logic.go`
- `D:\code\ayan\contact\backend(dev)\mailvetter\app\mailvetter-bak\internal\models\result.go`
- `D:\code\ayan\contact\backend(dev)\mailvetter\app\mailvetter-bak\internal\lookup\smtp.go`
- `D:\code\ayan\contact\backend(dev)\mailvetter\app\mailvetter-bak\internal\lookup\dns.go`
- `D:\code\ayan\contact\backend(dev)\mailvetter\app\mailvetter-bak\internal\lookup\security.go`
- `D:\code\ayan\contact\backend(dev)\mailvetter\app\mailvetter-bak\internal\lookup\probes.go`
- `D:\code\ayan\contact\backend(dev)\mailvetter\app\mailvetter-bak\internal\lookup\probes_extended.go`
- `D:\code\ayan\contact\backend(dev)\mailvetter\app\mailvetter-bak\internal\lookup\breach.go`
- `D:\code\ayan\contact\backend(dev)\mailvetter\app\mailvetter-bak\internal\lookup\static.go`

Also important for score exposure/consumption:

- `D:\code\ayan\contact\backend(dev)\mailvetter\app\mailvetter-bak\internal\services\validate_service.go`
- `D:\code\ayan\contact\backend(dev)\mailvetter\app\mailvetter-bak\internal\services\job_service.go`
- `D:\code\ayan\contact\backend(dev)\mailvetter\app\mailvetter-bak\internal\worker\runner.go`
- `D:\code\ayan\contact\backend(dev)\mailvetter\app\mailvetter-bak\internal\validator\scoring_test.go`

---

## 3) End-to-end request -> score pipeline

### Single email API path
- Client calls `POST /v1/emails/validate` (auth + plan rate limit via middleware).
- Handler `ValidateSingleHandler`:
  - validates request/body/email shape
  - resolves options (`verify_smtp`, `check_disposable`, `full_details`)
  - does MX check (for `domain_valid` field)
  - calls `validator.VerifyEmailWithOptions(...)`
- `VerifyEmailWithOptions`:
  - rejects malformed/disposable early
  - computes hygiene signals (role account, entropy)
  - concurrently collects:
    - **infra signals:** provider, SPF, DMARC, SaaS TXT tokens, domain age
    - **SMTP signals:** MX -> VRFY -> RCPT target/ghost timing + catch-all behavior
    - **OSINT signals:** Google Calendar, Teams, SharePoint, Adobe, Gravatar, GitHub, optional HIBP
  - builds `RiskAnalysis`
  - calls `CalculateRobustScore(analysis)`
- `CalculateRobustScore`:
  - sets base score/status (valid/catch-all/unknown/hard-bounce)
  - applies weighted boosts/penalties/resolution logic
  - clamps final score to `[0,99]`
  - maps reachability: `safe/risky/bad`
- API response mapping:
  - `BuildValidationResponse` converts engine result to v1 schema (`is_valid`, confidence, flags/details)

### Bulk path
- Client calls `POST /v1/emails/validate-bulk`.
- Handler dedupes/filters emails, enforces plan limits, creates job row (`jobs` table), enqueues one Redis task per email.
- Worker pool BLPOPs `tasks:verify`, runs same validator path per email, stores raw engine JSON + score in `results`, updates job counters/status.
- Client polls:
  - `GET /v1/jobs/:job_id` for progress
  - `GET /v1/jobs/:job_id/results` for paginated/csv results
- On completion, webhook dispatch may fire if callback configured.

### Scoring heuristics currently implemented
- Base: SMTP 250 -> 90, hard bounce -> 0, catch-all -> 30, unknown -> 20.
- Strong positives: VRFY short-circuit 99, SharePoint/Teams/Calendar/breach.
- Medium/soft positives: GitHub/Adobe/Gravatar, provider enterprise gateway, SaaS tokens, SPF/DMARC, timing delta, domain age.
- Penalties: high entropy, role account, very new domain, empty catch-all/ghost behavior.
- Status upgrade logic: catch-all can become risky/valid depending on proof strength and score banding.

---

## 4) Risks/gaps in scoring logic/testing

- **O365 zombie correction appears documented but not implemented.**  
  In `scoring.go`, `o365ZombieCorrected` is declared but never set true; comments mention correction but no subtractive correction logic actually runs. This can over-score Office365 “250 but not truly deliverable” cases.
- **Confidence scaling mismatch with docs.**  
  Responses normalize by `score/99.0` while README describes a 0-100 score interpretation; potential product/API confusion.
- **`is_valid` is strict `status == valid`.**  
  `risky` outcomes are returned as invalid in API schema; that may be intended, but it can be surprising for users who treat risky as “deliverable with caution.”
- **Single-email error mapping likely conflates runtime failures with bad input.**  
  `ValidateSingleHandler` maps any non-nil verifier error to `INVALID_EMAIL_FORMAT` (400), including timeouts/context cancellations.
- **High external dependency sensitivity.**  
  GitHub/Adobe/Microsoft/Google/HIBP probes rely on third-party behavior/rate limits; false negatives can depress score, and no per-signal confidence/quality weighting by probe reliability is exposed.
- **Testing coverage is narrow for end-to-end behavior.**  
  Only `internal/validator/scoring_test.go` plus proxy tests exist; no integration tests for full verifier pipeline, no queue/worker persistence tests, no deterministic tests for probe fallback/timeouts.
- **No fixture-based regression harness for probe responses.**  
  Given many heuristic branches, lack of replayed HTTP/SMTP fixtures increases regression risk when third-party endpoints change behavior.

If useful, I can next provide a **signal-by-signal reliability table** (what can false-positive/false-negative, and how to rebalance weights safely).

