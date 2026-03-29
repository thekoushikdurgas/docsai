# Email API system exploration
_Exported on 3/24/2026 at 01:26:06 GMT+5:30 from Cursor (2.6.20)_

---

**User**

Explore D:\code\ayan\contact\lambda\emailapigo with medium thoroughness. Return: (1) architecture map, (2) key modules/files for email system behavior, (3) end-to-end flow from API request to final email result, (4) major risks/gaps and missing tests.

---

**Cursor**

I’ll map `D:\code\ayan\contact\lambda\emailapigo` by scanning its structure and core request/email paths, then I’ll trace the end-to-end flow and highlight concrete risks and test gaps with medium-depth coverage. I’m starting with a quick repository survey and targeted code reads.

I found the service layout and I’m now reading the core API/router and service files to build a concrete flow map. I’ll also cross-check docs versus implementation to surface any behavior gaps.

I have the core handlers/services now; next I’m validating supporting modules (`utils`, models, docs) to complete the architecture map and identify concrete risk/test blind spots.

## Architecture Map

`D:\code\ayan\contact\lambda\emailapigo` is a Go Gin service that can run in two modes:

- **Runtime entrypoint**: `D:\code\ayan\contact\lambda\emailapigo\main.go`
  - Loads env, initializes logging, config, DB, and router.
  - Runs as local HTTP server or AWS Lambda (API Gateway v2 adapter).
- **HTTP/API layer**: `D:\code\ayan\contact\lambda\emailapigo\internal\api\router.go`
  - Registers routes for finder, verifier, web search, and pattern learning.
  - Applies middleware: logger/recovery, CORS, gzip, monitoring, API-key auth.
- **Service layer**: `D:\code\ayan\contact\lambda\emailapigo\internal\services\*.go`
  - `email_finder_service.go`: orchestration core.
  - `email_verification_service.go`: provider abstraction (`mailvetter`, `icypeas`).
  - `web_search_service.go`: DDG + OpenAI fallback flow.
  - `email_pattern_service.go`: pattern learning/prediction from DB.
- **Clients / external integrations**: `D:\code\ayan\contact\lambda\emailapigo\internal\clients\*.go`
  - Connectra, Mailvetter, IcyPeas, OpenAI, DuckDuckGo, DB init.
- **Persistence/repositories/models**:
  - Repos: `internal\repositories\email_pattern_repository.go`, `email_finder_cache_repository.go`
  - Models: `internal\models\email_pattern.go`, `email_finder_cache.go`
- **Pattern/util logic**:
  - `internal\email_patterns\*` for detect/render patterns.
  - `internal\utils\email_generator.go`, `unmask_email.go`, domain/cache metrics helpers.
- **Deploy/config/docs**:
  - `template.yaml` (SAM Lambda + HTTP API).
  - `internal\config\config.go`, `.env.example`.
  - Docs in `docs\api.md`, `docs\mailvaiter-api-docs.md`.

---

## Key Modules For Email System Behavior

- **Request routing and contract surface**
  - `D:\code\ayan\contact\lambda\emailapigo\internal\api\router.go`
  - `D:\code\ayan\contact\lambda\emailapigo\internal\schemas\requests.go`
  - `D:\code\ayan\contact\lambda\emailapigo\internal\schemas\responses.go`
- **Email finding orchestration (most important)**
  - `D:\code\ayan\contact\lambda\emailapigo\internal\services\email_finder_service.go`
  - Priorities: cache -> connectra -> pattern+generator+verify race -> web search fallback.
- **Email verification behavior**
  - `D:\code\ayan\contact\lambda\emailapigo\internal\services\email_verification_service.go`
  - `D:\code\ayan\contact\lambda\emailapigo\internal\clients\mailvetter_client.go`
  - `D:\code\ayan\contact\lambda\emailapigo\internal\clients\icypeas_client.go`
- **Pattern learning/prediction**
  - `D:\code\ayan\contact\lambda\emailapigo\internal\services\email_pattern_service.go`
  - `D:\code\ayan\contact\lambda\emailapigo\internal\repositories\email_pattern_repository.go`
  - `D:\code\ayan\contact\lambda\emailapigo\internal\email_patterns\detector.go`
  - `D:\code\ayan\contact\lambda\emailapigo\internal\email_patterns\renderer.go`
