# email.server — finder pipeline (Connectra-first)

Implementation: [`EmailFinderService.FindEmails`](../../../../EC2/email.server/internal/services/email_finder_service.go).

## Order of operations

1. **Normalize domain** — `ExtractDomainFromURL` on the input domain/website string.
2. **Cache** — `email_finder_cache` (if present) returns immediately with `source` from cache.
3. **Connectra** — `POST /contacts/` via `ConnectraClient` with a **10s** timeout. On success with at least one email, return immediately with `source: connectra`.
4. **Parallel** — `errgroup`: pattern service (`fetchFromPatternService`) and **email generator** (`fetchFromGenerator`).
5. **Dedup** — merge pattern + generator candidates.
6. **Race verification** — `raceVerification` against configured providers (mailtester / mailvetter / truelist / icypeas per [`EmailVerificationService`](../../../../EC2/email.server/internal/services/email_verification_service.go)).
7. **Cache write** — if a winner is found, persist to cache when applicable.

## Bulk finder

`POST /email/finder/bulk` runs the same `FindEmails` per row with a **concurrency limit of 15** (goroutine semaphore), matching the Python asyncio pattern.

## S3 CSV jobs

`POST /email/finder/s3` creates an `emailapi_jobs` row and streams the CSV into Asynq queue **`email_finder`** (see [`cmd/worker/main.go`](../../../../EC2/email.server/cmd/worker/main.go)).