- **Fallback intelligence**
  - `D:\code\ayan\contact\lambda\emailapigo\internal\services\web_search_service.go`
  - `D:\code\ayan\contact\lambda\emailapigo\internal\clients\duckduckgo_client.go`
  - `D:\code\ayan\contact\lambda\emailapigo\internal\clients\openai_client.go`
- **Caching and DB**
  - `D:\code\ayan\contact\lambda\emailapigo\internal\repositories\email_finder_cache_repository.go`
  - `D:\code\ayan\contact\lambda\emailapigo\internal\clients\database.go`

---

## End-to-End Flow (API Request -> Final Email Result)

For `POST /email/finder/` (core path):

1. **Request enters Gin router**
   - Endpoint expects query params: `first_name`, `last_name`, `domain`.
   - `X-API-Key` enforced by middleware.

2. **Finder service starts orchestration**
   - `FindEmails(...)` normalizes/extracts domain and starts timer.

3. **Cache lookup first**
   - Repository checks `email_finder_cache` table for `(first,last,domain)`.
   - If hit: immediate response, source=`cached.EmailSource`.

4. **Parallel source fan-out**
   - Three goroutines execute in parallel:
     - Connectra contact lookup (`/contacts` with exact filters).
     - Pattern prediction from DB patterns for domain.
     - Local generator combinations.

5. **Priority rule: Connectra wins directly**
   - If Connectra returns email, service returns immediately as valid-like winner.
   - Winner is cached.

6. **If no Connectra hit: verification race**
   - Merge/deduplicate pattern+generated candidates.
   - Verify up to first 10 candidates concurrently using `VerifySingleEmail(..., "mailvetter")`.
   - First candidate with accepted status wins; context cancels remaining workers.

7. **If no verified winner: web search fallback**
   - If enabled, calls DDG search + OpenAI extraction.
   - Optional unmask logic tries to recover masked emails.

8. **Final response**
   - If winner found: response with single email, source, total=1, perf timing.
   - Else: empty result set (`source: "none"`).
   - Winner is upserted to cache (best-effort, non-fatal if cache write fails).

Related endpoint variants:
- `POST /email/finder/bulk`: runs many `FindEmails` concurrently (semaphore=15), preserves input order.
- `POST /email/single/verifier/` and `POST /email/bulk/verifier/`: direct provider verification path.

---

## Major Risks / Gaps / Missing Tests

### Major risks

- **No automated tests at all**
  - No `*_test.go` exists under `D:\code\ayan\contact\lambda\emailapigo`.
- **Status semantic mismatch**
  - Mailvetter maps catch-all-ish outcomes to `"risky"`, but finder race looks for `"valid"` or `"catchall"`; bulk verifier counts `"catchall"` too. This can suppress intended winners and skew metrics.
- **DB init failure handling is unsafe**
  - `main.go` logs DB init error but continues boot; downstream handlers can operate with invalid DB dependency.
- **Missing migration coverage**
  - AutoMigrate only runs for `EmailPattern`; cache table (`email_finder_cache`) is not migrated there, so cache reads/writes can fail in fresh envs.
- **Web-search unmask likely degraded**
  - Router passes empty `first,last` into `DiscoverEmail`, while unmask utility requires names; masked email recovery can silently fail.
- **Docs/API drift**
  - Documented endpoint names differ from live router paths (e.g., bulk finder path forms), creating integration risk.
- **Security/ops concerns**
  - CORS is fully open (`cors.Default()`), and deployment template uses raw IP-based upstream URLs.

### Missing high-value tests

- **Finder orchestration tests**
  - Priority correctness: cache > connectra > verified candidate > websearch > none.
  - Candidate dedupe and cap-to-10 verification behavior.
- **Status mapping and winner tests**
  - Mailvetter response variants -> internal status -> winner/metrics outcomes.
- **Concurrency tests**
  - Bulk finder order preservation, semaphore limits, partial failure behavior.
  - Verification race cancellation and goroutine completion.
- **Repository integration tests**
  - Cache upsert/read with case-insensitive identities.
  - Pattern increment/create paths including concurrent bulk insert.
- **API contract tests**
  - Request validation and response schema stability for each endpoint.
  - Auth middleware behavior and error code mapping.
- **Fallback tests**
  - DDG/OpenAI failure modes, masked-email unmask scenarios, and disabled/enabled websearch toggles.

If you want, I can next produce a prioritized test plan (quick wins first) and a “fix-first” shortlist ranked by production impact.

